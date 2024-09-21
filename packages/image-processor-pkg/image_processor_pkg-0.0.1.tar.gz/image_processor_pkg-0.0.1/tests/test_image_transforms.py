import pytest
from PIL import Image
from image_processor_pkg.image_transforms.resize_transform import resize_image
from image_processor_pkg.image_transforms.rotate_transform import rotate_image

@pytest.fixture
def sample_image():
    return Image.new("RGB", (100, 100), "white")

def test_resize_image(sample_image):
    new_width, new_height = 50, 50
    resized_image = resize_image(sample_image, new_width, new_height)
    
    assert isinstance(resized_image, Image.Image)
    
    assert resized_image.size == (new_width, new_height)

def test_rotate_image(sample_image):
    rotated_image = rotate_image(sample_image, 90)
    
    assert isinstance(rotated_image, Image.Image)
    
    assert rotated_image.size == (100, 100)
