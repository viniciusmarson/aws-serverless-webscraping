"""Test module for lib.scrape"""
from lib.scrape import create_options


def test_create_options_sandbox():
    """"Should have the sandbox argument in chrome options"""
    options = create_options()
    assert options.arguments.index('--no-sandbox') != -1


def test_create_options_disable_dev_shm_usage():
    """"Should have the sandbox argument in chrome options"""
    options = create_options()
    assert options.arguments.index('--disable-dev-shm-usage') != -1


def test_create_options_disable_gpu():
    """"Should have the sandbox argument in chrome options"""
    options = create_options()
    assert options.arguments.index('--disable-gpu') != -1
