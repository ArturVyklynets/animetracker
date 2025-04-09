import requests

def translate_text(text, target_language='UK'):
    api_key = "9be44ae3-4fc5-4f02-b908-d480d9004f73:fx"
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": api_key,
        "text": text,
        "target_lang": target_language
    }
    response = requests.post(url, data=params)
    if response.status_code == 200:
        translated_text = response.json()['translations'][0]['text']
        return translated_text
    else:
        print(f"Помилка: {response.status_code}")
        return None
