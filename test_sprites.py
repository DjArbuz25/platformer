import pytest
from pathlib import Path
import os
import psutil
def test_directory_exists():
    assert os.path.exists('ArcherAssets'), 'Каталог no существует'
    assert os.path.exists('assets'), 'Каталог no существует'
    assert os.path.exists('EasyBotAssets'), 'Каталог no существует'
    assert os.path.exists('HardBotAssets'), 'Каталог no существует'
    assert os.path.exists('PlayerAssets'), 'Каталог no существует'

def test_count_files_in_folder():
    assert len(os.listdir("ArcherAssets")) == 11
    assert len(os.listdir("assets")) == 10
    assert len(os.listdir("EasyBotAssets")) == 10
    assert len(os.listdir("HardBotAssets")) == 10
    assert len(os.listdir("PlayerAssets")) == 10


def test_if_png():
    for filename in os.listdir("ArcherAssets"):
        assert filename.endswith('.png')
    for filename in os.listdir("assets"):
        assert filename.endswith('.png')
    for filename in os.listdir("EasyBotAssets"):
        assert filename.endswith('.png')
    for filename in os.listdir("HardBotAssets"):
        assert filename.endswith('.png')
    for filename in os.listdir("PlayerAssets"):
        assert filename.endswith('.png')

def test_system_requeiments():
    assert os.cpu_count() >= 2
    memory = psutil.virtual_memory()
    available_memory = memory.available
    available_memory_gb = available_memory / (1024 * 1024 * 1024)
    assert available_memory_gb > 1.5
        # проверить требовия пк: озу:2гб, количество ядер:2