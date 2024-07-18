from PIL import ImageGrab, Image
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
import base64
import io
from io import BytesIO
import cv2


def resize_base64_image(base64_string, size=(128, 128)):
    """
    Resize an image encoded as a Base64 string

    :param base64_string: Base64 string
    :param size: Image size
    :return: Re-sized Base64 string
    """
    # Decode the Base64 string
    img_data = base64.b64decode(base64_string)
    img = Image.open(io.BytesIO(img_data))

    # Resize the image
    resized_img = img.resize(size, Image.LANCZOS)

    # Save the resized image to a bytes buffer
    buffered = io.BytesIO()
    resized_img.save(buffered, format=img.format)

    # Encode the resized image to Base64
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def convert_to_base64(pil_image):
    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    img_str = resize_base64_image(img_str, size=(960, 540))
    return img_str


model = ChatOpenAI(
    model="gpt-4o-2024-05-13",
    openai_api_key="",
)

path = "/Users/jameshe/Desktop"

while True:
    image = ImageGrab.grab(bbox=None).convert("RGB")
    image.show()

    converted_image = convert_to_base64(image)

    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": "What is the correct answer to this math problem from the options provided?",
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{converted_image}"},
            },
        ],
    )

    response = model.invoke([message])
    print(response.content)
