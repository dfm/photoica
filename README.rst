Getting started
---------------

First you'll need to download the K2 Campaign 0 data. To do this, run:

.. code-block:: bash

    mkdir -p data/k2
    cd data/k2
    wget -q -nH --cut-dirs=6 -r -l0 -c -N -np -R 'index*' -erobots=off \
        http://archive.stsci.edu/missions/k2/target_pixel_files/c0/200000000/00000/
