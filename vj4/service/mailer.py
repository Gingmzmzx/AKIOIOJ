import aiosmtplib
import aiosmtplib.errors
import logging
from email.mime import text

from vj4 import error
from vj4.util import argmethod
from vj4.util import options

options.define('smtp_host', default='', help='SMTP server')
options.define('smtp_port', default=465, help='SMTP server')
options.define('smtp_user', default='', help='SMTP username')
options.define('smtp_password', default='', help='SMTP password')
options.define('mail_from', default='', help='Mail from')

_logger = logging.getLogger(__name__)


@argmethod.wrap
async def send_mail(to: str, subject: str, content: str):
  _logger.info('Sending mail')
  _logger.debug(f'to: {to}, subject: {subject}, content: {content}')
  msg = text.MIMEText(content, _subtype='html', _charset='UTF-8')
  msg['Subject'] = subject
  msg['From'] = options.mail_from
  msg['To'] = to

  try:
    _logger.debug(f'Connecting to SMTP server')
    async with aiosmtplib.SMTP(hostname=options.smtp_host, port=options.smtp_port) as server:
      await server.ehlo()
      _logger.debug(f'SMTP server established')
      await server.login(options.smtp_user, options.smtp_password)
      _logger.debug(f'SMTP server login successful')
      await server.sendmail(options.mail_from, to, msg.as_string())
      _logger.debug(f'SMTP server send mail successful')
  except aiosmtplib.errors.SMTPException as e:
    _logger.exception(e)
    raise error.SendMailError(to)

if __name__ == '__main__':
  argmethod.invoke_by_args()
