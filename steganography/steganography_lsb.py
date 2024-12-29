from PIL import Image


def text_to_bin(text):
    return ''.join(format(ord(char), '08b') for char in text)


def bin_to_text(binary):
    chars = [binary[i:i + 8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars if int(char, 2) != 0)


def hide_message(image_path, message, output_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = img.load()

    # Zamiana tekstu na binarny
    binary_message = text_to_bin(message) + '00000000'  # znak null

    binary_index = 0
    for y in range(img.height):
        for x in range(img.width):
            if binary_index < len(binary_message):
                r, g, b = pixels[x, y]

                # Modyfikacja ostatniego bitu koloru RGB
                if binary_index < len(binary_message):
                    # ~1 to 11111110, wiec mozemy go uzyc do wyzerowania ostatniego bitu
                    r = (r & ~1) | int(binary_message[binary_index])
                    binary_index += 1
                if binary_index < len(binary_message):
                    g = (g & ~1) | int(binary_message[binary_index])
                    binary_index += 1
                if binary_index < len(binary_message):
                    b = (b & ~1) | int(binary_message[binary_index])
                    binary_index += 1

                pixels[x, y] = (r, g, b)
            else:
                break

    img.save(output_path)
    print(f"Ukryta widomość zapisana w {output_path}")


def reveal_message(image_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = img.load()

    binary_message = ''
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            # 'and' na ostatnim bicie
            binary_message += str(r & 1)
            binary_message += str(g & 1)
            binary_message += str(b & 1)

    # Stop gdy znajdzie '00000000' (znak null)
    delimiter_index = binary_message.find('00000000')
    if delimiter_index != -1:
        binary_message = binary_message[:delimiter_index]

    return bin_to_text(binary_message)


message = "To jest wiadomosc ukrytwa w obrazie!"
input_image_path = "input_image.png"
output_image_path = "output_image.png"
hide_message(input_image_path, message, output_image_path)

hidden_message = reveal_message(output_image_path)
print("Hidden message:", hidden_message)
