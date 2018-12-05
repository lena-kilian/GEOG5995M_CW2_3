import pandas
import class_framework
from matplotlib import pyplot
from matplotlib import animation
from matplotlib.lines import Line2D


'''
load data

---> CHANGE COUNTRY DATA TO REMOVE ALL THE NANs IN DATA ORGANISATION FILE. WILL THEN HAVE TO ADAPT THIS!!!
'''
regions = pandas.read_csv('country_index.csv', sep = '\t').drop(['region'], axis = 1)

country_data = pandas.read_csv('country_data.csv', sep = '\t').set_index('Unnamed: 0').sort_index(axis=0, ascending=True)

regions = country_data.T.join(regions.set_index('short_name'))['region_code'].sort_index(axis=0, ascending=True).reset_index().rename(columns = {'index':'short_name'})

'''
make lists and countries in class 
'''

cba_data = country_data[(country_data.index.str.contains('cba'))].T
wdi_data = country_data[(country_data.index.str.contains('wdi'))].T

cba_list = []
wdi_list = []
for i in range(len(cba_data)):
    cba_list.append(cba_data.iloc[i].values.tolist())
    wdi_list.append(wdi_data.iloc[i].values.tolist())
    
year_list = cba_data.columns.str.replace('cba_', '').tolist()

countries = []

for i in range(len(cba_list)):
    countries.append(class_framework.Countries(regions['short_name'][i], regions['region_code'][i], year_list, cba_list[i], wdi_list[i], countries))

cols = countries[0].make_colours()

for i in range(len(countries)):
    countries[i].assign_colours(cols)
    
'''
make animation
'''

legend_elements = []   
for j in range(len(cols[0])):
    legend_elements.append(Line2D([0], [0], marker = 'o', color = 'w', label = cols[0][j], markerfacecolor = cols[1][j], markersize=10))

fig = pyplot.figure(figsize=(8, 8))
k = []      

def update_graph(frame_number):
    fig.clear()
    pyplot.ylim(0, 120000)
    pyplot.xlim(0, 60)
    pyplot.xlabel("CBA (CO2 Mt/capita)")
    pyplot.ylabel("GDP per capita (current US$)")
    pyplot.title('Year: ' + str(year_list[len(k)]))
    for i in range(len(countries)):
        pyplot.scatter(countries[i].cba[len(k)], countries[i].wdi[len(k)], color = countries[i].colour, s=20)
    pyplot.legend(handles = legend_elements, loc = 2)
    if len(k) < (len(year_list)):
        k.append(1)

animation = animation.FuncAnimation(fig, update_graph, frames = (len(year_list)), repeat=False)