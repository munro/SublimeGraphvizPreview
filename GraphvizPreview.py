import sublime, sublime_plugin
from subprocess import call
import os
import platform

try:  # python 3
    from .helpers import surroundingGraphviz, graphvizPDF, ENVIRON
except ValueError:  # python 2
    from helpers import surroundingGraphviz, graphvizPDF, ENVIRON

DOT_SYNTAX = 'Packages/Graphviz/DOT.tmLanguage'

class GraphvizPreviewCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        code = self.code()

        if not code:
            sublime.error_message('Graphviz: Please place cursor in graphviz code before running')
            return

        pdf_filename = graphvizPDF(code)

        try:
            if platform.system() == 'Windows':
                os.startfile(pdf_filename)
            else:
                call(['open', pdf_filename], env=ENVIRON)            
        except Exception as e:
            sublime.error_message('Graphviz: Could not open PDF, ' + str(e))
            raise e

    def code(self):        
        syntax = self.view.settings().get('syntax')
        sel = self.view.sel()[0]

        if syntax == DOT_SYNTAX:
            return self.content()            
        elif not sel.empty():
            code = self.view.substr(sel).strip()
        else:
            code = surroundingGraphviz(self.content(), sel.begin())

    def content(self):
        return self.view.substr(sublime.Region(0, self.view.size()))