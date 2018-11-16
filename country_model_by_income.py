'''
If I do it by country I can divide the colours into regions?

Then I will also add some correlations.

Could also find a way to select countries and then make chart for individual countries? --> maybe too much
'''

import pandas
from matplotlib import pyplot
from matplotlib import animation
from matplotlib.lines import Line2D


'''
make colours --> maybe automate this to make a certain number of colours? could turn this into a function
'''

plot_colour = ["#27ae61", "#f1c40f", "#e77e23", "#2a80b9", "#34495e", "#e84c3d", "#7e8c8d"]
pc2 = pandas.DataFrame(plot_colour, columns = list('a'))


income_filter = pandas.read_csv('income_filter.csv', sep = '\t').drop(['country_code', 'region'], axis = 1).set_index('short_name')

income_legend = income_filter.reset_index().drop('short_name', axis = 1).drop_duplicates().set_index('income_group')
income_legend['colour_code'] = str('colour')

for i in range(len(income_legend)):  
    income_legend['colour_code'][i] = pc2['a'][i]
    
income_filter = income_filter.join(income_legend, on = 'income_group')
    
    
"""
step 1: turn country data into one file, which has regions in it, but also only has overlapping countries!!! (do an inner join)
"""


country_data_all = pandas.read_csv('cba_wdi_country.csv', sep = '\t')
country_data_all['Unnamed: 0'] = country_data_all['Unnamed: 0'].astype(str)
country_data_all = country_data_all.set_index('Unnamed: 0')
country_data_all['code'] = country_data_all['code'].astype(str)

country_filter = pandas.read_csv('country_filter.csv', sep = '\t')
country_filter['country'] = country_filter['country'].astype(str)
country_filter = country_filter.set_index('country').drop(['code_cba', 'code_wdi'], axis = 1)
country_filter['country_list'] = country_filter.index.astype(str)

country_index = pandas.read_csv('county_index.csv', sep = '\t').set_index('short_name').drop('region', axis = 1)

country_dat = country_filter.join(country_data_all).join(country_index).join(income_filter).sort_index(axis=1, ascending=True).sort_values(by = ['code', 'country_list'], ascending=True)

legend_elements = []
for j in range(len(income_legend)):
    legend_elements.append(Line2D([0], [0], marker = 'o', color = 'w', label = income_legend.index[j], markerfacecolor = income_legend['colour_code'][j], markersize=10))

fig = pyplot.figure(figsize=(8, 8))
k = []

def update_graph(frame_number):
    fig.clear()
    pyplot.ylim(0, 130000)
    pyplot.xlim(0, 60)
    pyplot.xlabel("CBA (CO2 Mt/capita)")
    pyplot.ylabel("GDP per capita (current US$)")
    pyplot.title('Year: ' + str(country_dat.columns[len(k)]))

    for i in range(int((len(country_dat)) /2)):
        pyplot.scatter(country_dat.iloc[i][len(k)], country_dat.iloc[i + int((len(country_dat)) /2)][len(k)], color = country_dat['colour_code'][i], s=20)

    pyplot.legend(handles = legend_elements, loc = 2) #, bbox_to_anchor=(0, 1))
    if len(k) < (len(country_dat.columns) - 6):
        k.append(1)
    

animation = animation.FuncAnimation(fig, update_graph, frames = (len(country_dat.columns)-2), repeat=False)