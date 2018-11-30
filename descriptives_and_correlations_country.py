import pandas
from matplotlib import pyplot
from scipy.stats import pearsonr

'''
load data
'''

country_dat = pandas.read_csv('country_data.csv', sep = '\t').set_index('Unnamed: 0').sort_index(axis=1, ascending=True).sort_values(by = ['code', 'country_list'], ascending=True)
   

'''
make lists and countries in class 
'''
    
year_list = country_dat.drop(['code', 'country_list', 'region_code'], axis = 1).columns.values.tolist()

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

cor_dat2 = cor_dat.T.reset_index().rename(columns = {'Unnamed: 0':'index'})
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
