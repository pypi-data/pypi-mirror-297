# Copyright 2024 by Falconry maintainers.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pygments.style import Style
from pygments.token import Comment
from pygments.token import Error
from pygments.token import Generic
from pygments.token import Keyword
from pygments.token import Name
from pygments.token import Number
from pygments.token import Operator
from pygments.token import String
from pygments.token import Token

from .common import bold
from .common import bold_italic
from .common import italic


class Colors:
    yellow = '#ffc66d'
    orange = '#df5a1f'
    crimson = '#ed3b5f'
    brown = '#bc9458'
    olive = '#c2c200'
    green = '#73b07b'
    pear = '#c9cc3f'
    purple = '#ce7ebe'
    darkgray = '#171717'
    white = '#e6e1dc'


class FalconryDarkStyle(Style):
    """Falconry dark Pygments style."""

    name = 'falconry-dark'

    background_color = Colors.darkgray
    highlight_color = Colors.white

    styles = {
        Token: Colors.white,
        Comment: italic | Colors.brown,
        Comment.PreProc: italic | Colors.brown,
        Comment.Special: bold_italic | Colors.brown,
        Keyword: bold | Colors.orange,
        Keyword.Type: Colors.olive,
        Operator: Colors.white,
        Operator.Word: Colors.white,
        String: Colors.olive,
        String.Escape: Colors.pear,
        Number: Colors.purple,
        Name.Builtin: bold | Colors.orange,
        Name.Builtin.Pseudo: Colors.yellow,
        Name.Variable: Colors.green,
        Name.Variable.Magic: Colors.purple,
        Name.Constant: Colors.green,
        Name.Class: bold | Colors.green,
        Name.Function: bold | Colors.green,
        Name.Namespace: Colors.white,
        Name.Exception: Colors.crimson,
        Name.Tag: Colors.white,
        Name.Attribute: Colors.white,
        Name.Decorator: bold | Colors.purple,
        Generic.Heading: bold | Colors.yellow,
        Generic.Subheading: bold | Colors.olive,
        Generic.Deleted: Colors.crimson,
        Generic.Inserted: Colors.purple,
        Generic.Error: Colors.crimson,
        Generic.Emph: italic,
        Generic.Strong: bold,
        Generic.Prompt: Colors.green,
        Generic.Output: Colors.yellow,
        Generic.Traceback: Colors.crimson,
        Error: Colors.crimson,
    }


__all__ = ['FalconryDarkStyle']
