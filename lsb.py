from PIL import Image, ImageFont, ImageDraw
import textwrap

def decode_image(file_location="images/UG_encode.png"):
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()

    for i in range(x_size):
        for j in range(y_size):
            if bin(red_channel.getpixel((i, j)))[-1] == '1':
                pixels[i, j] = (0,0,0)
            else:
                pixels[i, j] = (255, 255, 255)

    decoded_image.save("images/UG_decode.png")

def write_text(text_to_write, image_size):
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin,offset), line, font=font)
        offset += 10
    return image_text

def encode_image(text_to_encode, template_image="images/UG.jpg"):
    image_before = Image.open(template_image)

    red_part = image_before.split()[0]
    green_part = image_before.split()[1]
    blue_part = image_before.split()[2]

    x_size = image_before.size[0]
    y_size = image_before.size[1]

    text_image = write_text(text_to_encode, image_before.size).convert('1')
    new_img = Image.new("RGB", (x_size, y_size))

    new_img_pix = new_img.load()

    for i in range(x_size):
        for j in range(y_size):
            pix_text_image = bin(text_image.getpixel((i,j)))
            pix_red_part = bin(red_part.getpixel((i,j)))

            if pix_text_image[-1] == '0':
                pix_red_part = pix_red_part[:-1] + '0'
            else:
                pix_red_part = pix_red_part[:-1] + '1'

            new_img_pix[i, j] = (int(pix_red_part, 2), green_part.getpixel((i,j)), blue_part.getpixel((i,j)))

    new_img.save("images/UG_encode.png")


if __name__ == '__main__':
    print("Encoding the image...")
    encode_image("My super extended text prepared especially to be encoded")
    print("Decoding the image...")
    decode_image()
