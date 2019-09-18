import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Bad subjects
exclude = [4, 10]

# Import the data
PSC_fname = 'ROI_percent_signal_change.csv'
FIR_fname = 'ROI_BOLD_FIR_signals.csv'
pscdf, firdf = pd.read_csv(PSC_fname), pd.read_csv(FIR_fname)

# Calculate a 'time' column from the TR
firdf['time'] = firdf['TR'] * 2.5

# Exclude bad subjects
pscdf = pscdf[~pscdf['subject'].isin(exclude)]
firdf = firdf[~firdf['subject'].isin(exclude)]

# Regions
psc_regions = pscdf['region'].unique()
fir_regions = firdf['region'].unique()

# Plot % SC
fig, ax = plt.subplots(4,6)
pal = 'Set1'

for i, axis in enumerate(ax.flatten()):
    if i > len(psc_regions)-1:
        continue
    
    df = pscdf[pscdf['region']==psc_regions[i]]
    sns.barplot(x='condition', y='signal_change', data=df, palette=pal, ax=axis)
    axis.set_title(psc_regions[i])
    
plt.tight_layout(pad=-0.5)
sns.despine()
fig.delaxes(axis)
plt.show()

# Plot FIR
fig, ax = plt.subplots(4,6)
pal = 'Set1'

for i, axis in enumerate(ax.flatten()):
    if i > len(fir_regions)-1:
        continue
    
    df = firdf[firdf['region']==fir_regions[i]]
    sns.lineplot(x='time', y='y', hue='condition', data=df, palette=pal, ax=axis)
    axis.set_title(fir_regions[i])
    if i < len(fir_regions)-1:
        axis.get_legend().remove()

plt.tight_layout(pad=-0.5)
fig.delaxes(axis)
sns.despine()
plt.show()



