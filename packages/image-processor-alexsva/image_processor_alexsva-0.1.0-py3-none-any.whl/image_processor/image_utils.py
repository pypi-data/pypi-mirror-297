import numpy as np
from skimage.io import imread, imsave


def read_image(path, is_gray=False):
    """
    Carrega uma imagem a partir de um arquivo.

    Args:
        path (str): Caminho do arquivo da imagem.
        is_gray (bool, optional): Se True, carrega a imagem em tons de cinza. Por padrão, False (carrega colorida).

    Returns:
        numpy.ndarray: A imagem carregada como um array NumPy.
    """

    return imread(path, as_gray=is_gray)


def save_image(path, image):
    """
    Salva uma imagem em um arquivo.

    Args:
        path (str): Caminho do arquivo de destino para salvar a imagem.
        image (numpy.ndarray): A imagem a ser salva como um array NumPy.
    """

    if image.dtype == np.float64 or image.dtype == np.float32:
        image = (image * 255).astype(np.uint8)

    imsave(path, image)
