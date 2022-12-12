
import os
import logging
from logging.handlers import RotatingFileHandler


# Get a bot token from botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "5487582756:AAGE2ym9BYeGdyX2IqeMLlqnNXBvQCAzD9Q")

# Get from my.telegram.org (or @UseTGXBot)
APP_ID = int(os.environ.get("APP_ID", "12158462"))

# Get from my.telegram.org (or @UseTGXBot)
API_HASH = os.environ.get("API_HASH", "0b962717d931f4480c46d56c85d409a5")

# Generate a user session string 
TG_USER_SESSION = os.environ.get("TG_USER_SESSION", "BQCiHIAE42u8616YVYFs0XNkBp1Oi1qn7qKj4c28MkepHOp8BL9GGo8fQ2w8XWzw81d0hYRQy6EYLZ1n1DsMMWYMG02ipYcNKW28UyOm-Grvb1MZFtGO9-fm_hTIbMW-01b05dczBpCNWF6uR3qvTK05WAWUqbHout9s8xe4iSyRRgjC0tVE-6rxKLMYIucyISW1lyEW4Mu_XrHESEXsI--qjA875PtB1lSj__3LRQDsQtLiX6UDlfDZ1_ECh5aY9pY4E5pr9N3YT34-w-h6yrsExVFM1sFWL50qVWeu8xzKexrUeilFamaXdWU5Nn6l0REWE6MYzLtlaBX2vOTJQ7h3UFsxVQA")

# Database URL from https://cloud.mongodb.com/
DATABASE_URI = os.environ.get("DATABASE_URI", "mongodb+srv://yoenaung:yoenaung@cluster0.t67tc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

# Your database name from mongoDB
DATABASE_NAME = os.environ.get("DATABASE_NAME", "Cluster0")

# ID of users that can use the bot commands
AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "1348153685").split())

# Should bot search for document files in channels
DOC_SEARCH = os.environ.get("DOC_SEARCH", "yes").lower()

# Should bot search for video files in channels
VID_SEARCH = os.environ.get("VID_SEARCH", "yes").lower()

# Should bot search for music files in channels
MUSIC_SEARCH = os.environ.get("MUSIC_SEARCH", "yes").lower()




TG_BOT_SESSION = os.environ.get("TG_BOT_SESSION", "bot")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))
LOG_FILE_NAME = "filterbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)


IMDB_TEXT = """**Hey [{user}](https://t.me/{un}) 

သင်ရှာတဲ့ 👉🏻 {query} 👈🏻  စီးရီးကို VIP Series Channel မှာတင်ထားပါတယ်။

😊 Life Time 3000 Kyats နဲ့ VIP Member ဝင်ဖို့ဖိတ်ခေါ်ပါတယ်ဗျ။

မန်ဘာဝင်ရန်အတွက် အောက်က
Bot မှာအသေးစိတ်ကြည့်နိုင်ပါတယ်။

နှိပ်ပါ 👉 @YNVIPMEMBERBOT
Admin အကောင့် 👉 @YoeNaung

__📺 **Movie** : **{title} {year}**
🌟 **Rating** : {rating}/10
🔖 **Genres** : {genres}__

**🙋🏼 စီး ရီး ရှာ သူ : [{user}](https://t.me/{un})** """
