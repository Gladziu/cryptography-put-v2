from PIL import Image
import numpy as np
import random


def generate_shares(image_path, output_share1, output_share2):
    # Wczytaj obraz
    image = Image.open(image_path).convert('1')  # Konwersja do czarno-białego obrazu
    image_array = np.array(image)

    # Rozmiary obrazu
    height, width = image_array.shape

    # Przygotowanie udziałów (każdy udział jest dwa razy większy)
    share1 = np.zeros((height * 2, width * 2), dtype=np.uint8)
    share2 = np.zeros((height * 2, width * 2), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            pixel = image_array[y, x]  # Pobierz wartość piksela
            # Wylosuj układ (A lub B)
            if pixel == 0:  # Czarny piksel
                pattern1, pattern2 = [(1, 0), (0, 1)], [(0, 1), (1, 0)]
            else:  # Biały piksel
                pattern1, pattern2 = [(1, 0), (0, 1)], [(1, 0), (0, 1)]

            # Losuj kolejność wzorca
            if random.random() > 0.5:
                pattern1, pattern2 = pattern2, pattern1

            # Wpisz wzorce do udziałów
            share1[y * 2, x * 2], share1[y * 2, x * 2 + 1] = pattern1[0]
            share1[y * 2 + 1, x * 2], share1[y * 2 + 1, x * 2 + 1] = pattern1[1]

            share2[y * 2, x * 2], share2[y * 2, x * 2 + 1] = pattern2[0]
            share2[y * 2 + 1, x * 2], share2[y * 2 + 1, x * 2 + 1] = pattern2[1]

    # Zapisz udziały jako obrazy
    share1_image = Image.fromarray(share1 * 255)
    share2_image = Image.fromarray(share2 * 255)

    share1_image.save(output_share1)
    share2_image.save(output_share2)


def combine_shares(share1_path, share2_path, output_combined):
    # Wczytaj udziały
    share1 = Image.open(share1_path).convert('1')
    share2 = Image.open(share2_path).convert('1')

    share1_array = np.array(share1)
    share2_array = np.array(share2)

    # Połączenie udziałów przez operację logiczną AND
    combined = np.bitwise_and(share1_array, share2_array)

    # Zapisz wynikowy obraz
    combined_image = Image.fromarray(combined)
    combined_image.save(output_combined)


# Przykład użycia
generate_shares('input_image.png', 'share1.png', 'share2.png')
combine_shares('share1.png', 'share2.png', 'combined.png')
