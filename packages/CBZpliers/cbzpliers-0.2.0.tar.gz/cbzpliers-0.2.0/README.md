# CBZpliers

Pliers is a Python tool that helps you combine multiple `.cbz` (comic book archive) files into a single file.

## Installation

You will be able to install Pliers directly from PyPI:

```bash
pip install CBZpliers
```
## Usage

You can use the tool from command line

```bash
combine_cbz <cbz_dir> <volume_title> <series_title>
```

<cbz_dir> - path to the directory which contains the files you want to combine. It is recommended to have a separate directory, containing nothing BUT the .cbz files

<volume_title> - name of the final .cbz file

<series_title> - name of the series, only shows in the .xml file inside the .cbz archive, but might be useful for some applications
