import time
import telegram
from scanner import get_new_tokens
from honeypot_check import is_safe_token
from config import *

bot = telegram.Bot(token=TELEGRAM_TOKEN)

def send_alert(token):
    msg = f"""🚀 *New GEM Detected!*
*Name:* {token['name']} ({token['symbol']})
*Liquidity:* ${token['liquidity']}
*Volume (24h):* ${token['volume']}
*FDV:* ${token['fdv']}

🔗 [View Chart]({token['url']})"""
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

if __name__ == "__main__":
    while True:
        try:
            gems = get_new_tokens()
            for gem in gems:
                if is_safe_token(gem):
                    send_alert(gem)
            time.sleep(30)
        except Exception as e:
            print("Error:", e)
            time.sleep(10)
