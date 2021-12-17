# napari-labeller
<!--
[![License](https://img.shields.io/pypi/l/napari-labeller.svg?color=green)](https://github.com/Hekstra-Lab/napari-labeller/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-labeller.svg?color=green)](https://pypi.org/project/napari-labeller)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-labeller.svg?color=green)](https://python.org)
[![tests](https://github.com/Hekstra-Lab/napari-labeller/workflows/tests/badge.svg)](https://github.com/Hekstra-Lab/napari-labeller/actions)
[![codecov](https://codecov.io/gh/Hekstra-Lab/napari-labeller/branch/main/graph/badge.svg)](https://codecov.io/gh/Hekstra-Lab/napari-labeller)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-labeller)](https://napari-hub.org/plugins/napari-labeller)
-->
A plugin for doing manual instance segmentation.

Maybe very similar to [zarpaint](https://github.com/jni/zarpaint)

----------------------------------


## Installation
```bash
git clone https://github.com/Hekstra-Lab/napari-labeller
cd napari-labeller
conda create -n labeller -c conda-forge python=3.9
pip install napari[all]
pip install .
```

You can then launch napari with extension active by running:

`napari -w napari-labeller`


## Keybindings
- `q` : erase
- `w` : fill
- `e` : paint
- `r` : pick
- `t` : create new label

- `scroll` : modify brush size when in paint mode
- `Shift + Scroll` : scrub through time points


## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [BSD-3] license,
"napari-labeller" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

## misc
This [napari] plugin was generated with [Cookiecutter] using [@napari]'s [cookiecutter-napari-plugin] template.

<!--
Don't miss the full getting started guide to set up your new package:
https://github.com/napari/cookiecutter-napari-plugin#getting-started

and review the napari docs for plugin developers:
https://napari.org/docs/plugins/index.html
-->
[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin

[file an issue]: https://github.com/Hekstra-Lab/napari-labeller/issues

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
