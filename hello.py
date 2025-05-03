import argparse
from dataclasses import dataclass
import json
import appex
from PIL import Image
import io
import base64

@dataclass
class Args:
	name: str
	data: str


def load_image_from_base64_datauri(base64_datauri: str) -> Image.Image:
    """Load an image from a base64 data URI string."""
    if base64_datauri.startswith("data:"):
        base64_str = base64_datauri.split(",", 1)[1]
    else:
        base64_str = base64_datauri

    image_data = base64.b64decode(base64_str)
    with io.BytesIO(image_data) as input_buffer:
        img = Image.open(input_buffer)
        img.load()
        return img


def convert_image_to_grayscale_base64(img: Image.Image) -> str:
    """Convert a PIL Image to grayscale and output as base64 data URI."""
    grayscale_img = img.convert("L")

    with io.BytesIO() as output_buffer:
        grayscale_img.save(output_buffer, format="JPEG")
        output_bytes = output_buffer.getvalue()

    output_base64 = base64.b64encode(output_bytes).decode("utf-8")
    output_datauri = f"data:image/jpeg;base64,{output_base64}"
    return output_datauri


def main(args: Args):
	image = load_image_from_base64_datauri(args.data)
	res = convert_image_to_grayscale_base64(image)
	print(res)
	

if __name__ == "__main__":
	args_parser = argparse.ArgumentParser()
	args_parser.add_argument('--name')
	args_parser.add_argument('--data')
	args = vars(args_parser.parse_args())
	main(Args(**args))
