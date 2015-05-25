# -*- coding: utf-8 -*-

import sys
import pickle
from docutils import nodes
from sphinx_testing import with_app
from sphinxcontrib.imagehelper import add_image_type, ImageConverter
from sphinxcontrib.imagehelper.imageext import on_builder_inited

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class MyImageConverter(ImageConverter):
    def get_filename_for(self, node):
        return 'converted.png'

    def convert(self, node, filename, to):
        print node, filename, to
        return True


class TestSphinxcontrib(unittest.TestCase):
    @with_app(buildername='html', write_docstring=True, create_new_srcdir=True)
    def test_add_image_type1(self, app, status, warnings):
        """
        .. image:: index.rst
           :option: foo=1&bar=abc
        """
        add_image_type(app, 'name', '.rst', MyImageConverter)
        on_builder_inited(app)
        app.build()

        with open(app.builddir / 'doctrees' / 'contents.doctree') as fd:
            doctree = pickle.load(fd)
            self.assertIsInstance(doctree[0], nodes.image)
            self.assertEqual(doctree[0]['uri'], 'index.rst')
            self.assertEqual(doctree[0]['foo'], '1')
            self.assertEqual(doctree[0]['bar'], 'abc')

        with open(app.outdir / 'contents.html') as fd:
            html = fd.read()
            self.assertIn('<img alt="_images/converted.png" src="_images/converted.png" />', html)

    @with_app(buildername='html', write_docstring=True, create_new_srcdir=True)
    def test_add_image_type2(self, app, status, warnings):
        """
        .. figure:: index.rst
           :option: foo=1&bar=abc

           here is caption
        """
        add_image_type(app, 'name', '.rst', MyImageConverter)
        on_builder_inited(app)
        app.build()

        with open(app.builddir / 'doctrees' / 'contents.doctree') as fd:
            doctree = pickle.load(fd)
            self.assertIsInstance(doctree[0], nodes.figure)
            self.assertIsInstance(doctree[0][0], nodes.image)
            self.assertEqual(doctree[0][0]['uri'], 'index.rst')
            self.assertEqual(doctree[0][0]['foo'], '1')
            self.assertEqual(doctree[0][0]['bar'], 'abc')
            self.assertIsInstance(doctree[0][1], nodes.caption)
            self.assertEqual(doctree[0][1][0], 'here is caption')

        with open(app.outdir / 'contents.html') as fd:
            html = fd.read()
            self.assertIn('<img alt="_images/converted.png" src="_images/converted.png" />', html)
