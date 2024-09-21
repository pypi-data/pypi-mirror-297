# Copyright 2022 The PyGlove Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utilities for formatting objects."""

import enum
import io
import sys
from typing import Any, Callable, List, Optional, Sequence, Set, Tuple
from pyglove.core.object_utils import common_traits
from pyglove.core.object_utils.value_location import KeyPath


class BracketType(enum.IntEnum):
  """Bracket types used for complex type formatting."""
  # Round bracket.
  ROUND = 0

  # Square bracket.
  SQUARE = 1

  # Curly bracket.
  CURLY = 2


_BRACKET_CHARS = [
    ('(', ')'),
    ('[', ']'),
    ('{', '}'),
]


def bracket_chars(bracket_type: BracketType) -> Tuple[str, str]:
  """Gets bracket character."""
  return _BRACKET_CHARS[int(bracket_type)]


class RawText(common_traits.Formattable):
  """Raw text."""

  def __init__(self, text: str):
    self.text = text

  def format(self, *args, **kwargs):
    return self.text

  def __eq__(self, other: Any) -> bool:
    if isinstance(other, RawText):
      return self.text == other.text
    elif isinstance(other, str):
      return self.text == other
    return False

  def __ne__(self, other: Any) -> bool:
    return not self.__eq__(other)


def kvlist_str(
    kvlist: List[Tuple[str, Any, Any]],
    compact: bool = True,
    verbose: bool = False,
    root_indent: int = 0,
    *,
    label: Optional[str] = None,
    bracket_type: BracketType = BracketType.ROUND,
    markdown: bool = False,
    custom_format: Optional[str] = None,
    **kwargs,
) -> str:
  """Formats a list key/value pairs into a comma delimited string.

  Args:
    kvlist: List of tuples in format of
      (key, value, default_value or a tuple of default values)
    compact: If True, format value in kvlist in compact form.
    verbose: If True, format value in kvlist in verbose.
    root_indent: The indent should be applied for values in kvlist if they are
      multi-line.
    label: (Optional) If not None, add label to brace all kv pairs.
    bracket_type: Bracket type used for embracing the kv pairs. Applicable only
      when `name` is not None.
    markdown: If True, use markdown notion to quote the formatted object.
    custom_format: A string as the name of custom format method. It's effective
      only on value that has the method, for those who do not have the method,
      they will be formatted using `format`, `str` or `repr` method.
    **kwargs: Keyword arguments that will be passed through unto child
      ``Formattable`` objects.
  Returns:
    A formatted string from a list of key/value pairs delimited by comma.
  """
  s = io.StringIO()
  is_first = True
  bracket_start, bracket_end = bracket_chars(bracket_type)

  child_indent = (root_indent + 1) if label else root_indent
  body = io.StringIO()
  for k, v, d in kvlist:
    if isinstance(d, tuple):
      include_pair = True
      for sd in d:
        if sd == v:
          include_pair = False
          break
    else:
      include_pair = v != d
    if include_pair:
      if not is_first:
        body.write(',')
        body.write(' ' if compact else '\n')
      v = format(
          v, compact=compact,
          verbose=verbose,
          root_indent=child_indent,
          custom_format=custom_format,
          **kwargs
      )
      if not compact:
        body.write(_indent('', child_indent))
      if k:
        body.write(f'{k}={str_ext(v, custom_format)}')
      else:
        body.write(str_ext(v, custom_format))
      is_first = False

  if label and not is_first and not compact:
    body.write('\n')

  body = body.getvalue()
  if label is None:
    s = body
  else:
    s.write(label)
    s.write(bracket_start)
    if body:
      if not compact:
        s.write('\n')
      s.write(body)
      if not compact:
        s.write(_indent('', root_indent))
    s.write(bracket_end)
    s = s.getvalue()
  return maybe_markdown_quote(s, markdown)


def quote_if_str(value: Any) -> Any:
  """Quotes the value if it is a str."""
  if isinstance(value, str):
    return repr(value)
  return value


def comma_delimited_str(value_list: Sequence[Any]) -> str:
  """Gets comma delimited string."""
  return ', '.join(str(quote_if_str(v)) for v in value_list)


def auto_plural(
    number: int, singular: str, plural: Optional[str] = None) -> str:
  """Use singular form if number is 1, otherwise use plural form."""
  if plural is None:
    plural = singular + 's'
  return singular if number == 1 else plural


def message_on_path(
    message: str, path: KeyPath) -> str:
  """Formats a message that is associated with a `KeyPath`."""
  if path is None:
    return message
  return f'{message} (path={path})'


def format(   # pylint: disable=redefined-builtin
    value: Any,
    compact: bool = False,
    verbose: bool = True,
    root_indent: int = 0,
    list_wrap_threshold: int = 80,
    strip_object_id: bool = False,
    include_keys: Optional[Set[str]] = None,
    exclude_keys: Optional[Set[str]] = None,
    markdown: bool = False,
    max_str_len: Optional[int] = None,
    max_bytes_len: Optional[int] = None,
    *,
    custom_format: Optional[str] = None,
    **kwargs,
) -> str:
  """Formats a (maybe) hierarchical value with flags.

  Args:
    value: The value to format.
    compact: If True, this object will be formatted into a single line.
    verbose: If True, this object will be formatted with verbosity. Subclasses
      should define `verbosity` on their own.
    root_indent: The start indent level for this object if the output is a
      multi-line string.
    list_wrap_threshold: A threshold in number of characters for wrapping a list
      value in a single line.
    strip_object_id: If True, format object as '<class-name>(...)' other than
      'object at <address>'.
    include_keys: A set of keys to include from the top-level dict or object.
    exclude_keys: A set of keys to exclude from the top-level dict or object.
      Applicable only when `include_keys` is set to None.
    markdown: If True, use markdown notion to quote the formatted object.
    max_str_len: The max length of the string to be formatted. If the string is
      longer than this length, it will be truncated.
    max_bytes_len: The max length of the bytes to be formatted. If the bytes is
      longer than this length, it will be truncated.
    custom_format: A string as the name of custom format method. It's effective
      only on value that has the method, for those who do not have the method,
      they will be formatted using `format`, `str` or `repr` method.
    **kwargs: Keyword arguments that will be passed through unto child
      ``Formattable`` objects.

  Returns:
    A string representation for `value`.
  """

  exclude_keys = exclude_keys or set()

  def _should_include_key(key: str) -> bool:
    if include_keys:
      return key in include_keys
    return key not in exclude_keys

  def _format_child(v):
    return format(v, compact=compact, verbose=verbose,
                  root_indent=root_indent + 1,
                  list_wrap_threshold=list_wrap_threshold,
                  strip_object_id=strip_object_id,
                  max_str_len=max_str_len,
                  max_bytes_len=max_bytes_len,
                  custom_format=custom_format,
                  **kwargs)

  if isinstance(value, common_traits.Formattable):
    return value.format(compact=compact,
                        verbose=verbose,
                        root_indent=root_indent,
                        list_wrap_threshold=list_wrap_threshold,
                        strip_object_id=strip_object_id,
                        include_keys=include_keys,
                        exclude_keys=exclude_keys,
                        max_str_len=max_str_len,
                        max_bytes_len=max_bytes_len,
                        custom_format=custom_format,
                        **kwargs)
  elif isinstance(value, (list, tuple)):
    # Always try compact representation if length is not too long.
    open_bracket, close_bracket = bracket_chars(
        BracketType.SQUARE if isinstance(value, list) else BracketType.ROUND)
    s = [open_bracket]
    s.append(', '.join([_format_child(elem) for elem in value]))
    s.append(close_bracket)
    s = [''.join(s)]
    if not compact and len(s[-1]) > list_wrap_threshold:
      s = [f'{open_bracket}\n']
      s.append(',\n'.join([
          _indent(_format_child(elem), root_indent + 1)
          for elem in value
      ]))
      s.append('\n')
      s.append(_indent(close_bracket, root_indent))
  elif isinstance(value, dict):
    if compact or not value:
      s = ['{']
      s.append(', '.join([
          f'{k!r}: {_format_child(v)}'
          for k, v in value.items() if _should_include_key(k)
      ]))
      s.append('}')
    else:
      s = ['{\n']
      s.append(',\n'.join([
          _indent(f'{k!r}: {_format_child(v)}', root_indent + 1)
          for k, v in value.items() if _should_include_key(k)
      ]))
      s.append('\n')
      s.append(_indent('}', root_indent))
  else:
    if isinstance(value, str):
      if max_str_len is not None and len(value) > max_str_len:
        value = value[:max_str_len] + '...'
      s = [repr_ext(value, custom_format)]
    elif isinstance(value, bytes):
      if max_bytes_len is not None and len(value) > max_bytes_len:
        value = value[:max_bytes_len] + b'...'
      s = [repr_ext(value, custom_format)]
    else:
      s = [repr_ext(value, custom_format)
           if compact else str_ext(value, custom_format)]
      if strip_object_id and 'object at 0x' in s[-1]:
        s = [f'{value.__class__.__name__}(...)']
  return maybe_markdown_quote(''.join(s), markdown)


def _maybe_custom_format(
    v: Any,
    default_fn: Callable[[Any], str],
    custom_format: Optional[str] = None) -> str:
  if custom_format is None:
    return default_fn(v)
  x = getattr(v, custom_format, None)
  if callable(x):
    return x()
  return default_fn(v)


def str_ext(v: Any, custom_format: Optional[str] = None) -> str:
  """"str operator with special format support."""
  return _maybe_custom_format(v, str, custom_format)


def repr_ext(v: Any, custom_format: Optional[str] = None) -> str:
  """repr operator with special format support."""
  return _maybe_custom_format(v, repr, custom_format)


def maybe_markdown_quote(s: str, markdown: bool = True) -> str:
  """Maybe quote the formatted string with markdown."""
  if not markdown:
    return s
  if '\n' not in s:
    return f'`{s}`'
  else:
    return f'```\n{s}\n```'


def printv(v: Any, **kwargs):
  """Prints formatted value."""
  fs = kwargs.pop('file', sys.stdout)
  print(format(v, **kwargs), file=fs)


def _indent(text: str, indent: int) -> str:
  return ' ' * 2 * indent + text
