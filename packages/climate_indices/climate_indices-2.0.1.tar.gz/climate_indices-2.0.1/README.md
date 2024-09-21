![Banner Image](assets/Global_Monthly_SPI.jpg)

# climate_indices

[//]: # ([![Coverage Status]&#40;https://coveralls.io/repos/github/monocongo/climate_indices/badge.svg?branch=master&#41;]&#40;https://coveralls.io/github/monocongo/climate_indices?branch=master&#41;)
[//]: # ([![Codacy Status]&#40;https://api.codacy.com/project/badge/Grade/48563cbc37504fc6aa72100370e71f58&#41;]&#40;https://www.codacy.com/app/monocongo/climate_indices?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=monocongo/climate_indices&amp;utm_campaign=Badge_Grade&#41;)
[![Actions Status](https://github.com/monocongo/climate_indices/workflows/tests/badge.svg)](https://github.com/monocongo/climate_indices/actions)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-green.svg)](https://opensource.org/licenses/BSD-3-Clause)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/climate-indices)

#### Python library of indices useful for climate monitoring

This project contains Python implementations of various climate index algorithms which provide
a geographical and temporal picture of the severity and duration of precipitation and temperature
anomalies useful for climate monitoring and research.

The following indices are provided:

- [SPI](https://climatedataguide.ucar.edu/climate-data/standardized-precipitation-index-spi),
  Standardized Precipitation Index, utilizing both gamma and Pearson Type III distributions
- [SPEI](https://www.researchgate.net/publication/252361460_The_Standardized_Precipitation-Evapotranspiration_Index_SPEI_a_multiscalar_drought_index),
  Standardized Precipitation Evapotranspiration Index, utilizing both gamma and Pearson Type III distributions
- [PET](https://www.ncdc.noaa.gov/monitoring-references/dyk/potential-evapotranspiration), Potential Evapotranspiration, utilizing either [Thornthwaite](http://dx.doi.org/10.2307/21073)
  or [Hargreaves](http://dx.doi.org/10.13031/2013.26773) equations
- [PNP](http://www.droughtmanagement.info/percent-of-normal-precipitation/),
  Percentage of Normal Precipitation
- [PCI](https://www.tandfonline.com/doi/abs/10.1111/J.0033-0124.1980.00300.X), Precipitation Concentration Index

This Python implementation of the above climate index algorithms is being developed
with the following goals in mind:

- to provide an open source software package to compute a suite of
  climate indices commonly used for climate monitoring, with well
  documented code that is faithful to the relevant literature and
  which produces scientifically verifiable results
- to provide a central, open location for participation and collaboration
  for researchers, developers, and users of climate indices
- to facilitate standardization and consensus on best-of-breed
  climate index algorithms and corresponding compliant implementations in Python
- to provide transparency into the operational code used for climate
  monitoring activities at NCEI/NOAA, and consequent reproducibility
  of published datasets computed from this package
- to incorporate modern software engineering principles and scientific programming
  best practices


This is a developmental/forked version of code that was originally developed by NIDIS/NCEI/NOAA. 
See [drought.gov](https://www.drought.gov/drought/python-climate-indices).

- [__Documentation__](https://climate-indices.readthedocs.io/en/latest/)
- [__License__](LICENSE)
- [__Disclaimer__](DISCLAIMER)

#### Citation
You can cite `climate_indices` in your projects and research papers via the BibTeX 
entry below.
```
@misc {climate_indices,
    author = "James Adams",
    title  = "climate_indices, an open source Python library providing reference implementations of commonly used climate indices",
    url    = "https://github.com/monocongo/climate_indices",
    month  = "may",
    year   = "2017--"
}
```
