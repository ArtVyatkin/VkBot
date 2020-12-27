import io
from math import floor
from PIL import Image


def resize_image(image):
    width, height = image.size
    if width < 210 or height < 140:
        ratio = height / width
        width = width * 1.2
        height = ratio * width
        width = int(width)
        height = int(height)
        return image.resize((width, height), Image.ANTIALIAS)
    else:
        return image


def crop_image(image):
    width, height = image.size
    image = resize_image(image)

    if width / height <= 1.625:
        tmp = int(width / 1.625 + 0.5)
        h_2 = (tmp - tmp % 8)
        w_2 = 1.625 * h_2
    else:
        h_2 = (height - height % 8)
        w_2 = 1.625 * h_2

    left = floor((width - w_2) / 2)
    top = floor((height - h_2) / 2)
    right = left + w_2
    bottom = top + h_2
    area = (left, top, right, bottom)
    return image.crop(area)


class ImageHandler:
    def __init__(self, vk_bot):
        self.vk_bot = vk_bot

    def load_image_for_carousel(self, url):
        data = self.vk_bot.session.get(url, stream=True).content
        image = Image.open(io.BytesIO(data))
        cropped_img = crop_image(image)
        bytes_io = io.BytesIO()
        if Image.MIME[image.format] == "image/jpeg":
            image_format = "JPEG"
        else:
            image_format = "PNG"
        cropped_img.save(bytes_io, image_format)
        bytes_io.seek(0)
        photo = self.vk_bot.upload.photo_messages(photos=bytes_io)[0]
        return '{}_{}'.format(photo['owner_id'], photo['id'])
