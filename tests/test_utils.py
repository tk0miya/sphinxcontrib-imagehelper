# -*- coding: utf-8 -*-

import os
import sys
from sphinx_testing import with_app
from sphinxcontrib.imagehelper.utils import get_imagedir

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
