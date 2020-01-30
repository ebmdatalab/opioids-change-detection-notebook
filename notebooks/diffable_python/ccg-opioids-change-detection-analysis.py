# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

#import libraries required for analysis
from change_detection import functions as chg
from change_detection import *
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from ebmdatalab import bq
from ebmdatalab import charts
from ebmdatalab import maps
from lib.outliers import *  #This is copied into the local folder from a branch ebmdatalab pandas library - it will be placed in its own repo to install at a later dat

opioids_class = chg.ChangeDetection('ccg_data_opioid%',
                                    measure=True,
                                    direction='down',
                                    use_cache=True,
                                    overwrite=False,
                                    verbose=False,
                                    draw_figures='no')
opioids_class.run()

opioids = opioids_class.concatenate_outputs()
opioids.head()

# ## Total OME

filtered_sparkline(opioids,
                   'ccg_data_opioid/ccg_data_opioidome',
                   'ccg_data_opioidome')

# ## ccg_data_opioidspercent

# [High dose opioids as percentage regular opioids](https://openprescribing.net/measure/opioidspercent/)  

filtered_sparkline(opioids,
                   'ccg_data_opioid/ccg_data_opioidspercent',
                   'ccg_data_opioidspercent')

# ## High dose opioids per 1000 patients

# [High dose opioids per 1000 patients](https://openprescribing.net/measure/opioidper1000/)

filtered_sparkline(opioids,
                   'ccg_data_opioid/ccg_data_opioidper1000',
                   'ccg_data_opioidper1000')
