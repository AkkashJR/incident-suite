import subprocess
import os
from datetime import datetime
import smtplib
from email.message import EmailMessage

def run_compliance_check():
    log = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Check Windows Defender
        result = subprocess.run(["sc", "query", "WinDefend"], capture_output=True, text=True)
        if "RUNNING" in result.stdout:
            log.append("✅ Windows Defender is running.")
        else:
            log.append("❌ Windows Defender is not running.")

        # Check Firewall status
        result = subprocess.run(["netsh", "advfirewall", "show", "allprofiles"], capture_output=True, text=True)
        if "State ON" in result.stdout:
            log.append("✅ Firewall is enabled.")
        else:
            log.append("❌ Firewall is disabled.")

        # Check BITS service
        result = subprocess.run(["sc", "query", "BITS"], capture_output=True, text=True)
        if "RUNNING" in result.stdout:
            log.append("✅ BITS service is running.")
        else:
            log.append("❌ BITS service is not running.")

        # Check admin accounts
        result = subprocess.run(["net", "localgroup", "administrators"], capture_output=True, text=True)
        log.append("👥 Admin accounts:\n" + result.stdout)

        # Check password policy
        result = subprocess.run(["net", "accounts"], capture_output=True, text=True)
        log.append("🔐 Password policy:\n" + result.stdout)

    except Exception as e:
        log.append(f"❌ Error during compliance check: {e}")

    # Save log
    os.makedirs("C:\\SystemReports", exist_ok=True)
    log_path = "C:\\SystemReports\\compliance_log.txt"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] Compliance Check:\n" + "\n".join(log) + "\n\n")

    # Email summary
    try:
        msg = EmailMessage()
        msg["Subject"] = "Compliance Check Summary"
        msg["From"] = "14akashjoseph@gmail.com"
        msg["To"] = "14akashjoseph@gmail.com"
        msg.set_content(f"🛡️ Compliance Results:\n\n" + "\n".join(log))

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login("14akashjoseph@gmail.com", "gwbhvmokpxliotpr")
            smtp.send_message(msg)
    except Exception as e:
        log.append(f"❌ Failed to send email: {e}")

    return "✅ Compliance check complete. Check email and C:\\SystemReports\\compliance_log.txt"