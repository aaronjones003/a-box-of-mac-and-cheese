import json
import random
import boto3
import base64
# from PIL import Image, ImageDraw, ImageFont

def generate_cover_image(title):
    # Bedrock Configuration
    bedrock_client = boto3.client('bedrock-runtime')
    model_id = "amazon.titan-image-generator-v1"  # Replace with your actual Titan model ID 

    # Generate image using Bedrock Titan
    # response = bedrock_client.generate_image(
    #     modelId=model_id,
    #     prompt=f"A fantasy background image with a theme of {title} with NO text",
    #     numInferenceUnits=1,  # Adjust based on desired image quality and cost
    #     outputFormat="PNG"
    # )
    
    # try:
        # The different model providers have individual request and response formats.
        # For the format, ranges, and default values for Titan Image models refer to:
        # https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-image.html

    request = json.dumps(
{
    "taskType": "TEXT_IMAGE",
    "textToImageParams": {"text": f"A fantasy background image with a theme of {title} with NO text"},
    "imageGenerationConfig": {
        "numberOfImages": 1,
        "quality": "standard",
        "cfgScale": 8.0,
        "height": 640,
        "width": 384,
        "seed": 0,
    },
}
    )

    response = bedrock_client.invoke_model(
        modelId="amazon.titan-image-generator-v1", body=request
    )

    response_body = json.loads(response["body"].read())
    base64_image_data = response_body["images"][0]
    
    # except Exception:
    #     logger.error("Couldn't invoke Titan Image generator")
    #     raise

    # Get image bytes from response
    # image_bytes = response['generatedImage']

    # Create Pillow Image object
    # image = Image.open(io.BytesIO(image_bytes))

    # # Overlay title on image
    # draw = ImageDraw.Draw(image)
    # font = ImageFont.truetype("arial.ttf", 48)  # Choose appropriate font and size
    # text_width, text_height = draw.textsize(title, font=font)
    # position = ((image.width - text_width) // 2, (image.height - text_height) // 2)
    # draw.text(position, title, font=font, fill=(255, 255, 255))  # White text

    # Save image to S3
    s3_client = boto3.client('s3')
    bucket_name = "a-box-of-mac-and-cheese-images"  # Replace with your S3 bucket name
    file_key = f"covers/{title}.png"
    # img_byte_arr = io.BytesIO()
    # image.save(img_byte_arr, format='PNG')
    # img_byte_arr = img_byte_arr.getvalue()
    s3_client.put_object(Body=base64.b64decode(base64_image_data), Bucket=bucket_name, Key=file_key)

    # Return image URL
    image_url = f"https://{bucket_name}.s3.amazonaws.com/{file_key.replace(' ', '+')}"
    return image_url

def lambda_handler(event, context):
    # Extensive lists of nouns and elements
    singular_nouns = ["Throne", "Court", "Crown", "Kingdom", "Empire", "Shadow", "Light", "Night", "Queen", "King", "Prince", "Princess", "Magic", "Power", "War", "Love", "Death", "Blood", "Fate", "Prophecy", "Curse", "Blessing", "Deity", "Demon", "Angel", "Dragon", "Fae", "Witch", "Shifter", "Vampire", "Warrior", "Assassin", "Rebellion", "Revolution", "Betrayal", "Sacrifice", "Destiny", "Choice", "Academy", "Tournament", "Trial", "Quest", "Journey", "Mask", "Dagger", "Sword", "Castle", "Forest", "Mountain", "Sea", "Sky", "Box", "Heart", "Soul", "Mind", "Spirit", "Bloodline", "Legacy", "Secret", "Lie", "Truth", "Vow", "Promise", "Dream", "Nightmare", "Wish", "Desire", "Hope", "Despair", "Fear", "Courage", "Strength", "Weakness", "Song", "Silence", "Whisper", "Shout", "Gift", "Curse", "Power", "Knowledge", "Wisdom", "Ignorance", "Choice", "Consequence", "Path", "Doorway", "Bridge", "Wall", "Tower", "Dungeon", "Temple", "Library", "Garden", "Wilderness", "City", "Village", "Ruins", "Artifact", "Weapon", "Armor", "Shield", " Amulet", "Ring", "Crown", "Scepter", "Throne"]
    plural_nouns = ["Stars", "Moon", "Sun", "Gods", "Goddesses", "Demons", "Angels", "Dragons", "Fae", "Witches", "Shifters", "Vampires", "Warriors", "Assassins", "Rebels", "Revolutionaries", "Secrets", "Lies", "Truths", "Vows", "Promises", "Dreams", "Nightmares", "Wishes", "Desires", "Hopes", "Despairs", "Fears", "Whispers", "Shouts", "Gifts", "Curses", "Powers", "Choices", "Consequences", "Paths", "Doors", "Bridges", "Walls", "Towers", "Dungeons", "Temples", "Libraries", "Gardens", "Cities", "Villages", "Ruins", "Artifacts", "Weapons", "Armors", "Shields", "Amulets", "Rings", "Crowns", "Scepters", "Thrones"]
    elements = ["Fire", "Water", "Air", "Earth", "Ice", "Wind", "Shadow", "Light", "Dreams", "Nightmares", "Stars", "Bones", "Ash", "Thorns", "Roses", "Lies", "Truth", "Illusion", "Time", "Space", "Chaos", "Order", "Poison", "Venom", "Music", "Silence", "Fear", "Hope", "Rage", "Peace", "Life", "Death", "Spirit", "Soul", "Mac", "Cheese", "Mist", "Fog", "Rain", "Snow", "Storm", "Thunder", "Lightning", "Sun", "Moon", "Stars", "Darkness", "Light", "Void", "Chaos", "Order", "Creation", "Destruction", "Love", "Hate", "Joy", "Sorrow", "Passion", "Apathy", "Beauty", "Ugliness", "Life", "Death", "Growth", "Decay", "Change", "Stagnation", "Time", "Space", "Reality", "Illusion", "Dream", "Nightmare", "Memory", "Oblivion", "Knowledge", "Ignorance", "Wisdom", "Foolishness", "Power", "Weakness", "Freedom", "Slavery", "Hope", "Despair", "Faith", "Doubt", "Trust", "Betrayal", "Loyalty", "Deception", "Truth", "Lies", "Justice", "Injustice", "Mercy", "Cruelty", "Forgiveness", "Revenge"] 

    # Choose noun and determine article
    noun = random.choice(singular_nouns + plural_nouns)
    article = "An" if noun[0] in "AEIOU" else "A"
    if noun in plural_nouns:
        article = " " 

    # Choose elements ensuring they are different
    element1 = random.choice(elements)
    elements.remove(element1)
    element2 = random.choice(elements)

    # Generate and trim title with correct grammar
    title = f"{article} {noun} of {element1} and {element2}"
    title = title.strip() 

    cover_url = generate_cover_image(title)

    return {
        'statusCode': 200,
        'body': json.dumps({'title': title, 'cover_url': cover_url})
    }