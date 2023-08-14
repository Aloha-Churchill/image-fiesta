
from PIL import Image
import hashlib
import math

def text_to_binary(text):
    '''Convert text to its binary representation.'''
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_hashed_rgb(binary_string):
    '''Convert a binary string to an RGB tuple using SHA-256 hash.'''
    sha256_hash = hashlib.sha256(binary_string.encode()).hexdigest()
    # Extract RGB values from the hash
    return (int(sha256_hash[:2], 16), int(sha256_hash[2:4], 16), int(sha256_hash[4:6], 16))

def generate_image_from_text(text):
    '''Generate an image from the binary representation of text with height of 1 pixel.'''
    binary_repr = text_to_binary(text)
    
    # Ensure that the binary representation length is a multiple of 24
    while len(binary_repr) % 24 != 0:
        binary_repr += '0'
    
    # Convert binary to RGB values
    pixels = [binary_to_hashed_rgb(binary_repr[i:i+24]) for i in range(0, len(binary_repr), 24)]
    
    # Set width to the number of pixels and height to 1
    width = len(pixels)
    height = 1
    
    # Create the image
    image = Image.new('RGB', (width, height))
    image.putdata(pixels)
    return image


def generate_normalized_image_from_text(text, width=256):
    '''Generate an image with a normalized width from the binary representation of text.'''
    # Generate the image from text
    image = generate_image_from_text(text)
    
    # Resize the image to the desired width while keeping the height as 1
    image = image.resize((width, 1))
    return image

def stack_images_vertically(images):
    '''Stack a list of images vertically.'''
    total_width = images[0].width
    total_height = sum(img.height for img in images)
    
    # Create a blank image with the calculated width and height
    stacked_image = Image.new('RGB', (total_width, total_height))
    
    # Paste each image into the stacked image
    y_offset = 0
    for img in images:
        stacked_image.paste(img, (0, y_offset))
        y_offset += img.height
        
    return stacked_image

# Sample list of phrases
phrases = ["Happy Birthday", "Best Wishes", "Congratulations", "Party Time", "Cheers", "With Love"]

# Read the content of the text file
with open("cookie.txt", "r") as file:
    content = file.read()

# Determine the number of segments and segment length
num_segments = int(math.sqrt(len(content)))
segment_length = len(content) // num_segments

# Split the text into segments
segments = [content[i:i+segment_length] for i in range(0, len(content), segment_length)]

# Adjust the last segment if there's any leftover content
if len(segments[-1]) < segment_length:
    segments[-1] += " " * (segment_length - len(segments[-1]))

segments[:5]  # Display the first 5 segments for verification

# Generate normalized images for each segment and stack them
images = [generate_normalized_image_from_text(segment, width=num_segments) for segment in segments]
final_square_image = stack_images_vertically(images)
final_square_image.show()



# Generate normalized images for each phrase and stack them
# images = [generate_normalized_image_from_text(phrase) for phrase in phrases]
# final_image = stack_images_vertically(images)
# final_image.show()


# # Test the function with a sample text
# text_sample = "hello. "
# image_from_text = generate_image_from_text(text_sample)
# image_from_text.show()