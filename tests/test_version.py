#!/bin/python3
#
import subprocess
import pytest


@pytest.fixture
def get_version(cmd)
    cmd = ['../jobsubmit', '-v']
    with open('test_data/version', 'w') as out:
            subprocess.call(cmd, stdout=out)
