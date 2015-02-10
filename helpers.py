from subprocess import call
import os
import platform
import re
import tempfile

ENVIRON = os.environ
if platform.system() != 'Windows':
    ENVIRON['PATH'] += ':/usr/local/bin'

DIGRAPH_START = re.compile('.*(digraph([ \t\n\r]+[a-zA-Z\200-\377_][a-zA-Z\200-\3770-9_]*[ \t\n\r]*{|[ \t\n\r]*{).*)', re.DOTALL | re.IGNORECASE)


def surroundingGraphviz(data, cursor):
    '''
    Find graphviz code in source surrounding the cursor.
    '''
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
    code_after_match = re.compile('(' + ('.*\\}' * unopened_braces) + ').*', re.DOTALL).match(data_after)
    if not code_after_match:
        return None
    code_after = code_after_match.group(1)

    # done!
    code = code_before + code_after
    return code


def graphvizPDF(code):
    '''
    Convert graphviz code to a PDF.
    '''
    # temporary graphviz file
    grapviz = tempfile.NamedTemporaryFile(prefix='sublime_text_graphviz_', dir=None, suffix='.viz', delete=False, mode='wb')
    grapviz.write(code.encode('utf-8'))
    grapviz.close()

    # compile pdf
    pdf_filename = tempfile.mktemp(prefix='sublime_text_graphviz_', dir=None, suffix='.pdf')
    call(['dot', '-Tpdf', '-o' + pdf_filename, grapviz.name], env=ENVIRON)
    os.unlink(grapviz.name)

    return pdf_filename
