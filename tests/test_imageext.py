# -*- coding: utf-8 -*-

import sys
import pickle
from time import time
from docutils import nodes
from shutil import copyfile
from sphinx_testing import with_app
from sphinx_testing.path import path
from docutils.parsers.rst import directives
from sphinxcontrib.imagehelper import add_image_type, ImageConverter
from sphinxcontrib.imagehelper.imageext import on_builder_inited

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class MyImageConverter(ImageConverter):
    option_spec = {
        'foo': directives.positive_int,
        'bar': directives.unchanged
    }

    def get_filename_for(self, node):
        return 'converted.png'

    def convert(self, node, filename, to):
        copyfile(filename, to)
        return True


class TestSphinxcontrib(unittest.TestCase):
    @with_app(buildername='html', write_docstring=True, create_new_srcdir=True)
    def test_add_image_type1(self, app, status, warnings):
        """
        .. image:: example.img
           :option: foo=1&bar=abc
        """
        # first build
        (app.srcdir / 'example.img').write_text('')
        add_image_type(app, 'name', '.img', MyImageConverter)
        on_builder_inited(app)
        app.build()

        with open(app.builddir / 'doctrees' / 'contents.doctree', 'rb') as fd:
            doctree = pickle.load(fd)
            self.assertIsInstance(doctree[0], nodes.image)
            self.assertEqual(doctree[0]['uri'], 'example.img')
            self.assertEqual(doctree[0]['foo'], 1)
            self.assertEqual(doctree[0]['bar'], 'abc')

        with open(app.outdir / 'contents.html') as fd:
            html = fd.read()
            self.assertIn('<img alt="_images/converted.png" src="_images/converted.png" />', html)

        # second build (no updates)
        status.truncate(0)
        warnings.truncate(0)
        app.build()

        self.assertIn('0 added, 0 changed, 0 removed', status.getvalue())

        # thrid build (image has changed)
        status.truncate(0)
        warnings.truncate(0)
        (app.srcdir / 'example.img').utime((time() + 1, time() + 1))
        app.build()

        self.assertIn('0 added, 1 changed, 0 removed', status.getvalue())

    @with_app(buildername='html', write_docstring=True, create_new_srcdir=True)
    def test_add_image_type2(self, app, status, warnings):
        """
        .. figure:: example.img
           :option: foo=1&bar=abc

           here is caption
        """
        (app.srcdir / 'example.img').write_text('')
        add_image_type(app, 'name', '.img', MyImageConverter)
        on_builder_inited(app)
        app.build()

        with open(app.builddir / 'doctrees' / 'contents.doctree', 'rb') as fd:
            doctree = pickle.load(fd)
            self.assertIsInstance(doctree[0], nodes.figure)
            self.assertIsInstance(doctree[0][0], nodes.image)
            self.assertEqual(doctree[0][0]['uri'], 'example.img')
            self.assertEqual(doctree[0][0]['foo'], 1)
            self.assertEqual(doctree[0][0]['bar'], 'abc')
            self.assertIsInstance(doctree[0][1], nodes.caption)
            self.assertEqual(doctree[0][1][0], 'here is caption')

        with open(app.outdir / 'contents.html') as fd:
            html = fd.read()
            self.assertIn('<img alt="_images/converted.png" src="_images/converted.png" />', html)

    @with_app(buildername='html', write_docstring=True, create_new_srcdir=True)
    def test_add_image_type3(self, app, status, warnings):
        """
        .. figure:: http://example.com/example.img
           :option: foo=1&bar=abc

           here is caption
        """
        class TestImageConverter(MyImageConverter):
            def get_last_modified_for(self, node):
                return 0

            def convert(self, node, filename, to):
                path(to).write_text('')
                return True

        add_image_type(app, 'name', 'http://example.com/', TestImageConverter)
        on_builder_inited(app)
        app.build()

        with open(app.builddir / 'doctrees' / 'contents.doctree', 'rb') as fd:
            doctree = pickle.load(fd)
            self.assertIsInstance(doctree[0], nodes.figure)
            self.assertIsInstance(doctree[0][0], nodes.image)
            self.assertEqual(doctree[0][0]['uri'], 'http://example.com/example.img')
            self.assertEqual(doctree[0][0]['foo'], 1)
            self.assertEqual(doctree[0][0]['bar'], 'abc')
            self.assertIsInstance(doctree[0][1], nodes.caption)
            self.assertEqual(doctree[0][1][0], 'here is caption')

        with open(app.outdir / 'contents.html') as fd:
            html = fd.read()
            self.assertIn('<img alt="_images/converted.png" src="_images/converted.png" />', html)

    @with_app(buildername='html', write_docstring=True, create_new_srcdir=True)
    def test_add_image_type_in_subdir(self, app, status, warnings):
        """
        .. image:: subdir/example.img
        """
        class TestImageConverter(MyImageConverter):
            def convert(_self, node, filename, to):
                self.assertEqual(_self.app.srcdir / 'subdir' / 'example.img', filename)
                self.assertEqual(_self.app.outdir / '_images' / 'converted.png', to)
                return super(TestImageConverter, _self).convert(node, filename, to)

        (app.srcdir / 'subdir').makedirs()
        (app.srcdir / 'subdir' / 'example.img').write_text('')
        add_image_type(app, 'name', '.img', TestImageConverter)
        on_builder_inited(app)
        app.build()

        with open(app.outdir / 'contents.html') as fd:
            html = fd.read()
            self.assertIn('<img alt="_images/converted.png" src="_images/converted.png" />', html)

    @with_app(buildername='html', write_docstring=True, create_new_srcdir=True)
    def test_add_image_type_with_unsupported_option(self, app, status, warnings):
        """
        .. image:: example.img
           :option: foo=1&bar=abc&baz=def
        """
        (app.srcdir / 'example.img').write_text('')
        add_image_type(app, 'name', '.img', MyImageConverter)
        on_builder_inited(app)
        app.build()

        self.assertIn('WARNING: Unsupported option `baz` found at example.img', warnings.getvalue())
        with open(app.builddir / 'doctrees' / 'contents.doctree', 'rb') as fd:
            doctree = pickle.load(fd)
            self.assertIsInstance(doctree[0], nodes.image)
            self.assertEqual(doctree[0]['uri'], 'example.img')
            self.assertEqual(doctree[0]['foo'], 1)
            self.assertEqual(doctree[0]['bar'], 'abc')
            self.assertNotIn('baz', doctree[0])

    @with_app(buildername='html', write_docstring=True, create_new_srcdir=True)
    def test_add_image_type_with_invalid_option(self, app, status, warnings):
        """
        .. image:: example.img
           :option: foo=abc
        """
        (app.srcdir / 'example.img').write_text('')
        add_image_type(app, 'name', '.img', MyImageConverter)
        on_builder_inited(app)
        app.build()

        self.assertIn(('WARNING: Fail to apply `foo` option to example.img:\n'
                       'invalid literal for int() with base 10: \'abc\'\n'),
                      warnings.getvalue())
        with open(app.builddir / 'doctrees' / 'contents.doctree', 'rb') as fd:
            doctree = pickle.load(fd)
            self.assertIsInstance(doctree[0], nodes.image)
            self.assertEqual(doctree[0]['uri'], 'example.img')
            self.assertNotIn('foo', doctree[0])

    @with_app(buildername='html', write_docstring=True, create_new_srcdir=True)
    def test_add_image_type_with_multiple_extensions(self, app, status, warnings):
        """
        .. image:: example.img

        .. image:: example.imgx
        """
        (app.srcdir / 'example.img').write_text('')
        (app.srcdir / 'example.imgx').write_text('')
        add_image_type(app, 'name', ('.img', '.imgx'), MyImageConverter)
        on_builder_inited(app)
        app.build()

        with open(app.builddir / 'doctrees' / 'contents.doctree', 'rb') as fd:
            doctree = pickle.load(fd)
            self.assertIsInstance(doctree[0], nodes.image)
            self.assertEqual(doctree[0]['uri'], 'example.img')
            self.assertIsInstance(doctree[1], nodes.image)
            self.assertEqual(doctree[1]['uri'], 'example.imgx')

    @with_app(buildername='html', write_docstring=True, create_new_srcdir=True)
    def test_add_image_type_on_conversion_failed(self, app, status, warnings):
        """
        .. image:: example.img
        """
        class FailureConverter(ImageConverter):
            def convert(self, node, filename, to):
                return False

        (app.srcdir / 'example.img').write_text('')
        add_image_type(app, 'name', '.img', FailureConverter)
        on_builder_inited(app)
        app.build()

        html = (app.builddir / 'html' / 'contents.html').read_text()
        self.assertRegexpMatches(html, '<div class="body" role="main">\s*</div>')
