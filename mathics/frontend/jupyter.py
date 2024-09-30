import json

from IPython.display import HTML, Math
from IPython.core.magic import Magics, magics_class, line_cell_magic

from mathics.session import MathicsSession

from .format import format_output


@magics_class
class MathicsMagic(Magics):
    def __init__(self, shell):
        super().__init__(shell)
        self.session = MathicsSession()
        self.reset_session()

    def reset_session(self):
        self.session.reset()
        self.session.evaluation.format = "unformatted"
        self.session.evaluation.format_output = lambda expr, format: format_output(
            self.session.evaluation, expr, format
        )

    @line_cell_magic
    def mathics3(self, line, cell=""):
        data = self.session.evaluate_as_in_cli(line + "\n" + cell).get_data()
        result = data["result"].strip()
        if result.startswith("<svg") or result.startswith("<math"):
            result = result.replace("<math", "<div")
            result = result.replace("<mglyph", '<img style="display: inline-block" ')
            result = result.replace("<mrow>", "")
            result = result.replace("<mo>", "")
            return HTML(result)
        if data["form"] == "TeXForm":
            return Math(result)
        if result.startswith(r"\["):
            result = result.replace(r"\[", "")
            result = result.replace(r"\]", "")
            return Math(result)
        if result.startswith('{"elements":'):
            return json.loads(result)
        return result


def load_ipython_extension(ipython):
    ipython.register_magics(MathicsMagic)
