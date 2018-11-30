'''
cba_data from http://www.worldmrio.com/footprints/carbon/

wdi_data from https://datacatalog.worldbank.org/dataset/world-development-indicators

gender_data from https://datacatalog.worldbank.org/dataset/gender-statistics


check out for animation:
    https://python-graph-gallery.com/341-python-gapminder-animation/
'''

'''
CHECK WHICH FILES I ACTUALLY USE LATER ON AND TIDY THIS UP
'''

import pandas
import numpy

'''
functions
'''

def clean_col_headers(x):
    '''
    removes special characters from column headers, adds 'Y' to years in headers and removes capitalisation
    '''
    x.columns = x.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('"', '').str.replace('ï»¿', '')#.str.replace("19", "y19").str.replace("20", "y20")
    x = x.dropna(axis = 1, how='all')

'''
loading and manipulating data
'''

cba_data = pandas.read_csv('national_cba_report_1970-2015.txt', sep = None).replace(0, numpy.nan)
clean_col_headers(cba_data)
cba_data.set_index('country', inplace=True)

wdi_data = pandas.read_csv('WDIData.csv', sep = None).replace(0, numpy.nan)
clean_col_headers(wdi_data)
wdi_data.set_index('country_name', inplace=True)

country_data = pandas.read_csv('WDI_StatsCountry.csv', sep = None).replace(0, numpy.nan)
clean_col_headers(country_data)
country_data.set_index('country_code', inplace=True)


'''
making filter indecies 
'''

income_filter = country_data[['short_name', 'region', 'income_group']].dropna(axis = 0)
income_filter.to_csv('income_filter.csv', sep = '\t')

country_filter = country_data[(country_data.currency_unit.notnull())][['currency_unit', 'region', 'short_name']]


regions = country_data[(country_data.short_name == 'East Asia & Pacific') | 
            (country_data.short_name == 'Europe & Central Asia') |
            (country_data.short_name == 'Latin America & Caribbean') |
            (country_data.short_name == 'Middle East & North Africa') |
            (country_data.short_name == 'North America') |
            (country_data.short_name == 'South Asia') |
            (country_data.short_name == 'Sub-Saharan Africa')][('short_name')].reset_index().set_index('country_code')
regions.to_csv('region_index.csv', sep = '\t')
    

country_index = country_filter.set_index('region').join(regions.reset_index().set_index('short_name'), lsuffix='_country', rsuffix='_region').drop(['currency_unit'], axis = 1).reset_index().rename(columns = {'country_code':'region_code', 'index':'region'}).set_index('short_name')

country_index.to_csv('county_index.csv', sep = '\t')

'''
cbd by region
'''

cba_region = cba_data.join(country_index, lsuffix='_cba', rsuffix='_country')
cba_region = cba_region[(cba_region.record == 'CBA_MtCO2perCap')].drop(['record'], axis = 1).reset_index()
cba_region.columns = cba_region.columns.str.replace('index', 'country').str.replace('country_code', 'region_code')

cba_rgn_means = cba_region.groupby(['region_code']).mean().T.drop('unnamed:_48', axis = 0)

cba_rgn_means.to_csv('cba_rgn.csv', sep = '\t')


'''
wdi by regions (GDP)
'''

wdi_region = regions.reset_index().set_index('short_name').join(wdi_data, lsuffix='_region', rsuffix='_wdi').set_index('country_code_wdi').drop(['country_code_region', 'indicator_code'], axis = 1)

wdi_rgn_gdp = wdi_region[(wdi_region.indicator_name == 'GDP per capita (current US$)')].drop('indicator_name', axis = 1).T.reset_index().rename(columns = {'index':'year'})
wdi_rgn_gdp['year'] = wdi_rgn_gdp['year'].astype(int)
wdi_rgn_gdp = wdi_rgn_gdp[(wdi_rgn_gdp.year >= 1970) & (wdi_rgn_gdp.year <= 2015)].set_index('year')

wdi_rgn_gdp.to_csv('wdi_rgn_gdp.csv', sep = '\t')



'''
By country wdi (GDP) and cba
'''


cba_country = cba_data[(cba_data.record == "CBA_MtCO2perCap")].drop(['record', 'unnamed:_48'], axis = 1)
cba_country['code'] = 'cba'


wdi_country = country_index.drop('region_code', axis = 1).join(wdi_data, lsuffix='_country', rsuffix = '_wdi')
wdi_country = wdi_country[(wdi_country.indicator_name == "GDP per capita (current US$)")].drop(['indicator_name', 'country_code', 'indicator_code', 'region'], axis = 1).T.reset_index()
wdi_country = wdi_country.rename(index=str, columns={"index": "year"})
wdi_country['year'] = wdi_country['year'].astype(int)
wdi_country = wdi_country[(wdi_country.year >= 1970) & (wdi_country.year <= 2015)]
wdi_country['year'] = wdi_country['year'].astype(str)
wdi_country = wdi_country.set_index('year').T
wdi_country['code'] = 'wdi'


cba_wdi = cba_country.append(wdi_country)
cba_wdi.to_csv('cba_wdi_country.csv', sep = '\t')

wdi_country_filter = wdi_country['code'].reset_index().set_index('index')

country_filter = cba_country['code'].reset_index().set_index('country').join(wdi_country_filter, lsuffix = '_cba', rsuffix = '_wdi')
country_filter = country_filter[(country_filter.code_cba == 'cba') & (country_filter.code_wdi == 'wdi')].drop(['code_cba', 'code_wdi'], axis = 1)
country_filter.to_csv('country_filter.csv', sep = '\t')



'''
merge data for country analysis
'''

country_filter['country_list'] = country_filter.index.astype(str)
country_dat = country_filter.join(cba_wdi).join(country_index.drop(['region'], axis = 1)).join(regions, on = 'region_code').sort_index(axis=1, ascending=True).sort_values(by = ['code', 'country_list'], ascending=True)
country_dat.to_csv('country_data.csv', sep = '\t')

