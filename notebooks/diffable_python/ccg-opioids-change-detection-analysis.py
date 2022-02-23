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

# NBVAL_IGNORE_OUTPUT
# ^this is a magic comment to work around this issue https://github.com/ebmdatalab/custom-docker/issues/10
from change_detection import functions as chg
from lib.outliers import *  #This is copied into the local folder from a branch ebmdatalab pandas library - it will be placed in its own repo to install at a later dat

# ## Run change detection for the 3 OpenPrescribing opioid measures
# - looks for changes in time-series data
# - as described in https://www.bmj.com/content/367/bmj.l5205

# NBVAL_IGNORE_OUTPUT
# ^this is a magic comment to work around this issue https://github.com/ebmdatalab/custom-docker/issues/10
opioids_class = chg.ChangeDetection('ccg_data_opioid%',
                                    measure=True,
                                    direction='down',
                                    use_cache=True,
                                    overwrite=False,
                                    verbose=False,
                                    draw_figures='no')
opioids_class.run()

# ## Import results of change detection

opioids = opioids_class.concatenate_outputs()
opioids.head()

# # Results
# These are filtered:
# - to only include CCGs that started within the highest 20% of all CCGs
# - to remove any CCGs that have a short sudden spike that would lead the change detection algorithm to detect a sudden drop
#
# and then sorted according to the largest total measured drop.

# ## Total Oral Morphine Equivalence
# https://openprescribing.net/measure/opioidome

OME_table, all_OME_changes  = filtered_sparkline(opioids,
                   'ccg_data_opioid/ccg_data_opioidome',
                   'ccg_data_opioidome')

OME_table

# ## High dose opioids as percentage regular opioids

# https://openprescribing.net/measure/opioidspercent

highperc_table, all_highperc_changes = filtered_sparkline(opioids,
                   'ccg_data_opioid/ccg_data_opioidspercent',
                   'ccg_data_opioidspercent')


highperc_table

# ## High dose opioids per 1000 patients

# https://openprescribing.net/measure/opioidper1000

high1000_table, all_high1000_changes = filtered_sparkline(opioids,
                   'ccg_data_opioid/ccg_data_opioidper1000',
                   'ccg_data_opioidper1000')

high1000_table

# ## Summary statistics
#
# Summary statistics shown for all CCGs demonstrating a decrease.

# +
all_OME_changes["measure"] = "Total oral morphine equivalence"
all_highperc_changes["measure"] = "High dose opioids as percentage regular opioids"
all_high1000_changes["measure"] = "High dose opioids per 1000 patients"

all_changes = all_OME_changes.append(all_highperc_changes).append(all_high1000_changes)
all_changes = all_changes[~all_changes.isin([np.nan, np.inf, -np.inf]).any(1)]
all_decreases = all_changes[all_changes['is.intlev.levdprop']>0]

CCG_decreases_summary = all_decreases.groupby("measure")["is.intlev.levdprop"].describe()
CCG_decreases_summary['IQR'] = CCG_decreases_summary['75%'] - CCG_decreases_summary['25%']
CCG_decreases_summary.rename( columns={'50%' : 'median'}, inplace=True)

CCG_decreases_summary_tosave = CCG_decreases_summary[['median','IQR','min', 'max']].multiply(100).round(2)
CCG_decreases_summary_tosave
# -

CCG_decreases_summary_tosave.to_csv('data/CCG_summary_statistics.csv')


