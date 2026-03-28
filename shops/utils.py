import qrcode
from io import BytesIO
from django.core.files import File

def generate_qr_code(shop):
    url = f"http://127.0.0.1:8000/shop/{shop.slug}/subscribe/"

    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')

    filename = f'{shop.slug}.png'
    shop.qr_code.save(filename, File(buffer), save=True)