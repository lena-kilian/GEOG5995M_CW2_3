
import pandas
from matplotlib import pyplot


cba_rgn = pandas.read_csv('cba_rgn.csv', sep = '\t').set_index('Unnamed: 0').sort_index(axis=0, ascending=True).sort_index(axis=1, ascending=True)

wdi_rgn_gdp = pandas.read_csv('wdi_rgn_gdp', sep = '\t').set_index('year').sort_index(axis=0, ascending=True).sort_index(axis=1, ascending=True)



fig = pyplot.figure(figsize=(8, 8))
k = []
def update_graph(frame_number):
    fig.clear()
    pyplot.ylim(0, 60000)
    pyplot.xlim(0, 27)
    pyplot.xlabel("CBA (CO2 Mt/capita)")
    pyplot.ylabel("GDP per capita (current US$)")
    pyplot.title('Year: ' + str(cba_rgn.index[len(k)]))
    pyplot.legend()
    for i in range(len(cba_rgn.columns)):
        pyplot.scatter(cba_rgn.iloc[len(k)][i], wdi_rgn_gdp.iloc[len(k)][i], s=20)
    k.append(1)
    

from matplotlib import animation
animation = animation.FuncAnimation(fig, update_graph, frames = len(cba_rgn), repeat=False)

'''
If I do it by country I can divide the colours into regions?

Then I will also add some correlations.

Could also find a way to select countries and then make chart for individual countries? --> maybe too much
'''