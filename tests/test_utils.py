# -*- coding: utf-8 -*-

import os
import sys
from sphinx_testing import with_app, with_tmpdir
from sphinxcontrib.imagehelper.utils import is_outdated, get_imagedir

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestSphinxcontrib(unittest.TestCase):
    @with_app(buildername='html', create_new_srcdir=True)
    def test_get_imagedir_html(self, app, status, warnings):
        # docname: index
        (relpath, abspath) = get_imagedir(app, 'index')
        self.assertEqual('_images', relpath)
        self.assertEqual(os.path.join(app.outdir, '_images'), abspath)

        # docname: subdir/index
        (relpath, abspath) = get_imagedir(app, 'subdir/index')
        self.assertEqual('../_images', relpath)
        self.assertEqual(os.path.join(app.outdir, '_images'), abspath)

    @with_app(buildername='latex', create_new_srcdir=True)
    def test_get_imagedir_latex(self, app, status, warnings):
        # docname: index
        (relpath, abspath) = get_imagedir(app, 'index')
        self.assertEqual('', relpath)
        self.assertEqual(os.path.join(app.outdir, ''), abspath)

        # docname: subdir/index
        (relpath, abspath) = get_imagedir(app, 'subdir/index')
        self.assertEqual('', relpath)
        self.assertEqual(os.path.join(app.outdir, ''), abspath)

    @with_tmpdir
    def test_is_outdated(self, dir):
        source = dir / 'source.asta'
        destination = dir / 'output.png'

        # source file not exists
        self.assertEqual(False, is_outdated(source, destination))

        # destination file not exists
        source.write_text('')
        self.assertEqual(True, is_outdated(source, destination))

        # destination file is newer than source
        last_modified = os.stat(source).st_mtime
        destination.write_text('')
        destination.utime((last_modified + 1, last_modified + 1))
        self.assertEqual(False, is_outdated(source, destination))

        # destination file is older than source
        destination.utime((last_modified - 1, last_modified - 1))
        self.assertEqual(True, is_outdated(source, destination))
