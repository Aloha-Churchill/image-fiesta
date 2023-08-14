from PIL import Image



print("Generating stenographic image")
def message_to_bin(message):
    '''Convert a string message to binary.'''
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    return binary_message

def embed_message(image_path, message):
    '''Embed a message into an image.'''
    
    binary_message = message_to_bin(message)
    binary_message += '1111111111111110'  # Add a 16-bit delimiter which indicates end of the text
    image = Image.open(image_path).convert("RGB")
    pixels = list(image.getdata())
    new_pixels = []
    message_idx = 0

    for pixel in pixels:
        # If there's more message to embed, do it
        if message_idx < len(binary_message):
            # Embed 1 bit in each color channel (R, G, B)
            new_pixel = [(pixel[i] & ~1) | (int(binary_message[message_idx + i]) if message_idx + i < len(binary_message) else 0) for i in range(3)]
            message_idx += 3
        else:
            new_pixel = pixel
        new_pixels.append(tuple(new_pixel))
    

    # Create a new image with the modified pixels
    image.putdata(new_pixels)
    return image

# Test the embed function
image_path = "ico.png" 
message = "Happy Birthday"
embedded_image = embed_message(image_path, message)
embedded_image.save("embedded_image.jpg")

