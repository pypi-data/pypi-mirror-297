import pytest
from PIL import Image
from image_processor_pkg.image_filters.blur_filter import apply_blur
from image_processor_pkg.image_filters.sharpen_filter import apply_sharpen

@pytest.fixture
def sample_image():
    return Image.new("RGB", (100, 100), "white")

def test_apply_blur(sample_image):
    blurred_image = apply_blur(sample_image)
    
    assert isinstance(blurred_image, Image.Image)
    
    assert blurred_image.size == sample_image.size

def test_apply_sharpen(sample_image):
    sharpened_image = apply_sharpen(sample_image)
    
    assert isinstance(sharpened_image, Image.Image)
    
    assert sharpened_image.size == sample_image.size
