import pandas
import class_framework
from matplotlib import pyplot
from matplotlib import animation
from matplotlib.lines import Line2D
from scipy.stats import pearsonr


cba_rgn = pandas.read_csv('cba_rgn.csv', sep = '\t').set_index('Unnamed: 0').sort_index(axis=0, ascending=True).sort_index(axis=1, ascending=True).T

wdi_rgn_gdp = pandas.read_csv('wdi_rgn_gdp.csv', sep = '\t').set_index('year').sort_index(axis=0, ascending=True).sort_index(axis=1, ascending=True).T

rgn_list = cba_rgn.index.tolist()

cba_list = []
for i in range(len(cba_rgn)):
    cba_list.append(cba_rgn.iloc[i].values.tolist())
    
wdi_list = []
for i in range(len(wdi_rgn_gdp)):
    wdi_list.append(wdi_rgn_gdp.iloc[i].values.tolist())
    
year_list = cba_rgn.columns.values.tolist()

countries = []
for i in range(len(cba_list)):
    countries.append(class_framework.Countries(rgn_list[i], rgn_list[i], year_list, cba_list[i], wdi_list[i], countries))

cols = countries[0].make_colours()

for i in range(len(countries)):
    countries[i].assign_colours(cols) 


'''
make animation
'''

legend_elements = []   
for i in range(len(cols[0])):
    legend_elements.append(Line2D([0], [0], marker = 'o', color = 'w', label = cols[0][i], markerfacecolor = cols[1][i], markersize=10))

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

'''
correlation
'''

cor_list = []
p_list = []
country_list = []
for i in range(len(cba_rgn)):
    cor_list.append(pearsonr(cba_rgn.iloc[i].tolist(), wdi_rgn_gdp.iloc[i].tolist())[0])
    p_list.append(pearsonr(cba_rgn.iloc[i].tolist(), wdi_rgn_gdp.iloc[i].tolist())[1])
    country_list.append(cba_rgn.index[i])

cor_data = pandas.DataFrame({'country': country_list, 'pearson_correlation': cor_list, 'p-value': p_list}).sort_values(by = ['pearson_correlation'])
       
for i in range(len(cor_data)):
    if cor_data['p-value'][i] < 0.001:
        cor_data['significance'] = '***'
    elif cor_data['p-value'][i] < 0.01:
        cor_data['significance'] = '**'
    elif cor_data['p-value'][i] < 0.05:
        cor_data['significance'] = '*'

pyplot.scatter(cor_data['country'], cor_data['pearson_correlation'])
pyplot.xlabel("Country")
pyplot.ylabel("Correlation Coefficient (Pearson's r)")