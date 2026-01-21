from demand_ops.config import get_settings

def test_sqlalchemy_url_builds():
    s = get_settings()
    url = s.sqlalchemy_url()
    assert "postgresql" in url
