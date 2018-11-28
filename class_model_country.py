import pandas
import class_framework
from matplotlib import pyplot
from matplotlib import animation
from matplotlib.lines import Line2D
from scipy.stats import pearsonr


'''
load data
'''
regions = pandas.read_csv('region_index.csv', sep = '\t').drop('short_name', axis = 1).rename(columns = {'country_code' : 'region_code'}).set_index('region_code')

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
   

'''
make lists and countries in class 
'''

country_dat[(country_dat['code'] == 'cba')].reset_index()['index'].tolist()

rgn_list = []
for i in range(2):
    rgn_list.append(country_dat[(country_dat['code'] == 'cba')].reset_index().filter(['index', 'region_code']).T.iloc[i].values.tolist())

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


'''
correlations by year
'''

cor_dat = country_dat[country_dat.code == 'wdi'].drop(['code', 'region_code', 'country_list'], axis = 1).add_prefix('wdi_').join(country_dat[country_dat.code == 'cba'].drop(['code', 'region_code', 'country_list'], axis = 1).add_prefix('cba_'), rsuffix = '_cba', lsuffix = '_wdi').dropna().sort_index(axis = 1).T
      
cor_list = []
p_list = []
for i in range(len(year_list)):
    cor_list.append(pearsonr(cor_dat.iloc[i].tolist(), cor_dat.iloc[i + len(year_list)].tolist())[0])
    p_list.append(pearsonr(cor_dat.iloc[i].tolist(), cor_dat.iloc[i + len(year_list)].tolist())[1])

cor_data = pandas.DataFrame({'year': year_list, 'pearson_correlation': cor_list, 'p-value': p_list})
cor_data['year'] = cor_data['year'].astype('int')
       
for i in range(len(cor_data)):
    if cor_data['p-value'][i] < 0.001:
        cor_data['significance'] = '***'
    elif cor_data['p-value'][i] < 0.01:
        cor_data['significance'] = '**'
    elif cor_data['p-value'][i] < 0.05:
        cor_data['significance'] = '*'

pyplot.scatter(cor_data['year'], cor_data['pearson_correlation'])
pyplot.plot(cor_data['year'], cor_data['pearson_correlation'], color = 'black')
pyplot.xlabel("Year")
pyplot.ylabel("Correlation Coefficient (Pearson's r)")


'''
correlations by country
'''

cor_dat2 = cor_dat.T.reset_index() 
dat_wdi = cor_dat2[['index']].set_index('index').join(country_dat[country_dat.code == 'wdi'].drop(['code', 'region_code', 'country_list'], axis = 1)).T.add_prefix('wdi_')
dat_cba =cor_dat2[['index']].set_index('index').join(country_dat[country_dat.code == 'cba'].drop(['code', 'region_code', 'country_list'], axis = 1)).T.add_prefix('cba_')

cor_dat3 = dat_wdi.join(dat_cba).T.sort_index(axis = 0)

cor_list = []
p_list = []
country_list = []
a = int(len(cor_dat3) / 2)

for i in range(a):
    cor_list.append(pearsonr(cor_dat3.iloc[i].tolist(), cor_dat3.iloc[i + len(year_list)].tolist())[0])
    p_list.append(pearsonr(cor_dat3.iloc[i].tolist(), cor_dat3.iloc[i + len(year_list)].tolist())[1])
    country_list.append(cor_dat3.index[i])

cor_data = pandas.DataFrame({'country': country_list, 'pearson_correlation': cor_list, 'p-value': p_list}).sort_values(by = ['pearson_correlation'])
cor_data['country'] = cor_data['country'].str.replace('cba_', '')
       
for i in range(len(cor_data)):
    if cor_data['p-value'][i] < 0.001:
        cor_data['significance'] = '***'
    elif cor_data['p-value'][i] < 0.01:
        cor_data['significance'] = '**'
    elif cor_data['p-value'][i] < 0.05:
        cor_data['significance'] = '*'

'''
pyplot.scatter(cor_data['country'], cor_data['pearson_correlation'])
pyplot.plot(cor_data['country'], cor_data['pearson_correlation'], color = 'black')
pyplot.xlabel("Country")
pyplot.ylabel("Correlation Coefficient (Pearson's r)")
'''