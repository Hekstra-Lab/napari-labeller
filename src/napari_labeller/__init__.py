try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"
__author__ = "Ian Hunt-Isaak and John Russell"

from ._dock_widget import napari_experimental_provide_dock_widget
from ._function import napari_experimental_provide_function

__all__ = [
    "__version__",
    "__author__",
    "napari_experimental_provide_function",
    "napari_experimental_provide_dock_widget",
]
