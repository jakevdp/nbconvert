"""Notebook export in Blogger-aware HTML.

This file contains `ConverterBloggerHTML`, a subclass of `ConverterHTML` that
provides output suitable for easy pasting into a blog hosted on the Blogger
platform. See the class docstring for more information.
"""
#-----------------------------------------------------------------------------
# Copyright (c) 2012, the IPython Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Stdlib imports
import io
import re

# Our own imports
from .html import ConverterHTML


#-----------------------------------------------------------------------------
# Classes declarations
#-----------------------------------------------------------------------------

class ConverterBloggerHTML(ConverterHTML):
    """Convert a notebook to html suitable for easy pasting into Blogger.

    It generates an html file that has *only* the pure HTML contents, and a
    separate file with `_header` appended to the name with all header contents.
    Typically, the header file only needs to be used once when setting up a
    blog, as the CSS for all posts is stored in a single location in Blogger.
    """

    def optional_header(self):
        with io.open(self.outbase + '_header.html', 'w',
                     encoding=self.default_encoding) as f:
            f.write('\n'.join(self.header_body()))
        return []

    def optional_footer(self):
        return []


class ConverterBloggerHTMLSeparate(ConverterBloggerHTML):
    """Convert a notebook to html suitable for easy pasting into Blogger.

    This generates separate files like ConverterBloggerHTML, but the CSS
    styles are modified so that they will not interfere with the CSS
    controlling the overall look of the blog.
    """
    def header_body(self):
        header = super(ConverterBloggerHTMLSeparate, self).header_body()
        header = '\n'.join(header)

        # replace the highlight tags
        header = header.replace('highlight', 'highlight-ipynb')

        # specify pre tags
        header = header.replace('html, body',
                                '\n'.join(('pre.ipynb {',
                                           '  color: black;',
                                           '  background: #f7f7f7;',
                                           '  border: 0;',
                                           '  box-shadow: none;',
                                           '  margin-bottom: 0;',
                                           '  padding: 0;'
                                           '}\n',
                                           'html, body')))

        # create a special div for notebook
        R = re.compile(r'^body ?{', re.MULTILINE)
        header = R.sub('div.ipynb {', header)

        # specify all headers
        R = re.compile(r'^(h[1-6])', re.MULTILINE)
        repl = lambda match: '.ipynb ' + match.groups()[0]
        header = R.sub(repl, header)

        # substitude ipynb class for html and body modifiers
        header = header.replace('html, body', '.ipynb div,')

        return header.split('\n')

    def main_body(self, cell_separator='\n'):
        body = super(ConverterBloggerHTMLSeparate, self).main_body()

        # create a special div for notebook
        body = ["<div class='ipynb'>"] + body + ["</div>"]
        body = '\n'.join(body)

        # specialize the highlight tags
        body = body.replace('highlight', 'highlight-ipynb')

        # specify <pre> tags
        body = body.replace('<pre', '<pre class="ipynb"')

        # specialize headers
        for h in '123456':
            body = body.replace('<h%s' % h, '<h%s class="ipynb"' % h)

        return body.split('\n')
