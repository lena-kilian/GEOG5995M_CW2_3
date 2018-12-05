import pandas
from matplotlib import pyplot
from statsmodels.graphics.gofplots import qqplot
from scipy.stats import shapiro
from scipy.stats import spearmanr

'''
CLEAN UP NEEDED!!
'''
cba_data = pandas.read_csv('cba_rgn.csv', sep = '\t').set_index('Unnamed: 0').sort_index(axis=0, ascending=True).sort_index(axis=1, ascending=True).T

wdi_data = pandas.read_csv('wdi_rgn_gdp.csv', sep = '\t').set_index('year').sort_index(axis=0, ascending=True).sort_index(axis=1, ascending=True).T

norm_test = pandas.DataFrame(index = cba_data.index, columns = ['cba_sw', 'cba_p', 'wdi_sw', 'wdi_p', 'normal_dist'])

for i in range(len(cba_data)):
    norm_test['cba_sw'][i] = shapiro(cba_data.iloc[i])[0]
    norm_test['cba_p'][i] = shapiro(cba_data.iloc[i])[1]
    norm_test['wdi_sw'][i] = shapiro(wdi_data.iloc[i])[0]
    norm_test['wdi_p'][i] = shapiro(wdi_data.iloc[i])[1]
    if norm_test['cba_p'][i] > 0.05 and norm_test['wdi_p'][i] > 0.05:
        norm_test['normal_dist'][i] = 'Yes'
    else:
        norm_test['normal_dist'][i] = 'No'   

'''
descriptives
'''

all_data = pandas.merge(cba_data.stack().to_frame().reset_index().rename(columns = {0:'cba', 'level_0':'region', 'Unnamed: 0':'year'}), 
                     wdi_data.stack().to_frame().reset_index().rename(columns = {0:'wdi', 'level_0':'region'}), 
                     how = 'left', left_on = ['region', 'year'], right_on = ['region', 'year']).drop(['region', 'year'], axis = 1)
all_data.describe()

pyplot.scatter(all_data['cba'], all_data['wdi'], s = 3)


pyplot.hist(all_data['cba'], bins= 20)
pyplot.boxplot(all_data['cba'])
qqplot(all_data['cba'], line = 's')
shapiro(all_data['cba'])

pyplot.boxplot(all_data['wdi'])
qqplot(all_data['wdi'], line = 's')
shapiro(all_data['wdi'])

spearmanr(all_data['cba'], all_data['wdi'])

'''
correlation
'''

cor_list = []
p_list = []
country_list = []
for i in range(len(cba_data)):
    cor_list.append(spearmanr(cba_data.iloc[i].tolist(), wdi_data.iloc[i].tolist())[0])
    p_list.append(spearmanr(cba_data.iloc[i].tolist(), wdi_data.iloc[i].tolist())[1])
    country_list.append(cba_data.index[i])

cor_data = pandas.DataFrame({'country': country_list, 'spearmans_rho': cor_list, 'p-value': p_list}).sort_values(by = ['spearmans_rho'])
       
for i in range(len(cor_data)):
    if cor_data['p-value'][i] < 0.001:
        cor_data['significance'] = '***'
    elif cor_data['p-value'][i] < 0.01:
        cor_data['significance'] = '**'
    elif cor_data['p-value'][i] < 0.05:
        cor_data['significance'] = '*'

pyplot.scatter(cor_data['country'], cor_data['spearmans_rho'])
pyplot.xlabel("Country")
pyplot.ylabel("Correlation Coefficient (Spearman's rho)")