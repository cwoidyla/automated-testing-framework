"""
Copyright 2005-2018 QuantumRocket. All rights reserved.
Use of this source code is governed by a BSD-style
license that can be found in the LICENSE file.
"""

import lib.kvpairs as kvpairs
import lib.log as log

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import imaplib


cfg = kvpairs.load(kvpairs.get_config_filename())

email_live = cfg['email.live']

email_server_smtp_host = cfg['email.server.smtp.host']
email_server_smtp_port = cfg['email.server.smtp.port']
email_server_smtp_username = cfg['email.server.smtp.username']
email_server_smtp_password = cfg['email.server.smtp.password']

email_server_imap_host = cfg['email.server.imap.host']
email_server_imap_username = cfg['email.server.imap.username']
email_server_imap_password = cfg['email.server.imap.password']

email_from = cfg['email.from']


def send(to, subject, body_html):
    """
    Send an email using the configured email server.

    The email will be sent as both html and plain text, therefore making
    no assumptions about the user's email preferences.
    """

    try:

        smtp = smtplib.SMTP(email_server_smtp_host, email_server_smtp_port)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(email_server_smtp_username, email_server_smtp_password)

        msg = MIMEMultipart('alternative')

        text = 'text version of the email message'
        html = body_html

        msg.attach(MIMEText(text, 'plain'))
        msg.attach(MIMEText(html, body_html))

        msg['Subject'] = subject
        msg['From'] = email_from
        msg['To'] = to
        
        if email_live == 'true':
            smtp.sendmail(email_from, [to], msg.as_string())
            log.debug('lib/email.py::send', 'sent email to: ' + to)
        else:
            log.debug('lib/email.py::send', 'sent *MOCK* email to: ' + to)

        smtp.quit()

    except Exception as e:
        log.alert('lib/email.py::send', 'email_server_smtp_host [' + email_server_smtp_host + '], email_server_smtp_port ['
                  + email_server_smtp_port + ']. Error attempting to send email: ' + str(e))


def get_imap_messages():
    """
    Retrieve email messages from the configured IMAP inbox,
    yielding to the caller on each message.
    """

    try:

        imap = imaplib.IMAP4_SSL(email_server_imap_host)
        imap.login(email_server_imap_username, email_server_imap_password)
        imap.select('inbox')

        typ, data = imap.search(None, '(UNSEEN SUBJECT "keyword-goes-here")')

        for num in data[0].split():

            body = imap.fetch(num, '(RFC822)')
            result = imap.copy(num, 'Archive')
            result = imap.store(num, '+FLAGS', '\\Deleted')
            imap.expunge()

            yield body

            # this works, but we don't get the body; do we really need the subject, from, and to?
            #data = imap.fetch(num, '(BODY[HEADER.FIELDS (SUBJECT FROM TO)])')
            #msg = data[1][0][1]
            #yield msg

        imap.expunge()

    except Exception as e:
        log.error('lib/email.py::get_imap_messages', str(e))


def receive():
    """
    Fetch all email from the configured IMAP inbox.
    Return to the caller as a list of dict objects, each one with the contents of a single email.
    """

    inbound_events = {}

    try:

        for body in get_imap_messages():

            # find the ulids
            raw = body[1][0][1]
            body_str = raw.decode("utf-8")
            last_left_bracket = body_str.rfind('[')
            last_right_bracket = body_str.rfind(']')
            ulids = body_str[last_left_bracket + 1 : last_right_bracket].split(':')

            user_task_id = ulids[0]
            button_id = ulids[1]

            inbound_events[user_task_id] = button_id

        # sort of works to parse subject
        # for msg in get_imap_messages():
        #
        #     msg_dict = parse_message(msg)
        #     email_list.append(msg_dict)

    except Exception as e:
        log.alert('lib/email.py::receive', str(e))

    if len(inbound_events) == 0:
        inbound_events = None

    return inbound_events
