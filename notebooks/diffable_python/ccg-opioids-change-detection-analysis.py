# -*- coding: utf-8 -*-
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

# # Identifying successful interventions (CCGs) in opioid prescribing data

# This notebook contains methodology and results of an analysis of opioid prescribing data. The CCGs with the ten largest reductions in opioid prescribing are shown here, but it is also possible to access the most recent (last five years) results for any CCG or practice via the [OpenPrescribing.net](OpenPrescribing.net) website.
#
# To find an organisation’s data for any of the three opioid measures use in this analysis, navigate to the specific measure’s landing page. For the measures described in this notebook, these are:
#
# - [Total oral morphine equivalence](https://openprescribing.net/measure/opioidome/)
# - [High dose opioids as percentage regular opioids](https://openprescribing.net/measure/opioidspercent/)
# - [High dose opioids per 1000 patients](https://openprescribing.net/measure/opioidper1000/)
#
# Decile plots for all current CCGs are available on the measure landing page; specific CCGs can be identified via a text search in your browser. To view similar decile plots for a practice, click the “Split the measure into chargers for individual practice” link under the parent CCG.
#
# Alternatively, summary results can be obtained for more than one organisation at once by selecting “View this measure on the analyse page” (under “Explore”) on the measure’s landing page (10–12); this will launch a new analysis, pre-loaded with the relevant drugs or BNF sections. Any number of organisations (CCGs or practices) can then be selected by typing code or text into the “highlighting” box; clicking on the “Show me the data!” button will launch this analysis and display the results as a histogram, time series or as a choropleth map. All plots and raw data are available for download.

# ## Import libraries required for analysis

# NBVAL_IGNORE_OUTPUT
# ^this is a magic comment to work around this issue https://github.com/ebmdatalab/custom-docker/issues/10
from change_detection import functions as chg
from lib.outliers import *  #This is copied into the local folder from a branch ebmdatalab pandas library - it will be placed in its own repo to install at a later dat
import numpy as np

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

display( OME_table )

# ## High dose opioids as percentage regular opioids

# https://openprescribing.net/measure/opioidspercent

# +
highperc_table, all_highperc_changes = filtered_sparkline(opioids,
                   'ccg_data_opioid/ccg_data_opioidspercent',
                   'ccg_data_opioidspercent')
# -


display( highperc_table )

# ## High dose opioids per 1000 patients

# https://openprescribing.net/measure/opioidper1000

high1000_table, all_high1000_changes = filtered_sparkline(opioids,
                   'ccg_data_opioid/ccg_data_opioidper1000',
                   'ccg_data_opioidper1000')

display( high1000_table )

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

CCG_decreases_summary_tosave = CCG_decreases_summary[['count', 'median','IQR','min', 'max']]
CCG_decreases_summary_tosave['median'] = (100 * CCG_decreases_summary_tosave['median']).round(1)
CCG_decreases_summary_tosave['IQR'] = (100 * CCG_decreases_summary_tosave['IQR']).round(1)
CCG_decreases_summary_tosave['min'] = (100 * CCG_decreases_summary_tosave['min']).round(1)
CCG_decreases_summary_tosave['max'] = (100 * CCG_decreases_summary_tosave['max']).round(1)

display( CCG_decreases_summary_tosave )
# +


