import pandas
from matplotlib import pyplot
from scipy.stats import pearsonr


cba_rgn = pandas.read_csv('cba_rgn.csv', sep = '\t').set_index('Unnamed: 0').sort_index(axis=0, ascending=True).sort_index(axis=1, ascending=True).T

wdi_rgn_gdp = pandas.read_csv('wdi_rgn_gdp.csv', sep = '\t').set_index('year').sort_index(axis=0, ascending=True).sort_index(axis=1, ascending=True).T

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