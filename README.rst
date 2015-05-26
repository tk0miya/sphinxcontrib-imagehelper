sphinxcontrib-imagehelper
==========================

.. image:: https://travis-ci.org/tk0miya/sphinxcontrib-imagehelper.svg?branch=master
   :target: https://travis-ci.org/tk0miya/sphinxcontrib-imagehelper

.. image:: https://coveralls.io/repos/tk0miya/sphinxcontrib-imagehelper/badge.png?branch=master
   :target: https://coveralls.io/r/tk0miya/sphinxcontrib-imagehelper?branch=master

.. image:: https://codeclimate.com/github/tk0miya/sphinxcontrib-imagehelper/badges/gpa.svg
   :target: https://codeclimate.com/github/tk0miya/sphinxcontrib-imagehelper

This package contains the helpers for creating Sphinx image extensions.

This extension enhance common image directives; `image` and `figure` directive.
With `sphinxcontrib-imagehelper`, these image directives get capability to embed custom images.

Setting
=======

Install
-------

::

   $ pip install sphinxcontrib-imagehelper



Helpers
=======

`sphinxcontrib.imagehelper.add_image_type(app, name, ext, handler)`
    Register a new image type which is identified with file extension `ext`.
    The `handler` is used to convert image formats.

`sphinxcontrib.imagehelper.ImageConverter`
    A handler class for converting image formats. It is used at `add_image_type()`.
    The developers of sphinx-extensions should create a handler class which inherts `ImageConverter`,
    and should override two following methods:

    `ImageConverter.get_filename_for(self, node)`
        Determine a filename of converted image.
        By default, this method returns the filename replaced its extension with '.png'::

            def get_filename_for(self, node):
                return os.path.splitext(node['uri'])[0] + '.png'

    `ImageConverter.convert(self, node, filename, to)`
        Convert image to embedable format.
        By default, this method does nothing.

    For example::

        class AstahConverter(ImageConverter):
            def get_filename_for(self, node):
                # filename is determined from its URI and configuration
                hashed = sha1((node['uri'] + self.app.config.some_convert_settings).encode('utf-8')).hexdigest()
                return 'astah-%s.png' % hashed

            def convert(self, node, filename, to):
                succeeded = convert_astah_to_png(filename, to,
                                                 option1=node['option'],
                                                 option2=self.app.config.some_convert_settings)
                if succeeded:
                    return True  # return True if conversion succeeded
                else:
                    return False


`sphinxcontrib.imagehelper.add_image_directive(app, name, option_spec={})`
    Add a custom image directive to Sphinx.
    The directive is named as `name`-image (cf. astah-image).

    If `option_spec` is given, the new directive accepts custom options.

`sphinxcontrib.imagehelper.add_figure_directive(app, name, option_spec={})`
    Add a custom figure directive to Sphinx.
    The directive is named as `name`-figure (cf. astah-figure).

    If `option_spec` is given, the new directive accepts custom options.

`sphinxcontrib.imagehelper.generate_image_directive(name, option_spec={})`
    Generate a custom image directive class. The class is not registered to Sphinx.
    You can enhance the directive class with subclassing.

`sphinxcontrib.imagehelper.generate_figure_directive(name, option_spec={})`
    Generate a custom figure directive class. The class is not registered to Sphinx.
    You can enhance the directive class with subclassing.
