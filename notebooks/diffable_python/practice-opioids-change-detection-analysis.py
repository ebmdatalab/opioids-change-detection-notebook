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

open_practices.size

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

small_list_size.size

# ### Remove small list sizes and closed/dormant practices

opioids_saved = opioids

opioids.index.get_level_values(0).unique()

#print(len(opioids))
print(f"practice_data_opioidome: {len(opioids.loc['practice_data_opioidome',:])}")
print(f"practice_data_opioidper1000: {len(opioids.loc['practice_data_opioidper1000',:])}")
print(f"practice_data_opioidspercent: {len(opioids.loc['practice_data_opioidspercent',:])}")

# +

mask = opioids.index.get_level_values(1).isin(open_practices['code'])
print( f"Number of open practices (from input file): {open_practices.size}" )
print( f"Number of practices that we identify as open (practice_data_opioidome): {len(opioids[mask].loc['practice_data_opioidome',:])}" )
print( f"Number of practices that we identify as open (practice_data_opioidper1000): {len(opioids[mask].loc['practice_data_opioidper1000',:])}" )
print( f"Number of practices that we identify as open (practice_data_opioidspercent): {len(opioids[mask].loc['practice_data_opioidspercent',:])}" )

# -



opioids = opioids.loc[mask]
#print(len(opioids))


# +
mask = opioids.index.get_level_values(1).isin(small_list_size['practice'])
print( f"Number of small practices (from input file): {small_list_size.size}" )
print( f"Number of practices that we identify as open AND with a small list size (practice_data_opioidome): {len(opioids[~mask].loc['practice_data_opioidome',:])}" )
print( f"Number of practices that we identify as open AND with a small list size (practice_data_opioidper1000): {len(opioids[~mask].loc['practice_data_opioidper1000',:])}" )
print( f"Number of practices that we identify as open AND with a small list size (practice_data_opioidspercent): {len(opioids[~mask].loc['practice_data_opioidspercent',:])}" )

opioids = opioids.loc[~mask]


# +
#print(len(opioids))
#opioids.head()
# -

len(opioids.loc["practice_data_opioidome",:])

# # Results
# These are filtered:
# - to only include practices that started within the highest 20% of all practices
# - to remove any practices that have a short sudden spike that would lead the change detection algorithm to detect a sudden drop
#
# and then sorted according to the largest total measured drop.

# ## Total Oral Morphine Equivalence
# https://openprescribing.net/measure/opioidome

filtered_sparkline(opioids,
                   'practice_data_opioid/practice_data_opioidome',
                   'practice_data_opioidome')

# ## High dose opioids as percentage regular opioids

# https://openprescribing.net/measure/opioidspercent



filtered_sparkline(opioids,
                   'practice_data_opioid/practice_data_opioidspercent',
                   'practice_data_opioidspercent')



# ## High dose opioids per 1000 patients

# https://openprescribing.net/measure/opioidper1000

filtered_sparkline(opioids,
                   'practice_data_opioid/practice_data_opioidper1000',
                   'practice_data_opioidper1000')
