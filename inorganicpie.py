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

#Define Inorganic Data
copper = 0.1369
lead = 1.4900
barium = 0.0160
fluoride = 0.8900
nitrate = 1.9000

data = np.array([copper, lead, barium, fluoride, nitrate])
total_sum = np.sum(data)

# Calculate percentage for each element
percentage_copper = (copper / total_sum) * 100
percentage_lead = (lead / total_sum) * 100
percentage_barium = (barium / total_sum) * 100
percentage_fluoride = (fluoride / total_sum) * 100
percentage_nitrate = (nitrate / total_sum) * 100

# Pie chart configuration
labels = ['Copper', 'Lead', 'Barium', 'Fluoride', 'Nitrate']
sizes = [percentage_copper, percentage_lead, percentage_barium, percentage_fluoride, percentage_nitrate]
colors = ['#5d8aa8','#367588','#2f4f4f','#264348','#004242']
explode = (0, 0, 0, 0, 0.025)  

# Pie Chart
y = np.array(sizes)

plt.axis('equal')
plt.title('Inorganic Contaminants in Drinking Water', fontproperties=bold_prop)
plt.pie(y, labels=labels, colors=colors, explode=explode, startangle=90, textprops={'fontproperties': thin_prop})
plt.show()

for text in plt.gca().texts:
    text.set_fontproperties(thin_prop)
    text.set_text(text.get_text().capitalize())