import json
import random

def who_is_speaking():
    try:
        with open("family_data.json", "r") as f:
            data = json.load(f)

        member = random.choice(data["family"])
        audio_file = member.get("audio", "")
        answer = member["name"]

        return audio_file, answer

    except Exception as e:
        return "", str(e)
