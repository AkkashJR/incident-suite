import platform
import socket
import psutil
import smtplib
from email.message import EmailMessage
from datetime import datetime
import os

def collect_system_info():
    try:
        info = {
            "Hostname": socket.gethostname(),
            "IP Address": socket.gethostbyname(socket.gethostname()),
            "OS": platform.system() + " " + platform.release(),
            "Architecture": platform.machine(),
            "Processor": platform.processor(),
            "RAM (GB)": round(psutil.virtual_memory().total / (1024 ** 3), 2),
            "Uptime (hrs)": round((datetime.now().timestamp() - psutil.boot_time()) / 3600, 2)
        }

        report = "\n".join([f"{key}: {value}" for key, value in info.items()])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Log to file
        os.makedirs("C:\\SystemReports", exist_ok=True)
        with open("C:\\SystemReports\\system_snapshot.txt", "a", encoding="utf-8") as log:
            log.write(f"[{timestamp}] System Snapshot:\n{report}\n\n")

        # Email report
        msg = EmailMessage()
        msg["Subject"] = "System Info Snapshot"
        msg["From"] = "14akashjoseph@gmail.com"
        msg["To"] = "14akashjoseph@gmail.com"
        msg.set_content(f"🖥️ System Info Snapshot:\n\n{report}")

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login("14akashjoseph@gmail.com", "gwbhvmokpxliotpr")  # App password
            smtp.send_message(msg)

        return f"✅ Snapshot collected and emailed.\nCheck C:\\SystemReports\\system_snapshot.txt"

    except Exception as e:
        return f"❌ Failed to collect system info: {e}"