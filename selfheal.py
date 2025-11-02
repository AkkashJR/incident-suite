import subprocess
import os
from datetime import datetime
import smtplib
from email.message import EmailMessage

def self_heal_system():
    log = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Restart critical services
        services = ["wuauserv", "Spooler"]
        for svc in services:
            subprocess.run(["sc", "start", svc], capture_output=True)
            log.append(f"✅ Restarted service: {svc}")

        # Reset network adapters
        subprocess.run(["netsh", "interface", "set", "interface", "Ethernet", "admin=ENABLED"], shell=True)
        log.append("✅ Network adapter reset")

        # Kill and restart explorer.exe
        subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], shell=True)
        subprocess.run(["start", "explorer.exe"], shell=True)
        log.append("✅ Restarted explorer.exe")

        # Trigger disk cleanup
        subprocess.run(["cleanmgr", "/sagerun:1"], shell=True)
        log.append("✅ Disk cleanup triggered")

    except Exception as e:
        log.append(f"❌ Error during self-heal: {e}")

    # Save log
    os.makedirs("C:\\SystemReports", exist_ok=True)
    log_path = "C:\\SystemReports\\self_heal_log.txt"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] Self-Heal Summary:\n" + "\n".join(log) + "\n\n")

    # Email summary
    try:
        msg = EmailMessage()
        msg["Subject"] = "Self-Heal Summary"
        msg["From"] = "14akashjoseph@gmail.com"
        msg["To"] = "14akashjoseph@gmail.com"
        msg.set_content(f"🛠️ Self-Heal Actions:\n\n" + "\n".join(log))

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login("14akashjoseph@gmail.com", "gwbhvmokpxliotpr")
            smtp.send_message(msg)
    except Exception as e:
        log.append(f"❌ Failed to send email: {e}")

    return "✅ Self-Heal complete. Check email and C:\\SystemReports\\self_heal_log.txt"