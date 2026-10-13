import base64
import hashlib
import bleach
import markdown as _md
import markupsafe
import re
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
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
# dollar sign or bracket.
MATH_RE = re.compile(r'''
    (?<!\\)\$\$(?P<display>.+?)(?<!\\)\$\$
  | (?<!\\)\\\[(?P<display_bracket>.+?)(?<!\\)\\\]
  | (?<!\\)\$(?!\$)(?P<inline>[^\n]+?)(?<!\\)\$(?!\$)
  | (?<!\\)\\\((?P<inline_bracket>.+?)(?<!\\)\\\)
''', re.VERBOSE | re.DOTALL)

MATH_PLACEHOLDER = '@@MATH{0}@@'


class _MathTreeprocessor(Treeprocessor):
  """Replace math with placeholders before the HTML is sanitized.

  Markdown would otherwise mangle TeX source (underscores turn into emphasis,
  backslashes turn into escapes) and bleach would strip the markup KaTeX needs.
  The placeholders are substituted back, HTML escaped, once bleach has run.
  """

  def __init__(self, md, store):
    super(_MathTreeprocessor, self).__init__(md)
    self.store = store

  def run(self, root):
    self._walk(root)
    return root

  def _walk(self, element):
    # Code spans and blocks are never math.
    if element.tag in ('code', 'pre'):
      return
    if element.text:
      element.text = self._replace(element.text)
    for child in element:
      self._walk(child)
      if child.tail:
        child.tail = self._replace(child.tail)

  def _replace(self, text):
    def repl(match):
      index = len(self.store)
      self.store.append(match.group(0))
      return MATH_PLACEHOLDER.format(index)
    return MATH_RE.sub(repl, text)


class _MathExtension(Extension):
  def __init__(self, store):
    super(_MathExtension, self).__init__()
    self.store = store

  def extendMarkdown(self, md):
    # Runs last. It has to come after the inline processor (20) so that the
    # TeX source is read from finished text nodes, and after UnescapeTreeprocessor
    # (0), which turns Markdown's internal escapes back into real characters.
    md.treeprocessors.register(_MathTreeprocessor(md, self.store), 'vj4_math', -1)


def _restore_math(html, store):
  for index, source in enumerate(store):
    html = html.replace(MATH_PLACEHOLDER.format(index),
                        markupsafe.escape(source))
  return html


def markdown(text):
  text = FS_RE.sub(fs_replace, text)
  math = []
  md_ctx = _md.markdown(text,
                        extensions=MARKDOWN_EXTENSIONS + [_MathExtension(math)])
  clean_html = bleach.clean(md_ctx, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
  clean_html = clean_html.replace("<iframe ", "<iframe sandbox='allow-scripts' ")
  return markupsafe.Markup(_restore_math(clean_html, math))


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

