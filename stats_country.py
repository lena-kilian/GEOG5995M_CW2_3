import pandas
from matplotlib import pyplot
from scipy.stats import shapiro
from scipy.stats import spearmanr

'''
ADD DESCRIPTIVES, CHECK NORMALITY --> will probably have to use spearman's rho
'''
'''
load data
'''

cor_data = pandas.read_csv('country_data.csv', sep = '\t').set_index('Unnamed: 0').sort_index(axis=1, ascending=True)

wdi_data = cor_data[(cor_data.index.str.contains('wdi'))].T

cba_data = cor_data[(cor_data.index.str.contains('cba'))].T

norm_test_country = pandas.DataFrame(index = cba_data.index, columns = ['cba_sw', 'cba_p', 'wdi_sw', 'wdi_p', 'normal_dist'])

for i in range(len(cba_data)):
    norm_test_country['cba_sw'][i] = shapiro(cba_data.iloc[i])[0]
    norm_test_country['cba_p'][i] = shapiro(cba_data.iloc[i])[1]
    norm_test_country['wdi_sw'][i] = shapiro(wdi_data.iloc[i])[0]
    norm_test_country['wdi_p'][i] = shapiro(wdi_data.iloc[i])[1]
    if norm_test_country['cba_p'][i] > 0.05 and norm_test_country['wdi_p'][i] > 0.05:
        norm_test_country['normal_dist'][i] = 'Yes'
    else:
        norm_test_country['normal_dist'][i] = 'No'   

norm_test_year = pandas.DataFrame(index = cba_data.T.index, columns = ['cba_sw', 'cba_p', 'wdi_sw', 'wdi_p', 'normal_dist'])

for i in range(len(cba_data.T)):
    norm_test_year['cba_sw'][i] = shapiro(cba_data.T.iloc[i])[0]
    norm_test_year['cba_p'][i] = shapiro(cba_data.T.iloc[i])[1]
    norm_test_year['wdi_sw'][i] = shapiro(wdi_data.T.iloc[i])[0]
    norm_test_year['wdi_p'][i] = shapiro(wdi_data.T.iloc[i])[1]
    if norm_test_year['cba_p'][i] > 0.05 and norm_test_year['wdi_p'][i] > 0.05:
        norm_test_year['normal_dist'][i] = 'Yes'
    else:
        norm_test_year['normal_dist'][i] = 'No'   

'''
make lists and countries in class 
'''
    
year_list = cba_data.columns.str.replace('cba_', '').tolist()

'''
correlations by year
'''


cor_list = []
p_list = []
for i in range(len(year_list)):
    cor_list.append(spearmanr(cor_data.iloc[i].tolist(), cor_data.iloc[i + len(year_list)].tolist())[0])
    p_list.append(spearmanr(cor_data.iloc[i].tolist(), cor_data.iloc[i + len(year_list)].tolist())[1])

cor_data_year = pandas.DataFrame({'year': year_list, 'spearman_correlation': cor_list, 'p-value': p_list})
cor_data_year['year'] = cor_data_year['year'].astype('int')
       
for i in range(len(cor_data_year)):
    if cor_data_year['p-value'][i] < 0.001:
        cor_data_year['significance'] = '***'
    elif cor_data_year['p-value'][i] < 0.01:
        cor_data_year['significance'] = '**'
    elif cor_data_year['p-value'][i] < 0.05:
        cor_data_year['significance'] = '*'

pyplot.scatter(cor_data_year['year'], cor_data_year['spearman_correlation'])
pyplot.plot(cor_data_year['year'], cor_data_year['spearman_correlation'], color = 'black')
pyplot.xlabel("Year")
pyplot.ylabel("Correlation Coefficient (Spearman's rho)")

print(cor_data_year)

'''
correlations by country
'''

cor_data_country = cor_data.T.reset_index().rename(columns = {'Unnamed: 0':'index'}).set_index('index')

cor_list = []
p_list = []
country_list = []

for i in range(int(len(cor_data_country) / 2)):
    cor_list.append(spearmanr(cor_data_country.iloc[i].tolist(), cor_data_country.iloc[i + len(year_list)].tolist())[0])
    p_list.append(spearmanr(cor_data_country.iloc[i].tolist(), cor_data_country.iloc[i + len(year_list)].tolist())[1])
    country_list.append(cor_data_country.index[i])

cor_data_country = pandas.DataFrame({'country': country_list, 'spearman_correlation': cor_list, 'p-value': p_list})
cor_data_country['country'] = cor_data_country['country'].str.replace('cba_', '')
       
for i in range(len(cor_data_country)):
    if cor_data_country['p-value'][i] < 0.001:
        cor_data_country['significance'] = '***'
    elif cor_data_country['p-value'][i] < 0.01:
        cor_data_country['significance'] = '**'
    elif cor_data_country['p-value'][i] < 0.05:
        cor_data_country['significance'] = '*'


print(cor_data_country)