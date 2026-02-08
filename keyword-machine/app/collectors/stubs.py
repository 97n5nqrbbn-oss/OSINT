
"""
Stubs for future connectors (often require credentials).

X / Telegram / Discord usually require API keys or bot tokens.
The pipeline is modular so you can add these later without changing DB or analytics.
"""

def collect_x(*args, **kwargs):
return []

def collect_telegram(*args, **kwargs):
return []

def collect_discord(*args, **kwargs):
return []
