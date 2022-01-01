#!/bin/bash
#
#-------------------------#
# prepare the for packing #
#-------------------------#
#
# cleaning up unwanted files
./cleanup
#
./jobsubmit -v|sed -n 1p|gawk {'print $2'}|xargs > VERSION
#
