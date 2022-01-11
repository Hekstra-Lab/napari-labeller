"""
This module is an example of a barebones QWidget plugin for napari

It implements the ``napari_experimental_provide_dock_widget`` hook specification.
see: https://napari.org/docs/dev/plugins/hook_specifications.html

Replace code below according to your needs.
"""
from pathlib import Path
from typing import Optional, Union

import napari
from napari_plugin_engine import napari_hook_implementation
from qtpy import QtWidgets as QtW
from qtpy import uic
from qtpy.QtWidgets import QWidget

from ._dataset_handling import get_dataset, list_datasets
from ._keybinds import apply_label_keybinds, scroll_time


class LabellerWidget(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter

    _browse_folder_btn: QtW.QPushButton
    _folder_line_edit: QtW.QLineEdit
    _next_batch_btn: QtW.QPushButton
    _prev_batch_btn: QtW.QPushButton
    _save_progress_btn: QtW.QPushButton

    def __init__(self, napari_viewer: "napari.viewer.Viewer"):
        super().__init__()
        self.viewer = napari_viewer
        UI_FILE = str(Path(__file__).parent / "_ui" / "labeller_gui.ui")
        uic.loadUi(str(UI_FILE), self)  # Load the .ui file

        self._data_folder: Optional[Path] = None
        self._browse_folder_btn.clicked.connect(self._browse_folders)
        self._folder_line_edit.setEnabled(False)

        self._next_batch_btn.setEnabled(False)
        self._prev_batch_btn.setEnabled(False)
        self._next_batch_btn.clicked.connect(self._on_next)
        self._prev_batch_btn.clicked.connect(self._on_prev)

        self._save_progress_btn.clicked.connect(self._save_progress)

        # recover if our plugin was closed but our layers are still hanging around
        for l in self.viewer.layers:
            if hasattr(l, "_labeller_images"):
                self._recover_information()

    @property
    def data_folder(self) -> Union[Path, None]:
        return self._data_folder

    @data_folder.setter
    def data_folder(self, value: Union[str, Path]):
        self._data_folder = Path(value)
        self._set_up_folder_variables()
        self._on_next()

    def _set_up_folder_variables(self):
        self._folder_line_edit.setText(str(self._data_folder))
        self._file_list = list_datasets(self._data_folder)
        self._num_files = len(self._file_list)
        self._next_batch_btn.setEnabled(True)
        self._prev_batch_btn.setEnabled(True)
        self._file_idx = -1

    def _browse_folders(self):
        self.data_folder = Path(
            QtW.QFileDialog.getExistingDirectory(self, "Select Data Folder")
        )

    def _save_progress(self):
        self._working_ds.to_netcdf(self._file_list[self._file_idx])

    def _on_next(self):
        if self._file_idx == -1:
            self._initialize_viewer()

        else:
            self._save_progress()
            self._file_idx = (
                self._file_idx + 1
                if self._file_idx + 1 < self._num_files
                else self._num_files - 1
            )
            self._get_next_image_batch()

    def _on_prev(self):
        self._working_ds.to_netcdf(self._file_list[self._file_idx])
        self._file_idx = self._file_idx - 1 if self._file_idx > 0 else 0

        self._get_next_image_batch()

    def _get_next_image_batch(self):
        self._working_ds = get_dataset(self._data_folder, self._file_idx)
        if "Z" in self._working_ds.dims:
            images = self._working_ds.images.mean("Z")
        else:
            images = self._working_ds.images

        self._img.data = images
        self._labels.data = self._working_ds.labels

    def _recover_information(self):
        # for i in range(len(self.viewer.layers)):
        for layer in self.viewer.layers:
            if hasattr(layer, "_labeller_images"):
                self._img = layer
            elif hasattr(layer, "_labeller_labels"):
                self._labels = layer
                self._file_list = list
                self._data_folder = self._labels._data_folder
                self._set_up_folder_variables()
                self._file_idx = self._labels._file_idx
                self._working_ds = get_dataset(self._data_folder, self._file_idx)
                self._working_ds.labels.data = self._labels.data

    def _initialize_viewer(self):
        self._file_idx = 0
        self._working_ds = get_dataset(self._data_folder, self._file_idx)
        if "Z" in self._working_ds.dims:
            images = self._working_ds.images.mean("Z")
        else:
            images = self._working_ds.images

        self._img = self.viewer.add_image(images)
        self._img._labeller_images = True
        self._labels = self.viewer.add_labels(self._working_ds.labels.data)
        self._labels._labeller_labels = True
        self._labels._data_folder = self._data_folder
        self._labels._file_idx = self._file_idx

        scroll_time(self.viewer)
        apply_label_keybinds(self._labels)


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return LabellerWidget
