import os
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot

# Token nuevo y actualizado
TOKEN = "9029036889:AAEPxpsbU3BKueDAVgyjx8ACAcVPNKvPkbs"
ADMIN_ID = 8970733209

# 1. Servidor web para satisfacer el puerto de Render
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# Arrancar el servidor web en segundo plano
threading.Thread(target=run_server, daemon=True).start()
print("Servidor web iniciado en el puerto de Render.")

# 2. Inicializar y configurar el bot de Telegram
try:
    bot = telebot.TeleBot(TOKEN)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        
        texto = (
            f"Id: {user_id}\n"
            f"First: {first_name}\n"
            f"Lang: {message.from_user.language_code}\n"
            f"Registered: ¡Conectado con éxito!\n\n"
            f"📊 **OTC Signal Pro** activo y funcionando."
        )
        bot.reply_to(message, texto)

    def run_bot():
        print("Iniciando bucle de escucha del bot...")
        bot.infinity_polling(timeout=60, long_polling_timeout=60)

    # Arrancar el bot en un hilo separado
    threading.Thread(target=run_bot, daemon=True).start()
    print("Módulo de Telegram configurado correctamente.")

except Exception as e:
    print(f"Error al configurar el bot: {e}")

# 3. Mantener el proceso principal vivo en Render
while True:
    time.sleep(3600)
