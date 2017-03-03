"""A program that encodes and decodes hidden messages in images through LSB steganography"""
from PIL import Image, ImageFont, ImageDraw
import textwrap


def decode_image(file_location="images/encoded_sample.png"):
    """Decodes the hidden message in an image

    file_location: the location of the image file to decode. By default is the provided encoded image in the images folder
    """
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]
    red_pix = red_channel.load()

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()
    for x in range(x_size):
        for y in range(y_size):
            if bin(red_pix[x, y])[-1] == '1':
                pixels[x, y] = (255, 255, 255)
            else:
                pixels[x, y] = (0, 0, 0)

    decoded_image.save("images/decoded_image2.png")

def write_text(text_to_write, image_size):
    """Writes text to an RGB image. Automatically line wraps

    text_to_write: the text to write to the image
    image_size: size of the resulting text image. Is a tuple (x_size, y_size)
    """
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    #Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin,offset), line, font=font)
        offset += 10
    return image_text


def encode_image(text_to_encode, template_image="images/shiba.png"):
    """Encodes a text message into an image

    text_to_encode: the text to encode into the template image
    template_image: the image to use for encoding. An image is provided by default.
    """
    encode_image = Image.open(template_image)
    x_size, y_size = encode_image.size
    secret_image = write_text(text_to_encode, encode_image.size)
    secret_pixels = secret_image.load()
    output_image = Image.new("RGB", encode_image.size)
    out_pixels = output_image.load()
    pixels = encode_image.load()

    for x in range(x_size):
        for y in range(y_size):
            if secret_pixels[x, y][0] > 0:  # We want the last bit of this number to be 1.
                if bin(pixels[x, y][0])[-1] == '0':
                    out_pixels[x, y] = (pixels[x, y][0] | 1, pixels[x, y][1], pixels[x, y][2])
                else:
                    out_pixels[x, y] = (pixels[x, y][0], pixels[x, y][1], pixels[x, y][2])

            else:  # We want the last bit of this number ot be 0.
                if bin(pixels[x, y][0])[-1] == '1':
                    out_pixels[x, y] = (pixels[x, y][0] & ~1, pixels[x, y][1], pixels[x, y][2])
                else:
                    out_pixels[x, y] = (pixels[x, y][0], pixels[x, y][1], pixels[x, y][2])

    output_image.save("images/shiba.png")


if __name__ == '__main__':
    # print("Decoding the image...")
    # decode_image()

    print("Encoding the image...")
    encode_image("Congratulations! You have been visited by the R A R E P U P P E R of good luck! Upvote in 4.7 seconds to receive good luck.")
    decode_image(file_location="images/shiba.png")
