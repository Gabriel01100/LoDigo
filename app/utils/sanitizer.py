import html

def sanitize_text(text: str) -> str:
    return html.escape(text)
