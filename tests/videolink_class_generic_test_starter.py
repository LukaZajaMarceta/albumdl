#!/usr/bin/env python3

import repackage
repackage.up()  # this solves some problems of importing stuff from albumdl by adding upper directory to lib path

from albumdl import videolink, albumdl


test_url = "https://www.youtube.com/watch?v=sHN0x718N7A"
VL = videolink.VideoLink(test_url)