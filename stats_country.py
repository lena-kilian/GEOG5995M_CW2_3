import pandas
from matplotlib import pyplot
from scipy.stats import pearsonr

'''
ADD DESCRIPTIVES, CHECK NORMALITY --> will probably have to use spearman's rho
'''
'''
load data
'''

country_data = pandas.read_csv('country_data.csv', sep = '\t').set_index('Unnamed: 0').sort_index(axis=1, ascending=True).sort_values(by = ['code', 'country_list'], ascending=True)

'''
make lists and countries in class 
'''
    
year_list = country_data.drop(['code', 'country_list', 'region_code'], axis = 1).columns.values.tolist()

'''
correlations by year
'''

cor_data = country_data[country_data.code == 'wdi'].drop(['code', 'region_code', 'country_list'], axis = 1).add_prefix('wdi_').join(country_data[country_data.code == 'cba'].drop(['code', 'region_code', 'country_list'], axis = 1).add_prefix('cba_'), rsuffix = '_cba', lsuffix = '_wdi').dropna().sort_index(axis = 1).T
  
cor_list = []
p_list = []
for i in range(len(year_list)):
    cor_list.append(pearsonr(cor_data.iloc[i].tolist(), cor_data.iloc[i + len(year_list)].tolist())[0])
    p_list.append(pearsonr(cor_data.iloc[i].tolist(), cor_data.iloc[i + len(year_list)].tolist())[1])

cor_data_year = pandas.DataFrame({'year': year_list, 'pearson_correlation': cor_list, 'p-value': p_list})
cor_data_year['year'] = cor_data_year['year'].astype('int')
       
for i in range(len(cor_data_year)):
    if cor_data_year['p-value'][i] < 0.001:
        cor_data_year['significance'] = '***'
    elif cor_data_year['p-value'][i] < 0.01:
        cor_data_year['significance'] = '**'
    elif cor_data_year['p-value'][i] < 0.05:
        cor_data_year['significance'] = '*'

pyplot.scatter(cor_data_year['year'], cor_data_year['pearson_correlation'])
pyplot.plot(cor_data_year['year'], cor_data_year['pearson_correlation'], color = 'black')
pyplot.xlabel("Year")
pyplot.ylabel("Correlation Coefficient (Pearson's r)")

print(cor_data_year)

'''
correlations by country
'''
cor_data_country = cor_data.T.reset_index().rename(columns = {'Unnamed: 0':'index'})
wdi_data = cor_data_country[['index']].set_index('index').join(country_data[country_data.code == 'wdi'].drop(['code', 'region_code', 'country_list'], axis = 1)).T.add_prefix('wdi_')
cba_data =cor_data_country[['index']].set_index('index').join(country_data[country_data.code == 'cba'].drop(['code', 'region_code', 'country_list'], axis = 1)).T.add_prefix('cba_')

cor_data_country = wdi_data.join(cba_data).T.sort_index(axis = 0)

cor_list = []
p_list = []
country_list = []

for i in range(int(len(cor_data_country) / 2)):
    cor_list.append(pearsonr(cor_data_country.iloc[i].tolist(), cor_data_country.iloc[i + len(year_list)].tolist())[0])
    p_list.append(pearsonr(cor_data_country.iloc[i].tolist(), cor_data_country.iloc[i + len(year_list)].tolist())[1])
    country_list.append(cor_data_country.index[i])

cor_data_country = pandas.DataFrame({'country': country_list, 'pearson_correlation': cor_list, 'p-value': p_list})
cor_data_country['country'] = cor_data_country['country'].str.replace('cba_', '')
       
for i in range(len(cor_data_country)):
    if cor_data_country['p-value'][i] < 0.001:
        cor_data_country['significance'] = '***'
    elif cor_data_country['p-value'][i] < 0.01:
        cor_data_country['significance'] = '**'
    elif cor_data_country['p-value'][i] < 0.05:
        cor_data_country['significance'] = '*'


print(cor_data_country)