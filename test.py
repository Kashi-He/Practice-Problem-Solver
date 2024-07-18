from PIL import Image
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
import base64
import io
from io import BytesIO
import os
from os import system
import time


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


path = "/Users/jameshe/Desktop"

model = ChatOpenAI(
    model="gpt-4o-2024-05-13",
    openai_api_key="",
)


while True:
    desktop_files = os.listdir(path)

    while os.listdir(path) == desktop_files:
        pass

    os.system("clear")
    print("New image detected. Processing...")

    s = set(desktop_files)
    new_image = [x for x in os.listdir(path) if x not in s][0][1:]
    image_name = new_image[: new_image.index(".png") + len(".png")]

    time.sleep(0.5)

    print("Opening image...")
    try:
        image = Image.open("/Users/jameshe/Desktop/" + image_name).convert("RGB")
    except:
        image = Image.open("/Users/jameshe/Desktop/" + image_name[1:]).convert("RGB")

    print("Removing image...")
    try:
        os.remove("/Users/jameshe/Desktop/" + image_name)
    except:
        os.remove("/Users/jameshe/Desktop/" + image_name[1:])

    converted_image = convert_to_base64(image)

    print("Sending image to AI...")
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": "What is the correct answer to this problem given the options provided? Give the answer only",
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{converted_image}"},
            },
        ],
    )

    response = model.invoke([message])
    os.system("clear")
    print(response.content)
    
    
    sentence = "say " + response.content
    system(sentence)
