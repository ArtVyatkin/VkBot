import unittest
from PIL import Image

from vk_bot.image_handler import resize_image, crop_image


class ImageHandlerTests(unittest.TestCase):
    def test_resizing_narrow_image(self):
        image = Image.open("resources/image_handler/narrow_image.jpg")
        self.assert_(resize_image(image).size[0] > 221)

    def test_resizing_image_with_small_height(self):
        image = Image.open("resources/image_handler/image_with_small_height.jpg")
        self.assert_(resize_image(image).size[1] > 136)

    def test_resizing_simple_small_image_check_height(self):
        image = Image.open("resources/image_handler/simple_small_image.jpg")
        self.assert_(resize_image(image).size[1] > 136)

    def test_resizing_simple_small_image_check_width(self):
        image = Image.open("resources/image_handler/simple_small_image.jpg")
        self.assert_(resize_image(image).size[0] > 221)

    def test_resizing_big_image_check_height(self):
        image = Image.open("resources/image_handler/big_image.jpg")
        self.assert_(resize_image(image).size[1] > 136)

    def test_resizing_big_image_check_width(self):
        image = Image.open("resources/image_handler/big_image.jpg")
        self.assert_(resize_image(image).size[0] > 221)

    def test_crop_big_image(self):
        image = Image.open("resources/image_handler/big_image.jpg")
        new_width, new_height = crop_image(image).size
        self.assertEquals(new_width / new_height, 1.625)

    def test_crop_small_image(self):
        image = Image.open("resources/image_handler/simple_small_image.jpg")
        new_width, new_height = crop_image(image).size
        self.assertEquals(new_width / new_height, 1.625)


if __name__ == '__main__':
    unittest.main()
