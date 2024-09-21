from PIL import Image

def resize_image(image: Image.Image, new_width: int, new_height: int) -> Image.Image:
    """
    Redimensiona a imagem para as dimensões fornecidas.
    
    :param image: Objeto Image a ser redimensionado
    :param new_width: Nova largura da imagem
    :param new_height: Nova altura da imagem
    :return: Objeto Image redimensionado
    """
    resized_image = image.resize((new_width, new_height))
    return resized_image