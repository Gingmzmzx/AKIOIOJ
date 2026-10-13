import logging
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

import aiosmtplib

from vj4 import error
from vj4.util import argmethod
from vj4.util import options

options.define('smtp_host', default='', help='SMTP server')
options.define('smtp_port', default=465, help='SMTP server port')
options.define('smtp_user', default='', help='SMTP username')
options.define('smtp_password', default='', help='SMTP password')
options.define('smtp_use_tls', default=True,
               help='Connect with implicit TLS (SMTPS). Set to false to use '
                    'plain SMTP with opportunistic STARTTLS upgrade.')
options.define('mail_from', default='', help='Mail from')

_logger = logging.getLogger(__name__)


@argmethod.wrap
async def send_mail(to: str, subject: str, content: str):
  _logger.info('Sending mail')
  _logger.debug('to: %s, subject: %s, content: %s', to, subject, content)

  msg = EmailMessage()
  msg.set_content(content, subtype='html', charset='utf-8')
  msg['Subject'] = subject
  msg['From'] = options.mail_from
  msg['To'] = to
  msg['Date'] = formatdate(localtime=True)
  msg['Message-ID'] = make_msgid()

  try:
    _logger.debug('Connecting to SMTP server')
    async with aiosmtplib.SMTP(hostname=options.smtp_host,
                               port=options.smtp_port,
                               username=options.smtp_user or None,
                               password=options.smtp_password or None,
                               use_tls=options.smtp_use_tls) as server:
      _logger.debug('SMTP server established')
      _logger.debug('SMTP server login successful')
      await server.send_message(msg)
      _logger.debug('SMTP server send mail successful')
  except (aiosmtplib.SMTPException, OSError) as e:
    _logger.exception('Failed to send mail to %s', to)
    raise error.SendMailError(to) from e


if __name__ == '__main__':
  argmethod.invoke_by_args()
