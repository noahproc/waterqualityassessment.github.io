import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager

thin_font_path = '/Users/noahproctor/Library/Fonts/Lato-Thin.ttf'
bold_font_path = '/Users/noahproctor/Library/Fonts/Lato-Bold.ttf'
font_manager.fontManager.addfont(thin_font_path)
font_manager.fontManager.addfont(bold_font_path)

# Set the font properties
thin_prop = font_manager.FontProperties(fname=thin_font_path)
bold_prop = font_manager.FontProperties(fname=bold_font_path)

# Set global text and tick color
plt.rcParams['text.color'] = 'black'
plt.rcParams['axes.labelcolor'] = 'black'
plt.rcParams['xtick.color'] = 'black'
plt.rcParams['ytick.color'] = 'black'


# Miscellaneous Contaminants Bar Chart

N = 5

level_found = (0.1369, 1.4900, 0.0160, 0.8900, 1.9000)
mcl = (1.3, 15.0, 2.0, 4.0, 10.0)
ind = np.arange(N)   
width = 0.35  

fig, ax = plt.subplots(figsize=(10, 7))

p1 = ax.bar(ind - width/2, level_found, width, label='Levels Found', color='#367588')
p2 = ax.bar(ind + width/2, mcl, width, label='Maximum Contaminant Level (MCL)', color= '#2f4f4f')


ax.set_ylabel('Levels Found (PPM)', fontproperties=thin_prop)
ax.set_title('Inorganic Contaminants in Drinking Water', fontproperties=bold_prop)
ax.set_xticks(ind)
ax.set_xticklabels(('Copper', 'Lead', 'Barium', 'Fluoride', 'Nitrate'), fontproperties=thin_prop)
ax.legend(prop=thin_prop)

# Set tick label properties
for label in ax.get_yticklabels():
    label.set_fontproperties(thin_prop)
for label in ax.get_xticklabels():
    label.set_fontproperties(thin_prop)

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.show()
