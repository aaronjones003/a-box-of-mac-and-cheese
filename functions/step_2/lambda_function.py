import json
import random
import boto3
import base64
import io
from PIL import Image, ImageDraw, ImageFont

def draw_line(image, text, font_size, offset):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("lancelot-regular.ttf", font_size)  # Choose appropriate font and size
    text_width = draw.textlength(text, font=font)
    position = ((image.width - text_width) // 2, ((image.height) // 2 + offset))
    draw.text(position, text, font=font, fill=(255, 255, 255), stroke_width=2, stroke_fill='black')  # White text

def lambda_handler(event, context):
    s3_client = boto3.client('s3')

    body = event.get('body')

    title = body.get('title')
    noun, elements = title.split('of')
    element_1, element_2 = elements.split('and')
    author = body.get('author')

    background_object = s3_client.get_object(Bucket=body.get('bucket'), Key=body.get('background_key'))
    background_image_base64 = json.loads(background_object.get('Body').read()).get('images')[0]

    # Create Pillow Image object
    image = Image.open(io.BytesIO(base64.b64decode(background_image_base64)))

    # Overlay title on image
    draw_line(image, noun , 56, 50)
    draw_line(image, "of" , 40, 100)
    draw_line(image, element_1 , 56, 132)
    draw_line(image, "and" , 40, 182)
    draw_line(image, element_2 , 56, 214)

    # Save image to S3
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    s3_client.put_object(Body=img_byte_arr, Bucket=body.get('bucket'), Key=body.get('cover_key'))

    return {
        'statusCode': 200,
        'body': {
            'output': body.get('output_url')
        }
    }