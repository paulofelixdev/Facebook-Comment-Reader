import smtplib, ssl, json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send(emailTo, subject, commentData):

    with open('config.json') as json_file:
        data = json.load(json_file)
        EMAIL = data['Email']['EMAIL']
        PASSWORD = data['Email']['PASSWORD']

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = EMAIL
    message["To"] = emailTo

    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = EMAIL
    password = PASSWORD

    html = """\
    <html>
      <body>
      <tbody>
        {%content%}
        </tbody>
      </body>
    </html>
    """

    trTemplate = """<tr style="border: 5px solid black;">
                    <td style="width: 400px;"><a href="{%authorid%}" target="_blank" rel="noopener">{%authorname%}</a> {%DateTime%}</td>
                    </tr>
                    <tr>
                    <td style="width: 400px;">{%Comment%}</td>
                    </tr>
                    <tr>
                    <td style="width: 400px;"><a href="https://www.facebook.com/permalink.php?comment_id={%commentid%}&story_fbid={%pageid%}">See Comment</a></td>
                    </tr><hr>"""

    tableRows = ''
    for data in commentData["NeedHelp"]:

        pageId = data["id"].split('_')[0]
        commentId = data["id"].split('_')[1]
        tableRows = tableRows + trTemplate\
            .replace("{%authorid%}", data["from"]["id"])\
            .replace("{%authorname%}", data["from"]["name"])\
            .replace("{%DateTime%}", data["created_time"])\
            .replace("{%Comment%}", data["message"])\
            .replace("{%commentid%}", commentId)\
            .replace("{%pageid%}", pageId)









    html = html.replace("{%content%}", tableRows)

    # Turn these into plain/html MIMEText objects
    htmlMessage = MIMEText(html, "html")

    message.attach(htmlMessage)
    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, emailTo, message.as_string()
        )
    print("Sent!")