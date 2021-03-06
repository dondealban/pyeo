import sys
import gdal
import numpy
import os

def setup_module():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

def test_windows_monkeypatch(monkeypatch):
    # monkeypatch.setattr(sys,'platform','win32')
    out_file = r"test_outputs\windows_stack.tif"
    try:
        os.remove(out_file)
    except FileNotFoundError:
        pass
    from pyeo import raster_manipulation as ras
    test_rasters = [
            r"test_data\class_reproj.tif",
            r"test_data\composite_reproj.tif"
            ]
    ras.stack_images(test_rasters, out_file)
    out = gdal.Open(out_file)
    out_array = out.ReadAsArray()
    assert out_array.max() > 0
