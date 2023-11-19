from io import BytesIO

from PIL import Image


class ImageService:
    IMAGE_SIZE = 512

    @staticmethod
    def resize(image: bytes) -> bytes:
        image = Image.open(BytesIO(image))
        image_resized = image.resize((ImageService.IMAGE_SIZE, ImageService.IMAGE_SIZE))

        output_buffer = BytesIO()
        image_resized.save(output_buffer, format="JPEG")

        return output_buffer.getvalue()



