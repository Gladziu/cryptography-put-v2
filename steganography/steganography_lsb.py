from PIL import Image

def text_to_bin(text):
    """Convert text to a binary string."""
    return ''.join(format(ord(char), '08b') for char in text)

def bin_to_text(binary):
    """Convert binary string to text."""
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars if int(char, 2) != 0)

def hide_message(image_path, message, output_path):
    """Hide a message in the image using the LSB algorithm."""
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = img.load()

    # Convert the message to binary and add a delimiter
    binary_message = text_to_bin(message) + '00000000'  # Null character as a delimiter

    binary_index = 0
    for y in range(img.height):
        for x in range(img.width):
            if binary_index < len(binary_message):
                r, g, b = pixels[x, y]

                # Modify the LSB of each channel if there are still bits to hide
                # ~1 is 11111110, so we can use it to clear the last bit
                if binary_index < len(binary_message):
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
    print(f"Message hidden and saved to {output_path}")

def reveal_message(image_path):
    """Reveal a hidden message from the image using the LSB algorithm."""
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = img.load()

    binary_message = ''
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            # and na ostatnim bicie
            binary_message += str(r & 1)
            binary_message += str(g & 1)
            binary_message += str(b & 1)

    # Stop reading at the delimiter
    delimiter_index = binary_message.find('00000000')
    if delimiter_index != -1:
        binary_message = binary_message[:delimiter_index]

    # Split binary string into bytes and convert to text
    return bin_to_text(binary_message)

# Example usage
# Hide a message
hide_message('input_image.png', 'Hello, World!', 'output_image.png')

# Reveal the hidden message
hidden_message = reveal_message('output_image.png')
print("Hidden message:", hidden_message)
