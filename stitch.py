#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import os
import glob
import h5py
import fitsio
import numpy as np

fns = glob.glob("data/k2/*.fits.gz")
base_fns = [os.path.split(fn)[1] for fn in fns]
n = len(fns)
meta = np.empty(n, dtype=[
    ("fn", np.str_, max(map(len, base_fns))), ("ra", float), ("dec", float),
    ("xmin", int), ("xmax", int), ("ymin", int), ("ymax", int)
])

print("First pass...")
for i, fn in enumerate(fns):
    meta["fn"][i] = base_fns[i]
    hdr = fitsio.read_header(fn, 2)
    meta["ra"][i] = hdr["RA_OBJ"]
    meta["dec"][i] = hdr["DEC_OBJ"]
    meta["xmin"][i] = hdr["CRVAL1P"]
    meta["xmax"][i] = hdr["CRVAL1P"] + hdr["NAXIS1"]
    meta["ymin"][i] = hdr["CRVAL2P"]
    meta["ymax"][i] = hdr["CRVAL2P"] + hdr["NAXIS2"]

# Normalize the axes.
meta["xmax"] -= meta["xmin"].min()
meta["xmin"] -= meta["xmin"].min()
meta["ymax"] -= meta["ymin"].min()
meta["ymin"] -= meta["ymin"].min()

print("Second pass...")
img, mask = None, None
quality = None
for i, fn in enumerate(fns):
    tbl = fitsio.read(fn)
    xi, yi = np.meshgrid(range(meta["xmin"][i], meta["xmax"][i]),
                         range(meta["ymin"][i], meta["ymax"][i]))
    flux = tbl["FLUX"]
    if img is None:
        img = np.empty((len(flux), meta["xmax"].max(),
                        meta["ymax"].max()), dtype=float)
        mask = np.zeros(img.shape[1:], dtype=bool)
    img[:, xi, yi] = flux
    mask[xi, yi] = True
    time = tbl["TIME"]

# Save a FITS image for WCS calibration using astrometry.net
fitsio.write("data/k2.fits", img[-1], clobber=True)

# Save the block of frames as a huge HDF5 file.
print("Saving...")
with h5py.File("data/k2.h5", "w") as f:
    f.create_dataset("frames", data=img)
    f.create_dataset("mask", data=mask)
    f.create_dataset("time", data=time)
