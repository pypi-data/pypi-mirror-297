# 🌀 blue-objects

🌀 `blue-objects` is an abstraction for cloud objects that are accessible in Python and Bash. For example, the Sentinel-2 [datacube](https://github.com/kamangir/blue-geo/tree/main/blue_geo/datacube) `datacube-EarthSearch-sentinel_2_l1c-S2A_10UDC_20240731_0_L1C` and 🌐 [`@geo watch`  outputs](https://github.com/kamangir/blue-geo/tree/main/blue_geo/watch) are objects.

## installation

```bash
pip install blue-objects
```

## use in Bash

```bash
@select
@catalog query copernicus sentinel_2 - . \
  --count 10 \
  --datetime 2024-07-30/2024-08-09 \
  --lat  51.83 \
  --lon -122.78

@select $(@catalog query read - . --count 1 --offset 3)
@datacube ingest scope=metadata+quick .

@publish tar .
```

from [`blue_geo/catalog/copernicus`](https://github.com/kamangir/blue-geo/tree/main/blue_geo/catalog/copernicus).

## use in Python

```python
def map_function(
    datacube_id: str,
    object_name: str,
) -> bool:
    success, target, list_of_files = load_watch(object_name)
    if not success or not list_of_files:
        return success
    filename = list_of_files[0]

    logger.info(
        "{}.map: {} @ {} -> {}".format(
            NAME,
            target,
            datacube_id,
            object_name,
        )
    )

    logger.info("🪄")

```

from [`blue_geo/watch/workflow/map.py`](https://github.com/kamangir/blue-geo/blob/main/blue_geo/watch/workflow/map.py).

---

to use on [AWS SageMaker](https://aws.amazon.com/sagemaker/) replace `<plugin-name>` with "blue_objects" and follow [these instructions](https://github.com/kamangir/notebooks-and-scripts/blob/main/SageMaker.md).

[![pylint](https://github.com/kamangir/blue-objects/actions/workflows/pylint.yml/badge.svg)](https://github.com/kamangir/blue-objects/actions/workflows/pylint.yml) [![pytest](https://github.com/kamangir/blue-objects/actions/workflows/pytest.yml/badge.svg)](https://github.com/kamangir/blue-objects/actions/workflows/pytest.yml) [![bashtest](https://github.com/kamangir/blue-objects/actions/workflows/bashtest.yml/badge.svg)](https://github.com/kamangir/blue-objects/actions/workflows/bashtest.yml) [![PyPI version](https://img.shields.io/pypi/v/blue-objects.svg)](https://pypi.org/project/blue-objects/)

built by 🌀 [`blue_options-4.76.1-abcli-current`](https://github.com/kamangir/awesome-bash-cli), based on 🌀 [`blue_objects-5.75.1`](https://github.com/kamangir/blue-objects).

