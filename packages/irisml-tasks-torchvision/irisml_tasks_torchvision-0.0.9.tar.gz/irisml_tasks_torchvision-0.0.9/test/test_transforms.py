import pytest
from PIL import Image
from irisml.tasks.create_torchvision_transform import ResizeDown


class TestTransforms:
    @pytest.mark.parametrize("img_size,size,max_size,expected_size", [
        ((128, 256), 768, None, (128, 256)),
        ((1000, 1000), 768, None, (768, 768)),
        ((1000, 4000), 768, None, (768, 3072)),
        ((128, 256), (1024, 768), None, (128, 256)),
        ((128, 800), (1024, 768), None, (128, 768)),
        ((2000, 800), (1024, 768), None, (1024, 768)),
        ((128, 256), 768, 2048, (128, 256)),
        ((1000, 1000), 768, 2048, (768, 768)),
        ((1000, 4000), 768, 2048, (512, 2048)),
    ])
    def test_resize_down(self, img_size, size, max_size, expected_size):
        img = Image.new("RGB", (img_size[1], img_size[0]))
        transform = ResizeDown(size, max_size=max_size)
        resized_img = transform(img)
        assert resized_img.size == (expected_size[1], expected_size[0])
