import cv2
import numpy as np
import email, smtplib, ssl
import time

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)
kernel = np.ones((5, 5), np.uint8)

flagBool = True
faceCascade = cv2.CascadeClassifier("C:/Users/hassa/Downloads/haarcascades/haarcascade_frontalface_default.xml")

userEmail = input("Please enter your email here: ")
sender_email = userEmail
receiver_email = userEmail
password = input("Please enter your email's password here: ")

while True:
    success, img = cap.read()
    cv2.imshow("Result", img)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        if flagBool == True:


            #email video
            subject = "An email with attachment from Python"
            body = "This is an email with attachment sent from Python"

            # Create a multipart message and set headers
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            message["Bcc"] = receiver_email  # Recommended for mass emails

            # Add body to email
            message.attach(MIMEText(body, "plain"))

            # take video for 5 seconds
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

            capture_duration = 5
            start_time = time.time()
            while (int(time.time() - start_time) < capture_duration):
                ret, frame = cap.read()
                if ret == True:
                    out.write(frame)
                else:
                    break
                cv2.imshow('Result', frame)


            filename = "output.avi"  # In same directory as script

            # Open PDF file in binary mode
            with open(filename, "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )

            # Add attachment to message and convert message to string
            message.attach(part)
            text = message.as_string()

            # Log in to server using secure context and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, text)

                flagBool = False

    cv2.imshow("Result", img)
    cv2.waitKey(2)

