import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager

# Add the specific font files to Matplotlib's font manager
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


# Volatile Organic Contaminants Bar Chart

N = 2

level_found = (57.1, 22.58)
mcl = (80, 60)
ind = np.arange(N)   
width = 0.35  

fig, ax = plt.subplots(figsize=(10, 7))

# Draw standard bars, which will not have rounded corners but will not cause an error.
p1 = ax.bar(ind - width/2, level_found, width, label='Levels Found', color='#367588')
p2 = ax.bar(ind + width/2, mcl, width, label='Maximum Contaminant Level (MCL)', color= '#2f4f4f')


ax.set_ylabel('Levels Found (PPB)', fontproperties=thin_prop)
ax.set_title('Volatile Organic Elements in Drinking Water', fontproperties=bold_prop)
ax.set_xticks(ind)
ax.set_xticklabels(('Trihalomethanes', 'Haloacetic Acids'), fontproperties=thin_prop)
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