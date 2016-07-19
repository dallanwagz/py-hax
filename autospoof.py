import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import argparse

p = argparse.ArgumentParser()
p.add_argument('-s', 
               '--server', 
               type=str, 
               help='smtp server', 
               required='True')
p.add_argument('-p', 
               '--port', 
               type=int, 
               help='smtp server port', 
               required='True')
p.add_argument('-t', 
               '--to', 
               type=str, 
               help='to address', 
               required='True')
p.add_argument('-F', 
              '--From', 
              type=str, 
              help='from address', 
              required='True')
p.add_argument('-j', 
              '--subject', 
              type=str, 
              help='email subject', 
              required='True')
p.add_argument('-f', 
              '--filename', 
              type=str, 
              help='file attachment')
p.add_argument('-d',
              '--displayname',
              type=str,
              help='Display name email header (From)')
p.add_argument('-b',
              '--body',
              type=str,
              help='Body of email')
args = p.parse_args()

class mysmtp:
   def __init__(self, server, port, toEmail, fromEmail, subject):
       self.server = server 
       self.port = port
       self.toEmail = toEmail
       self.fromEmail = fromEmail
       self.subject = subject
       self.filename = ''
       self.displayname = ''
       self.body = ''

   def send_message(self):
        
       msg = MIMEMultipart('alternative')
       msg['From'] = self.fromEmail
       msg['To'] = self.toEmail
       msg['Subject'] = self.subject
       if self.filename:
           f = file(self.filename)
           attachment = MIMEText(f.read())
           attachment.add_header('Content-Disposition',
                                 'attachment', 
                                 filename=self.filename)
           msg.attach(attachment)
           print f
       if self.displayname:
           display_name = self.displayname + "<" + self.fromEmail + ">'"
           msg.replace_header('From', display_name)
       if self.body:
           body = self.body
           content = MIMEText(body, 'plain')
           msg.attach(content)
       else:
           body = 'Whenever I\'m about to do something, I think, \'Would an idiot do that?\' And if they would, I do not do that thing.'
           content = MIMEText(body, 'plain')
           msg.attach(content)
       try: 
           print '[+] attempting to send message'
           s = smtplib.SMTP(self.server, self.port)
           s.sendmail(self.fromEmail, self.toEmail, msg.as_string())
           print '[$] successfully sent through {}:{}'.format(self.server,
                                                              self.port)
       except socket.error as e:
           print '[!] could not connect'


q = mysmtp(args.server, args.port, args.to, args.From, args.subject)
if args.filename:
    q.filename = args.filename
if args.displayname:
    q.displayname = args.displayname
if args.body:
    q.body = args.body
q.send_message()
