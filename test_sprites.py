import pytest
from pathlib import Path
import os

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


def test_if_png():
    for filename in os.listdir("ArcherAssets"):
        assert filename.endswith('.png')
    for filename in os.listdir("assets"):
        assert filename.endswith('.png')
    for filename in os.listdir("EasyBotAssets"):
        assert filename.endswith('.png')
    for filename in os.listdir("HardBotAssets"):
        assert filename.endswith('.png')

        # проверить требовия пк: озу:4гб, количество ядер:2