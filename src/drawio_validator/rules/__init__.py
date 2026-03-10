"""Rule registry for drawio-validator."""

import xml.etree.ElementTree as ET
from typing import Callable, List

from drawio_validator.severity import Finding

# Type alias for rule functions
RuleFunc = Callable[[ET.Element], List[Finding]]

# Registry of all rule functions
_RULES: List[RuleFunc] = []


def register(func: RuleFunc) -> RuleFunc:
    """Register a rule function."""
    _RULES.append(func)
    return func


def get_all_rules() -> List[RuleFunc]:
    """Return all registered rule functions."""
    return list(_RULES)
