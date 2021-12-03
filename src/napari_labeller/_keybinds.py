import napari

__all__ = [
    "scroll_time",
    "apply_label_keybinds",
]


def scroll_time(viewer: napari.Viewer, time_axis: int = 0) -> None:
    def scroll_callback(layer, event):
        modifiers = [key.name for key in event.modifiers]
        if "Shift" in modifiers:
            new = list(viewer.dims.current_step)

            # get the max time
            max_time = viewer.dims.range[time_axis][1]

            # event.delta is (float, float) for horizontal and vertical scroll
            # on linux shift-scroll gives vertical
            # but on mac it gives horizontal. So just take the max and hope
            # for the best
            if max(event.delta) > 0:
                if new[time_axis] < max_time:
                    new[time_axis] += 1
            else:
                if new[time_axis] > 0:
                    new[time_axis] -= 1
            viewer.dims.current_step = new

    viewer.mouse_wheel_callbacks.append(scroll_callback)


def apply_label_keybinds(labels):
    @labels.bind_key("q")
    def paint_mode(viewer):  # noqa: F811
        labels.mode = "erase"

    @labels.bind_key("w")
    def paint_mode(viewer):  # noqa: F811
        labels.mode = "fill"

    @labels.bind_key("s")
    def paint_mode(viewer):  # noqa: F811
        labels.selected_label = 0
        labels.mode = "fill"

    @labels.bind_key("e")
    def paint_mode(viewer):  # noqa: F811
        labels.mode = "paint"

    @labels.bind_key("r")
    def paint_mode(viewer):  # noqa: F811
        labels.mode = "pick"

    @labels.bind_key("t")
    def new_cell(viewer):  # noqa: F811
        labels.selected_label = labels.data.max() + 1

    def scroll_callback(layer, event):
        if len(event.modifiers) == 0 and labels.mode in ["paint", "erase"]:
            if event.delta[1] > 0:
                labels.brush_size += 1
            else:
                labels.brush_size = max(labels.brush_size - 1, 1)

    labels.mouse_wheel_callbacks.append(scroll_callback)
