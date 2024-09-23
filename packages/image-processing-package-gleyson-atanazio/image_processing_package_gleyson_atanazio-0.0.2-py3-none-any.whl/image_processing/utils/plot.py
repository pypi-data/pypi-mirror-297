"""Módulo de Plotagem de Imagens.

Este módulo fornece funções para exibir imagens e histogramas usando matplotlib.
"""

# Importa o módulo pyplot do matplotlib, usado para plotagem de gráficos.
import matplotlib.pyplot as plt


def plot_image(image):
    """Exibe uma única imagem em escala de cinza.

    Args:
        image (np.ndarray): A imagem a ser exibida.
    """
    # Cria uma nova figura com tamanho 12x4 polegadas.
    plt.figure(figsize=(12, 4))
    # Exibe a imagem em escala de cinza.
    plt.imshow(image, cmap="gray")
    # Desativa os eixos da imagem.
    plt.axis("off")
    # Mostra a imagem.
    plt.show()


def plot_result(*args):
    """Exibe várias imagens em escala de cinza em uma única linha.

    Args:
        *args (np.ndarray): Um número variável de imagens para exibir.
    """
    # Obtém o número de imagens a serem exibidas.
    number_images = len(args)
    # Cria uma figura e um conjunto de eixos para as imagens.
    fig, axis = plt.subplots(nrows=1, ncols=number_images, figsize=(12, 4))
    # Cria uma lista de nomes para as imagens, com o último nome sendo "Result".
    names_lst = ["Image {}".format(i) for i in range(1, number_images)]
    names_lst.append("Result")
    # Itera sobre as imagens, nomes e eixos, exibindo cada imagem com seu respectivo nome.
    for ax, name, image in zip(axis, names_lst, args):
        ax.set_title(name)  # Define o título do eixo.
        ax.imshow(image, cmap="gray")  # Exibe a imagem em escala de cinza.
        ax.axis("off")  # Desativa os eixos da imagem.
    # Ajusta o layout da figura para evitar sobreposições.
    fig.tight_layout()
    # Mostra as imagens.
    plt.show()


def plot_histogram(image):
    """Exibe o histograma de cores de uma imagem.

    Args:
        image (np.ndarray): A imagem para calcular o histograma.
    """
    # Cria uma figura e três eixos para os histogramas de cada canal de cor.
    fig, axis = plt.subplots(
        nrows=1, ncols=3, figsize=(12, 4), sharex=True, sharey=True
    )
    # Define uma lista de cores para os histogramas.
    color_lst = ["red", "green", "blue"]
    # Itera sobre os eixos e cores, calculando e exibindo o histograma de cada canal de cor.
    for index, (ax, color) in enumerate(zip(axis, color_lst)):
        # Define o título do eixo com o nome da cor.
        ax.set_title("{} histogram".format(color.title()))
        # Calcula e exibe o histograma do canal de cor.
        ax.hist(image[:, :, index].ravel(), bins=256, color=color, alpha=0.8)
    # Ajusta o layout da figura para evitar sobreposições.
    fig.tight_layout()
    # Mostra os histogramas.
    plt.show()
