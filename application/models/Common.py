from yaml import load, FullLoader


def get_config() -> dict:
    with open("config.yaml", "r") as f:
        config = load(f, Loader=FullLoader)
    return config


CONFIG = get_config()


# Нормалиировка текста
def normalize(text):
    # trim, to lower, replace
    text = text.strip().lower().replace("ё", "е")
    return text
