import qrcode

img = qrcode.make("http://192.168.0.1/index.html#home")
img.save("qr.png", "PNG")
