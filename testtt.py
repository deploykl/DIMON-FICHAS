import qrcode

# Enlace
url = "http://172.27.0.200:8081/reuniones"

# Crear el objeto QR
qr = qrcode.QRCode(
    version=1,  # tamaño del QR (1 es el más pequeño)
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # nivel de corrección de errores
    box_size=10,  # tamaño de cada “cuadro”
    border=4  # grosor del borde
)

# Agregar datos
qr.add_data(url)
qr.make(fit=True)

# Crear imagen del QR
img = qr.make_image(fill_color="black", back_color="white")

# Guardar la imagen
img.save("qr_consultaexterna.png")

print("QR generado y guardado como 'qr_consultaexterna.png'")
