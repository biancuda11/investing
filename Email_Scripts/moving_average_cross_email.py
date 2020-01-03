import pandas as pd
import email_module as sendemail
from html_builder import make_table
from premailer import transform
import datetime as dt
from datetime import datetime

df_receivers = pd.read_csv("C:/Users/us52873/Documents/Personal/investing/recipients.csv")

df = pd.read_csv("C:/Users/us52873/Documents/Personal/investing/ETL_Scripts/detected_crosses_in_moving_avg.csv")

date = dt.datetime.now().date()

to_list = ['AlohaAlerts11@gmail.com']
cc_list = ['AlohaAlerts11@gmail.com']
bcc_list = list(df_receivers.Email.unique())

classes = {
    'Symbol': 'bold',
}

custom_styles = 'th{background-color: #22767C;}'

html_table = make_table(df, col_classes=classes, columns=['Symbol', 'Narrative'], styles=custom_styles)

html_table_transform = transform(html_table)

html = open("./html_files/Moving_Average_trigger.html", "r").read()

html_formatted = html.format(name='Gang', table=html_table_transform)

s, logger, log_capture_string = sendemail.open_conn()

print(s)
print(logger)

subject = 'Moving Averages Crossover Email: {date}'.format(date=date)

result = sendemail.send_moving_average_email('text', html_formatted, s, logger, log_capture_string, to_list, cc_list , bcc_list, subject)

print(result)

status = result.split(":")[0]
if status == 'FAILURE':
    logger.error(result)
else:
    logger.info(result)

sendemail.close_conn(s, logger, log_capture_string, 'C:/Users/us52873/Documents/Personal/investing/logs/moving_avg_email_log.txt')
