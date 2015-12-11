# -*- coding: utf-8 -*-

import sys
import pickle
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx_testing import with_app
from sphinxcontrib.imagehelper import add_image_directive, add_figure_directive, image_node

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestSphinxcontrib(unittest.TestCase):
    @with_app(buildername='html', write_docstring=True, create_new_srcdir=True)
    def test_add_image_directive(self, app, status, warnings):
        """
        .. foo-image:: contents.rst
        """
        add_image_directive(app, 'foo')
        with self.assertRaises(NotImplementedError):  # will raise error on writer
            app.build()

        with open(app.builddir / 'doctrees' / app.config.master_doc + '.doctree', 'rb') as fd:
            doctree = pickle.load(fd)
            self.assertIsInstance(doctree[0], image_node)
            self.assertEqual(doctree[0]['uri'], 'contents.rst')

    @with_app(buildername='html', write_docstring=True, create_new_srcdir=True)
    def test_add_image_directive2(self, app, status, warnings):
        """
        .. foo-image:: subdir/contents.rst
        """
        (app.srcdir / 'subdir').makedirs()
        (app.srcdir / 'subdir' / 'contents.rst').write_text('')

        add_image_directive(app, 'foo')
        with self.assertRaises(NotImplementedError):  # will raise error on writer
            app.build()

        with open(app.builddir / 'doctrees' / app.config.master_doc + '.doctree', 'rb') as fd:
            doctree = pickle.load(fd)
            self.assertIsInstance(doctree[0], image_node)
            self.assertEqual(doctree[0]['uri'], 'subdir/contents.rst')

    @with_app(buildername='html', create_new_srcdir=True)
    def test_add_image_directive_in_subdir(self, app, status, warnings):
        (app.srcdir / 'contents.rst').write_text('')
        (app.srcdir / 'subdir').makedirs()
        (app.srcdir / 'subdir' / 'contents.rst').write_text('.. foo-image:: filename.rst')
        (app.srcdir / 'subdir' / 'filename.rst').write_text('')
        add_image_directive(app, 'foo')
        with self.assertRaises(NotImplementedError):  # will raise error on writer
            app.build()

        with open(app.builddir / 'doctrees' / 'subdir' / 'contents.doctree', 'rb') as fd:
            doctree = pickle.load(fd)
            self.assertIsInstance(doctree[0], image_node)
            self.assertEqual(doctree[0]['uri'], 'subdir/filename.rst')

    @with_app(buildername='html', write_docstring=True, create_new_srcdir=True)
    def test_add_image_directive_for_http(self, app, status, warnings):
        """
        .. foo-image:: http://example.com/
        """
        (app.srcdir / 'subdir').makedirs()
        (app.srcdir / 'subdir' / 'contents.rst').write_text('')

        add_image_directive(app, 'foo')
        with self.assertRaises(NotImplementedError):  # will raise error on writer
            app.build()

        with open(app.builddir / 'doctrees' / app.config.master_doc + '.doctree', 'rb') as fd:
            doctree = pickle.load(fd)
            self.assertIsInstance(doctree[0], image_node)
            self.assertEqual(doctree[0]['uri'], 'http://example.com/')

    @with_app(buildername='html', create_new_srcdir=True)
    def test_add_image_directive_for_http_in_subdir(self, app, status, warnings):
        (app.srcdir / 'contents.rst').write_text('')
        (app.srcdir / 'subdir').makedirs()
        (app.srcdir / 'subdir' / 'contents.rst').write_text('.. foo-image:: http://example.com/')
        (app.srcdir / 'subdir' / 'filename.rst').write_text('')

        add_image_directive(app, 'foo')
        with self.assertRaises(NotImplementedError):  # will raise error on writer
            app.build()

        with open(app.builddir / 'doctrees' / 'subdir' / 'contents.doctree', 'rb') as fd:
            doctree = pickle.load(fd)
            self.assertIsInstance(doctree[0], image_node)
            self.assertEqual(doctree[0]['uri'], 'http://example.com/')

    @with_app(buildername='html', write_docstring=True, create_new_srcdir=True)
    def test_add_image_directive_with_name_option(self, app, status, warnings):
        """
        .. foo-image:: contents.rst
           :name: target
        """
        add_image_directive(app, 'foo')
        with self.assertRaises(NotImplementedError):  # will raise error on writer
            app.build()

        with open(app.builddir / 'doctrees' / 'contents.doctree', 'rb') as fd:
            doctree = pickle.load(fd)
            print doctree
            self.assertIsInstance(doctree[0], image_node)
            self.assertEqual(doctree[0]['uri'], 'contents.rst')
            self.assertEqual(doctree[0]['names'], ['target'])

    @with_app(buildername='html', write_docstring=True, create_new_srcdir=True)
    def test_add_image_directive_with_option_spec(self, app, status, warnings):
        """
        .. foo-image:: contents.rst
           :bar: 255
        """
        option_spec = {'bar': directives.positive_int}
        add_image_directive(app, 'foo', option_spec)
        with self.assertRaises(NotImplementedError):  # will raise error on writer
            app.build()

        with open(app.builddir / 'doctrees' / 'contents.doctree', 'rb') as fd:
            doctree = pickle.load(fd)
            self.assertIsInstance(doctree[0], image_node)
            self.assertEqual(doctree[0]['uri'], 'contents.rst')
            self.assertEqual(doctree[0]['bar'], 255)

    @with_app(buildername='html', write_docstring=True, create_new_srcdir=True)
    def test_add_figure_directive(self, app, status, warnings):
        """
        .. foo-figure:: contents.rst

           here is caption
        """
        add_figure_directive(app, 'foo')
        with self.assertRaises(NotImplementedError):  # will raise error on writer
            app.build()

        with open(app.builddir / 'doctrees' / 'contents.doctree', 'rb') as fd:
            doctree = pickle.load(fd)
            self.assertIsInstance(doctree[0], nodes.figure)
            self.assertIsInstance(doctree[0][0], image_node)
            self.assertEqual(doctree[0][0]['uri'], 'contents.rst')
            self.assertIsInstance(doctree[0][1], nodes.caption)
            self.assertEqual(doctree[0][1][0], 'here is caption')

    @with_app(buildername='html', write_docstring=True, create_new_srcdir=True)
    def test_add_figure_directive_with_option_spec(self, app, status, warnings):
        """
        .. foo-figure:: contents.rst
           :bar: 255

           here is caption
        """
        option_spec = {'bar': directives.positive_int}
        add_figure_directive(app, 'foo', option_spec)
        with self.assertRaises(NotImplementedError):  # will raise error on writer
            app.build()

        with open(app.builddir / 'doctrees' / 'contents.doctree', 'rb') as fd:
            doctree = pickle.load(fd)
            self.assertIsInstance(doctree[0], nodes.figure)
            self.assertIsInstance(doctree[0][0], image_node)
            self.assertEqual(doctree[0][0]['uri'], 'contents.rst')
            self.assertEqual(doctree[0][0]['bar'], 255)
            self.assertIsInstance(doctree[0][1], nodes.caption)
            self.assertEqual(doctree[0][1][0], 'here is caption')
