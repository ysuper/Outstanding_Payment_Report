from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders
import smtplib


class Email:

    def __init__(self, mail_dict):
        self.From = mail_dict.get('from')
        self.To = mail_dict.get('to')
        self.Cc = mail_dict.get('cc')
        self.Subject = mail_dict.get('subject')
        self.Body = mail_dict.get('body')
        self.Attachment = mail_dict.get('attachment')
        self.Date = formatdate(localtime=True)  # Mon, 09 May 2022 17:58:29 +0800
        self.Content_Transfer_Encoding = mail_dict.get('content_transfer_encoding', '8bit')
        self.Content_Type = mail_dict.get('content_type', 'text/html; charset="UTF-8"')
        self.SMTP = mail_dict.get('smtp', 'smtp.automodules.com')

    def sendmail(self):
        msg = MIMEMultipart()
        split_string = ', '
        msg['From'] = self.From
        msg['To'] = split_string.join(self.To) if isinstance(self.To, list) else self.To
        msg['Cc'] = split_string.join(self.Cc) if isinstance(self.Cc, list) else self.Cc
        msg['Subject'] = self.Subject
        msg["Date"] = self.Date
        msg["Content-Transfer-Encoding"] = self.Content_Transfer_Encoding
        msg["Content-Type"] = self.Content_Type
        msg.attach(MIMEText(self.Body, _subtype='html', _charset='utf-8'))
        if self.Attachment:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(self.Attachment, "rb").read(), "utf-8")
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=self.Attachment)
            msg.attach(part)
        try:
            s = smtplib.SMTP(self.SMTP)
            s.send_message(msg)
            s.quit()
            print("郵件已發送完成。")
        except Exception as e:
            print("Error: 無法發送郵件。")
            print(e)

    @staticmethod
    def to_html(df, table_title):
        df.index += 1
        table_html = df.to_html(justify="left").replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
        title_html = "<h3><font color='blue'>{}</font></h3>".format(table_title)
        rtn_html = title_html + '\n' + table_html
        return rtn_html


if __name__ == "__main__":
    mail_dict = {
        'from': 'noreply@automodules.com',
        'to': [],
        'cc': 'ysuper.liang@automodules.com',
        'subject': 'test',
        'body': 'hello world'
    }
    mail = Email(mail_dict)
    mail.sendmail()
