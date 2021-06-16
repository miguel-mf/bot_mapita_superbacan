#import telegram
import telebot
from mapa_automatico import *

bot_token = '1502244964:AAGTgZpyTmsWszoKZ6m9-ZL4AoC87C2KhN4'
bot = telebot.TeleBot(bot_token)
path_mapita = 'mapita_superbacan.png' #definir path

class Sismo:
    def __init__(self, lat):
        self.lat = lat
        self.lon = None
        self.prof = None
        self.mag = None
        self.lim = None
        self.firma = None

@bot.message_handler(commands=['help', 'start'])
def handle_command(message):
  msg = bot.reply_to(message, """\
Hola, soy el bot de mapitas superbacanes de la Tatilonia.
Para crear un nuevo mapa usa el comando /mapita
""")

@bot.message_handler(func=lambda message: True)
def handle_all_message(message):
    bot.reply_to(message, """\
Hola, soy el bot de mapitas superbacanes de la Tatilonia.
Para crear un nuevo mapa usa el comando /mapita
""")

@bot.message_handler(commands=['mapita'])
def handle_command(message):
    bot.reply_to(message, "Latitud del sismo [°]")
    bot.register_next_step_handler(msg, process_lat)
    
def process_lat(message):
    try:
        txt = message.text
        sismo = Sismo(txt)
        msg = bot.reply_to(message, 'Longitud del sismo [°]')
        bot.register_next_step_handler(msg, process_lon)
    except Exception as e:
        bot.reply_to(message, "Me mandé una cagá ¯\_(ツ)_/¯")
        
def process_lon(message):
    try:
        txt = message.text
        sismo.lon = txt
        msg = bot.reply_to(message, 'Profundidad del sismo [km]')
        bot.register_next_step_handler(msg, process_prof)
    except Exception as e:
        bot.reply_to(message, "Me mandé una cagá ¯\_(ツ)_/¯")
 
def process_prof(message):
    try:
        txt = message.text
        sismo.prof = txt
        msg = bot.reply_to(message, 'Magnitud del sismo')
        bot.register_next_step_handler(msg, process_mag)
    except Exception as e:
        bot.reply_to(message, "Me mandé una cagá ¯\_(ツ)_/¯")
        
def process_mag(message):
    try:
        txt = message.text
        sismo.mag = txt
        msg = bot.reply_to(message, 'Deseas definir los límites de mapa? (Y/[N])')
        bot.register_next_step_handler(msg, process_lim)
    except Exception as e:
        bot.reply_to(message, "Me mandé una cagá ¯\_(ツ)_/¯")
        
def process_lim(message):
    try:
        txt = message.text
        if str(txt).lower() == 'y':
            msg = bot.reply_to(message, 'Ingresar límites [latmin latmax lonmin lonmax]')
            bot.register_next_step_handler(msg, process_limites)
        else:
            sismo.lim = ()
            msg = bot.reply_to(message, 'Deseas que aparezca tu firma en el mapa ([Y]/N)')
            bot.register_next_step_handler(msg, process_firma)
    except Exception as e:
        bot.reply_to(message, "Me mandé una cagá ¯\_(ツ)_/¯")

 def process_limites(message):
    try:
        txt = message.text
        latmin,latmax,lonmin,lonmax = str(txt).split(' ', 4)
        sismo.lim = (latmin,latmax,lonmin,lonmax)
        msg = bot.reply_to(message, 'Deseas que aparezca tu firma en el mapa ([Y]/N)')
        bot.register_next_step_handler(msg, process_firma)
    except Exception as e:
        bot.reply_to(message, "Me mandé una cagá ¯\_(ツ)_/¯")

 def process_firma(message):
    try:
        txt = message.text
        if str(txt).lower() == 'n':
            sismo.firma = False
        else:
            sismo.firma = True
        msg = bot.reply_to(message, 'El mapita está siendo creado ...')
        mapita_superbacan(sismo.lat,sismo.lon,sismo.prof,sismo.mag,limites=sismo.lim,mapa_firmado=sismo.firma)
        chat_id = message.chat.id
        msg = bot.send_photo(chat_id, photo=open('path_mapita', 'rb'))
        msg = bot.reply_to(message, 'Para generar otro mapita usar el comando /mapita')
    except Exception as e:
        bot.reply_to(message, "Me mandé una cagá ¯\_(ツ)_/¯")
        
        
if __name__ == '__main__':
    while True:
        try:
            bot.enable_save_next_step_handlers(delay=1)
            bot.load_next_step_handlers()
            bot.polling(none_stop=True)
        except:
            time.sleep(10)
