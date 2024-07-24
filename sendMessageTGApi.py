import requests
from environs import Env
import json

env = Env()
env.read_env(".env")

token, chat_id = env.str("TOKEN"), env.str("CHAT_ID")
def send(photos:list[str] = None, text:str = None):
    '''
    Sends a message with optional photos and text to a Telegram chat.
    
    Args:
        photos (list[str], optional): List of photo file paths. Defaults to None.
        text (str, optional): Message text. Defaults to None.

    Returns:
        dict: The JSON response from the Telegram API.
    '''
    if photos is not None and len(photos) > 1:
        # Send media group with photos
        url = f"https://api.telegram.org/bot{token}/sendMediaGroup"
        media = []
        files = {}
        for i, photo in enumerate(photos):
            media.append({"type": "photo", "media": f"attach://photo{i}"})
            files[f"photo{i}"] = open(photo, "rb")
        payload = {"chat_id": chat_id, "media": json.dumps(media)}
        response = requests.post(url, data=payload, files=files)
        if text:
            # Send a reply message
            response_text = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": text, "reply_to_message_id": response.json()['result'][0]['message_id']})
            return response.json(), response_text.json()
    else:
        # Send a single photo or text message to the chat
        url = f"https://api.telegram.org/bot{token}/{('sendPhoto', 'sendMessage')[not photos]}"
        payload = {"chat_id": chat_id, **({"caption": text} if photos else {"text": text})}
        response = requests.post(url, data=payload, files={"photo": open(photos[0], "rb")} if photos else {})
    return response.json()

# Example usage:
send(photos=["Totem.jpg", "Malefor.jpg"])
send(photos=["Totem.jpg", "Malefor.jpg"], text="Check out these photos!")
send(photos=["Malefor.jpg"], text="This is a single photo!")
send(text="This is a text")