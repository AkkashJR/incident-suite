import subprocess

def cleanup_disk():
    try:
        subprocess.run(['cleanmgr.exe', '/sagerun:1'], shell=True)
        return "Disk Cleanup triggered successfully."
    except Exception as e:
        return f"Error: {str(e)}"