import sublime, sublime_plugin
from subprocess import call
import os
import platform

try:  # python 3
    from .helpers import extract_graphviz_snippet, graphviz_pdf, open_pdf, GraphvizException
except ValueError:  # python 2
    from helpers import extract_graphviz_snippet, graphviz_pdf, open_pdf, GraphvizException


class GraphvizPreviewCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            open_pdf(self.graphviz_pdf())
        except GraphvizException as e:
            self.display_error(edit, 'Could not compile Graphviz:\n\n{}'.format(e.trace))
            raise
        except Exception as e:
            self.display_error(edit, str(e))
            raise

    def graphviz_pdf(self):
        code = self.view.substr(sublime.Region(0, self.view.size()))
        sel = self.view.sel()[0]

        for snippet in filter(None, [
            # current selection
            self.view.substr(sel).strip() or None,
            # the snippet where the cursor start is
            extract_graphviz_snippet(code, cursor=sel.begin()),
            # the snippet where the cursor end is
            extract_graphviz_snippet(code, cursor=sel.end()) if sel.end() != sel.begin() else None,
        ]):
            try:
                return graphviz_pdf(snippet)
            except GraphvizException as e:
                pass

        # finally try everything
        return graphvizPDF(code)

    def display_error(self, edit, msg):
        """Makes an error popup, or snippet if it's too large."""
        msg = str(msg)
        if len(msg) <= 1000:
            sublime.error_message(msg)
        else:
            x = self.view.window().new_file()
            x.set_scratch(True)
            x.insert(edit, 0, msg)
