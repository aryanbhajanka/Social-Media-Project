import smtplib

sender = 'redstonehomeai@gmail.com'
mail_pwd = 'Aryanbhajanka@0204'
receivers = ['aryanbhajanka204@gmail.com','amritabhajanka@gmail.com','manish.bhajanka@gmail.com']
message = "This Message Was Sent Using Python By Aryan!"

mail_server = smtplib.SMTP('smtp.gmail.com',587)
mail_server.starttls()
mail_server.login(sender, mail_pwd)
mail_server.sendmail(sender,receivers,message)

smtpObj = smtplib.SMTP('localhost')
smtpObj.sendmail(sender, receivers, message)