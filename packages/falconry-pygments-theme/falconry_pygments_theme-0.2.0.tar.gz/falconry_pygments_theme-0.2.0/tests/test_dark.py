import pytest

from falconry_pygments_theme.dark import Colors
from falconry_pygments_theme.dark import FalconryDarkStyle

_color_names = sorted(name for name in dir(Colors) if not name.startswith('_'))


@pytest.mark.parametrize('color_name', _color_names)
def test_contrast(contrast, color_name):
    value = getattr(Colors, color_name)
    if value != FalconryDarkStyle.background_color:
        assert contrast(value, FalconryDarkStyle.background_color) >= 'AA'
