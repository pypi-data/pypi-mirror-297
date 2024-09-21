from PIL import Image, ImageFilter

def apply_blur(image: Image.Image, blur_radius: int = 2) -> Image.Image:
    """
    Aplica um filtro de desfoque (blur) na imagem.
    
    :param image: Objeto Image a ser desfocado
    :param blur_radius: Raio do desfoque (padrão: 2)
    :return: Objeto Image com o efeito de desfoque aplicado
    """
    blurred_image = image.filter(ImageFilter.GaussianBlur(blur_radius))
    return blurred_image