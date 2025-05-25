from unittest import mock

import pytest

import tfds.config.config as config

API_CONFIG = {"foo": "bar"}
FILE_CONFIG = {"baz": "qux"}


@pytest.fixture
def patch_config_sources():
    with (
        mock.patch("tfds.config.config.get_config_from_api") as mock_api,
        mock.patch("tfds.config.config.get_config_from_file") as mock_file,
    ):
        # Set default return values here if you want
        mock_api.return_value = API_CONFIG
        mock_file.return_value = FILE_CONFIG
        yield mock_api, mock_file


def test_get_config_raises_on_none():
    with pytest.raises(ValueError, match="A config_name must be provided."):
        config.get_config(None)  # type: ignore[arg-type]


def test_get_config_raises_on_empty():
    with pytest.raises(ValueError, match="A config_name must be provided."):
        config.get_config("")


def test_get_config_api_available(patch_config_sources):
    with mock.patch("tfds.config.config.is_api_avaiable", return_value=True):
        result = config.get_config("myconfig")
        assert result == API_CONFIG


def test_get_config_api_not_available(patch_config_sources):
    with mock.patch("tfds.config.config.is_api_avaiable", return_value=False):
        result = config.get_config("myconfig")
        assert result == FILE_CONFIG
