import telegram

bot_token = '1502244964:AAGTgZpyTmsWszoKZ6m9-ZL4AoC87C2KhN4'
bot = telegram.Bot(token=bot_token)
chat_id = '...'


#crear mapita aca
path_mapita = 'path/al/mapita/superbacan'
bot.send_message(chat_id, text=mensajito, parse_mode=telegram.ParseMode.HTML)
bot.send_photo(chat_id, photo=open('path_mapita', 'rb'))
# equivalente pero con URL
# bot.send_photo(chat_id, 'URl')
