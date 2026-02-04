import json

def meet_family():
    try:
        with open("family_data.json", "r") as f:
            data = json.load(f)

        result = ""
        for member in data["family"]:
            result += f"{member['relation']} : {member['name']}\n"

        return result

    except Exception as e:
        return f"Error: {e}"
