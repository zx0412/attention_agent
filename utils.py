import json
import os
from datetime import datetime

def save_log(user_id, dialog, final_json):
    os.makedirs("logs", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    with open(f"logs/{user_id}_{ts}.json", "w", encoding="utf-8") as f:
        json.dump({
            "user_id": user_id,
            "timestamp": ts,
            "dialog": dialog,
            "output_json": final_json
        }, f, ensure_ascii=False, indent=2)
