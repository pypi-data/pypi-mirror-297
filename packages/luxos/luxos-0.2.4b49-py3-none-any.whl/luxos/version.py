from __future__ import annotations

import sys
import types
from pathlib import Path

__version__ = "0.2.4b49"
__hash__ = "e305ee7a746434e1ebb18484bdf25c6e8ff97cc2"


def get_version_info(modules: list[types.ModuleType] | None = None) -> dict[str, str]:
    result = {
        "py": sys.version.partition(" ")[0],
        "luxos": ", ".join(
            str(c) if str(c) else "N/A" for c in [__version__, __hash__]
        ),
    }

    module = modules[-1] if modules else None
    if module:
        if path := getattr(module, "__file__", None):
            name = Path(path).name
        else:
            name = getattr(module, "__name__", str(module))
        if name not in {
            "luxos.py",
            "luxos_run.py",
        }:
            result[name] = getattr(module, "__version__", "N/A")

    return result


def get_version(modules: list[types.ModuleType] | None = None) -> str:
    return ", ".join(f"{k}[{v}]" for k, v in get_version_info().items())
