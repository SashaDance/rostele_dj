import urllib.request
from telebot import *
from image_generation import PostImage

CHANNEL_ID = "@numbers_game_dsj"


class PostBot:
    def __init__(self, token):
        self.bot = TeleBot(token)
        self.image_urls = []
        self.texts = []

        @self.bot.message_handler(commands=["start"])
        def send_greetings(message):
            self.markup_start = types.ReplyKeyboardMarkup()
            image_button = types.KeyboardButton("Добавить картинку")
            self.markup_start.row(image_button)
            self.bot.send_message(message.chat.id,
                                  "Привет! Я помогу тебе сделать пост. Вот пример того, как он будет выглядеть",
                                  reply_markup=self.markup_start)
            image_data = open("example.jpeg", "rb")
            self.bot.send_photo(message.chat.id, image_data)

        @self.bot.message_handler(content_types=['photo'])
        def handle_image_message(message):
            # image should be around 5:4
            # download the image sent by the user
            photo_id = message.photo[-1].file_id
            file_info = self.bot.get_file(photo_id)
            file_url = f'https://api.telegram.org/file/bot{token}/{file_info.file_path}'
            urllib.request.urlretrieve(file_url, f'input_image_{len(self.image_urls)}.jpg')
            self.image_urls.append(f'input_image_{len(self.image_urls)}.jpg')
            self.bot.send_message(message.chat.id, "Отлично! Теперь одной строкой отправь текст к этой картинке")

        @self.bot.message_handler(func=lambda message: True)
        def handle_text_message(message):
            text = message.text
            self.markup_post = types.ReplyKeyboardMarkup()
            confirm_button = types.KeyboardButton("Опубликовать пост")
            more_images_button = types.KeyboardButton("Добавить картинок к посту")
            self.markup_post.row(confirm_button, more_images_button)
            self.markup_confirm = types.ReplyKeyboardMarkup()
            one_more_post_button = types.KeyboardButton("Опубликовать еще один пост")
            self.markup_confirm.row(one_more_post_button)
            if text == "Добавить картинку":
                self.bot.send_message(message.chat.id, "Отправь мне картинку")
            elif text == "Добавить картинок к посту":
                self.bot.send_message(message.chat.id, "Хорошо, отправьте следующую картинку")
            elif text == "Опубликовать пост":
                i = 0
                media = []
                post_text = "#ds #dj #numbers_game"
                for text, image_url in zip(self.texts, self.image_urls):
                    post_image = PostImage(text, image_url)
                    post_image.save(f"post_image_{i}.jpg")
                    if i == 0:
                        # adding text to post
                        media.append(telebot.types.InputMediaPhoto(open(f"post_image_{i}.jpg", "rb"),
                                                                   caption=post_text))
                    else:
                        media.append(telebot.types.InputMediaPhoto(open(f"post_image_{i}.jpg", "rb")))
                    i += 1
                self.bot.send_media_group(CHANNEL_ID, media)
                self.image_urls = []
                self.texts = []
                self.bot.send_message(message.chat.id, "Пост был опубликован", reply_markup=self.markup_confirm)
            elif text == "Опубликовать еще один пост":
                self.bot.send_message(message.chat.id, "Отправь мне картинку")
            else:
                self.texts.append(text)
                self.bot.send_message(message.chat.id, "Опубликовать пост или добавить еще картинок к нему?",
                                      reply_markup=self.markup_post)

    def start_bot(self):
        self.bot.polling()
