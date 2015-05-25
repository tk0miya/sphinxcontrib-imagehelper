import os
from sphinx.util.osutil import relative_uri


def get_imagedir(app, docname):
    if hasattr(app.builder, 'imagedir'):  # Sphinx (>= 1.3.x)
        dirname = app.builder.imagedir
    elif hasattr(app.builder, 'imgpath') or app.builder.format == 'html':  # Sphinx (<= 1.2.x) and HTML writer
        dirname = '_images'
    else:
        dirname = ''

    if dirname:
        relpath = relative_uri(app.builder.get_target_uri(docname), dirname)
    else:
        relpath = ''

    abspath = os.path.join(app.builder.outdir, dirname)
    return (relpath, abspath)


def is_outdated(astah_path, png_path):
    if not os.path.exists(astah_path):
        return False
    else:
        last_modified = os.stat(astah_path).st_mtime
        if not os.path.exists(png_path) or os.stat(png_path).st_mtime < last_modified:
            return True
        else:
            return False


def if_outdated(fn):
    def wrap(self, filename, to, **kwargs):
        if is_outdated(filename, to):
            return fn(self, filename, to, **kwargs)
        else:
            return True

    return wrap
