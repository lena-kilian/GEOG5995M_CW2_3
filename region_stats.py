import pandas
from scipy.stats import shapiro
from scipy.stats import spearmanr
from class_framework import sig_level
   
# loading data

cba_data = pandas.read_csv('cba_rgn.csv', sep = '\t').set_index('Unnamed: 0').sort_index(axis=0, ascending=True).sort_index(axis=1, ascending=True).T

wdi_data = pandas.read_csv('wdi_rgn.csv', sep = '\t').set_index('year').sort_index(axis=0, ascending=True).sort_index(axis=1, ascending=True).T

all_data = pandas.merge(cba_data.stack().to_frame().reset_index().rename(columns = {0:'cba', 'level_0':'region', 'Unnamed: 0':'year'}), 
                     wdi_data.stack().to_frame().reset_index().rename(columns = {0:'wdi', 'level_0':'region'}), 
                     how = 'left', left_on = ['region', 'year'], right_on = ['region', 'year']).drop(['region', 'year'], axis = 1)


# descriptive statistics

descriptives = pandas.DataFrame(wdi_data.T.describe()).join(
        pandas.DataFrame(cba_data.T.describe()), lsuffix = '_wdi', rsuffix = '_cba').sort_index(axis=1, ascending=True).join(
        pandas.DataFrame(all_data.describe()).rename(columns = {'cba':'All_combined_cba', 'wdi':'All_combined_wdi'})).T

print(descriptives)

# normality testing 

norm_test = pandas.DataFrame(index = cba_data.index, columns = ['cba_sw', 'cba_p', 'wdi_sw', 'wdi_p', 'normal_dist']).append(
        pandas.DataFrame(index = ['All_combined'], columns = ['cba_sw', 'cba_p', 'wdi_sw', 'wdi_p', 'normal_dist']))

norm_test['cba_sw']['All_combined'] = shapiro(all_data['cba'])[0]
norm_test['cba_p']['All_combined'] = shapiro(all_data['cba'])[1]
norm_test['wdi_sw']['All_combined'] = shapiro(all_data['wdi'])[0]
norm_test['wdi_p']['All_combined'] = shapiro(all_data['wdi'])[1]

for i in range(len(cba_data)):
    norm_test['cba_sw'][i] = shapiro(cba_data.iloc[i])[0]
    norm_test['cba_p'][i] = shapiro(cba_data.iloc[i])[1]
    norm_test['wdi_sw'][i] = shapiro(wdi_data.iloc[i])[0]
    norm_test['wdi_p'][i] = shapiro(wdi_data.iloc[i])[1]

for i in range(len(norm_test)):
    if norm_test['cba_p'][i] > 0.05 and norm_test['wdi_p'][i] > 0.05:
        norm_test['normal_dist'][i] = True
    else:
        norm_test['normal_dist'][i] = False  

print(norm_test)

# correlations using spearman's rho, because distributions were not normal

cor_list = []
p_list = []
country_list = []
for i in range(len(cba_data)):
    cor_list.append(spearmanr(cba_data.iloc[i].tolist(), wdi_data.iloc[i].tolist())[0])
    p_list.append(spearmanr(cba_data.iloc[i].tolist(), wdi_data.iloc[i].tolist())[1])
    country_list.append(cba_data.index[i])
country_list.append('All_combined')
cor_list.append(spearmanr(all_data['cba'], all_data['wdi'])[0])
p_list.append(spearmanr(all_data['cba'], all_data['wdi'])[1])

cor_data = pandas.DataFrame({'region': country_list, 'spearmans_rho': cor_list, 'p_value': p_list}).set_index('region')
cor_data['significance'] = 'ns'

for i in range(len(cor_data)):
    cor_data['significance'][i] = sig_level(cor_data['p_value'][i])

print(cor_data)

# saving findings to an excel file
        
results_all = pandas.ExcelWriter('region_stats.xlsx')
descriptives.to_excel(results_all,'Descriptives Statistics')
norm_test.to_excel(results_all,'Normality Tests')
cor_data.to_excel(results_all,'Spearman Correlation')
results_all.save()