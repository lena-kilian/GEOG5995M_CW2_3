import pandas
from scipy.stats import shapiro
from scipy.stats import spearmanr
from class_framework import sig_level


# loading data

cor_data = pandas.read_csv('country_data.csv', sep = '\t').set_index('Unnamed: 0').sort_index(axis=1, ascending=True)

wdi_data = cor_data[(cor_data.index.str.contains('wdi'))].T
wdi_data.columns = wdi_data.columns.str.replace('wdi_', '')

cba_data = cor_data[(cor_data.index.str.contains('cba'))].T
cba_data.columns = cba_data.columns.str.replace('cba_', '')

all_data = pandas.merge(cba_data.stack().to_frame().reset_index().rename(columns = {0:'cba', 'level_0':'country', 'Unnamed: 0':'year'}), 
                        wdi_data.stack().to_frame().reset_index().rename(columns = {0:'wdi', 'level_0':'country', 'Unnamed: 0':'year'}), 
                        how = 'left', left_on = ['country', 'year'], right_on = ['country', 'year']).drop(['country', 'year'], axis = 1)

year_list = cba_data.columns.tolist()


# descriptive statistics

## all data
descriptives_all = pandas.DataFrame(all_data.describe()).rename(columns = {'cba':'All_combined_cba', 'wdi':'All_combined_wdi'}).T

## by countries
descriptives_country = pandas.DataFrame(cba_data.T.describe()).join(pandas.DataFrame(wdi_data.T.describe()), lsuffix = '_cba', rsuffix = '_wdi').T

## by years
descriptives_year = pandas.DataFrame(cba_data.describe()).join(pandas.DataFrame(wdi_data.describe()), lsuffix = '_cba', rsuffix = '_wdi').T


# normality testing

## all data
norm_test_all = pandas.DataFrame(index = ['All_combined'], columns = ['cba_sw', 'cba_p', 'wdi_sw', 'wdi_p', 'normal_dist'])

norm_test_all['cba_sw']['All_combined'] = shapiro(all_data['cba'])[0]
norm_test_all['cba_p']['All_combined'] = shapiro(all_data['cba'])[1]
norm_test_all['wdi_sw']['All_combined'] = shapiro(all_data['wdi'])[0]
norm_test_all['wdi_p']['All_combined'] = shapiro(all_data['wdi'])[1]

if norm_test_all['cba_p'][0] > 0.05 and norm_test_all['wdi_p'][0] > 0.05:
    norm_test_all['normal_dist'][0] = True
else:
    norm_test_all['normal_dist'][0] = False 

## by countries
norm_test_country = pandas.DataFrame(index = cba_data.index, columns = ['cba_sw', 'cba_p', 'wdi_sw', 'wdi_p', 'normal_dist'])

for i in range(len(cba_data)):
    norm_test_country['cba_sw'][i] = shapiro(cba_data.iloc[i])[0]
    norm_test_country['cba_p'][i] = shapiro(cba_data.iloc[i])[1]
    norm_test_country['wdi_sw'][i] = shapiro(wdi_data.iloc[i])[0]
    norm_test_country['wdi_p'][i] = shapiro(wdi_data.iloc[i])[1]
    if norm_test_country['cba_p'][i] > 0.05 and norm_test_country['wdi_p'][i] > 0.05:
        norm_test_country['normal_dist'][i] = True
    else:
        norm_test_country['normal_dist'][i] = False 

## by years
norm_test_year = pandas.DataFrame(index = cba_data.T.index, columns = ['cba_sw', 'cba_p', 'wdi_sw', 'wdi_p', 'normal_dist'])

for i in range(len(cba_data.T)):
    norm_test_year['cba_sw'][i] = shapiro(cba_data.T.iloc[i])[0]
    norm_test_year['cba_p'][i] = shapiro(cba_data.T.iloc[i])[1]
    norm_test_year['wdi_sw'][i] = shapiro(wdi_data.T.iloc[i])[0]
    norm_test_year['wdi_p'][i] = shapiro(wdi_data.T.iloc[i])[1]
    if norm_test_year['cba_p'][i] > 0.05 and norm_test_year['wdi_p'][i] > 0.05:
        norm_test_year['normal_dist'][i] = True
    else:
        norm_test_year['normal_dist'][i] = False  


# correlations using spearman's rho, because distributions were not normal

## all data
cor_data_all = pandas.DataFrame(index = ['All_combined'], columns = ['spearman_correlation', 'p_value', 'significance'])
cor_data_all['spearman_correlation'][0] = spearmanr(all_data['cba'], all_data['wdi'])[0]
cor_data_all['p_value'][0] = spearmanr(all_data['cba'], all_data['wdi'])[1]

cor_data_all['significance'][0] = sig_level(cor_data_all['p_value'][0])

## by country
cor_data_country = cor_data.T.reset_index().rename(columns = {'Unnamed: 0':'index'}).set_index('index')

cor_list = []
p_list = []
country_list = []

for i in range(int(len(cor_data_country) / 2)):
    cor_list.append(spearmanr(cor_data_country.iloc[i].tolist(), cor_data_country.iloc[i + len(year_list)].tolist())[0])
    p_list.append(spearmanr(cor_data_country.iloc[i].tolist(), cor_data_country.iloc[i + len(year_list)].tolist())[1])
    country_list.append(cor_data_country.index[i])

cor_data_country = pandas.DataFrame({'country': country_list, 'spearman_correlation': cor_list, 'p_value': p_list})
cor_data_country['country'] = cor_data_country['country'].str.replace('cba_', '')
cor_data_country['significance'] = 'ns'
       
for i in range(len(cor_data_country)):
    cor_data_country['significance'][i] = sig_level(cor_data_country['p_value'][i])


## by years
cor_list = []
p_list = []
for i in range(len(year_list)):
    cor_list.append(spearmanr(cor_data.iloc[i].tolist(), cor_data.iloc[i + len(year_list)].tolist())[0])
    p_list.append(spearmanr(cor_data.iloc[i].tolist(), cor_data.iloc[i + len(year_list)].tolist())[1])

cor_data_year = pandas.DataFrame({'year': year_list, 'spearman_correlation': cor_list, 'p_value': p_list})
cor_data_year['year'] = cor_data_year['year'].astype('int')
cor_data_year['significance'] = 'ns'
       
for i in range(len(cor_data_year)):
    cor_data_year['significance'][i] = sig_level(cor_data_year['p_value'][i])


# saving findings to an excel file
       
results_all = pandas.ExcelWriter('country_stats.xlsx')
descriptives_all.to_excel(results_all,'Descriptives - All')
descriptives_country.to_excel(results_all,'Descriptives - Country')
descriptives_year.to_excel(results_all,'Descriptives - Year')
norm_test_all.to_excel(results_all,'Normality Tests - All')
norm_test_country.to_excel(results_all,'Normality Tests - Country')
norm_test_year.to_excel(results_all,'Normality Tests - Year')
cor_data_all.to_excel(results_all,'Spearman Correlation - All')
cor_data_country.to_excel(results_all,'Spearman Correlation - Country')
cor_data_year.to_excel(results_all,'Spearman Correlation - Year')
results_all.save()