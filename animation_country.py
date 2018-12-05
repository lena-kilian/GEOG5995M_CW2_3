import pandas
import class_framework
from matplotlib import pyplot
from matplotlib import animation
from matplotlib.lines import Line2D


'''
load data
'''
regions = pandas.read_csv('region_index.csv', sep = '\t').drop('short_name', axis = 1).rename(columns = {'country_code' : 'region_code'}).set_index('region_code')

country_filter = pandas.read_csv('country_filter.csv', sep = '\t')
country_filter['country'] = country_filter['country'].astype(str)
country_filter = country_filter.set_index('country')

country_dat = pandas.read_csv('country_data.csv', sep = '\t').set_index('Unnamed: 0').sort_index(axis=1, ascending=True).sort_values(by = ['code', 'country_list'], ascending=True)
   

'''
make lists and countries in class 
'''

rgn_list = []
for i in range(2):
    rgn_list.append(country_dat[(country_dat['code'] == 'cba')].reset_index().filter(['Unnamed: 0', 'region_code']).T.iloc[i].values.tolist())

cba_list = []
wdi_list = []
for i in range(len(country_dat)):
    if country_dat['code'][i] == 'cba':
        cba_list.append(country_dat.drop(['code', 'country_list', 'region_code'], axis = 1).iloc[i].values.tolist())
    elif country_dat['code'][i] == 'wdi':
        wdi_list.append(country_dat.drop(['code', 'country_list', 'region_code'], axis = 1).iloc[i].values.tolist())
    
year_list = country_dat.drop(['code', 'country_list', 'region_code'], axis = 1).columns.values.tolist()

countries = []

for i in range(len(cba_list)):
    countries.append(class_framework.Countries(rgn_list[0][i], rgn_list[1][i], year_list, cba_list[i], wdi_list[i], countries))

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
    pyplot.ylim(0, 60000)
    pyplot.xlim(0, 27)
    pyplot.xlabel("CBA (CO2 Mt/capita)")
    pyplot.ylabel("GDP per capita (current US$)")
    pyplot.title('Year: ' + str(year_list[len(k)]))
    for i in range(len(countries)):
        pyplot.scatter(countries[i].cba[len(k)], countries[i].wdi[len(k)], color = countries[i].colour, s=20)
    pyplot.legend(handles = legend_elements, loc = 2)
    if len(k) < (len(year_list)):
        k.append(1)

animation = animation.FuncAnimation(fig, update_graph, frames = (len(year_list)), repeat=False)