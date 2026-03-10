"""Rule registry for drawio-validator with mode support."""

import xml.etree.ElementTree as ET
from enum import Enum
from typing import Callable, List

from drawio_validator.severity import Finding

# Type alias for rule functions
RuleFunc = Callable[[ET.Element], List[Finding]]


class Mode(Enum):
    """Validation modes, ordered from least to most strict."""

    LOOSE = "loose"
    STANDARD = "standard"
    STRICT = "strict"
    PRODUCTION = "production"


# Ordered mode levels for comparison
_MODE_ORDER = {
    Mode.LOOSE: 0,
    Mode.STANDARD: 1,
    Mode.STRICT: 2,
    Mode.PRODUCTION: 3,
}

# Registry of (rule_func, min_mode) pairs
_RULES: List[tuple[RuleFunc, Mode]] = []


def register(func: RuleFunc = None, *, mode: Mode = Mode.STANDARD) -> RuleFunc:
    """Register a rule function with a minimum mode level.

    Usage:
        @register                      # defaults to STANDARD
        def check_something(root): ...

        @register(mode=Mode.LOOSE)
        def check_basic(root): ...
    """
    if func is not None:
        # Called as @register without arguments
        _RULES.append((func, mode))
        return func

    # Called as @register(mode=...) — return decorator
    def decorator(fn: RuleFunc) -> RuleFunc:
        _RULES.append((fn, mode))
        return fn

    return decorator


def get_all_rules() -> List[RuleFunc]:
    """Return all registered rule functions (regardless of mode)."""
    return [func for func, _ in _RULES]


def get_rules_for_mode(mode: Mode) -> List[RuleFunc]:
    """Return rules applicable at the given mode level.

    A rule registered at Mode.LOOSE will run in all modes.
    A rule registered at Mode.STANDARD will run in STANDARD, STRICT, PRODUCTION.
    """
    target_level = _MODE_ORDER[mode]
    return [func for func, min_mode in _RULES if _MODE_ORDER[min_mode] <= target_level]
