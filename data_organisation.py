'''
cba_data from http://www.worldmrio.com/footprints/carbon/

wdi_data from https://datacatalog.worldbank.org/dataset/world-development-indicators

gender_data from https://datacatalog.worldbank.org/dataset/gender-statistics
'''

import pandas
import numpy
from class_framework import clean_col_headers

# loading data files

cba_data = pandas.read_csv('national_cba_report_1970-2015.txt', sep = None).replace(0, numpy.nan)
clean_col_headers(cba_data)
cba_data.set_index('country', inplace=True)

wdi_data = pandas.read_csv('WDIData.csv', sep = None).replace(0, numpy.nan)
clean_col_headers(wdi_data)
wdi_data.set_index('country_name', inplace=True)

country_data = pandas.read_csv('WDI_StatsCountry.csv', sep = None).replace(0, numpy.nan)
clean_col_headers(country_data)
country_data.set_index('country_code', inplace=True)


# making filter indecies (to ensure that countries are the same for cba and wdi, and to assign regions)

country_filter = country_data[(country_data.currency_unit.notnull())][['currency_unit', 'region', 'short_name']]

region_index = country_data[(country_data.short_name == 'East Asia & Pacific') | 
            (country_data.short_name == 'Europe & Central Asia') |
            (country_data.short_name == 'Latin America & Caribbean') |
            (country_data.short_name == 'Middle East & North Africa') |
            (country_data.short_name == 'North America') |
            (country_data.short_name == 'South Asia') |
            (country_data.short_name == 'Sub-Saharan Africa')][('short_name')].reset_index().set_index('country_code')

country_index = country_filter.set_index('region').join(
        region_index.reset_index().set_index('short_name'), lsuffix='_country', rsuffix='_region').drop(['currency_unit'], axis = 1
                                ).reset_index().rename(columns = {'country_code':'region_code', 'index':'region'}).set_index('short_name')
country_index.to_csv('country_index.csv', sep = '\t')


# wdi (gdp) and cba by country

cba_country = cba_data[(cba_data.record == "CBA_MtCO2perCap")].drop(['record', 'unnamed:_48'], axis = 1)
cba_country['code'] = 'cba'

wdi_country = country_index.drop('region_code', axis = 1).join(wdi_data, lsuffix='_country', rsuffix = '_wdi')
wdi_country = wdi_country[(wdi_country.indicator_name == "GDP per capita (current US$)")].drop(
        ['indicator_name', 'country_code', 'indicator_code', 'region'], axis = 1).T.reset_index()
wdi_country = wdi_country.rename(index=str, columns={"index": "year"})
wdi_country['year'] = wdi_country['year'].astype(int)
wdi_country = wdi_country[(wdi_country.year >= 1970) & (wdi_country.year <= 2015)]
wdi_country['year'] = wdi_country['year'].astype(str)
wdi_country = wdi_country.set_index('year').T
wdi_country['code'] = 'wdi'

country_filter = cba_country['code'].reset_index().set_index('country').join(
        wdi_country['code'].reset_index().set_index('index'), lsuffix = '_cba', rsuffix = '_wdi')
country_filter = country_filter[(country_filter.code_cba == 'cba') & (country_filter.code_wdi == 'wdi')].drop(['code_cba', 'code_wdi'], axis = 1)
country_filter['country_list'] = country_filter.index.astype(str)

country_data = country_filter.join(cba_country.append(wdi_country)).join(
        country_index.drop(['region'], axis = 1)).sort_index(axis=1, ascending=True).sort_values(by = ['code', 'country_list'], ascending=True)

country_data = country_data[country_data.code == 'wdi'].drop(
        ['code', 'region_code', 'country_list'], axis = 1).add_prefix('wdi_').join(
                country_data[country_data.code == 'cba'].drop(
                        ['code', 'region_code', 'country_list'], axis = 1).add_prefix('cba_'), rsuffix = '_cba', lsuffix = '_wdi').dropna(
                        ).sort_index(axis = 1).T
country_data.to_csv('country_data.csv', sep = '\t')