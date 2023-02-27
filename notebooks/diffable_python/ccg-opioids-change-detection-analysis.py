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


def filtered_sparkline_test(df, name, measure):
    data = pd.read_csv('data/{}/bq_cache.csv'.format(name),index_col='code')
    data['month'] = pd.to_datetime(data['month'])
    data['rate'] = data['numerator'] / data['denominator']
    data = data.sort_values('month')
   
    filtered = df.loc[measure]
    
    #pick entities that start high
    #mask = filtered['is.intlev.initlev'] > filtered['is.intlev.initlev'].quantile(0.8)
    #filtered = filtered.loc[mask]
    
    #remove entities with a big spike
    #mean_std_max = data['rate'].groupby(['code']).agg(['mean','std','max'])
    #mask = mean_std_max['max'] < (mean_std_max['mean'] + (1.96*mean_std_max['std']))
    #filtered = filtered.loc[mask]
    
    #drop duplicates
    #filtered = filtered.loc[~filtered.index.duplicated(keep='first')]
    
    #filtered = filtered.sort_values('is.intlev.levdprop', ascending=False).head(10)
   # plot_series = sparkline_table(data, 'rate', subset=filtered.index)

    #get entity names and turn into link
    #entity_type = name.split('_')[0]
    #entity_names = get_entity_names(entity_type)
    #entity_names['code'] = entity_names.index
    #measure_name = measure.split('_')[-1]
    #entity_names['link'] = entity_names[['code','name']].apply(lambda x:
     #   '<a href="https://openprescribing.net/measure/{0}/{1}/{2}/">{3}</a>'.format(
     #       measure_name,
     #       entity_type,
     #       x[0],
     #       x[1]
     #       ),axis=1)

    #change month integer to dates
    #filtered['min_month'] = data['month'].min()
    #filtered['is.tfirst.big'] = filtered.apply(lambda x:
    #    x['min_month']
    #    + pd.DateOffset(months = x['is.tfirst.big']-1 ),
    #    axis=1)

    #create output table
    #out_table = filtered[['is.tfirst.big','is.intlev.levdprop']]
    #out_table = out_table.join(entity_names['link'])
    #out_table = out_table.join(plot_series)
    #out_table = out_table.rename(columns={
    #    "is.tfirst.big": "Month when change detected",
    #     "is.intlev.levdprop": "Measured proportional change"
     #    })
    #return out_table.set_index('link')


# ## Run change detection for the 3 OpenPrescribing opioid measures
# - looks for changes in time-series data
# - as described in https://www.bmj.com/content/367/bmj.l5205

# NBVAL_IGNORE_OUTPUT
# ^this is a magic comment to work around this issue https://github.com/ebmdatalab/custom-docker/issues/10
opioids_class = chg.ChangeDetection('ccg_data_opioid%',
                                    measure=True,
                                    direction='down',
                                    use_cache=False,
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

filtered_sparkline_test(opioids,
                   'ccg_data_opioid/ccg_data_opioidome',
                   'ccg_data_opioidome')

filtered

# ## High dose opioids as percentage regular opioids

# https://openprescribing.net/measure/opioidspercent

filtered_sparkline(opioids,
                   'ccg_data_opioid/ccg_data_opioidspercent',
                   'ccg_data_opioidspercent')

# ## High dose opioids per 1000 patients

# https://openprescribing.net/measure/opioidper1000

filtered_sparkline(opioids,
                   'ccg_data_opioid/ccg_data_opioidper1000',
                   'ccg_data_opioidper1000')

# +
#def filtered_sparkline_test(df, name, measure):
data = pd.read_csv('data/ccg_data_opioid/ccg_data_opioidper1000/bq_cache.csv'.format('ccg_data_opioidper1000'),index_col='code')
data['month'] = pd.to_datetime(data['month'])
data['rate'] = data['numerator'] / data['denominator']
data = data.sort_values('month')
   
filtered = opioids.loc['ccg_data_opioidper1000']

#pick entities that start high
mask = filtered['is.intlev.initlev'] > filtered['is.intlev.initlev'].quantile(0.8)
filtered = filtered.loc[mask]

#remove entities with a big spike
mean_std_max = data['rate'].groupby(['code']).agg(['mean','std','max'])
mask = mean_std_max['max'] < (mean_std_max['mean'] + (1.96*mean_std_max['std']))
filtered = filtered.loc[mask]

#drop duplicates
#filtered = filtered.loc[~filtered.index.duplicated(keep='first')]

#filtered = filtered.sort_values('is.intlev.levdprop', ascending=False).head(10)
# plot_series = sparkline_table(data, 'rate', subset=filtered.index)

#get entity names and turn into link
#entity_type = name.split('_')[0]
#entity_names = get_entity_names(entity_type)
#entity_names['code'] = entity_names.index
#measure_name = measure.split('_')[-1]
#entity_names['link'] = entity_names[['code','name']].apply(lambda x:
 #   '<a href="https://openprescribing.net/measure/{0}/{1}/{2}/">{3}</a>'.format(
 #       measure_name,
 #       entity_type,
 #       x[0],
 #       x[1]
 #       ),axis=1)

#change month integer to dates
#filtered['min_month'] = data['month'].min()
#filtered['is.tfirst.big'] = filtered.apply(lambda x:
#    x['min_month']
#    + pd.DateOffset(months = x['is.tfirst.big']-1 ),
#    axis=1)

#create output table
#out_table = filtered[['is.tfirst.big','is.intlev.levdprop']]
#out_table = out_table.join(entity_names['link'])
#out_table = out_table.join(plot_series)
#out_table = out_table.rename(columns={
#    "is.tfirst.big": "Month when change detected",
#     "is.intlev.levdprop": "Measured proportional change"
 #    })
#return out_table.set_index('link')
# -

filtered.head()

mean_std_max

mask


