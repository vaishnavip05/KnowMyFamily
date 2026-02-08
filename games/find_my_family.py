import json
import random
import os

def find_family():
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        json_path = os.path.join(base_dir, "family_data.json")

        with open(json_path, "r") as f:
            data = json.load(f)

        member = random.choice(data["family"])
        question = f"Who is your {member['relation']}?"
        answer = member["name"]

        return question, answer

    except Exception as e:
        return "Error", str(e)

