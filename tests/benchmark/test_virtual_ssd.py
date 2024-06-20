# coding=utf-8
import cProfile
import tempfile
from itertools import cycle, islice
from unittest import TestCase

from ssd.driver.virtual import VirtualSSD


class VirtualSSDTestCase(TestCase):

    def test_read_performance(self):
        ssd = VirtualSSD()
        loop = 100000

        with tempfile.TemporaryDirectory() as tmpdir:
            ssd.set_rootdir(tmpdir)

            with cProfile.Profile() as profiler:
                for i in islice(cycle(range(100)), loop):
                    ssd.read(i)
                profiler.print_stats(sort="cumulative")

    def test_write_performance(self):
        ssd = VirtualSSD()
        loop = 100000

        with tempfile.TemporaryDirectory() as tmpdir:
            ssd.set_rootdir(tmpdir)

            with cProfile.Profile() as profiler:
                for i in islice(cycle(range(100)), loop):
                    ssd.write(i, i)
                profiler.print_stats(sort="cumulative")
