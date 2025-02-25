# The development of the Mio-SC plug-ins for PySPEDAS
> refac_spm: SPM moduleの整理整頓用branch

The routines in this module can be used to load data from the BepiColombo/Mercury Magnetospheric Orbiter (MMO).

## Instruments 
* Solar Particle Monitor (SPM) 
* Coming soon...

## Instllation
To avoid potential dependency issues with other Python packages, we suggest creating a virtual environment for miopyspedas plug-in; you can create a virtual environment in your terminal with:

### Virtual Environment

```
python -m venv miopyspedas_test
```

To enter your virtual environment, run the 'activate' script:

**Windows**
```bash
~\miopyspedas_test\Scripts\activate
```

**macOS and Linux**
```bash
source ~/miopyspedas_test/bin/activate
```

#### Using Jupyter notebooks with your virtual environment
To get virtual environments working with Jupyter, in the virtual environment, type:

```bash
pip install ipykernel
python -m ipykernel install --user --name miopyspedas --display-name "(miopySPEDAS plug-in)"
```

(note: "miopyspedas" is the name of your virtual environment)

Then once you open the notebook, go to "Kernel" then "Change kernel" and select the one named "(miopySPEDAS plug-in)"

### Install
PySPEDAS supports Windows, macOS and Linux. To get started, install the pyspedas package using PyPI:
```bash
pip install pyspedas
```

### Install miopyspedas plug-in


## Examples


