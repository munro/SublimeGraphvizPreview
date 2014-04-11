import sublime, sublime_plugin
from subprocess import call

from helpers import surroundingGraphviz, graphvizPDF


class GraphvizPreviewCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sel = self.view.sel()[0]

        if not sel.empty():
            code = self.view.substr(sel).strip()
        else:
            code = surroundingGraphviz(
                self.view.substr(sublime.Region(0, self.view.size())),
                sel.begin()
            )

        if not code:
            sublime.error_message('Graphviz: Please place cursor in graphviz code before running')
            return

        pdf_filename = graphvizPDF(code)

        try:
            call(['open', pdf_filename])
        except Exception as e:
            sublime.error_message('Graphviz: Could not open PDF, only works for Mac... fork this repo for your OS!')
            raise e

