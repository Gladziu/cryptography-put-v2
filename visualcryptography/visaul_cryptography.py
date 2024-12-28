import numpy as np
from PIL import Image


def load_image(file_path):
    image = Image.open(file_path).convert('1')  # Konwersja do obrazu czarno-białego
    image = image.resize((100, 100))
    return np.array(image, dtype=np.uint8)


def save_image(array, file_path):
    image = Image.fromarray((array * 255).astype(np.uint8))
    image.save(file_path)


def generate_shares(image):
    height, width = image.shape
    share1 = np.random.randint(0, 2, (height, width), dtype=np.uint8)  # Losowe wypełnienie obrazu
    share2 = (image ^ share1)
    return share1, share2


def reconstruct_image(share1, share2):
    return share1 ^ share2  # XOR to combine shares


input_image_path = "input_image.png"  # Ścieżka do obrazu wejściowego
output_share1_path = "share1.png"
output_share2_path = "share2.png"
output_reconstructed_path = "reconstructed_image.png"

image = load_image(input_image_path)

share1, share2 = generate_shares(image)

save_image(share1, output_share1_path)
save_image(share2, output_share2_path)

reconstructed = reconstruct_image(share1, share2)

save_image(reconstructed, output_reconstructed_path)

print("Shares and reconstructed image have been saved.")
