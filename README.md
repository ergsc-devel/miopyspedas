# User's guide of Mio-SC plug-ins for PySPEDAS

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
.\miopyspedas_test\Scripts\activate
```

**macOS and Linux**
```bash
source ~/miopyspedas_test/bin/activate
```

#### Using Jupyter notebooks with your virtual environment
To get virtual environments working with Jupyter, in the virtual environment, type:

```bash
pip install ipykernel
python -m ipykernel install --user --name miopyspedas_test --display-name "(miopySPEDAS plug-in)"
```
> [!NOTE]
>"miopyspedas_test" is the name of your virtual environment

Then once you open the notebook, go to "Kernel" then "Change kernel" and select the one named "(miopySPEDAS plug-in)"

### Install
PySPEDAS supports Windows, macOS and Linux. To get started, install the pyspedas package using PyPI:
```bash
pip install pyspedas
```

### Install miopyspedas plug-in
After installing pyspedas, you need to add miopyspedas plug-in to your virtual environment.

```bash
pip install git+https://github.com/ergsc-devel/miopyspedas.git
```


## Examples
An example code for Jupyter notebooks 

```python
import miopyspedas
from pytplot import tplot, store_data, options, get_data
import pyspedas
```

Choose timespan by trange

```python
spm_vars = miopyspedas.spm(trange=["2020-4-10 00:00","2020-4-10 08:00"],level="l2pre")
```
> [!NOTE]
> If you want to use not public data, fill uname and passwd.

Print tplot valuables and sample plot
```python
for i in range(len(spm_vars)):
    print(spm_vars[i])
tplot(spm_vars[0])
```

Extract the data from tplot variables as xarray format.
```python
time, data = get_data('mmo_spm_l2p_spm1_lv3_cnt')
print(pyspedas.time_string(time))
print(data)
```

Similar plot to Fig.5(b) in Kinoshita et al. (2025)

```python
store_data("overplot", data = spm_vars)
options("overplot", 'ylog', 1)
options("overplot", 'legend_names', spm_vars)
options("overplot", 'Color', ['C0', 'C1', 'C2', 'C3', 'C0', 'C1', 'C2', 'C3'])
ls = ['solid_line', 'dash']
options("overplot", 'linestyle', [ls[0], ls[0], ls[0], ls[0], ls[1], ls[1], ls[1], ls[1]])
options("overplot", 'thick', 1.5)
options("overplot", 'ytitle', 'SPM cnt')
tplot("overplot")
```

> [!NOTE]
> unit is different from Kinoshita et al. (2025)








