import subprocess
from datetime import datetime

def unlock_user(username):
    try:
        result = subprocess.run(
            ['net', 'user', username, '/active:yes'],
            shell=True,
            capture_output=True,
            text=True
        )

        with open("logs/unLock_log.txt", "a", encoding="utf-8") as log:  # ✅ Add encoding
            log.write(f"{datetime.now()} - Tried unlocking {username} → {result.stdout.strip()} | {result.stderr.strip()}\n")

        if result.returncode == 0:
            return f"✔ Account {username} unlocked."
        else:
            return f"✘ Unlock failed: {result.stderr.strip()}"
    except Exception as e:
        return f"✘ Unlock failed: {str(e)}"