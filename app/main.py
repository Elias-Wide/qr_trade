import segno


wb_user_id = 1234567
code = 54321


qrcode = segno.make_qr(f"{wb_user_id}_{code}")
qrcode.save("basic_qrcode.png", scale=20,)