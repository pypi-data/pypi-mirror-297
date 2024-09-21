import dotenv

def reset_shared_status():
    with open(".aiq_status", "w") as f:
        f.write("")

def get_shared_status():
    dotenv.load_dotenv(".aiq_status")

def set_shared_status(key, value):
    with open(".aiq_status", "a") as f:
        f.write(f"{key}={value}\n")
