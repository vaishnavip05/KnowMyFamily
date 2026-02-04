import json
import random

def find_family():
    try:
        with open("family_data.json", "r") as f:
            data = json.load(f)

        member = random.choice(data["family"])
        question = f"Who is your {member['relation']}?"
        answer = member["name"]

        return question, answer

    except Exception as e:
        return "Error", str(e)
