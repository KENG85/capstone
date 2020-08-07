import smtplib
from email.mime.text import MIMEText


def send_mail(timestamp, org, sport, pos, player, sleep, nutrition, fatigue, motivation, stress, RPE, tweet):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = 'engardathletics@gmail.com'
    password = 'capstone1234'
    message = f"<h3>New Feedback Submission</h3><ul><li>Customer: {customer}</li><li>Dealer: {dealer}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"

    sender_email = 'engardathletics@gmail.co,'
    receiver_email = 'kate@engardathletics.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Player Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
