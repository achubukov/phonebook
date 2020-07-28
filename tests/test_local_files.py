import os

import pytest
import shutil

from phonebook.data_operations.local_files.local_files import LocalFiles
from tests.constants import BASE_DIR, RESOURCES_DIR


@pytest.fixture(autouse=True)
def file_structure():
    shutil.rmtree(BASE_DIR, ignore_errors=True)
    shutil.copytree(RESOURCES_DIR, BASE_DIR, symlinks=False, ignore=None, copy_function=shutil.copy2,
                    ignore_dangling_symlinks=False)
    yield
    shutil.rmtree(BASE_DIR)


def test_constructor():
    lf = LocalFiles(os.path.join(BASE_DIR, 'folder'))
    assert os.path.isdir(lf.base_path)


def test_is_phone_in_book():
    lf = LocalFiles(base_path=BASE_DIR)
    phones = ('00000', '', 'dsadad sdad')

    assert lf._is_phone_in_book('14158586273')
    for i in phones:
        assert not lf._is_phone_in_book(i)


def test_find_name_in_book():
    lf = LocalFiles(BASE_DIR)
    assert lf._find_name_in_book('Bob') != 'None'
    assert lf._find_name_in_book('Bob ') == 'None'
    assert lf._find_name_in_book('ada') == 'None'
    assert lf._find_name_in_book('ada ') == 'None'
    assert lf._find_name_in_book('') == 'None'
    assert lf._find_name_in_book('1121') == 'None'


def test_search_by_name():
    lf = LocalFiles(base_path=BASE_DIR)

    assert lf.search_by_name('Bob')
    assert not lf.search_by_name('Bob ')
    assert not lf.search_by_name('ada')
    assert not lf.search_by_name('ada ')
    assert not lf.search_by_name('')
    assert not lf.search_by_name('1121')


def test_delete_phone_by_name():
    lp = LocalFiles(BASE_DIR)
    try:
        open(os.path.join(BASE_DIR, '_справочник_', 'United States of America', 'Bob'), 'r')
        assert True
    except FileNotFoundError:
        assert False
    lp.delete_phone_by_name('Bob')
    try:
        open(os.path.join(BASE_DIR, '_справочник_', 'United States of America', 'Bob'), 'r')
        assert False
    except FileNotFoundError:
        assert True


def test_save_phone():
    lf = LocalFiles(BASE_DIR)

    lf.save_phone(434353453, 'barsik1')
    assert os.path.isfile(os.path.join(lf.base_path, 'Austria', 'barsik1'))

    lf.save_phone(434353453, 'barsik2')
    assert not os.path.isfile(os.path.join(lf.base_path, 'Austria', 'barsik2'))

    lf.save_phone('eqweqqwed', 'Cat2')
    tree = os.walk(BASE_DIR)
    for i in tree:
        if len(i[2]) != 0:
            for j in i[2]:
                assert j != 'Cat2'

    lf.save_phone('1415eqweq62qwe73d', 'Cat')
    tree = os.walk(BASE_DIR)
    for i in tree:
        if len(i[2]) != 0:
            for j in i[2]:
                assert j != 'Cat'

    lf.save_phone(434353455, 'Bob')
    lf.save_phone(434353452, 'Bob')
    with open(os.path.join(lf.base_path, 'Austria', 'Bob')) as f:
        assert f.read() == '434353455'
        assert not f.read() == '434353452'
