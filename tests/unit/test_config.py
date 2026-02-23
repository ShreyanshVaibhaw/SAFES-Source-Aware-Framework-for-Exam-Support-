from src.utils.config import ConfigLoader


def test_config_get_and_contains():
    cfg = ConfigLoader()
    assert cfg.get("app.name") is not None
    assert "app.name" in cfg
    assert cfg.get("missing.path", default="x") == "x"
    assert cfg.get_section("app")["name"]


def test_config_common_properties():
    cfg = ConfigLoader()
    assert isinstance(cfg.api_port, int)
    assert isinstance(cfg.allowed_extensions, list)
    assert cfg.llm_model
    assert isinstance(cfg.chunk_size, int)
    assert cfg.project_root.exists()
    cfg.reload()
