from PIL import Image, ImageFilter

def apply_sharpen(image: Image.Image) -> Image.Image:
    """
    Aplica um filtro de nitidez (sharpen) na imagem.
    
    :param image: Objeto Image a ser aprimorado
    :return: Objeto Image com o efeito de nitidez aplicado
    """
    sharpened_image = image.filter(ImageFilter.SHARPEN)
    return sharpened_image