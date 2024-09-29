from PIL import Image
import io

def validate_image(file):
    img = Image.open(file.stream)
    width, height = img.size
    ratio = width / height

    if ratio == 5 / 3:
        return True
    return False