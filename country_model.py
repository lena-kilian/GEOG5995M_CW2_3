'''
Then I will also add some correlations.

Could also find a way to select countries and then make chart for individual countries? --> maybe too much
--> if I can add the country name to the class index then this could be solved!!!
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


regions = pandas.read_csv('region_index.csv', sep = '\t').drop('short_name', axis = 1).rename(columns = {'country_code' : 'region_code'}).set_index('region_code')
regions['colour_code'] = str('colour')

for i in range(len(regions)):  
    regions['colour_code'][i] = pc2['a'][i]
    
    
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

country_dat = country_filter.join(country_data_all).join(country_index).join(regions, on = 'region_code').sort_index(axis=1, ascending=True).sort_values(by = ['code', 'country_list'], ascending=True)

legend_elements = []   
for j in range(len(regions)):
    legend_elements.append(Line2D([0], [0], marker = 'o', color = 'w', label = regions.index[j], markerfacecolor = regions['colour_code'][j], markersize=10))

fig = pyplot.figure(figsize=(8, 8))
k = []

def update_graph(frame_number):
    fig.clear()
    pyplot.ylim(0, 130000)
    pyplot.xlim(0, 40)
    pyplot.xlabel("CBA (CO2 Mt/capita)")
    pyplot.ylabel("GDP per capita (current US$)")
    pyplot.title('Year: ' + str(country_dat.columns[len(k)]))

    for i in range(int((len(country_dat)) /2)):
        pyplot.scatter(country_dat.iloc[i][len(k)], country_dat.iloc[i + int((len(country_dat)) /2)][len(k)], color = country_dat['colour_code'][i], s=20)

    pyplot.legend(handles = legend_elements, loc = 2) #, bbox_to_anchor=(0, 1))
    if len(k) < (len(country_dat.columns) - 5):
        k.append(1)
    

animation = animation.FuncAnimation(fig, update_graph, frames = (len(country_dat.columns)-2), repeat=False)


from scipy.stats.stats import pearsonr

