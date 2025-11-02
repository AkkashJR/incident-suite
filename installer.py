import subprocess
import os
from datetime import datetime
import smtplib
from email.message import EmailMessage

def install_all_softwares():
    try:
        # Path to installers (update if needed)
        installer_dir = "C:\\Installers"  # ✅ Change if you move files

        installers = {
            "7-Zip": os.path.join(installer_dir, "7z2501-x64.exe"),
            "Chrome": os.path.join(installer_dir, "ChromeSetup.exe"),
            "Notepad++": os.path.join(installer_dir, "npp.8.8.7.Installer.x64.exe")
        }

        log = []
        for name, path in installers.items():
            if os.path.exists(path):
                try:
                    subprocess.run([path, "/S"], check=True)
                    log.append(f"✅ {name} installed successfully.")
                except subprocess.CalledProcessError:
                    log.append(f"❌ {name} failed to install.")
            else:
                log.append(f"❌ {name} installer not found at {path}.")

        # Log to file
        os.makedirs("C:\\SystemReports", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_path = "C:\\SystemReports\\install_log.txt"
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] Install Summary:\n" + "\n".join(log) + "\n\n")

        # Email summary
        msg = EmailMessage()
        msg["Subject"] = "Software Installation Summary"
        msg["From"] = "14akashjoseph@gmail.com"
        msg["To"] = "14akashjoseph@gmail.com"
        msg.set_content(f"🧩 Installation Summary:\n\n" + "\n".join(log))

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login("14akashjoseph@gmail.com", "gwbhvmokpxliotpr")
            smtp.send_message(msg)

        return "✅ Installation complete. Check email and C:\\SystemReports\\install_log.txt"

    except Exception as e:
        return f"❌ Installation failed: {e}"