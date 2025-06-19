import os
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ================== CONFIG ==================
TOKEN = "7699013403:AAHJQCq7IoDnXfnQtca2Ttyx5tRAuf-eMkC"
CREATOR_NAME = "Vishal"
NISHU_NAME = "Nishu Yadav"

# In-memory DBs
ideas_db = {}
free_collabs = []

# ================== HANDLERS ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Hello {NISHU_NAME} 👋\n"
        "I'm your content assistant bot, made by Vishal.\n\n"
        "Use /help to explore my features."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "*Features:*\n"
        "/idea <topic> - Save a content idea\n"
        "/ideas - Show saved ideas\n"
        "/caption <topic> - Generate a caption\n"
        "/hashtag <topic> - Suggest hashtags\n"
        "/collab <brand> <amount> <due_date> - Track paid collaboration\n"
        "/collabs - Show all collabs\n"
        "/analytics <likes> <comments> <followers> - Get engagement rate\n"
        "/milestone <number> - Set milestone reminder\n"
        "/giveaway <desc> - Add giveaway idea\n"
        "/reply <msg> - Generate auto reply\n"
    )

async def idea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        topic = " ".join(context.args)
        date = datetime.now().strftime("%Y-%m-%d")
        ideas_db[topic] = date
        await update.message.reply_text(f"Idea saved: \"{topic}\" on {date}")
    else:
        await update.message.reply_text("Please provide a topic. Example: /idea Travel reel in Goa")

async def ideas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not ideas_db:
        await update.message.reply_text("No ideas saved yet.")
    else:
        message = "Saved Ideas:\n"
        for topic, date in ideas_db.items():
            message += f"- {topic} (on {date})\n"
        await update.message.reply_text(message)

async def caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        topic = " ".join(context.args)
        await update.message.reply_text(
            f"Caption for {topic}:\n"
            f"✨ Embrace every moment like it's made for you. #NishuVibes"
        )
    else:
        await update.message.reply_text("Please provide a topic. Example: /caption Beach morning")

async def hashtag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        topic = " ".join(context.args).lower()
        hashtags = {
            "travel": "#travel #wanderlust #explore #NishuTravels",
            "fashion": "#style #fashionista #OOTD #NishuStyle",
            "fitness": "#fitgirl #workoutmotivation #NishuFitness",
        }
        default = "#contentcreator #reels #NishuYadav"
        result = hashtags.get(topic, default)
        await update.message.reply_text(f"Hashtags for {topic}:\n{result}")
    else:
        await update.message.reply_text("Please provide a topic. Example: /hashtag fashion")

async def collab(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        await update.message.reply_text("Format: /collab <brand> <amount> <due_date>")
        return
    brand, amount, due_date = context.args[0], context.args[1], context.args[2]
    free_collabs.append((brand, amount, due_date))
    await update.message.reply_text(f"Collab saved: {brand} - ₹{amount} due by {due_date}")

async def collabs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not free_collabs:
        await update.message.reply_text("No collaborations added yet.")
        return
    msg = "📌 Collab Tracker:\n"
    for brand, amount, due_date in free_collabs:
        msg += f"- {brand}: ₹{amount}, Due: {due_date}\n"
    await update.message.reply_text(msg)

async def analytics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        likes, comments, followers = map(int, context.args)
        engagement = ((likes + comments) / followers) * 100
        await update.message.reply_text(f"📊 Engagement Rate: {engagement:.2f}%")
    except:
        await update.message.reply_text("Usage: /analytics <likes> <comments> <followers>")

async def milestone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please enter a milestone. Example: /milestone 100000")
    else:
        milestone = context.args[0]
        await update.message.reply_text(f"🎯 Milestone set: {milestone} followers! Keep going, {NISHU_NAME}!")

async def giveaway(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /giveaway <desc>")
    else:
        idea = " ".join(context.args)
        await update.message.reply_text(f"🎁 Giveaway idea saved:\n{idea}")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /reply <message>")
    else:
        message = " ".join(context.args)
        await update.message.reply_text(
            f"Auto-reply suggestion:\nThank you for the love! 💖 Stay tuned for more amazing content. 😊"
        )

# ================== APP ==================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("idea", idea))
    app.add_handler(CommandHandler("ideas", ideas))
    app.add_handler(CommandHandler("caption", caption))
    app.add_handler(CommandHandler("hashtag", hashtag))
    app.add_handler(CommandHandler("collab", collab))
    app.add_handler(CommandHandler("collabs", collabs))
    app.add_handler(CommandHandler("analytics", analytics))
    app.add_handler(CommandHandler("milestone", milestone))
    app.add_handler(CommandHandler("giveaway", giveaway))
    app.add_handler(CommandHandler("reply", reply))

    print(f"Bot is running for {NISHU_NAME} (Created by {CREATOR_NAME})")
    app.run_polling()

if__name=="__main__":
main()
