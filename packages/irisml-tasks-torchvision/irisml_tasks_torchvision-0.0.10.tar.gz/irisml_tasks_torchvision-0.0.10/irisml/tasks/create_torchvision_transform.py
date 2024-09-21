import ast
import dataclasses
from typing import Callable, List
import torch.nn
import torchvision.transforms
import irisml.core


class Task(irisml.core.TaskBase):
    """Create transform objects in torchvision library.

    This task creates a transform object in torchvision library from string expressions.
    The expression can be a simple method name such as "RandomCrop" or a method call such as "RandomCrop((32, 32))".

    ToTensor is always appended to the end of the transform object.

    Example expressions:
    - "RandomCrop((32, 32))"
    - "Resize(224, 'InterpolationMode.BICUBIC')"
    - "ResizeDown(768, max_size=2048)"

    Config:
        transforms ([str]): A list of transform descriptions.
    """
    VERSION = '0.2.1'

    @dataclasses.dataclass
    class Config:
        transforms: List[str] = dataclasses.field(default_factory=list)

    @dataclasses.dataclass
    class Outputs:
        transform: Callable

    class Transform:
        def __init__(self, transform_configs: List):
            transform_instances = []
            for method_name, args, kwargs in transform_configs:
                transform_class = getattr(torchvision.transforms, method_name)
                transform_instances.append(transform_class(*args, **kwargs))
            transform_instances.append(torchvision.transforms.ToTensor())
            self._transform = torchvision.transforms.Compose(transform_instances)
            self._transform_configs = transform_configs

        def __call__(self, x):
            return self._transform(x)

        def __getstate__(self):
            return {'transform_configs': self._transform_configs}

        def __setstate__(self, state):
            self.__init__(**state)

    def execute(self, inputs):
        transform_configs = []
        for t in self.config.transforms:
            method_name, args, kwargs = self._parse_transform(t)
            args, kwargs = self._convert_known_param(args, kwargs)
            if not hasattr(torchvision.transforms, method_name):
                raise ValueError(f"torchvision.transforms doesn't have {method_name}")

            transform_class = getattr(torchvision.transforms, method_name)
            if not issubclass(transform_class, torch.nn.Module):
                raise RuntimeError(f"{transform_class} has unexpected type.")

            transform_configs.append((method_name, args, kwargs))

        transform = Task.Transform(transform_configs)
        return self.Outputs(transform)

    def dry_run(self, inputs):
        return self.execute(inputs)

    @staticmethod
    def _convert_ast_value(ast_value):
        if isinstance(ast_value, ast.Tuple):
            if not all(isinstance(a, ast.Constant) for a in ast_value.elts):
                raise ValueError(f"Only simple types are supported: {ast.dump(ast_value)}")
            return tuple(a.value for a in ast_value.elts)
        elif isinstance(ast_value, ast.Constant):
            return ast_value.value
        else:
            raise ValueError(f"Only simple types such as a number, a string, a tuple can be used as arguments: {ast.dump(ast_value)}")

    @staticmethod
    def _parse_transform(expr):
        parsed = ast.parse(expr)
        if len(parsed.body) != 1:
            raise ValueError(f"Transform description cannot have multiple expressions: {expr}")

        if isinstance(parsed.body[0].value, ast.Name):
            return parsed.body[0].value.id, [], {}
        elif isinstance(parsed.body[0].value, ast.Call):
            method_name = parsed.body[0].value.func.id
            ast_args = parsed.body[0].value.args
            ast_kwargs = parsed.body[0].value.keywords

            args = [Task._convert_ast_value(arg) for arg in ast_args]
            kwargs = {keyword.arg: Task._convert_ast_value(keyword.value) for keyword in ast_kwargs}

            return method_name, args, kwargs
        else:
            raise ValueError(f"Unexpected transform description: {ast.dump(parsed)}")

    @staticmethod
    def _convert_known_param(args, kwargs):
        new_args = [Task._convert_known_value(a) for a in args]
        new_kwargs = {k: Task._convert_known_value(v) for k, v in kwargs.items()}
        return new_args, new_kwargs

    @staticmethod
    def _convert_known_value(value):
        if value == 'InterpolationMode.NEAREST':
            return torchvision.transforms.InterpolationMode.NEAREST
        elif value == 'InterpolationMode.NEAREST_EXACT':
            return torchvision.transforms.InterpolationMode.NEAREST_EXACT
        elif value == 'InterpolationMode.BILINEAR':
            return torchvision.transforms.InterpolationMode.BILINEAR
        elif value == 'InterpolationMode.BICUBIC':
            return torchvision.transforms.InterpolationMode.BICUBIC
        else:
            return value


class ResizeDown(torchvision.transforms.Resize):
    """
    This transform behaves the same as the built-in Resize transform,
    with the only exception that it only reduces the image resolution.
    It won't resize the image if the target size is larger.
    """

    def forward(self, img):
        size = self.size

        if isinstance(size, (list, tuple)):
            if len(size) not in [1, 2]:
                raise ValueError(
                    f"ResizeDown: size must be an int or a 1 or 2 element tuple/list, not a {len(size)} element tuple/list"
                )
            if self.max_size is not None and len(size) != 1:
                raise ValueError(
                    "ResizeDown: max_size should only be passed if size specifies the length of the smaller edge, "
                    "i.e. size should be an int or a sequence of length 1 in torchscript mode."
                )
        elif isinstance(size, int):
            size = [size]
        else:
            raise ValueError(f"ResizeDown: size must be an int or a 1 or 2 element tuple/list, not {type(size)}")

        _, image_height, image_width = torchvision.transforms.functional.get_dimensions(img)

        if (len(size) == 1 and (image_height > size[0] and image_width > size[0])) \
                or (len(size) == 2 and (image_height > size[0] or image_width > size[1])) \
                or (self.max_size is not None and (image_height > self.max_size or image_width > self.max_size)):
            if len(size) == 2:
                size = (min(size[0], image_height), min(size[1], image_width))
            return torchvision.transforms.functional.resize(img, size, self.interpolation, self.max_size, self.antialias)

        return img


setattr(torchvision.transforms, ResizeDown.__name__, ResizeDown)
