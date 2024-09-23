"""Módulo Python para processamento e comparação de imagens."""

import numpy as np
from skimage.color import rgb2gray
from skimage.exposure import match_histograms
from skimage.metrics import structural_similarity

def find_difference(image1, image2):
    """Calcula a diferença visual entre duas imagens.

    Converte as imagens de entrada para escala de cinza, calcula a
    similaridade estrutural entre elas e retorna uma imagem de
    diferença normalizada, destacando as áreas onde as imagens diferem.

    Args:
        image1 (np.ndarray): A primeira imagem.
        image2 (np.ndarray): A segunda imagem.

    Returns:
        np.ndarray: Imagem de diferença normalizada.

    Raises:
        AssertionError: Se as imagens não tiverem o mesmo formato.
    """
    # Verifica se as imagens têm o mesmo formato.
    assert image1.shape == image2.shape, "As imagens devem ter o mesmo formato."

    # Converte as imagens para escala de cinza.
    gray_image1 = rgb2gray(image1)
    gray_image2 = rgb2gray(image2)

    # Calcula a similaridade estrutural e a imagem de diferença.
    (score, difference_image) = structural_similarity(
        gray_image1, gray_image2, full=True
    )
    print(f"Similaridade entre as imagens: {score:.2f}")

    # Normaliza a imagem de diferença para o intervalo [0, 1].
    normalized_difference_image = (difference_image - np.min(difference_image)) / (
        np.max(difference_image) - np.min(difference_image)
    )

    # Retorna a imagem de diferença normalizada.
    return normalized_difference_image

def transfer_histogram(image1, image2):
    """Aplica a equalização de histograma da imagem2 na imagem1.

    Args:
        image1 (np.ndarray): Imagem de referência.
        image2 (np.ndarray): Imagem cujo histograma será ajustado.

    Returns:
        np.ndarray: Imagem 2 com histograma equalizado ao da imagem 1.
    """
    # Aplica a equalização de histograma.
    matched_image = match_histograms(image1, image2, multichannel=True)
    return matched_image

