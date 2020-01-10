import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import io

# set creds and login
username = "AlohaAlerts11@gmail.com"
password = "dAnnyb1234"

def open_conn():
    ### Create the logger
    logger = logging.getLogger('Log:')
    logger.setLevel(logging.DEBUG)

    ### Setup the console handler with a StringIO object
    log_capture_string = io.StringIO()
    ch = logging.StreamHandler(log_capture_string)
    ch.setLevel(logging.DEBUG)

    ### Add formatter
    formatter = logging.Formatter('%(asctime)s: %(name)s %(levelname)s, %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # define gmail login
    def estConection(user, pword):
        try:
            # creates SMTP session, activate debug
            s = smtplib.SMTP('smtp.gmail.com', 587)
            #s.set_debuglevel(1)

            # start TLS for security
            s.starttls()

            # Authentication
            s.login(user, pword)
            logger.info('GMAIL connection Success')

        except Exception as e:
            print(e)
            logger.error('GMAIL connection FAILED')
            print('GMAIL connection Failure')
        finally:
            return s

    s = estConection(username, password)

    return (s, logger, log_capture_string)

def send_moving_average_email(text, html, s, logger, string, to_list, cc_list, bcc_list, subject):

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = username
        msg['To'] = ",".join(to_list)
        msg['Cc'] = ",".join(cc_list)
        msg['Bcc'] = ",".join(bcc_list)
        msg.attach(MIMEText(text, 'plain'))
        msg.attach(MIMEText(html, 'html'))
        # receivers = to_list + cc_list + bcc_list
        print('Ready to send Email')
        receivers = ["biancuda11@gmail.com"] ## KEEP FOR TESTING
        s.sendmail(username, receivers, msg.as_string())
        return "SUCCESS"
    except Exception as e:
        print(e)
        return "FAILURE"


def close_conn(s, logger, log_capture_string, path):
    # terminate smtp session
    s.quit()
    logger.info('Close Connection Success')
    ### Pull the contents of logger into a string and close stream
    log_contents = log_capture_string.getvalue()
    log_capture_string.close()

    # Open and write log file
    logStr = "============" + "\n" + log_contents
    logFile = open(path, 'a')
    logFile.write(logStr)
    logFile.close()
