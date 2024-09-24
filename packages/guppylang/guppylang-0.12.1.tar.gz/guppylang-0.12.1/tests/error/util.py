import importlib.util
import pathlib
import pytest
from hugr import tys
from hugr.tys import TypeBound

from guppylang.error import GuppyError
from guppylang.module import GuppyModule

import guppylang.decorator as decorator


def run_error_test(file, capsys):
    file = pathlib.Path(file)

    with pytest.raises(GuppyError):
        importlib.import_module(f"tests.error.{file.parent.name}.{file.name}")

    err = capsys.readouterr().err

    with pathlib.Path(file.with_suffix(".err")).open() as f:
        exp_err = f.read()

    exp_err = exp_err.replace("$FILE", str(file))
    assert err == exp_err


util = GuppyModule("test")


@decorator.guppy.type(
    tys.Opaque(extension="", id="", args=[], bound=TypeBound.Copyable), module=util
)
class NonBool:
    pass
