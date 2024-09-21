from PIL import Image # type: ignore

def convert_to_grayscale(image_path, output_path):
    # Open the image file
    image = Image.open(image_path)

    # Convert the image to grayscale
    grayscale_image = image.convert('L')
    grayscale_image.save(output_path)
    return output_path

def resize_image(image_path, output_path, size):
    image = Image.open(image_path)
    resized_image = image.resize(size)
    resized_image.save(output_path)
    return output_path