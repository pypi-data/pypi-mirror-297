# HuBMAP Template Helper Package

This is a package with helper functions for using data from the [HuBMAP Data Portal](https://portal.hubmapconsortium.org).

It is used in various [templates](https://github.com/hubmapconsortium/user-templates-api).

Please refer to the [tutorial](https://github.com/thomcsmits/hubmap_template_helper/blob/main/tutorial.ipynb) to see the usage.


## Installs
Local install
```sh
python -m pip install -e .
```

Pip install
```sh
pip install hubmap-template-helper
```

Build
```sh
python3 -m build
```

Upload
```sh
twine upload dist/*
```

Lint
```sh
flake src/hubmap_template_helper/uuids.py
```