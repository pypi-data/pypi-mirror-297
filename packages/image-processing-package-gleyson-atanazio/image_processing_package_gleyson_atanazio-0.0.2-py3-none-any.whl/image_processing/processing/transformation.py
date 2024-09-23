"""Módulo de Transformação de Imagens.

Este módulo fornece funções para realizar transformações em imagens,
como redimensionamento, rotações, etc.
"""

from skimage.transform import resize


def resize_image(image, proportion):
    """Redimensiona uma imagem de acordo com a proporção fornecida.

    Args:
        image (np.ndarray): Imagem a ser redimensionada.
        proportion (float): Proporção de redimensionamento (entre 0 e 1).

    Returns:
        np.ndarray: A imagem redimensionada como um array NumPy.

    Raises:
        AssertionError: Se a proporção não estiver entre 0 e 1.
    """
    assert 0 <= proportion <= 1, "A proporção deve estar entre 0 e 1."

    # Calcula a nova altura e largura da imagem.
    height = round(image.shape[0] * proportion)
    width = round(image.shape[1] * proportion)

    # Redimensiona a imagem usando interpolação bilinear para suavização.
    resized_image = resize(image, (height, width), anti_aliasing=True)

    return resized_image
