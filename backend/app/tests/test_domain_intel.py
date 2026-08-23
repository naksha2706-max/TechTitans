from app.domain_intel import extract_domain, analyze_domain

def test_extract_domain():
    assert extract_domain("https://example.com/path") == "example.com"
    assert extract_domain("http://www.testcompany.org:8080/job") == "testcompany.org"
    assert extract_domain("") == ""

def test_analyze_domain():
    res_empty = analyze_domain("")
    assert res_empty["domain"] == ""
    assert res_empty["has_ssl_error"] is False

    res_example = analyze_domain("https://example.com")
    assert res_example["domain"] == "example.com"
