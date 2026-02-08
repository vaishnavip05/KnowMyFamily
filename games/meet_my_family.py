import json
import os

def meet_family():
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        json_path = os.path.join(base_dir, "family_data.json")

        with open(json_path, "r") as f:
            data = json.load(f)

        result = ""
        for member in data["family"]:
            result += f"{member['relation']} : {member['name']}\n"

        return result

    except Exception as e:
        return f"Error: {e}"
