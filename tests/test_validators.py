import importlib
import types
import sys
from pathlib import Path


def load_app_module():
    # Ensure project root is on sys.path for direct module import
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    mod = importlib.import_module("app")
    assert isinstance(mod, types.ModuleType)
    return mod


def test_validate_date_accepts_common_formats():
    app = load_app_module()
    ok, msg = app._validate_date("10/15/2025")
    assert ok and msg is None
    ok, msg = app._validate_date("10-15-2025")
    assert ok


def test_validate_date_rejects_bad_values():
    app = load_app_module()
    ok, msg = app._validate_date("13/40/2025")
    assert not ok and isinstance(msg, str)


def test_validate_payee_exact_and_case_insensitive():
    app = load_app_module()
    ok, _ = app._validate_payee("Plumbing Ink 123", "Plumbing Ink 123")
    assert ok
    ok, _ = app._validate_payee("plumbing   ink 123", "Plumbing Ink 123")
    assert ok


def test_parse_currency_handles_symbols_and_commas():
    app = load_app_module()
    assert app._parse_currency("$1,200.00") == 1200.0
    assert app._parse_currency("86.45") == 86.45
    assert app._parse_currency("bad") is None


def test_validate_amount_numeric_matches_within_cents():
    app = load_app_module()
    ok, _ = app._validate_amount_numeric("$150.00", "$150.00")
    assert ok
    ok, _ = app._validate_amount_numeric("150", "$150.00")
    assert ok
    ok, _ = app._validate_amount_numeric("149.99", "$150.00")
    assert not ok


def test_validate_amount_words_normalizes_whitespace_and_case():
    app = load_app_module()
    ok, _ = app._validate_amount_words(
        "one   hundred FIFTY dollars and 00/100",
        "One hundred fifty dollars and 00/100",
    )
    assert ok


def test_compute_filled_fields_steps_and_default_order():
    app = load_app_module()
    # Scenario 0 has explicit steps; verify progression
    fields0 = app._compute_filled_fields(0, -1)
    assert all(v == "" for v in fields0.values())
    fields0 = app._compute_filled_fields(0, 0)
    assert fields0["date"] != "" and fields0["payee"] == ""

    # A scenario with empty steps should follow default order
    fields1 = app._compute_filled_fields(1, 2)
    assert fields1["amount_numeric"] != "" and fields1["amount_words"] == ""


