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

# ## Import libraries required for analysis

# + scrolled=true
# NBVAL_IGNORE_OUTPUT
# ^this is a magic comment to work around this issue https://github.com/ebmdatalab/custom-docker/issues/10
from change_detection import functions as chg
from ebmdatalab import bq
from lib.outliers import *  #This is copied into the local folder from a branch ebmdatalab pandas library - it will be placed in its own repo to install at a later dat
import numpy as np
# -

# ## Run change detection for the 3 OpenPrescribing opioid measures
# - looks for changes in time-series data
# - as described in https://www.bmj.com/content/367/bmj.l5205

# NBVAL_IGNORE_OUTPUT
# ^this is a magic comment to work around this issue https://github.com/ebmdatalab/custom-docker/issues/10
opioids_class = chg.ChangeDetection('practice_data_opioid%',
                                    measure=True,
                                    direction='down',
                                    overwrite=False,
                                    verbose=False,
                                    draw_figures='no')
opioids_class.run()

# ## Import results of change detection

opioids = opioids_class.concatenate_outputs()
opioids.head()

# ### Get list to filter out closed practices

query = """
SELECT
  DISTINCT code
FROM
  ebmdatalab.hscic.practices
WHERE
  status_code = "A"
"""
open_practices = bq.cached_read(query,csv_path='data/open_practices.csv')
open_practices.head()

# ### Get practices with a small list size to filter them out 

query = """
SELECT
  DISTINCT practice
FROM
  ebmdatalab.hscic.practice_statistics
WHERE
  total_list_size < 2000
"""
small_list_size = bq.cached_read(query,csv_path='data/small_list_size.csv')
small_list_size.head()

# ### Remove small list sizes and closed/dormant practices

print(len(opioids))
mask = opioids.index.get_level_values(1).isin(open_practices['code'])
opioids = opioids.loc[mask]
print(len(opioids))
mask = opioids.index.get_level_values(1).isin(small_list_size['practice'])
opioids = opioids.loc[~mask]
print(len(opioids))
opioids.head()

# # Results
# These are filtered:
# - to only include practices that started within the highest 20% of all practices
# - to remove any practices that have a short sudden spike that would lead the change detection algorithm to detect a sudden drop
#
# and then sorted according to the largest total measured drop.

# ## Total Oral Morphine Equivalence
# https://openprescribing.net/measure/opioidome

OME_table, all_OME_changes = filtered_sparkline(opioids,
                   'practice_data_opioid/practice_data_opioidome',
                   'practice_data_opioidome')

OME_table

# ## High dose opioids as percentage regular opioids

# https://openprescribing.net/measure/opioidspercent

highperc_table, all_highperc_changes = filtered_sparkline(opioids,
                   'practice_data_opioid/practice_data_opioidspercent',
                   'practice_data_opioidspercent')

highperc_table

# ## High dose opioids per 1000 patients

# https://openprescribing.net/measure/opioidper1000

high1000_table, all_high1000_changes = filtered_sparkline(opioids,
                   'practice_data_opioid/practice_data_opioidper1000',
                   'practice_data_opioidper1000')

high1000_table

# ## Summary statistics
#
# Summary statistics shown for all practices demonstrating a decrease.

# +
all_OME_changes["measure"] = "Total oral morphine equivalence"
all_highperc_changes["measure"] = "High dose opioids as percentage regular opioids"
all_high1000_changes["measure"] = "High dose opioids per 1000 patients"

all_changes = all_OME_changes.append(all_highperc_changes).append(all_high1000_changes)
all_changes = all_changes[~all_changes.isin([np.nan, np.inf, -np.inf]).any(1)]
all_decreases = all_changes[all_changes['is.intlev.levdprop']>0]

practice_decreases_summary = all_decreases.groupby("measure")["is.intlev.levdprop"].describe()
practice_decreases_summary['IQR'] = practice_decreases_summary['75%'] - practice_decreases_summary['25%']
practice_decreases_summary.rename( columns={'50%' : 'median'}, inplace=True)

practice_decreases_summary_tosave = practice_decreases_summary[['count', 'median','IQR','min', 'max']]
practice_decreases_summary_tosave['median'] = (100 * practice_decreases_summary_tosave['median']).round(1)
practice_decreases_summary_tosave['IQR'] = (100 * practice_decreases_summary_tosave['IQR']).round(1)
practice_decreases_summary_tosave['min'] = (100 * practice_decreases_summary_tosave['min']).round(1)
practice_decreases_summary_tosave['max'] = (100 * practice_decreases_summary_tosave['max']).round(1)
practice_decreases_summary_tosave
# -


