import subprocess
import smtplib
import zipfile
import os
from email.message import EmailMessage
from datetime import datetime

def collect_and_email_logs():
    # Timestamp for folder and subject
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_dir = f"C:\\LogExports\\{timestamp}"
    os.makedirs(export_dir, exist_ok=True)

    # Export logs
    logs = ["System", "Application", "Security"]
    for log in logs:
        output = os.path.join(export_dir, f"{log}.evtx")
        subprocess.run(["wevtutil", "epl", log, output], check=True)

    # Zip the logs
    zip_path = f"{export_dir}.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in os.listdir(export_dir):
            zipf.write(os.path.join(export_dir, file), arcname=file)

    # Prepare email
    msg = EmailMessage()
    msg["Subject"] = f"Event Logs - {timestamp}"
    msg["From"] = "14akashjoseph@gmail.com"
    msg["To"] = "14akashjoseph@gmail.com"
    msg.set_content("Attached are the latest event logs from your VM.")

    with open(zip_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="zip", filename=os.path.basename(zip_path))

    # Send email via Gmail SMTP using App Password
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login("14akashjoseph@gmail.com", "gwbhvmokpxliotpr")  # ✅ App password (no spaces)
        smtp.send_message(msg)

    return "✅ Logs collected and emailed successfully."