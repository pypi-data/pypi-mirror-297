# Image Processor PKG

The image_processor_pkg package is designed for image processing, offering functionalities for applying filters and performing transformations on images. The main features include:

- Applying image filters like blur and sharpen.
- Performing transformations such as resizing and rotating images.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install package_name

```bash
pip install image_processor_pkg
```

## Usage

```
from PIL import Image
from image_processor_pkg.image_filters.blur_filter import apply_blur
from image_processor_pkg.image_transforms.resize_transform import resize_image

# Carregando uma imagem a partir de um arquivo
image_path = 'path_to_image.jpg'  # Substitua pelo caminho da sua imagem
image = Image.open(image_path)

# Aplicando um filtro de desfoque (blur)
blurred_image = apply_blur(image, blur_radius=5)
blurred_image.save('blurred_image.jpg')  # Salva a imagem desfocada

# Redimensionando a imagem
new_width, new_height = 100, 100
resized_image = resize_image(image, new_width, new_height)
resized_image.save('resized_image.jpg')  # Salva a imagem redimensionada
```

## Author
Leticia Martins dos Santos