import base64
import hashlib
import hoedown
# 懒得构建镜像了，就像这样凑活着用吧
try:
#   import markdown as mdparser
  import bleach
except ImportError:
  import pip
  pip.main("install bleach".split())
#   import markdown as mdparser
  import bleach
import jinja2
import markupsafe
import re
from urllib import parse

from vj4.util import options


MARKDOWN_EXTENSIONS = (hoedown.EXT_TABLES |  # Parse PHP-Markdown style tables.
                       hoedown.EXT_FENCED_CODE |  # Parse fenced code blocks.
                       hoedown.EXT_AUTOLINK |  # Automatically turn safe URLs into links.
                       hoedown.EXT_NO_INTRA_EMPHASIS |  # Disable emphasis_between_words.
                       hoedown.EXT_MATH |  # Parse TeX $$math$$ syntax, Kramdown style.
                       hoedown.EXT_SPACE_HEADERS |  # Require a space after '#' in headers.
                       hoedown.EXT_MATH_EXPLICIT |  # Instead of guessing by context, parse $inline math$ and $$always block math$$ (requires EXT_MATH).
                       hoedown.EXT_DISABLE_INDENTED_CODE |  # Don't parse indented code blocks.
                       hoedown.EXT_FOOTNOTES | hoedown.EXT_STRIKETHROUGH | hoedown.EXT_UNDERLINE | hoedown.EXT_HIGHLIGHT | hoedown.EXT_QUOTE | hoedown.EXT_SUPERSCRIPT )
MARKDOWN_RENDER_FLAGS = ( # hoedown.HTML_ESCAPE |  # Escape all HTML.
                         hoedown.HTML_HARD_WRAP)  # Render each linebreak as <br>.

ALLOWED_TAGS = bleach.sanitizer.ALLOWED_TAGS + [
    'table', 'tbody', 'thead', 'tr', 'th', 'td',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'blockquote', 'p', 'b', 'i', 'u', 'strong', 'em', 'sup', 'a', 'img', 'del', 'mark', 'br', 'hr',
    'div', 'span', 'iframe',
    'pre', 'code']
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'style'],
    'img': ['src', 'alt', 'style'],
    'div': ['class', 'style'],
    'span': ['class', 'style'],
    'th': ['class', 'style'],
    'td': ['class', 'style'],
    'tr': ['class', 'style'],
    'table': ['class', 'style'],
    'thead': ['class', 'style'],
    'tbody': ['class', 'style'],
    'iframe': ['src', 'style', 'width', 'height', 'frameborder', 'allow', 'allowfullscreen'],
}

FS_RE = re.compile(r'\(vijos\:\/\/fs\/([0-9a-f]{40,})\)')


def nl2br(text):
  markup = jinja2.escape(text)
  return jinja2.Markup('<br>'.join(markup.split('\n')))


def fs_replace(m):
  # TODO(twd2): reverse_url
  return '(' + options.cdn_prefix.rstrip('/') + '/fs/' + m.group(1) + ')'


def markdown(text):
  text = FS_RE.sub(fs_replace, text)
  # md_ctx = mdparser.markdown(text,
  #   extensions=[
  #       'markdown.extensions.toc',
  #       'markdown.extensions.extra',
  #       'markdown.extensions.admonition',
  #       'markdown.extensions.codehilite',
  #       'markdown.extensions.meta',
  #       'markdown_katex',
  #   ],
  #   extension_configs={
  #       'markdown_katex': {
  #           'no_inline_svg': True,      # fix for WeasyPrint
  #           'insert_fonts_css': True,
  #       },
  #   }
  # )
  # return markupsafe.Markup(md_ctx)

  md_ctx = hoedown.html(
      text, extensions=MARKDOWN_EXTENSIONS, render_flags=MARKDOWN_RENDER_FLAGS)
  clean_html = bleach.clean(md_ctx, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
  clean_html = clean_html.replace("<iframe ", "<iframe sandbox='allow-scripts' ")
  # clean_html = md_ctx
  return markupsafe.Markup(clean_html)


def gravatar_url(gravatar, size=200):
  # TODO: 'd' should be https://domain/img/avatar.png
  if not gravatar:
    gravatar = "https://old.xzynb.top/pic/1ico.png"
  return (gravatar)


def paginate(page, num_pages):
  radius = 2
  if page > 1:
    yield 'first', 1
    yield 'previous', page - 1
  if page <= radius:
    first, last = 1, min(1 + radius * 2, num_pages)
  elif page >= num_pages - radius:
    first, last = max(1, num_pages - radius * 2), num_pages
  else:
    first, last = page - radius, page + radius
  if first > 1:
    yield 'ellipsis', 0
  for page0 in range(first, last + 1):
    if page0 != page:
      yield 'page', page0
    else:
      yield 'current', page
  if last < num_pages:
    yield 'ellipsis', 0
  if page < num_pages:
    yield 'next', page + 1
    yield 'last', num_pages


def format_size(size, base=1, ndigits=3):
  size *= base
  unit = 1024
  unit_names = ['Bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
  for unit_name in unit_names:
    if size < unit:
      return '{0} {1}'.format(round(size, ndigits=ndigits), unit_name)
    size /= unit
  return '{0} {1}'.format(round(size * unit, ndigits=ndigits), unit_names[-1])


def format_seconds(seconds):
  seconds = int(seconds)
  return '{:02}:{:02}:{:02}'.format(seconds // 3600, seconds % 3600 // 60, seconds % 60)


def base64_encode(str):
  encoded = base64.b64encode(str.encode())
  return encoded.decode()


def dedupe(list):
  result = []
  result_set = set()
  for i in list:
    if i in result_set:
      continue
    result.append(i)
    result_set.add(i)
  return result