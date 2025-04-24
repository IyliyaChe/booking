
import smtplib
import ezgmail
from app.bookings.dao import BookingDAO
from app.config import settings
from app.tasks.email_templates import create_booking_reminder_template


async def remind_of_bookings(days: int):
    bookings = await BookingDAO.find_to_remind(days)
    email_to_mock = settings.SMTP_USER

    #Версия для сети
    for booking in bookings:
        print(booking)
        ezgmail.send(email_to_mock, 'Напоминание о бронировании', 
                     f''' Уважаемый <h1>пользователь</h1>, email: {booking.email},
                     Вы забронировали отель с {booking.date_from} по {booking.date_to}
                     ''')
    #Версия для прода
    # msgs = []
    # for booking in bookings:
    #     email_to = booking.email
    #     email_to = settings.SMTP_USER
    #     booking_data = {
    #         "date_to": booking.date_to,
    #         "date_from": booking.date_from,
    #     }
    #     msg_content = create_booking_reminder_template(booking_data, email_to, days)
    #     msgs.append(msg_content)

    # with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
    #     server.login(settings.SMTP_USER, settings.SMTP_PASS)
    #     for msg_content in msgs:
    #         server.send_message(msg_content)
