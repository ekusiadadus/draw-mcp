"""Tests for claims coverage: verify claims.yaml is the source of truth.

claims.yaml is the machine-readable manifest. Tests verify bidirectional
consistency: every claim must be backed by a registered rule, and every
registered rule must appear in claims.yaml.
"""

from pathlib import Path

import yaml

from drawio_validator.rules import Mode, get_all_rules, get_rules_for_mode
from drawio_validator.validator import validate  # noqa: F401 — triggers rule registration

ROOT = Path(__file__).parent.parent
CLAIMS_PATH = ROOT / "claims.yaml"


def _load_claims() -> dict:
    """Load claims.yaml as the single source of truth."""
    with open(CLAIMS_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


class TestClaimsYamlExists:
    def test_claims_yaml_exists(self) -> None:
        assert CLAIMS_PATH.exists(), "claims.yaml must exist as the source of truth"

    def test_claims_yaml_is_valid(self) -> None:
        claims = _load_claims()
        assert "rules" in claims, "claims.yaml must have a 'rules' key"
        assert "golden_examples" in claims, "claims.yaml must have 'golden_examples'"
        assert "mode_hierarchy" in claims, "claims.yaml must have 'mode_hierarchy'"


class TestClaimsRuleCoverage:
    """Bidirectional consistency: claims.yaml <-> rule registry."""

    def test_all_claimed_rules_exist_in_registry(self) -> None:
        """Every rule in claims.yaml must be registered."""
        claims = _load_claims()
        all_rule_names = {r.__name__ for r in get_all_rules()}
        for entry in claims["rules"]:
            func_name = entry["func"]
            assert func_name in all_rule_names, f"Claimed rule '{func_name}' not found in registry"

    def test_all_registered_rules_appear_in_claims(self) -> None:
        """Every registered rule must appear in claims.yaml."""
        claims = _load_claims()
        claimed_funcs = {entry["func"] for entry in claims["rules"]}
        registered_funcs = {r.__name__ for r in get_all_rules()}
        unclaimed = registered_funcs - claimed_funcs
        assert not unclaimed, f"Registered rules missing from claims.yaml: {unclaimed}"

    def test_claimed_mode_matches_registry(self) -> None:
        """Each rule's min_mode in claims.yaml must match its registration."""
        claims = _load_claims()
        for entry in claims["rules"]:
            func_name = entry["func"]
            claimed_mode = Mode(entry["min_mode"])
            rules_at_mode = get_rules_for_mode(claimed_mode)
            names_at_mode = [r.__name__ for r in rules_at_mode]
            assert func_name in names_at_mode, (
                f"Rule '{func_name}' claimed at mode '{claimed_mode.value}' "
                f"but not found at that mode level"
            )

    def test_rule_count_matches(self) -> None:
        """Total rules in claims.yaml must match registry count."""
        claims = _load_claims()
        assert len(claims["rules"]) == len(get_all_rules())


class TestClaimsModeMatrix:
    """Verify mode matrix is explicit and consistent."""

    def test_mode_hierarchy_defined(self) -> None:
        claims = _load_claims()
        hierarchy = claims["mode_hierarchy"]
        assert hierarchy["order"] == ["loose", "standard", "strict", "production"]

    def test_mode_rule_counts_match_claims(self) -> None:
        """Rule counts per mode in claims.yaml must match reality."""
        claims = _load_claims()
        expected_counts = claims["mode_hierarchy"]["rule_counts"]
        for mode_str, expected_count in expected_counts.items():
            mode = Mode(mode_str)
            actual_count = len(get_rules_for_mode(mode))
            assert actual_count == expected_count, (
                f"Mode '{mode_str}': claims.yaml says {expected_count} rules, "
                f"registry has {actual_count}"
            )

    def test_mode_hierarchy_is_monotonic(self) -> None:
        """Each mode level must have >= rules than the previous."""
        claims = _load_claims()
        order = claims["mode_hierarchy"]["order"]
        prev_count = 0
        for mode_str in order:
            count = len(get_rules_for_mode(Mode(mode_str)))
            assert count >= prev_count, (
                f"Mode '{mode_str}' has {count} rules, " f"less than previous level ({prev_count})"
            )
            prev_count = count


class TestClaimsGoldenExamples:
    def test_golden_example_count(self) -> None:
        claims = _load_claims()
        min_count = claims["golden_examples"]["min_count"]
        examples = list((ROOT / "examples").glob("*.drawio"))
        assert len(examples) >= min_count

    def test_required_examples_exist(self) -> None:
        claims = _load_claims()
        required = set(claims["golden_examples"]["required_files"])
        existing = {f.name for f in (ROOT / "examples").glob("*.drawio")}
        missing = required - existing
        assert not missing, f"Missing required examples: {missing}"
