import openai
import random
import time
import requests
import config

openai.api_key = config.API_KEY

personalities = [
    {"name": "person1", "keywords": ["", "", ""], "personality": "chill"},
    {"name": "person2", "keywords": ["", "", "", "", ""], "personality": "friendly"},
    {"name": "person3", "keywords": ["", "", ""], "personality": "enthusiastic"},
    {"name": "person 5", "keywords": ["", "", ""], "personality": "laid-back"},
    {"name": "person 6", "keywords": ["", "", ""], "personality": "funny"},
    {"name": "person 7", "keywords": ["", "", ""], "personality": "foodie"},
    {"name": "person 8", "keywords": ["", "", ""], "personality": "polite"},
]

def get_response(personality, message):
    prompt = f"{personality['name']}: {message.capitalize()}!"
    slang_keywords = [kw.capitalize() + "!" for kw in personality['keywords']]
    prompt += " " + " ".join(slang_keywords)

    response = openai.Completion.create(
        model=config.FINE_TUNED_MODEL_ID,
        prompt=prompt,
        temperature=0.7,
        max_tokens=50,
        n=1,
        stop=None
    )

    return response.choices[0].text.strip()

def send_webhook_message(webhook_url, name, message):
    data = {
        "content": f"**{name}:** {message.capitalize()}"
    }
    response = requests.post(webhook_url, json=data)
    response.raise_for_status()

def chat():
    webhook_url = config.DISCORD_WEBHOOK_URL
    print("started")
    while True:
        sender = random.choice(personalities)
        receiver = random.choice([p for p in personalities if p != sender])

        message = random.choice(sender['keywords'])
        response = get_response(receiver, message)

        send_webhook_message(webhook_url, sender['name'], message)
        send_webhook_message(webhook_url, receiver['name'], response)

        time.sleep(2)

chat()
