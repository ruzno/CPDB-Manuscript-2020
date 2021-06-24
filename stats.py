# %% [MUST RUN] treats the database that will be used in all analysis below
import pandas as pd

policies = pd.read_csv(r'results/treated_policy_database.csv')
emissions = pd.read_csv(r'data/emissions_data/emissions_edgar_fao.csv')
tags = pd.read_csv(r'data/country_data/country_tags.csv')


# Defining some relevant functions for aggregation
# 5th Percentile
def p05(x):
    return x.quantile(0.05)


# 95th Percentile
def p95(x):
    return x.quantile(0.95)


# treating the emissions database

# cross tags and policies db to bring G20 status
emissions_filtered = pd.merge(emissions, tags,
                              how='left', left_on='iso3', right_on='ISO3')

emissions_filtered = emissions_filtered[(emissions_filtered['G20'] == 'G20') &
                                        (~emissions_filtered['iso3'].isin(['DEU', 'FRA', 'ITA', 'GBR']))]

# cross emissions and policies db to bring  emissions
policies_tagged = pd.merge(policies, emissions_filtered,
                           how='left', left_on='policy_country_iso_code', right_on='iso3')

# filters policies
policies_filtered = policies_tagged[(policies_tagged['policy_start_date_analysis'] <= 2019) &
                                    (policies_tagged['policy_implementation_state'] == 'In force') &
                                    (policies_tagged['G20'] == 'G20') &
                                    (~policies_tagged['policy_country_iso_code'].isin(['DEU', 'FRA', 'ITA', 'GBR']))]

# %% Basic distribution of policy instruments

policy_instruments = ['DirectInvestment', 'FiscalFinancialIncentives',
                      'Market-basedInstruments', 'CodesStandards',
                      'OtherRegulatoryInstruments', 'RDD', 'InformationEducation',
                      'PolicySupport', 'VoluntaryApproaches', 'BarrierRemoval',
                      'ClimateStrategy', 'Target']

analysis_instruments = pd.DataFrame()

for col in policy_instruments:
    df = policies_filtered[policies_filtered[col]]
    df_1 = df.groupby(by='policy_country_iso_code').agg({'policy_id': ['nunique'],
                                                         'policy_start_date_analysis': [p05, p95,
                                                                                        'median']}).reset_index()
    df_1['variable'] = col
    analysis_instruments = pd.concat([analysis_instruments, df_1], axis=0)

# %% Basic distribution of sectors

sectors = ['GeneralSector', 'ElectricitySector', 'IndustrySector',
           'BuildingsSector', 'TransportSector', 'LandSector']

analysis_sectors = pd.DataFrame()

for col in sectors:
    df = policies_filtered[policies_filtered[col]]
    df_1 = df.groupby(by='policy_country_iso_code').agg({'policy_id': ['nunique'],
                                                         'policy_start_date_analysis': [p05, p95,
                                                                                        'median']}).reset_index()
    df_1['variable'] = col
    analysis_sectors = pd.concat([analysis_sectors, df_1], axis=0)

# %% Analysis of policy options

policy_options = ['g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7',
                  'eh1', 'eh2', 'eh3', 'eh4', 'eh5', 'eh6', 'eh7', 'eh8', 'eh9', 'eh10',
                  'i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8', 'i9', 'i10', 'i11',
                  'i12', 'i13', 'i14', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'lt1', 'lt2',
                  'lt3', 'lt4', 'lt5', 'lt6', 'lt7', 'af1', 'af2', 'af3', 'af4', 'af5',
                  'af6']

options_dictionary = {'g1': 'Climate strategy',
                      'g2': 'GHG reduction target',
                      'g3': 'Coordinating body for climate strategy',
                      'g4': 'No fossil fuel subsidies',
                      'g5': 'Support for low-emission and negative emissions RD&D',
                      'g6': 'Economy-wide energy efficiency target',
                      'g7': 'Renewable target for primary energy',

                      'eh1': 'Support for highly efficient power plant stock',
                      'eh2': 'Energy reduction obligation schemes',
                      'eh3': 'Renewable energy target for electricity sector',
                      'eh4': 'Support scheme for renewables',
                      'eh5': 'Grid infrastructure development and electricity storage',
                      'eh6': 'Coal and oil phase-out policies',
                      'eh7': 'Support scheme for CCS',
                      'eh8': 'Support for non-renewable low-carbon alternatives',
                      'eh9': 'Overarching carbon pricing scheme',
                      'eh10': 'Energy and other taxes',

                      'i1': 'Strategy for material efficiency',
                      'i2': 'Support for energy efficiency in industrial production',
                      'i3': 'Energy reporting and audits',
                      'i4': 'Performance and equipment standards',
                      'i5': 'Support scheme for renewables',
                      'i6': 'Support scheme for CCS',
                      'i7': 'Support scheme for fuel switch',
                      'i8': 'Carbon dioxide removal technology development',
                      'i9': 'Incentives to reduce CH4 from fuel exploration and production',
                      'i10': 'Incentives to reduce landfill CH4',
                      'i11': 'Incentives to reduce N2O from industrial processes',
                      'i12': 'Incentives to reduce F-gases',
                      'i13': 'Overarching carbon pricing scheme or emissions limit',
                      'i14': 'Energy and other taxes',

                      'b1': 'Urban planning strategies',
                      'b2': 'Building codes and standards as well as support for highly efficient construction',
                      'b3': 'Performance and equipment standards as well as support for highly efficient appliances',
                      'b4': 'Support scheme for heating and cooling',
                      'b5': 'Support scheme for hot water and cooking',
                      'b6': 'Energy and other taxes',

                      'lt1': 'Urban planning and infrastructure investment',
                      'lt2': 'Energy/emissions performance standards or support for energy efficient light-duty vehicles',
                      'lt3': 'Energy/emissions performance standards or support for energy efficient heavy-duty vehicles',
                      'lt4': 'Support scheme for biofuels',
                      'lt5': 'Support for modal share switch',
                      'lt6': 'Support for low-emissions land transportation',
                      'lt7': 'Tax on fuel and/or emissions',

                      'af1': 'Standards and support for sustainable agricultural practices and use of agricultural products',
                      'af2': 'Incentives to reduce CO2 emissions from agriculture',
                      'af3': 'Incentives to reduce CH4 emissions from agriculture',
                      'af4': 'Incentives to reduce N2O emissions from agriculture',
                      'af5': 'Incentives to reduce deforestation and enhance afforestation and reforestation',
                      'af6': 'Sustainability standards for biomass use'

                      }

options_dataframe = pd.DataFrame.from_dict(options_dictionary, orient='index').reset_index()
options_dataframe.columns = ['variable', 'name']

analysis_options = pd.DataFrame()

for col in policy_options:
    df = policies_filtered[policies_filtered[col]]
    df_1 = df.groupby(by='G20').agg({'policy_id': ['nunique'],
                                     'policy_country_iso_code': [lambda x: ','.join(sorted(pd.Series.unique(x))),
                                                                 'nunique'],
                                     'policy_start_date_analysis': [p05, p95, 'median'],
                                     'em_share': ['unique', lambda x: sum(pd.Series.unique(x))]}).reset_index()
    df_1['variable'] = col
    analysis_options = pd.concat([analysis_options, df_1], axis=0)

analysis_options = pd.merge(analysis_options, options_dataframe, how='left', on='variable')

analysis_options.to_csv('results/analysis_options.csv', index=False)

# %% Data for plot

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

policy_database = pd.read_csv('results/treated_policy_database.csv')
g20 = pd.read_csv('data/country_data/g20_countries.csv').squeeze()

# Adding only the IPCC instruments

policy_database['Economic instruments'] = ((policy_database['FiscalFinancialIncentives']) |
                                           (policy_database['DirectInvestment']))

policy_database['Regulatory instruments'] = ((policy_database['OtherRegulatoryInstruments']) |
                                             (policy_database['CodesStandards']))

policy_database['Other instruments'] = ((policy_database['InformationEducation']) |
                                        (policy_database['VoluntaryApproaches']) |
                                        (policy_database['ClimateStrategy']) |
                                        (policy_database['Target']))

policy_database = policy_database[
    (policy_database['policy_jurisdiction'] == 'Country') &
    (policy_database['policy_type_of_policy_instrument'].notnull()) &
    (policy_database['policy_sector_name'].notnull()) &
    (policy_database['policy_country_iso_code'].isin(g20)) &
    (policy_database['policy_implementation_state'] == 'In force') &
    (policy_database['policy_start_date_analysis'] >= 2000) &
    (policy_database['policy_start_date_analysis'] < 2020)]

# prepare sectors

col_sectors = ['policy_id', 'ElectricitySector', 'IndustrySector', 'BuildingsSector',
               'TransportSector', 'LandSector', 'GeneralSector']

for_sectors = policy_database[col_sectors]
for_date = policy_database[['policy_id', 'policy_start_date_analysis']]
for_sectors_m = pd.melt(for_sectors, id_vars='policy_id')
for_sectors_m = for_sectors_m[for_sectors_m['value']].drop(columns='value')

for_sectors_m = pd.merge(for_sectors_m, for_date, how='left')

# prepare instruments

col_instruments = ['policy_id', 'DirectInvestment', 'FiscalFinancialIncentives',
                   'Market-basedInstruments', 'CodesStandards',
                   'OtherRegulatoryInstruments', 'RDD', 'InformationEducation',
                   'VoluntaryApproaches',
                   'ClimateStrategy', 'Target']

# # 'Economic instruments', 'Regulatory instruments', 'Other instruments'
# 'DirectInvestment', 'FiscalFinancialIncentives',
# 'Market-basedInstruments', 'CodesStandards',
# 'OtherRegulatoryInstruments', 'RDD', 'InformationEducation',
# 'VoluntaryApproaches', 'BarrierRemoval',
# 'ClimateStrategy', 'Target'

for_instruments = policy_database[col_instruments]
for_instruments_m = pd.melt(for_instruments, id_vars='policy_id')
for_instruments_m = for_instruments_m[for_instruments_m['value']].drop(columns='value')

for_instruments_m = pd.merge(for_instruments_m, for_date, how='left')

# merge sector and instruments tables

for_plot = pd.merge(for_instruments_m, for_sectors_m, how='inner', on='policy_id', suffixes=['_inst', '_sec'])

# %% Making a boxplot to assess distribution of policy instruments across sectors

sns.set_style("whitegrid")
sns.color_palette("Set2")

# cols = ['General', 'Electricity and heat', 'Industry', 'Buildings', 'Land transport', 'Agriculture and forestry']

sns.catplot(data=for_plot, x='policy_start_date_analysis_sec',
            col='variable_sec', col_wrap=3, col_order=sectors,
            y='variable_inst',
            kind='box',
            sharex=True).set_titles('{col_name}')

plt.tight_layout()
plt.show()

x = for_sectors_m.groupby('variable').agg(
    {'policy_start_date_analysis': [lambda x: x.quantile(0.75), p05, 'median', p95, 'std'],
     'policy_id': 'nunique'})
# %% Evolution of policy instruments

instruments = ['DirectInvestment', 'FiscalFinancialIncentives',
               'Market-basedInstruments', 'CodesStandards',
               'VoluntaryApproaches']

melt_inst = pd.melt(policies_filtered, id_vars='policy_id', value_vars=instruments, var_name='instrument')
melt_inst = melt_inst[melt_inst['value']].sort_values(by='policy_id')

sectors = ['GeneralSector', 'ElectricitySector', 'IndustrySector',
           'BuildingsSector', 'TransportSector', 'LandSector']

melt_sec = pd.melt(policies_filtered, id_vars='policy_id', value_vars=sectors, var_name='sector')
melt_sec = melt_sec[melt_sec['value']].sort_values(by='policy_id')

# Merging the two tables

base = pd.merge(melt_inst, melt_sec, how='left', on='policy_id')
base = base.drop(labels=["value_x", "value_y"], axis='columns')
base = base.sort_values(by=['policy_id', 'instrument'])

df = pd.merge(base, policies_filtered, how='left', on='policy_id')[['policy_id', 'instrument', 'sector',
                                                                    'policy_start_date_analysis',
                                                                    'policy_country_iso_code', 'em_share']]

prevalence = pd.DataFrame()

for year in range(2000, 2020):
    df_temp = df[df['policy_start_date_analysis'] <= year]

    prevalence_temp = df_temp.groupby(['sector', 'instrument'])['policy_country_iso_code'].nunique().reset_index()
    prevalence_temp['year'] = year

    prevalence = pd.concat([prevalence, prevalence_temp], axis=0)

prevalence.to_csv(r'results/analysis_prevalence.csv')
