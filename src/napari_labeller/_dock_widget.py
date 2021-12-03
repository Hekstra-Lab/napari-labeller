"""
This module is an example of a barebones QWidget plugin for napari

It implements the ``napari_experimental_provide_dock_widget`` hook specification.
see: https://napari.org/docs/dev/plugins/hook_specifications.html

Replace code below according to your needs.
"""
from pathlib import Path

import napari
import numpy as np
from napari_plugin_engine import napari_hook_implementation
from qtpy import QtWidgets as QtW
from qtpy import uic
from qtpy.QtWidgets import QWidget


class LabellerWidget(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter

    _browse_folder_btn: QtW.QPushButton
    _folder_line_edit: QtW.QLineEdit
    _next_batch_btn: QtW.QPushButton
    _prev_batch_btn: QtW.QPushButton
    _mark_complete_btn: QtW.QPushButton

    def __init__(self, napari_viewer: "napari.viewer.Viewer"):
        super().__init__()
        self.viewer = napari_viewer
        UI_FILE = str(Path(__file__).parent / "_ui" / "labeller_gui.ui")
        uic.loadUi(str(UI_FILE), self)  # Load the .ui file

        self._browse_folder_btn.clicked.connect(self._browse_folders)
        self._folder_line_edit.setEnabled(False)

        self._img = self.viewer.add_image(self._get_next_image_batch(), name="images")
        self._next_batch_btn.clicked.connect(self._on_next)
        self._prev_batch_btn.clicked.connect(self._on_prev)

    def _on_click(self):
        print("napari has", len(self.viewer.layers), "layers")

    # from https://github.com/tlambert03/napari-micromanager
    def _browse_folders(self):
        self._data_folder = Path(
            QtW.QFileDialog.getExistingDirectory(self, "Select Data Folder")
        )
        self._folder_line_edit.setText(str(self._data_folder))

    def _on_next(self):
        self._img.data = self._get_next_image_batch()

    def _on_prev(self):
        pass

    def _get_next_image_batch(self):
        return np.random.randn(5, 256, 256)


# @magic_factory
# def example_magic_widget(img_layer: "napari.layers.Labels"):
#     print(f"you have selected {img_layer}")


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    # you can return either a single widget, or a sequence of widgets
    # return [ExampleQWidget, example_magic_widget]
    return [LabellerWidget]
