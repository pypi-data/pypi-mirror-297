from PIL import Image

def rotate_image(image: Image.Image, degrees: float) -> Image.Image:
    """
    Rotaciona a imagem pelo número de graus fornecido.
    
    :param image: Objeto Image a ser rotacionado
    :param degrees: Graus de rotação (positivo para sentido horário)
    :return: Objeto Image rotacionado
    """
    rotated_image = image.rotate(degrees)
    return rotated_image
