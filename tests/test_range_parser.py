#!/bin/python3
#
import sys

sys.path.append('../')

import jobsubmit

def test_display():
    jobrange = list(range(19))
    jobsubmit.display("./assets/jobs.lst",jobrange)



test_display()
