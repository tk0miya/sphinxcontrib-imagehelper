import os
import posixpath
from docutils import nodes
from docutils.parsers.rst.directives.images import Image, Figure
from sphinxcontrib.imagehelper import image_node


class ImageExtMixIn(object):
    def prerun(self):
        pass

    def postrun(self, node):
        pass

    def run(self):
        result = super(ImageExtMixIn, self).run()
        self.prerun()

        env = self.state.document.settings.env
        dirname = os.path.dirname(env.doc2path(env.docname, base=None))
        relpath = posixpath.join(dirname, self.arguments[0])
        if self.arguments[0].find('://') == -1:
            if not os.access(os.path.join(env.srcdir, relpath), os.R_OK):
                raise self.warning('%s file not readable: %s' % (self.imageext_type, self.arguments[0]))
            env.note_dependency(relpath)

        if isinstance(result[0], nodes.image):
            image = image_node(imageext_type=self.imageext_type,
                               **result[0].attributes)
            image['uri'] = relpath
            self.postrun(image)
            result[0] = image
        else:
            for node in result[0].traverse(nodes.image):
                image = image_node(imageext_type=self.imageext_type,
                                   **node.attributes)
                image['uri'] = relpath
                self.postrun(image)
                node.replace_self(image)

        return result


def generate_image_directive(name, option_spec={}):
    class ImageExt(ImageExtMixIn, Image):
        imageext_type = name

    for name, value in option_spec.items():
        ImageExt.option_spec[name] = value

    return ImageExt


def add_image_directive(app, name, option_spec={}):
    directive = generate_image_directive(name, option_spec)
    app.add_directive('%s-image' % name, directive)


def generate_figure_directive(name, option_spec={}):
    class FigureExt(ImageExtMixIn, Figure):
        imageext_type = name

    for name, value in option_spec.items():
        FigureExt.option_spec[name] = value

    return FigureExt


def add_figure_directive(app, name, option_spec={}):
    directive = generate_figure_directive(name, option_spec)
    app.add_directive('%s-figure' % name, directive)
