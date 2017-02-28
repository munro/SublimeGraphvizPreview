from subprocess import call, Popen, PIPE
import os
import platform
import re
import tempfile

ENVIRON = os.environ.copy()
if platform.system() != 'Windows':
    ENVIRON['PATH'] += '{}/usr/local/bin'.format(os.pathsep)
DIGRAPH_START = re.compile('.*(digraph([ \t\n\r]+[a-zA-Z\200-\377_][a-zA-Z\200-\3770-9_]*[ \t\n\r]*{|[ \t\n\r]*{).*)', re.DOTALL | re.IGNORECASE)
DIGRAPH_NEXT = re.compile('[\n\r][ \t\n\r]*digraph[ \t\n\r]+[a-zA-Z\200-\377_][a-zA-Z\200-\3770-9_]*[ \t\n\r]*{', re.MULTILINE | re.IGNORECASE)


def extract_graphviz_snippet(data, cursor):
    """
    Tries to extract the graphviz snippet embedded another language, for example
    a Python comment, or markdown file.
    """
    data_before = data[0:cursor]
    data_after = data[cursor:]

    # find code before selector
    code_before_match = DIGRAPH_START.match(data_before)
    if not code_before_match:
        return None
    code_before = code_before_match.group(1)
    unopened_braces = len(code_before.split('{')) - len(code_before.split('}'))

    # cursor must be in the middle of the graphviz code
    if unopened_braces <= 0:
        return None

    # find code after selector
    another_snippet = DIGRAPH_NEXT.search(data_after)
    code_after_match = re.compile('(' + ('.*\\}' * unopened_braces) + ').*', re.DOTALL).match(data_after)
    if another_snippet:
        next_start = another_snippet.span()[0]
        code_after= data_after[0:next_start]
    elif code_after_match:
        code_after = code_after_match.group(1)
    else:
        return None

    # done!
    code = code_before + code_after
    return code


def graphviz_pdf(code):
    """Convert graphviz code to a PDF."""
    # temporary graphviz file
    grapviz = tempfile.NamedTemporaryFile(prefix='sublime_text_graphviz_', dir=None, suffix='.viz', delete=False, mode='wb')
    grapviz.write(code.encode('utf-8'))
    grapviz.close()

    # compile pdf
    pdf_filename = tempfile.mktemp(prefix='sublime_text_graphviz_', dir=None, suffix='.pdf')
    p = Popen(['dot', '-Tpdf', '-o' + pdf_filename, grapviz.name], env=ENVIRON, stderr=PIPE)
    _, stderr = p.communicate()
    if p.returncode != 0:
        raise GraphvizException(stderr.decode('ascii'))

    return pdf_filename


def open_pdf(filename):
    """Opens a PDF preview window."""
    if platform.system() == 'Windows':
        os.startfile(filename)
    else:
        call(['open', filename], env=ENVIRON)


class GraphvizException(Exception):
    def __init__(self, trace):
        self.trace = trace
        super(Exception, self).__init__('Graphviz error\n{}'.format(trace))
