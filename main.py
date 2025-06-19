import os
from datetime import datetime
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
import random

# ================= CONFIG ====================
TOKEN = os.environ.get("TOKEN")
CREATOR_NAME = "Vishal"
NISHU_NAME = "Nishu Yadav"

# ================ FLASK ======================
app = Flask(_name_)

@app.route('/')
def home():
    return "🌐 Nishu Bot is Live!"

# ============ TELEGRAM BOT COMMANDS ============
# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Hello {NISHU_NAME} 👋\n\n"
        f"This is your personal assistant bot built by {CREATOR_NAME}.\n"
        f"You can manage your content, collaborations, analytics, captions, and much more!\n\n"
        f"Type /help to see all features."
    )

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✨ Available Commands:\n"
        "/start - Welcome message\n"
        "/help - Show this help message\n"
        "/addidea - Add a new content idea\n"
        "/listideas - List all saved ideas\n"
        "/addcollab - Track a brand collaboration\n"
        "/listcollabs - View all collaborations\n"
        "/caption - Generate a caption idea"
    )

# ==== CONTENT IDEAS ====
ideas_db = {}

async def addidea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    idea = " ".join(context.args)
    if not idea:
        await update.message.reply_text("❗ Usage: /addidea your-idea-here")
        return
    ideas_db.setdefault(user_id, []).append(idea)
    await update.message.reply_text("✅ Idea saved successfully.")

async def listideas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ideas = ideas_db.get(user_id, [])
    if not ideas:
        await update.message.reply_text("📭 You have no saved ideas yet.")
    else:
        await update.message.reply_text("📝 Your Content Ideas:\n" + "\n".join(f"- {i}" for i in ideas))

# ==== COLLAB TRACKING ====
collabs_db = []

async def addcollab(update: Update, context: ContextTypes.DEFAULT_TYPE):
    details = " ".join(context.args)
    if not details:
        await update.message.reply_text("❗ Usage: /addcollab Brand - Amount - DueDate - Status")
        return
    collabs_db.append(details)
    await update.message.reply_text("🤝 Collaboration saved.")

async def listcollabs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not collabs_db:
        await update.message.reply_text("No collaborations added yet.")
    else:
        await update.message.reply_text("💼 Collabs:\n" + "\n".join(f"{i+1}. {c}" for i, c in enumerate(collabs_db)))

# ==== CAPTIONS ====
captions = [
    "Chasing dreams, not people. ✨",
    "Creating moments that matter 💫",
    "Smile, sparkle, slay. 💖",
    "Your vibe attracts your tribe 🧿",
    "Turning reels into real love 💕",
]

async def caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💬 Caption Idea:\n" + random.choice(captions))

# ==== SCHEDULER (Optional Future) ====
def send_reminder():
    print("⏰ This is a placeholder for future reminder features.")

scheduler = BackgroundScheduler()
scheduler.add_job(send_reminder, "interval", hours=24)
scheduler.start()

# ==== TELEGRAM BOT INIT ====
telegram_app = ApplicationBuilder().token(TOKEN).build()
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("help", help_command))
telegram_app.add_handler(CommandHandler("addidea", addidea))
telegram_app.add_handler(CommandHandler("listideas", listideas))
telegram_app.add_handler(CommandHandler("addcollab", addcollab))
telegram_app.add_handler(CommandHandler("listcollabs", listcollabs))
telegram_app.add_handler(CommandHandler("caption", caption))

# ==== RUN BOTH: Flask for Render + Telegram Polling ====
if _name_ == '_main_':
    import threading

    # Start Telegram bot in a separate thread
    threading.Thread(target=telegram_app.run_polling, daemon=True).start()

    # Start Flask server for Render health check
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
