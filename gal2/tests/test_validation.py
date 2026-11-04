from gal2.validation import run_validation

def test_validation_smoke_report_all_checks_pass():
    report = run_validation(20261104)
    assert all(report["checks"].values())
    assert report["validation_type"] == "synthetic_mechanism_smoke_test"

def test_validation_is_reproducible():
    assert run_validation(12345) == run_validation(12345)
