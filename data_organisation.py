'''
cba_data from http://www.worldmrio.com/footprints/carbon/

wdi_data from https://datacatalog.worldbank.org/dataset/world-development-indicators

gender_data from https://datacatalog.worldbank.org/dataset/gender-statistics


check out for animation:
    https://python-graph-gallery.com/341-python-gapminder-animation/
'''

import pandas
import numpy as np


'''
functions
'''

def clean_col_headers(x):
    '''
    removes special characters from column headers, adds 'Y' to years in headers and removes capitalisation
    '''
    x.columns = x.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('"', '').str.replace('ï»¿', '')#.str.replace("19", "y19").str.replace("20", "y20")
    x = x.dropna(axis = 1, how='all') # does not work atm

"""
def region_filter(x, a): # not working atm
    x[(a == 'East Asia & Pacific') | 
            (a == 'Europe & Central Asia') |
            (a == 'Latin America & Caribbean') |
            (a == 'Middle East & North Africa') |
            (a == 'North America') |
            (a == 'South Asia') |
            (a == 'Sub-Saharan Africa')]
"""

'''
loading and manipulating data
'''

cba_data = pandas.read_csv('national_cba_report_1970-2015.txt', sep = None)
clean_col_headers(cba_data)
cba_data.set_index('country', inplace=True)

wdi_data = pandas.read_csv('WDIData.csv', sep = None)
clean_col_headers(wdi_data)
wdi_data.set_index('country_name', inplace=True)

country_data = pandas.read_csv('WDI_StatsCountry.csv', sep = None)
clean_col_headers(country_data)
country_data.set_index('country_code', inplace=True)


'''
making filter indecies 
'''
country_filter = country_data[(country_data.currency_unit.notnull())][['currency_unit', 'region', 'short_name']]

#regions = region_filter(country_data, country_data.short_name) # function not working 

regions = country_data[(country_data.short_name == 'East Asia & Pacific') | 
            (country_data.short_name == 'Europe & Central Asia') |
            (country_data.short_name == 'Latin America & Caribbean') |
            (country_data.short_name == 'Middle East & North Africa') |
            (country_data.short_name == 'North America') |
            (country_data.short_name == 'South Asia') |
            (country_data.short_name == 'Sub-Saharan Africa')][('short_name')].reset_index().set_index('country_code')
    

country_index = country_filter.set_index('region').join(regions.reset_index().set_index('short_name'), lsuffix='_country', rsuffix='_region').drop(['currency_unit'], axis = 1).reset_index()
country_index.columns = country_index.columns.str.replace('index', 'region')

country_index.to_csv('county_index.csv', sep = '\t')

'''
cbd by region - columns = regions, rows = years
'''

cba_region = cba_data.join(country_index.set_index('short_name'), lsuffix='_cba', rsuffix='_country')
cba_region = cba_region[(cba_region.record == 'CBA_MtCO2perCap')].drop(['record'], axis = 1).reset_index()
cba_region.columns = cba_region.columns.str.replace('index', 'country').str.replace('country_code', 'region_code')

cba_rgn_means = cba_region.replace(0, np.NaN).groupby(['region_code']).mean().T.drop('unnamed:_48', axis = 0)

cba_rgn_means.to_csv('cba_rgn.csv', sep = '\t')

cba_rgn_means.plot()


'''
wdi by regions  (GDP) - columns = regions, rows = years
'''

wdi_region = regions.reset_index().set_index('short_name').join(wdi_data, lsuffix='_region', rsuffix='_wdi').set_index('country_code_wdi').drop(['country_code_region', 'indicator_code'], axis = 1)

wdi_rgn_gdp = wdi_region[(wdi_region.indicator_name == 'GDP per capita (current US$)')].drop('indicator_name', axis = 1).T.reset_index().rename(columns = {'index':'year'})
wdi_rgn_gdp['year'] = wdi_rgn_gdp['year'].astype(int)
wdi_rgn_gdp = wdi_rgn_gdp[(wdi_rgn_gdp.year >= 1970) & (wdi_rgn_gdp.year <= 2015)].set_index('year')

wdi_rgn_gdp.to_csv('wdi_rgn_gdp.csv', sep = '\t')

#wdi_rgn_gdp.plot()


'''
cbd by region - columns = years, rows = regions
'''

cba_rgn_means_T = cba_rgn_means.T

cba_rgn_means_T.to_csv('cba_rgn_T.csv', sep = '\t')

#cba_rgn_means_T.plot()


'''
wdi by regions  (GDP) - columns = years, rows = regions
'''

wdi_rgn_gdp_T = wdi_rgn_gdp.T

wdi_rgn_gdp_T.to_csv('wdi_rgn_gdp_T.csv', sep = '\t')

#wdi_rgn_gdp_T.plot()




'''
wdi by regions  (Death rate)
'''

wdi_rgn_dr = wdi_region[(wdi_region.indicator_name == 'Death rate, crude (per 1,000 people)')].drop('indicator_name', axis = 1).T.reset_index().rename(columns = {'index':'year'})
wdi_rgn_dr['year'] = wdi_rgn_dr['year'].astype(int)
wdi_rgn_dr = wdi_rgn_dr[(wdi_rgn_dr.year >= 1970) & (wdi_rgn_dr.year <= 2015)].set_index('year')

wdi_rgn_dr.to_csv('wdi_rgn_dr.csv', sep = '\t')

#wdi_rgn_dr.plot()






'''
wdi by country (Death rate)

NOT YET REVISED AGAIN AFTER LOSING THE CODE!!!
'''

"""
cba_country = cba_data[(cba_data.record == "CBA_MtCO2perCap")].drop(['record', 'unnamed:_48'], axis = 1).T
cba_country['code'] = 'cba'
cba_country['year'] = cba_country['year'].astype(int)


wdi_country = country_index.set_index('short_name').drop('country_code', axis = 1).join(wdi_data, lsuffix='_country', rsuffix = '_wdi')
wdi_country = wdi_country[(wdi_country.indicator_name == "Death rate, crude (per 1,000 people)")].drop(['indicator_name', 'country_code', 'indicator_code', 'region', 'unnamed:_62'], axis = 1).T.reset_index()
wdi_country = wdi_country.rename(index=str, columns={"index": "year"})
wdi_country['code'] = 'wdi'
wdi_country['year'] = wdi_country['year'].astype(int)
wdi_country = wdi_country[(wdi_country.year >= 1970) & (wdi_country.year <= 2015)].set_index('year')

cba_wdi = cba_country.append(wdi_country)

wdi_cba = cba_country.drop('code', axis = 1).join(wdi_country.drop('code', axis = 1), lsuffix = '_cba', rsuffix = '_wdi')

#wdi_cba.plot()

"""

