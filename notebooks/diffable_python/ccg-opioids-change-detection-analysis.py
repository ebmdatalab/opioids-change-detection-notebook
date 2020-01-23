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
                                    overwrite=False,
                                    verbose=False,
                                    draw_figures='yes')
opioids_class.run()

opioids = opioids_class.concatenate_outputs()
opioids

opioids = opioids.reset_index()
opioids.head()

# +
ccg_data_opioidome = opioids.loc[(opioids["measure"] == "ccg_data_opioidome")]


# +
ccg_data_opioidspercent = opioids.loc[(opioids["measure"] == "ccg_data_opioidspercent")]
# -


ccg_data_opioidper1000 = opioids.loc[(opioids["measure"] == "ccg_data_opioidper1000")]
ccg_data_opioidper1000.head()

# ## Total OME

# +
data = pd.read_csv('data/ccg_data_opioid/ccg_data_opioidome/bq_cache.csv',index_col='code')
data['rate'] = data['numerator'] / data['denominator']
data = data.sort_values('month')

# is.slope.ma Average slope over steepest segment contributing at least XX% of total drop is.slope.ma
omeisslopema = ccg_data_opioidome.sort_values("is.slope.ma", ascending=False).head(5)
omeisslopema = omeisslopema.set_index('name')

#is.slope.ma.prop Average slope as proportion to prior level
omeisslopemaprop = ccg_data_opioidome.sort_values("is.slope.ma.prop", ascending=False).head(5)
omeisslopeamprop = omeisslopemaprop.set_index('name')


#is.intlev.levdprop Percentage of the total drop the segment used to evaluate the slope makes up
omeintlevlevprop = ccg_data_opioidome.sort_values("is.intlev.levdprop", ascending=False).head(5) 
omeintlevlevprop = omeintlevlevprop.set_index('name')

# + scrolled=true
data.loc['06F',['month','rate']]
# -

ser = sparkline_table(data, 'rate', subset=omeisslopeamprop.index)
ser
omeisslopeamprop[["is.tfirst.big","is.intlev.levdprop"]].join(ser)

ser = sparkline_table(data, 'rate', subset=omeisslopeamprop.index)
ser
omeisslopeamprop[["is.tfirst.big","is.slope.ma.prop"]].join(ser)

ser = sparkline_table(data, 'rate', subset=omeisslopema.index)
ser
omeisslopema [["is.tfirst.big","is.slope.ma"]].join(ser)

# ## ccg_data_opioidspercent

# [High dose opioids as percentage regular opioids](https://openprescribing.net/measure/opioidspercent/)  

# +
data = pd.read_csv('data/ccg_data_opioid/ccg_data_opioidspercent/bq_cache.csv',index_col='code')
data['rate'] = data['numerator'] / data['denominator']
data = data.sort_values('month')

#Average slope over steepest segment contributing at least XX% of total drop is.slope.ma
highdoseisslopema = ccg_data_opioidspercent.sort_values("is.slope.ma", ascending=False).head(5)
highdoseisslopema = highdoseisslopema.set_index('name')

#is.slope.ma.prop Average slope as proportion to prior level
highdoseisslopemaprop = ccg_data_opioidspercent.sort_values("is.slope.ma.prop", ascending=False).head(5)
highdoseisslopeamprop = highdoseisslopemaprop.set_index('name')

#is.intlev.levdprop Percentage of the total drop the segment used to evaluate the slope makes up
highdoseintlevlevprop = ccg_data_opioidspercent.sort_values("is.intlev.levdprop", ascending=False).head(5) 
highdoseintlevlevprop = highdoseintlevlevprop.set_index('name')
# -

ser = sparkline_table(data, 'rate', subset=highdoseisslopema.index)
ser
highdoseisslopema[["is.tfirst.big","is.slope.ma"]].join(ser)

ser = sparkline_table(data, 'rate', subset=highdoseisslopeamprop.index)
ser
highdoseisslopeamprop[["is.tfirst.big","is.slope.ma.prop"]].join(ser)

ser = sparkline_table(data, 'rate', subset=highdoseisslopema.index)
ser
highdoseisslopema[["is.tfirst.big","is.intlev.levdprop"]].join(ser)

# ## High dose opioids per 1000 patients

# [High dose opioids per 1000 patients](https://openprescribing.net/measure/opioidper1000/)

# +
data = pd.read_csv('data/ccg_data_opioid/ccg_data_opioidper1000/bq_cache.csv',index_col='code')
data['rate'] = data['numerator'] / data['denominator']
data = data.sort_values('month')

#Average slope over steepest segment contributing at least XX% of total drop is.slope.ma
higdoseistsizeisslopema = ccg_data_opioidome.sort_values("is.slope.ma", ascending=False).head(5)
higdoseistsizeisslopema = higdoseistsizeisslopema.set_index('name')

#is.slope.ma.prop Average slope as proportion to prior level
higdoseistsizeisslopemaprop = ccg_data_opioidome.sort_values("is.slope.ma.prop", ascending=False).head(5)
higdoseistsizeisslopeamprop = higdoseistsizeisslopemaprop.set_index('name')

#is.intlev.levdprop Percentage of the total drop the segment used to evaluate the slope makes up
higdoseistsizeintlevlevprop = ccg_data_opioidome.sort_values("is.intlev.levdprop", ascending=False).head(5) 
higdoseistsizeintlevlevprop = higdoseistsizeintlevlevprop.set_index('name')

# -

ser = sparkline_table(data, 'rate', subset=higdoseistsizeintlevlevprop.index)
ser
higdoseistsizeintlevlevprop[["is.tfirst.big","is.intlev.levdprop"]].join(ser)

ser = sparkline_table(data, 'rate', subset=higdoseistsizeisslopeamprop.index)
ser
higdoseistsizeisslopeamprop[["is.tfirst.big","is.slope.ma.prop"]].join(ser)

ser = sparkline_table(data, 'rate', subset=higdoseistsizeisslopema.index)
ser
higdoseistsizeisslopema[["is.tfirst.big","is.slope.ma"]].join(ser)
