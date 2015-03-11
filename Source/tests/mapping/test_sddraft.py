import datetime
import os.path
import shutil

import arcpyext
import pytest

from arcpyext.mapping import SDDraft
from .. helpers import *

SDDRAFT_FILE_PATH = "{0}/samples/example.sddraft".format(os.path.dirname(__file__))
SDDRAFT_FILE_PATH_COPY = "{0}/samples/example.copy.sddraft".format(os.path.dirname(__file__))
SDDRAFT_SAVE_TEST_FILE_PATH = "{0}/samples/example.savetest.sddraft".format(os.path.dirname(__file__))

@pytest.fixture
def sddraft():
    shutil.copyfile(SDDRAFT_FILE_PATH, SDDRAFT_FILE_PATH_COPY)
    return SDDraft(SDDRAFT_FILE_PATH_COPY)
    
from sddraftbase import *
from sddraft_cacheable import *

@pytest.mark.parametrize(("mode", "expected", "ex"), [
    (SDDraft.AntiAliasingMode.none, SDDraft.AntiAliasingMode.none, None),
    (SDDraft.AntiAliasingMode.fastest, SDDraft.AntiAliasingMode.fastest, None),
    (SDDraft.AntiAliasingMode.fast, SDDraft.AntiAliasingMode.fast, None),
    (SDDraft.AntiAliasingMode.normal, SDDraft.AntiAliasingMode.normal, None),
    (SDDraft.AntiAliasingMode.best, SDDraft.AntiAliasingMode.best, None),
    ("None", SDDraft.AntiAliasingMode.none, None),
    ("Fail", None, ValueError)
])
def test_aa_mode(sddraft, mode, expected, ex):
    if (ex != None):
        with pytest.raises(ex):
            sddraft.anti_aliasing_mode = mode
    else:
        sddraft.anti_aliasing_mode = mode
        assert sddraft.anti_aliasing_mode == expected
    
@pytest.mark.parametrize(("disabled", "expected"), TRUEISH_TEST_PARAMS)
def test_disable_indentify_relates(sddraft, disabled, expected):
    sddraft.disable_identify_relates = disabled
    assert sddraft.disable_identify_relates == expected

@pytest.mark.parametrize(("enabled", "expected"), TRUEISH_TEST_PARAMS)
def test_enable_dynamic_layers(sddraft, enabled, expected):
    sddraft.enable_dynamic_layers = enabled
    assert sddraft.enable_dynamic_layers == expected
    
@pytest.mark.parametrize(("enabled_ops", "expected", "ex"), [
    (["Query"], ["Query"], None),
    (["quErY"], ["Query"], None),
    ([SDDraft.FeatureAccessOperation.create, SDDraft.FeatureAccessOperation.update], ["Create", "Update"], None),
    (["Foo", "Bar"], None, ValueError),
    (["Query", 1], None, TypeError)
])
def test_feature_access_enabled_operations(sddraft, enabled_ops, expected, ex):
    if (ex != None):
        with pytest.raises(ex):
            sddraft.feature_access_enabled_operations = enabled_ops
    else:
        sddraft.feature_access_enabled_operations = enabled_ops
        assert set(sddraft.feature_access_enabled_operations) == set(expected)

@pytest.mark.parametrize(("file_path", "equal"), [
    (SDDRAFT_FILE_PATH_COPY, True),
    ("./FooBar", False),
])
def test_file_path(sddraft, file_path, equal):
    assert (os.path.normpath(sddraft.file_path) == os.path.normpath(file_path)) == equal    
    
def test_save(sddraft):
    sddraft.save()
    assert True

@pytest.mark.parametrize(("output"), [
    (SDDRAFT_SAVE_TEST_FILE_PATH)
])
def test_save_a_copy(sddraft, output):
    sddraft.save_a_copy(output)
    assert os.path.isfile(output) == True
    
@pytest.mark.parametrize(("enabled", "expected"), TRUEISH_TEST_PARAMS)
def test_schema_locking_enabled(sddraft, enabled, expected):
    sddraft.schema_locking_enabled = enabled
    assert sddraft.schema_locking_enabled == expected

@pytest.mark.parametrize(("mode", "expected", "ex"), [
    (SDDraft.TextAntiAliasingMode.none, SDDraft.TextAntiAliasingMode.none, None),
    (SDDraft.TextAntiAliasingMode.force, SDDraft.TextAntiAliasingMode.force, None),
    (SDDraft.TextAntiAliasingMode.normal, SDDraft.TextAntiAliasingMode.normal, None),
    ("None", SDDraft.TextAntiAliasingMode.none, None),
    ("Fail", None, ValueError)
])
def test_text_aa_mode(sddraft, mode, expected, ex):
    if (ex != None):
        with pytest.raises(ex):
            sddraft.text_anti_aliasing_mode = mode
    else:
        sddraft.text_anti_aliasing_mode = mode
        assert sddraft.text_anti_aliasing_mode == expected