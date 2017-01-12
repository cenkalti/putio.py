# coding=utf-8
import os
import shutil
import tempfile
import unittest

import putiopy


class TestCase(unittest.TestCase):
    def setUp(self):
        self.client = putiopy.Client('123456')
        self.destination = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.destination)

    def _download_file(self, name):
        f = self.client.File({
            'id': 'file',
            'name': name,
            'size': 0,
            'content_type': 'text/plain',
            'crc32': '00000000',
        })

        f.download(self.destination)

    def _file_exists(self, name):
        filepath = os.path.join(self.destination, name)
        return os.path.exists(filepath)

    def _test_file_download(self, name):
        self._download_file(name)
        self.assertTrue(self._file_exists(name))

    def test_regular_text(self):
        self._test_file_download('Robyn')

    def test_unicode_text(self):
        self._test_file_download(u'Robyn')

    def test_regular_non_ascii(self):
        self._test_file_download('Röyksopp')

    def test_regular_non_ascii_unicode(self):
        self._test_file_download(u'Röyksopp')


if __name__ == '__main__':
    unittest.main()
