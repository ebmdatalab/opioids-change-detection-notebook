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

# + scrolled=true
#import libraries required for analysis
from change_detection import functions as chg
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from ebmdatalab import bq
from ebmdatalab import charts
from ebmdatalab import maps
from lib.outliers import *  #This is copied into the local folder from a branch ebmdatalab pandas library - it will be placed in its own repo to install at a later dat
# -

opioids_class = chg.ChangeDetection('practice_data_opioid%',
                                    measure=True,
                                    direction='down',
                                    overwrite=False,
                                    verbose=False,
                                    draw_figures='no')
opioids_class.run()

opioids = opioids_class.concatenate_outputs()
opioids.head()

# ## Total OME

filtered_sparkline(opioids,
                   'practice_data_opioid/practice_data_opioidome',
                   'practice_data_opioidome')

practice_data_opioidome = opioids.loc["practice_data_opioidome"]

practice_data_opioidspercent = opioids.loc["practice_data_opioidspercent"]

practice_data_opioidper1000 = opioids.loc["practice_data_opioidper1000"]

practice_data_opioidome.index.nunique() #count of number of practices

practice_data_opioidome = practice_data_opioidome.replace([np.inf, -np.inf], np.nan) #replace infinite values https://stackoverflow.com/questions/17477979/dropping-infinite-values-from-dataframes-in-pandas
practice_data_opioidome.head()

decile_ome = pd.read_csv(r'data/practice_data_opioid/practice_data_opioidome/bq_cache.csv') ##why can't it find file if shortened url?
decile_ome['calc_value'] = decile_ome['numerator'] / decile_ome['denominator']
decile_ome['month'] = pd.to_datetime(decile_ome['month'])
decile_ome.head()

# +
charts.deciles_chart(
        decile_ome,
        period_column='month',
        column='calc_value',
        title="omes",
        ylabel="n",
        show_outer_percentiles=False,
        show_legend=True
)
plt.show()
# -


from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import seaborn as sns

offset_date = practice_data_opioidome['is.tfirst.big'] -1
offset_date = offset_date.dropna().apply(lambda x: relativedelta(months=x))
practice_breaks_ome = decile_ome['month'].min() + offset_date
#practice_breaks_cer.loc[practice_breaks_cer=='2013-03-01'] = practice_breaks_cer.loc[practice_breaks_cer=='2013-03-01'] + pd.DateOffset(days=1)
practice_breaks_ome.head()

mean_slope = practice_data_opioidome[['is.tfirst.big','is.slope.ma']]
mean_slope = mean_slope.groupby('is.tfirst.big').mean()
mean_slope = pd.concat([mean_slope,pd.DataFrame([[0]], columns=['is.slope.ma'])],axis=0)
mean_slope = mean_slope.sort_index()
mean_slope.head()#.plot.bar()

# +
mean_change = practice_data_opioidome[['is.tfirst.big','is.intlev.levd']]
mean_change = mean_change.groupby('is.tfirst.big').mean()
mean_change = pd.concat([mean_change,pd.DataFrame([[0]], columns=['is.intlev.levd'])],axis=0)
mean_change = mean_change.sort_index()
mean_change.head()#.plot.bar()


# +
# Plot figure with subplots of different sizes
fig,ax = plt.subplots(1)
# set up subplot grid
gridspec.GridSpec(7,4)

# decile subplot

ax = plt.subplot2grid((7,4), (3,0), colspan=4, rowspan=3)
charts.deciles_chart(
        decile_ome,
        period_column='month',
        column='calc_value',
        title="Total Oral Orphine Equivalence (OMEs) by practice ",
        ylabel=" (OME) ",
        show_outer_percentiles=True,
        show_legend=True,
        ax=ax
)
#ax.set_title('Practice deciles and extreme percentiles:',loc='left',fontweight='bold')
#ax.set_ylabel('Proportion of Cerazette prescribing')
#ax.set_xlim([practice_deciles_cer.index.min(),practice_deciles_cer.index.max()])
#ax.set_xlabel('Year', fontsize = 11)
#ax.set_ylim([0,1])



#ax.axvline(x='2012-12-01',linewidth=1, color='k')
#ax.axvline(x='2013-07-01',linewidth=1, color='k')
#ax.annotate('Cerazette patent expired', ('2012-12-08',0.65),
 #           fontweight='bold',rotation=90,fontsize=14,color='#2a72a3',alpha=.9)
#ax.annotate('Price begins to drop', ('2013-07-08',0.53),
 #           fontweight='bold',rotation=90,fontsize=14,color='#2a72a3',alpha=.9)

# timing of change
ax = plt.subplot2grid((7,4), (0,0), colspan=4)
ax.set_title('Timing of largest detected changes:',loc='left',fontweight='bold')
ax.set_ylabel('Number of practices')
ax.axes.xaxis.set_ticklabels([])
ax.set_xlim([decile_ome['month'].min(),decile_ome['month'].max()])
ax.set_xticks([])
ax.hist(practice_breaks_ome, bins=64)
#ax.axvline(x='2012-12-01',linewidth=1, color='k')
#ax.axvline(x='2013-07-01',linewidth=1, color='k')

# gradient of change
ax = plt.subplot2grid((7,4), (1,0), colspan=4)
ax.set_title('Mean gradient of detected changes:',loc='left',fontweight='bold')
ax.set_ylabel('Mean gradient')
ax.axes.xaxis.set_visible(False)
#ax.set_ylim([-0.25,0])
mean_slope.plot.bar(ax=ax, width=1, color = 'r',alpha=.6)
#ax.axvline(x=28,linewidth=1, color='k') commented out put used to put a time pint line in
#ax.axvline(x=35,linewidth=1, color='k')
ax.autoscale(enable=True, axis='x', tight=True)
ax.legend_.remove()

# magnitude of change
ax = plt.subplot2grid((7,4), (2,0), colspan=4)
ax.set_title('Mean size of detected changes:',loc='left',fontweight='bold')
ax.set_ylabel('Mean change')
ax.axes.xaxis.set_visible(False)
mean_change.plot.bar(ax=ax, width=1, color = 'g',alpha=.6)
#ax.axvline(x=28,linewidth=1, color='k')
#ax.axvline(x=35,linewidth=1, color='k')
ax.autoscale(enable=True, axis='x', tight=True)
ax.legend_.remove()

# fit subplots and save fig
fig.set_size_inches(w=12,h=14)
fig.savefig('data/practice_data_opioid/ome.png',
            format='png', dpi=300,bbox_inches='tight')
# -

# ## High dose opioids per 1000 patients

# [High dose opioids per 1000 patients](https://openprescribing.net/measure/opioidper1000/)

filtered_sparkline(opioids,
                   'practice_data_opioid/practice_data_opioidper1000',
                   'practice_data_opioidper1000')

# +
practice_data_opioidspercent = practice_data_opioidspercent.replace([np.inf, -np.inf], np.nan) #replace infinite values https://stackoverflow.com/questions/17477979/dropping-infinite-values-from-dataframes-in-pandas
# -


decile_highdose = pd.read_csv('data/practice_data_opioid/practice_data_opioidspercent/bq_cache.csv') ##why can't it find file if shortened url?
decile_highdose['calc_value'] = decile_highdose['numerator'] / decile_highdose['denominator']
decile_highdose['month'] = pd.to_datetime(decile_highdose['month'])
decile_highdose.head()

# +
charts.deciles_chart(
        decile_highdose,
        period_column='month',
        column='calc_value',
        title="High Dose Opioids",
        ylabel=" % ",
        show_outer_percentiles=False,
        show_legend=True
)


plt.show()
# -

from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import seaborn as sns

offset_date = practice_data_opioidspercent['is.tfirst.big'] -1
offset_date = offset_date.dropna().apply(lambda x: relativedelta(months=x))
practice_breaks_highdose = decile_highdose['month'].min() + offset_date
#practice_breaks_cer.loc[practice_breaks_cer=='2013-03-01'] = practice_breaks_cer.loc[practice_breaks_cer=='2013-03-01'] + pd.DateOffset(days=1)
practice_breaks_highdose.head()

mean_slope_hdose = practice_data_opioidspercent[['is.tfirst.big','is.slope.ma']]
mean_slope_hdose = mean_slope_hdose.groupby('is.tfirst.big').mean()
mean_slope_hdose = pd.concat([mean_slope_hdose,pd.DataFrame([[0]], columns=['is.slope.ma'])],axis=0)
mean_slope_hdose = mean_slope_hdose.sort_index()
mean_slope_hdose.head()#.plot.bar()

mean_change_hdose = practice_data_opioidspercent[['is.tfirst.big','is.intlev.levd']]
mean_change_hdose = mean_change_hdose.groupby('is.tfirst.big').mean()
mean_change_hdose = pd.concat([mean_change_hdose,pd.DataFrame([[0]], columns=['is.intlev.levd'])],axis=0)
mean_change_hdose = mean_change_hdose.sort_index()
mean_change_hdose.head()#.plot.bar()

# +
# Plot figure with subplots of different sizes
fig,ax = plt.subplots(1)
# set up subplot grid
gridspec.GridSpec(7,4)

# decile subplot

ax = plt.subplot2grid((7,4), (3,0), colspan=4, rowspan=3)
charts.deciles_chart(
        decile_highdose,
        period_column='month',
        column='calc_value',
        title=" High Dose Opioids ",
        ylabel=" % ",
        show_outer_percentiles=True,
        show_legend=True,
        ax=ax
)
#ax.set_title('Practice deciles and extreme percentiles:',loc='left',fontweight='bold')
#ax.set_ylabel('Proportion of Cerazette prescribing')
#ax.set_xlim([practice_deciles_cer.index.min(),practice_deciles_cer.index.max()])
#ax.set_xlabel('Year', fontsize = 11)
#ax.set_ylim([0,1])



#ax.axvline(x='2012-12-01',linewidth=1, color='k')
#ax.axvline(x='2013-07-01',linewidth=1, color='k')
#ax.annotate('Cerazette patent expired', ('2012-12-08',0.65),
 #           fontweight='bold',rotation=90,fontsize=14,color='#2a72a3',alpha=.9)
#ax.annotate('Price begins to drop', ('2013-07-08',0.53),
 #           fontweight='bold',rotation=90,fontsize=14,color='#2a72a3',alpha=.9)

# timing of change
ax = plt.subplot2grid((7,4), (0,0), colspan=4)
ax.set_title('Timing of largest detected changes:',loc='left',fontweight='bold')
ax.set_ylabel('Number of practices')
ax.axes.xaxis.set_ticklabels([])
ax.set_xlim([decile_highdose['month'].min(),decile_highdose['month'].max()])
ax.set_xticks([])
ax.hist(practice_breaks_highdose, bins=64)
#ax.axvline(x='2012-12-01',linewidth=1, color='k')
#ax.axvline(x='2013-07-01',linewidth=1, color='k')

# gradient of change
ax = plt.subplot2grid((7,4), (1,0), colspan=4)
ax.set_title('Mean gradient of detected changes:',loc='left',fontweight='bold')
ax.set_ylabel('Mean gradient')
ax.axes.xaxis.set_visible(False)
#ax.set_ylim([-0.25,0])
mean_slope_hdose.plot.bar(ax=ax, width=1, color = 'r',alpha=.6)
#ax.axvline(x=28,linewidth=1, color='k') commented out put used to put a time pint line in
#ax.axvline(x=35,linewidth=1, color='k')
ax.autoscale(enable=True, axis='x', tight=True)
ax.legend_.remove()

# magnitude of change
ax = plt.subplot2grid((7,4), (2,0), colspan=4)
ax.set_title('Mean size of detected changes:',loc='left',fontweight='bold')
ax.set_ylabel('Mean change')
ax.axes.xaxis.set_visible(False)
mean_change_hdose.plot.bar(ax=ax, width=1, color = 'g',alpha=.6)
#ax.axvline(x=28,linewidth=1, color='k')
#ax.axvline(x=35,linewidth=1, color='k')
ax.autoscale(enable=True, axis='x', tight=True)
ax.legend_.remove()

# fit subplots and save fig
fig.set_size_inches(w=12,h=14)
fig.savefig('data/practice_data_opioid/ome.png',
            format='png', dpi=300,bbox_inches='tight')
