import os

#evitar bots, activar captcha solo cuando haga falta

HCAPTCHA_SITE_KEY = os.getenv("HCAPTCHA_SITE_KEY")
HCAPTCHA_SECRET_KEY = os.getenv("HCAPTCHA_SECRET_KEY")

def captcha_enabled() -> bool:
    return bool(HCAPTCHA_SITE_KEY and HCAPTCHA_SECRET_KEY)

#proximamente exigirlo en los create_post y mostrar en caso de spam

