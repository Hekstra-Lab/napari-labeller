from pathlib import Path

import napari

v = napari.Viewer()
dw, labeller_widget = v.window.add_plugin_dock_widget("napari-labeller")

labeller_widget.data_folder = Path(__file__).parent / "dev-data" / "2021-11-11"

napari.run()
