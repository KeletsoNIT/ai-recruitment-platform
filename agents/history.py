import json
from datetime import datetime

HISTORY_FILE = "history.json"


def save_history(result):

    record = {
        "timestamp": str(datetime.now()),
        "cv": result["cv"],
        "job": result["job"],
        "match_score": result["match"]["match_score"],
        "placement": result["placement"]
    }

    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(record)

    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=2)