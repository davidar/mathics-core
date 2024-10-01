import json

from IPython.display import Code, HTML, JSON, Math
from IPython.core.magic import Magics, magics_class, line_cell_magic

from mathics.session import MathicsSession

from .format import Formatter


class JupyterFormatter(Formatter):
    def text(self, result):
        return Code(result, language="mathematica")

    def math(self, result):
        return Math(result)

    def graphics3d(self, result):
        return JSON(json.loads(result))

    def svg(self, result):
        return self.html(result)

    def html(self, result):
        result = result.replace("<math", "<div")
        result = result.replace("<mglyph", '<img style="display: inline-block" ')
        result = result.replace("<mrow>", "")
        result = result.replace("<mo>", "")
        return HTML(result)


@magics_class
class MathicsMagic(Magics):
    def __init__(self, shell):
        super().__init__(shell)
        self.session = MathicsSession()
        self.formatter = JupyterFormatter()

    @line_cell_magic
    def mathics3(self, line, cell=""):
        expr = self.session.evaluate(line + "\n" + cell)
        return self.formatter.format_output(self.session.evaluation, expr)


def load_ipython_extension(ipython):
    ipython.register_magics(MathicsMagic)
