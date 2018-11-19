
import pandas
from matplotlib import pyplot
from matplotlib import animation


cba_rgn = pandas.read_csv('cba_rgn.csv', sep = '\t').set_index('Unnamed: 0').sort_index(axis=0, ascending=True).sort_index(axis=1, ascending=True)

wdi_rgn_gdp = pandas.read_csv('wdi_rgn_gdp.csv', sep = '\t').set_index('year').sort_index(axis=0, ascending=True).sort_index(axis=1, ascending=True)


'''
Putting both in one table model:
'''

cba_rgn_T = pandas.read_csv('cba_rgn_T.csv', sep = '\t').set_index('region_code').sort_index(axis=0, ascending=True).sort_index(axis=1, ascending=True)
cba_rgn_T['def'] = str('cba')

wdi_rgn_gdp_T = pandas.read_csv('wdi_rgn_gdp_T.csv', sep = '\t').set_index('country_code_wdi').sort_index(axis=0, ascending=True).sort_index(axis=1, ascending=True)
wdi_rgn_gdp_T['def'] = str('wdi')

all_data = cba_rgn_T.append(wdi_rgn_gdp_T).sort_index(axis = 0, ascending = True).sort_values(by = ['def'])


fig = pyplot.figure(figsize=(8, 8))
k = []
plot_color = ["#27ae61", "#f1c40f", "#e77e23", "#2a80b9", "#34495e", "#e84c3d", "#7e8c8d"]
              
def update_graph(frame_number):
    fig.clear()
    pyplot.ylim(0, 60000)
    pyplot.xlim(0, 27)
    pyplot.xlabel("CBA (CO2 Mt/capita)")
    pyplot.ylabel("GDP per capita (current US$)")
    pyplot.title('Year: ' + str(all_data.columns[len(k)]))
    for i in range(int((len(all_data)) /2)):
            pyplot.scatter(all_data.iloc[i][len(k)], all_data.iloc[i + int((len(all_data)) /2)][len(k)], color = plot_color[i], s=20)
            pyplot.legend(all_data.index[0: int((len(all_data)) /2)], loc = 2)
    if len(k) < (len(all_data.columns) - 2):
        k.append(1)
    

animation = animation.FuncAnimation(fig, update_graph, frames = (len(all_data.columns) - 1), repeat=False)