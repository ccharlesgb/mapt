import os
import shutil
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict

import fiona
import py
from app.core.datasets.operations import parse_shapefile
from fiona.crs import from_epsg


def create_shapefile(record_count: int, tmpdir: py.path.local) -> bytes:
    # TODO: Figure out ohw to get fiona to write shape files from scratch
    schema: Dict[str, Any] = {}
    schema["properties"] = OrderedDict([("objectid", "int:4"), ("my_string", "str:32")])
    schema["geometry"] = "Point"
    out_filename = os.path.join(tmpdir.strpath, "test_file")
    with fiona.open(
        out_filename, "w", crs=from_epsg(27700), driver="ESRI Shapefile", schema=schema
    ) as dest:
        for index in range(0, record_count):
            record = {
                "geometry": {"type": "Point", "coordinates": [0.0, 0.0]},
                "properties": {"objectid": index, "my_string": "abcde"},
            }
            dest.write(record)
    zip_out_filename = os.path.join(tmpdir.strpath, "test_file")
    shutil.make_archive(zip_out_filename, "zip", tmpdir.strpath)
    os.listdir(tmpdir.strpath)
    with open(
        os.path.join(tmpdir.strpath, zip_out_filename) + ".zip", "rb"
    ) as out_file:
        binary_contents = out_file.read()
    return binary_contents


def test_parse_shapefile_valid(resource_path_root: Path) -> None:
    # This is a bit of a bad test until I can get fiona generating shape file zips properly
    # We can only check one example that it parses it without failure
    filename = "Canals_KM_View_Public-shp.zip"
    shp_contents = (resource_path_root / ("%s" % filename)).read_bytes()
    dataset, features = parse_shapefile("%s" % filename, shp_contents)

    assert dataset.label == filename
    assert filename in dataset.description
    assert len(dataset.features) > 0
