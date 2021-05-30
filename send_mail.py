
from Agile.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
def sendmail():
    send_mail('Jenkins Build Failed', 'The last build failed, check it!', EMAIL_HOST_USER, ['yarinaf1@gmail.com','gaico070@gmail.com'], fail_silently=True)

if __name__ == '__main__':
    try:
        sendmail()
    except Exception as e:
        print(e)