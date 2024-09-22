
import matplotlib
import matplotlib.pyplot as plt
from typing import Callable, Sequence


from unittest.mock import Mock
js = Mock()


class PyodidePlot:
    """
    Helper class, to draw figures from pyodide runtime, into a specified html element.
    If no argument is provided, the default `div_id` is used (arguments configuration of
    the plugin).

    Use as a remplacement for `matplotlib.pyplot`:

    ```python
    pyo_plt = PyodidePlot()
    pyo_plt.plot(xs, ys, ...)           # Same as pyplot.plot, but draw where appropriate
    pyo_plt.title("...")
    pyo_plt.show()
    ```

    Or draw quickly single curves:

    ```python
    pyo_plt = PyodidePlot("figure_id")
    pyo_plt.plot_func(                  # draw where appropriate + automatic plt.show()
        lambda x: x**3,
        range(-15, 16),
        'r-",
        "cube...",
    )
    ```

    In case you want to use other methods than `plot`, like `pyplot.table` you will have
    to call the `refresh()` method, which will prepare the GUI states and return the
    original `pyplot` module :

    ```python
    pyo_plt = PyodidePlot("figure_id")

    # ...
    pyo_plt.refresh().table(...)
    ```
    """

    def __init__(self, div_id:str=''):
        self.div_id = div_id or js.config().argsFigureDivId

    def __getattr__(self, prop:str):
        return getattr(plt, prop)

    def refresh(self):
        """
        Close any previously created figure, then setup the current run to draw
        in the desired div tag.
        """
        for _ in plt.get_fignums():
            plt.close()
        div = js.document.getElementById(self.div_id)
        div.textContent = ""
        js.document.pyodideMplTarget = div
        return plt

    def plot_func(
        self,
        func:Callable,
        rng:Sequence,
        fmt:str=None,
        title:str=None,
        *,
        show:bool=True,
        keep_figure_num: bool = False,
        **kw
    ):
        """
        Draw an automatic graph for the given function on the given range, then "show"
        automatically the resulting graph in the correct figure element in the page.

        Arguments:
            func:  Callable, func(x) -> y
            rng:   Sequence of xs
            fmt:   Curve formatting (just like `pyplot.plot`)
            title: If given, will be added as title of the graph.
            show:  Call `pyplot.show()` only if `True`. This allows to customize the graph
                   before applying show manually.
        """
        self.refresh()

        xs = list(rng)
        ys = [*map(func, rng)]
        args = (xs,ys) if fmt is None else (xs,ys,fmt)
        out = plt.plot(*args, **kw)

        if title:
            plt.title(title)
        if show:
            plt.show()
        self._cleanup_fig_num(keep_figure_num)
        return out


    def plot(self, *args, keep_figure_num:bool=False, **kw):
        """
        Generic interface, strictly equivalent to `pyplot.plot`, except the `PyodidePlot`
        instance will automatically apply the drawing to the desired html element it is
        related to.

        _Use specifically this method to "plot"_ ! You then can rely on `pyplot` to finalize
        the figure as you prefer.
        """
        self.refresh()
        out = plt.plot(*args, **kw)
        self._cleanup_fig_num(keep_figure_num)
        return out


    def _cleanup_fig_num(self, keep:bool):
        if not keep:
            plt.gcf().canvas.manager.set_window_title('')
