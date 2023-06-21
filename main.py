from telegram_bot import PostBot


if __name__ == "__main__":
    token = open(r"C:\Users\Александр\Desktop\token.txt", 'r').readline()
    bot = PostBot(token)
    bot.start_bot()
