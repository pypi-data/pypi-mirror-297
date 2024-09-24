# xcube_4d_viewer
This repository is a plugin for the xcube server.

xcube (https://xcube.readthedocs.io/en/latest/overview.html) is a Python package for generating and exploiting data
cubes powered by xarray, dask, and zarr. It also provides a web API and server which can be used to access and
visualise these data cubes.

This repository serves as an API extension to the xcube server, allowing xcube data cubes to be analysed and
visualised within the 4D viewer (https://4dviewer.com). It computes configuration details and
heatmap/3D heatmap/terrain tiles from the server's data cubes and provides them in a format expected by the 4D viewer.

In order to connect to the 4D viewer, the xcube server needs to be registered within a gateway service.

This work is done as part of the DeepESDL project (https://deepesdl.readthedocs.io/en/latest/).
