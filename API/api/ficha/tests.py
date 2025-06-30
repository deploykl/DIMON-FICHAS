from django.test import TestCase

# Create your tests here.
# Prueba las credenciales con este script simple
import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('bot.reporte.dimon@gmail.com', 'smhp kikf gbsm nhqr')
    print("Conexión exitosa!")
    server.quit()
except Exception as e:
    print(f"Error: {e}")