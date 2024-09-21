import os
import time

import numpy as np
from skimage.color import rgb2gray
from skimage.exposure import match_histograms
from skimage.metrics import structural_similarity

from image_processor.image_utils import read_image, save_image
from image_processor.processing import resize_image


def find_difference(image1, image2):
    """
    Calcula a diferença entre duas imagens.

    Args:
        image1 (numpy.ndarray): A primeira imagem.
        image2 (numpy.ndarray): A segunda imagem.

    Returns:
        numpy.ndarray: A imagem de diferença normalizada.
    """

    assert image1.shape == image2.shape, "Specify 2 images with the same shape."

    gray_image1 = rgb2gray(image1)
    gray_image2 = rgb2gray(image2)

    data_range = gray_image1.max() - gray_image1.min()
    (score, difference_image) = structural_similarity(
        gray_image1, gray_image2, full=True, data_range=data_range
    )

    print("Similarity of the images:", score)

    normalized_difference_image = (difference_image - np.min(difference_image)) / (
        np.max(difference_image) - np.min(difference_image)
    )

    return normalized_difference_image


def transfer_histogram(image1, image2):
    """
    Transfere
    o histograma de uma imagem para outra.

    Args:
        image1 (numpy.ndarray): A imagem de referência.
        image2 (numpy.ndarray): A imagem que terá o histograma transferido.

    Returns:
        numpy.ndarray: A imagem com o histograma transferido.
    """

    matched_image = match_histograms(image1, image2)
    return matched_image


def main():
    """
    Função principal do processamento de imagens.

    Carrega duas imagens, redimensiona-as para o mesmo tamanho, calcula a diferença entre elas
    utilizando a similaridade estrutural e transfere o histograma de uma imagem para a outra.
    As imagens de saída (diferença e com histograma transferido) são salvas em um diretório especificado.
    """

    print("Iniciando o processamento da imagem...")

    input_image_path1 = "assets/imag-1.jpg"
    input_image_path2 = "assets/imag-2.jpg"

    image1 = read_image(input_image_path1)
    image2 = read_image(input_image_path2)

    print(f"Dimensões da imagem 1: {image1.shape}")
    print(f"Dimensões da imagem 2: {image2.shape}")

    # Determine as novas dimensões
    target_height = min(image1.shape[0], image2.shape[0])
    target_width = min(image1.shape[1], image2.shape[1])
    target_size = (target_height, target_width)

    # Redimensionar ambas as imagens para o mesmo tamanho
    resized_image1 = resize_image(image1, target_size)
    resized_image2 = resize_image(image2, target_size)

    print(f"Dimensões da imagem 1 redimensionada: {resized_image1.shape}")
    print(f"Dimensões da imagem 2 redimensionada: {resized_image2.shape}")

    difference_image = find_difference(resized_image1, resized_image2)

    # Definir o diretório de saída usando caminho relativo
    output_dir = "assets/output"
    os.makedirs(output_dir, exist_ok=True)

    # Salvar a imagem de diferença
    timestamp = int(time.time())
    output_difference_image_path = os.path.join(
        output_dir, f"difference_image_{timestamp}.jpg"
    )
    save_image(output_difference_image_path, difference_image)

    # Processar a imagem com histograma transferido
    matched_image = transfer_histogram(resized_image1, resized_image2)

    # Salvar a imagem com histograma transferido
    output_matched_image_path = os.path.join(
        output_dir, f"matched_image_{timestamp}.jpg"
    )
    save_image(output_matched_image_path, matched_image)

    print("Processamento concluído.")


if __name__ == "__main__":
    main()
