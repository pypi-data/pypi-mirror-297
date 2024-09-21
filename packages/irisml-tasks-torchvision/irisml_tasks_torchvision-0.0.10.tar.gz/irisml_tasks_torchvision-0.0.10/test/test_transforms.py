import pytest
from PIL import Image
from irisml.tasks.create_torchvision_transform import ResizeDown


class TestTransforms:
    @pytest.mark.parametrize("size,max_size,input_output_size_pairs", [
        (768, None, [
            ((128, 256), (128, 256)),
            ((1000, 1000), (768, 768)),
            ((1000, 4000), (768, 3072))
        ]),
        ((1024, 768), None, [
            ((128, 256), (128, 256)),
            ((128, 800), (128, 768)),
            (((2000, 800), (1024, 768)))
        ]),
        (768, 2048, [
            ((128, 256), (128, 256)),
            ((1000, 1000), (768, 768)),
            ((1000, 4000), (512, 2048))
        ]),
    ])
    def test_resize_down(self, size, max_size, input_output_size_pairs):
        transform = ResizeDown(size, max_size=max_size)
        for img_size, expected_size in input_output_size_pairs:
            img = Image.new("RGB", (img_size[1], img_size[0]))
            resized_img = transform(img)
            assert resized_img.size == (expected_size[1], expected_size[0])
