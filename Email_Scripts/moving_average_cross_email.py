import pandas as pd
import email_module as sendemail
from html_builder import make_table


df_receivers = pd.read_csv("C:/Users/us52873/Documents/Personal/investing/recipients.csv")

df = pd.read_csv("C:/Users/us52873/Documents/Personal/investing/ETL_Scripts/detected_crosses_in_moving_avg.csv")


to_list = ['AlohaAlerts11@gmail.com']
cc_list = ['AlohaAlerts11@gmail.com']
bcc_list = list(df_receivers.Email.unique())

classes = {
    'Symbol': 'bold',
}

custom_styles = 'th{background-color: #22767C;}'

html_table = make_table(df, col_classes=classes, columns=['Symbol', 'Narrative'], styles=custom_styles)

html = open("./html_files/Moving_Average_trigger.html", "r").read()

html_formatted = html.format(name='Dan', table=html_table)

s, logger, log_capture_string = sendemail.open_conn()

print(s)
print(logger)

result = sendemail.send_moving_average_email('text', html_formatted, s, logger, log_capture_string, to_list, cc_list , bcc_list, 'test subject')

print(result)

status = result.split(":")[0]
if status == 'FAILURE':
    logger.error(result)
else:
    logger.info(result)

sendemail.close_conn(s, logger, log_capture_string, 'C:/Users/us52873/Documents/Personal/investing/logs/moving_avg_email_log.txt')
