from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import re
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# List of blocked words
BLACKLISTED_WORDS = ["spam", "scam", "fake"]

# Keywords that must be allowed
ALLOWED_KEYWORDS = ["buds", "handphone", "handsfree"]

# Affiliate link patterns (Amazon, Flipkart, etc.)
AFFILIATE_PATTERNS = [
    r"(https?:\/\/)?(www\.)?amazon\..+\/dp\/[A-Z0-9]+",
    r"(https?:\/\/)?(www\.)?flipkart\..+\/item\/[A-Z0-9]+"
]

def is_affiliate_link(text):
    """Check if the message contains an affiliate link."""
    for pattern in AFFILIATE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def contains_allowed_keywords(text):
    """Check if the message contains allowed keywords."""
    return any(keyword in text.lower() for keyword in ALLOWED_KEYWORDS)

def filter_messages(update: Update, context: CallbackContext):
    """Filter incoming messages based on the rules."""
    text = update.message.text

    # If message contains allowed keywords, let it pass
    if contains_allowed_keywords(text):
        return

    # Check for blacklisted words
    if any(word in text.lower() for word in BLACKLISTED_WORDS):
        update.message.delete()
        return

    # Check for affiliate links
    if is_affiliate_link(text):
        update.message.reply_text("Affiliate link detected! Please use your referral links.")
        update.message.delete()
        return

def start(update: Update, context: CallbackContext):
    """Start command."""
    update.message.reply_text("Affiliate Filter Bot is active!")

def main():
    """Run the bot."""
    TOKEN = "7478930293:AAE6GaASvI81biyDi1D782JqsSbyabWlzSU"  # Replace with your bot token
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler("start", start))

    # Message filtering
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, filter_messages))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
