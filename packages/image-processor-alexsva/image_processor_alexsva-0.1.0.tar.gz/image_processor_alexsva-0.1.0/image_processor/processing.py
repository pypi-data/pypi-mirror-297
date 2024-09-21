def resize_image(image, target_size):
    """
    Redimensiona uma imagem para um tamanho específico.

    Args:
        image (numpy.ndarray): A imagem a ser redimensionada.
        target_size (tuple): O tamanho de destino (altura, largura) para a imagem redimensionada.

    Returns:
        numpy.ndarray: A imagem redimensionada.
    """

    from skimage.transform import resize

    resized_image = resize(image, target_size, anti_aliasing=True)
    return resized_image
