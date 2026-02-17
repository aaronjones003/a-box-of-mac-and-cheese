import json
import random

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

    first_names = ["Clara", "Mara", "Tara", "Zara", "Lara"]
    middle_initials = ["A", "J", "K",]
    last_names = ["Glaas", "Braas", "Paas", "Saas", "Claas", "Blaas", "Graas", ] 

    first_name = random.choice(first_names)
    middle_initial = random.choice(middle_initials)
    last_name = random.choice(last_names)
    author = f"{first_name} {middle_initial}. {last_name}" 

    bucket_name = "a-box-of-mac-and-cheese-images"
    background_key = f"backgrounds/{title}.png"
    cover_key = f"covers/{title}.png"
    output_url = f"https://{bucket_name}.s3.amazonaws.com/{cover_key.replace(' ', '+')}"

    return {
        'statusCode': 200,
        'body': {
            'title': title,
            'author': author,
            'stable_image_params': {
                "text_prompts": [{"text": f"A fantasy background image with a theme of {title}, vibrant colors, detailed artwork, no text or words"}],
                "cfg_scale": 8,
                "height": 640,
                "width": 384,
                "steps": 50
            },
            'model_id': 'stability.stable-diffusion-xl-v1',
            'bucket': bucket_name,
            'background_key': background_key.replace(' ', '+'),
            'background_object': f"s3://{bucket_name}/{background_key.replace(' ', '+')}",
            'cover_key': cover_key.replace(' ', '+'),
            'cover_object': f"s3://{bucket_name}/{cover_key.replace(' ', '+')}",
            'output_url': output_url,
        }
    }