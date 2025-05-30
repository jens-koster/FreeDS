from tfds_cli.commands import dc as dc_module


# Patch subprocess and os.chdir to avoid side effects
def test_dc_no_extra(monkeypatch):
    # Patch dependencies
    monkeypatch.setattr(dc_module, "get_current_stack", lambda: "test_stack")
    monkeypatch.setattr(dc_module, "get_stack_config", lambda stack: {"plugins": ["plugin1", "plugin2"]})
    monkeypatch.setattr(dc_module, "get_stack_names", lambda: ["test_stack"])
    monkeypatch.setattr(dc_module, "get_config", lambda name: {"url": "http://mock-url"})

    # Patch os functions
    monkeypatch.setattr(dc_module.os, "getcwd", lambda: "/tmp")  # type: ignore[attr-defined]
    monkeypatch.setattr(dc_module.os, "chdir", lambda d: None)  # type: ignore[attr-defined]
    monkeypatch.setattr(dc_module.Path, "exists", lambda self: True)  # type: ignore[attr-defined]

    # Call with no extra argument
    result = dc_module.dc(single="current-stack", extra=[])
    assert result is None


def test_dc_plugin_not_found(monkeypatch):
    monkeypatch.setattr(dc_module, "get_current_stack", lambda: "test_stack")
    monkeypatch.setattr(dc_module, "get_stack_config", lambda stack: {"plugins": ["plugin1", "plugin2"]})
    monkeypatch.setattr(dc_module, "get_stack_names", lambda: ["test_stack"])
    monkeypatch.setattr(dc_module, "get_config", lambda name: {"url": "http://mock-url"})
    monkeypatch.setattr(dc_module.os, "getcwd", lambda: "/tmp")  # type: ignore[attr-defined]
    monkeypatch.setattr(dc_module.os, "chdir", lambda d: None)  # type: ignore[attr-defined]
    monkeypatch.setattr(dc_module.Path, "exists", lambda self: True)  # type: ignore[attr-defined]

    # Should print error and return None
    result = dc_module.dc(single="not_a_plugin", extra=["up"])
    assert result is None


def test_dc_malformed_config(monkeypatch):
    monkeypatch.setattr(dc_module, "get_current_stack", lambda: "test_stack")
    monkeypatch.setattr(dc_module, "get_stack_config", lambda stack: {})
    monkeypatch.setattr(dc_module, "get_stack_names", lambda: ["test_stack"])
    monkeypatch.setattr(dc_module, "get_config", lambda name: {"url": "http://mock-url"})
    monkeypatch.setattr(dc_module.os, "getcwd", lambda: "/tmp")  # type: ignore[attr-defined]
    monkeypatch.setattr(dc_module.os, "chdir", lambda d: None)  # type: ignore[attr-defined]
    monkeypatch.setattr(dc_module.Path, "exists", lambda self: True)  # type: ignore[attr-defined]

    result = dc_module.dc(single="current-stack", extra=["up"])
    assert result is None


def test_dc_plugins_key_missing(monkeypatch):
    monkeypatch.setattr(dc_module, "get_current_stack", lambda: "test_stack")
    monkeypatch.setattr(dc_module, "get_stack_config", lambda stack: {"not_plugins": []})
    monkeypatch.setattr(dc_module, "get_stack_names", lambda: ["test_stack"])
    monkeypatch.setattr(dc_module, "get_config", lambda name: {"url": "http://mock-url"})
    monkeypatch.setattr(dc_module.os, "getcwd", lambda: "/tmp")  # type: ignore[attr-defined]
    monkeypatch.setattr(dc_module.os, "chdir", lambda d: None)  # type: ignore[attr-defined]
    monkeypatch.setattr(dc_module.Path, "exists", lambda self: True)  # type: ignore[attr-defined]

    result = dc_module.dc(single="current-stack", extra=["up"])
    assert result is None
