import base64
import hashlib
import bleach
import markdown as _md
import markupsafe
import re
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from urllib import parse

from vj4.util import options

ALLOWED_TAGS = bleach.sanitizer.ALLOWED_TAGS + [
    'table', 'tbody', 'thead', 'tr', 'th', 'td',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'blockquote', 'q', 'p', 'b', 'i', 'u', 'strong', 'em', 'sup', 'a', 'img', 'del', 'mark', 'br', 'hr',
    'div', 'span', 'iframe',
    'pre', 'code']
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'style'],
    'img': ['src', 'alt', 'style'],
    'div': ['class', 'style'],
    'p': ['class', 'style'],
    'q': ['class', 'style'],
    'b': ['class', 'style'],
    'i': ['class', 'style'],
    'u': ['class', 'style'],
    'strong': ['class', 'style'],
    'sup': ['class', 'style'],
    'em': ['class', 'style'],
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
  markup = markupsafe.escape(text)
  return markupsafe.Markup('<br>'.join(markup.split('\n')))


def fs_replace(m):
  # TODO(twd2): reverse_url
  return '(' + options.cdn_prefix.rstrip('/') + '/fs/' + m.group(1) + ')'


MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.footnotes',
    'markdown.extensions.nl2br',
    'markdown.extensions.codehilite',
    'markdown.extensions.toc',
]


# Display math first, then inline math. A leading backslash escapes a literal
# dollar sign or bracket. Inline math stays on one line so that a stray `$`
# cannot swallow the rest of the paragraph.
MATH_PATTERN = (
    r'(?<!\\)\$\$(?P<display>.+?)(?<!\\)\$\$'
    r'|(?<!\\)\\\[(?P<display_bracket>.+?)(?<!\\)\\\]'
    r'|(?<!\\)\$(?!\$)(?P<inline>[^\n]+?)(?<!\\)\$(?!\$)'
    r'|(?<!\\)\\\((?P<inline_bracket>.+?)(?<!\\)\\\)'
)


class _MathInlineProcessor(InlineProcessor):
  """Keep TeX source out of Markdown's way, verbatim, for the KaTeX renderer.

  Markdown would otherwise mangle the source: underscores become emphasis,
  `\\` and `\\{` lose their backslash to the escape pattern, and the nl2br
  extension shreds multi-line display math into separate text nodes.

  Returning a plain string stashes the match, and stashed matches are skipped
  by every later inline pattern, so the source reaches the page untouched.
  """

  def handleMatch(self, m, data):
    return m.group(0), m.start(0), m.end(0)


class _MathExtension(Extension):
  def extendMarkdown(self, md):
    # Between the code span pattern (190) and the escape pattern (180): a `$`
    # inside `code` is not math, and `\\`/`\\{` inside math are still intact.
    md.inlinePatterns.register(_MathInlineProcessor(MATH_PATTERN, md), 'vj4_math', 185)


def markdown(text):
  text = FS_RE.sub(fs_replace, text)
  md_ctx = _md.markdown(text, extensions=MARKDOWN_EXTENSIONS + [_MathExtension()])
  clean_html = bleach.clean(md_ctx, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
  clean_html = clean_html.replace("<iframe ", "<iframe sandbox='allow-scripts' ")
  return markupsafe.Markup(clean_html)


def gravatar_url(gravatar, size=200):
  if not gravatar:
    gravatar = options.default_avatar
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


def is_digit(value):
  if isinstance(value, str):
    return value.isdigit()
  elif isinstance(value, int):
    return True
  return False

