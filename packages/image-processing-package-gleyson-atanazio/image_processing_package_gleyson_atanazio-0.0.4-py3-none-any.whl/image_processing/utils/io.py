"""Módulo de Leitura e Escrita de Imagens.

Este módulo fornece funções para realizar a leitura e escrita de imagens.
"""

from skimage.io import imread, imsave


def read_image(path, is_gray=False):
    """Carrega uma imagem de um arquivo.

    Args:
        path (str): O caminho para o arquivo de imagem.
        is_gray (bool, optional): Se True, converte a imagem para escala de cinza.
                                    Caso contrário, carrega como imagem colorida.
                                    Padrão é False.

    Returns:
        np.ndarray: A imagem carregada como um array NumPy.
    """
    image = imread(path, as_gray=is_gray)
    return image


def save_image(image, path):
    """Salva uma imagem em um arquivo.

    Args:
        image (np.ndarray): A imagem a ser salva, representada como um array NumPy.
        path (str): O caminho para o arquivo de imagem de saída.
    """
    imsave(path, image)
