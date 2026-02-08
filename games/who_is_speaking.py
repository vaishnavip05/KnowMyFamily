import json
import random
import os

def who_is_speaking():
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        json_path = os.path.join(base_dir, "family_data.json")

        with open(json_path, "r") as f:
            data = json.load(f)

        member = random.choice(data["family"])
        audio = member.get("audio", "")
        answer = member["name"]

        return audio, answer

    except Exception as e:
        return "", str(e)
