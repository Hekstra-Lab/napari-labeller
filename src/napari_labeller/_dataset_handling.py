from glob import glob
from pathlib import Path
from typing import Union

import xarray as xr


def list_datasets(base_path: Union[str, Path]):
    base = Path(base_path)
    return sorted(glob(str(base / "*.nc")))


def get_dataset(base_path: Union[str, Path], idx: int):
    path = list_datasets(base_path)[idx]
    ds = xr.load_dataset(path)
    if "update_status" not in ds.attrs:
        ds.attrs["update_status"] = "in_progress"
    else:
        if ds.attrs["update_status"] == "completed":
            # What do we want to do here?
            pass

    return ds


def set_completed(ds: xr.Dataset):
    ds.attrs["update_status"] = "completed"
