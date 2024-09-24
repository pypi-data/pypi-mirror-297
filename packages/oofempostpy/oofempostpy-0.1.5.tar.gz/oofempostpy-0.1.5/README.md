<h2 align="center">
  OOFEM Post-Processing Python Package (oofempostpy)
</h2>


`oofempostpy` is a simple Python package with following purposes:
* `log2csv`(log_file.log, output_file.csv): Process [OOFEM](https://github.com/cunyizju/oofem-vltava) simulation logs and export extracted data to a CSV file, based on which the computational efficiency can be analysed.
* Extract history variables such as force and displacement (to be done)
* `hm2oofem`(input_filename.inp, output_filename.in): Transform HyperMesh.input file to OOFEM.in files for [OOFEM](https://github.com/cunyizju/oofem-vltava)

## Prerequisite
* csv
* re
* twine (for build and upload to PyPi)

## Generate oofempostpy

```
python setup.py sdist bdist_wheel
```

## Upload to PyPi

```
twine upload dist/*
```

## Installation

You can install or upgrade the package by running:

```
pip install oofempostpy
```
To install the updatest version of oofempostpy,
```
pip install --upgrade oofempostpy
```