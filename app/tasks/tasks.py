from pathlib import Path


from pydantic import EmailStr
from app.config import settings
from app.tasks.celery_app import celery
from PIL import Image

from app.tasks.email_templates import create_booking_confirmation_template
import smtplib
import ezgmail
from time import sleep


@celery.task
def process_pic(
    path: str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_1000_500 = im.resize((1000,500))
    im_resized_200_100 = im.resize((200,100))
    im_resized_1000_500.save(f'app/static/images/resized_1000_500_{im_path.name}')
    im_resized_200_100.save(f'app/static/images/resized_200_100_{im_path.name}')

# для background_task первую строку закомментировать
@celery.task
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr,
):
    email_to_mock = settings.SMTP_USER
# Обходной путь для работы из сети
    ezgmail.send(email_to_mock, 'Подтверждение бронирования', 
        f'''
            <h1>Подтвердите бронирование</h1>
            Вы забронировали отель с {booking['date_from']} по {booking['date_to']}
        ''')

 # Раскомментировать для переноса на сервер
 #   msg_content = create_booking_confirmation_template(booking, email_to_mock)
 #   with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
 #       server.login(settings.SMTP_USER, settings.SMTP_PASS)
 #       server.send_message(msg_content)

    