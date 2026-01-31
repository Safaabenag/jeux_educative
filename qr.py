import qrcode

# 🔴 METS ICI TON LIEN
URL = "https://armani-preoriginal-unfemininely.ngrok-free.dev/"   # ou lien ngrok

qr = qrcode.QRCode(
    version=2,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=12,
    border=4,
)

qr.add_data(URL)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("QR_Loeuvre_en_Jeu.png")

print("✅ QR code créé : QR_Loeuvre_en_Jeu.png")
