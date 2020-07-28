from DataPreparation import df_PolWide
from DataPreparation import df_countries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Needs to be adjusted in case we are dealing with all policy instrument types
# This creates the dataframe that will be used to create the IPCC CH13 figure

df_IPCC = df_PolWide.drop(columns=['OtherRegulatoryInstruments',
                                   'RDD',
                                   'InformationEducation',
                                   'PolicySupport',
                                   'BarrierRemoval',
                                   'ClimateStrategy',
                                   'Target'])

df_IPCC['AnyPolicyInstrument'] = np.where(((df_IPCC['DirectInvestment'] == True) |
                                           (df_IPCC['FiscalorFinancialIncentives'] == True) |
                                           (df_IPCC['Market-basedInstruments'] == True) |
                                           (df_IPCC['CodesStandards'] == True) |
                                           (df_IPCC['VoluntaryApproaches'] == True)),
                                          True,
                                          False)

# <editor-fold desc="ANALYSIS PREVALENCE filtered">

# Melting the information on policy instruments into a column
# this will be used to transform the data from wide to tidy
select_instrument = df_IPCC.iloc[:, np.r_[0, 18:24]]  # current code needs this to be edited if n instruments change
melt_instrument = pd.melt(select_instrument, id_vars="PolicyID", value_vars=["DirectInvestment",
                                                                             "FiscalorFinancialIncentives",
                                                                             "Market-basedInstruments",
                                                                             "CodesStandards",
                                                                             "VoluntaryApproaches",
                                                                             "AnyPolicyInstrument"
                                                                             ])
melt_instrument.rename(columns={'variable': 'PolicyInstrument'}, inplace=True)
melt_instrument = melt_instrument[melt_instrument['value'] == True]
melt_instrument = melt_instrument.sort_values(by=['PolicyID'])

# Melting the information on Sectors into a column
# this will be used to transform the data from wide to tidy
select_sector = df_PolWide.iloc[:, np.r_[0, 12:18]]
melt_sector = pd.melt(select_sector, id_vars="PolicyID", value_vars=['GeneralSector', 'ElectricitySector',
                                                                     'IndustrySector', 'BuildingsSector',
                                                                     'TransportSector', 'LandSector'])
melt_sector.rename(columns={'variable': 'Sector'}, inplace=True)
melt_sector = melt_sector[melt_sector['value'] == True]
melt_sector = melt_sector.sort_values(by=['PolicyID'])

# Merging the two melted tables based on the policy ID
base = pd.merge(melt_instrument, melt_sector, how='left', on='PolicyID')
base = base.drop(labels=["value_x", "value_y"], axis='columns')
base = base.sort_values(by=['PolicyID', 'PolicyInstrument'])

# Bring all information necessary from the PolWide table using the PolicyID
df_PolTidy = pd.merge(base, df_PolWide, how='left', on="PolicyID")[['PolicyID',
                                                                    'PolicyInstrument',
                                                                    'Sector',
                                                                    'Country',
                                                                    'Dateofdecision']]

df_PolCountry = pd.merge(df_PolTidy, df_countries, how='left', left_on='Country', right_on='CountryCPDB')

# ANALYSIS PREVALENCE FOR THE IPCC

df2000 = df_PolCountry[df_PolCountry['Dateofdecision'] <= 2000]
df2005 = df_PolCountry[df_PolCountry['Dateofdecision'] <= 2005]
df2010 = df_PolCountry[df_PolCountry['Dateofdecision'] <= 2010]
df2015 = df_PolCountry[df_PolCountry['Dateofdecision'] <= 2015]
df2020 = df_PolCountry[df_PolCountry['Dateofdecision'] <= 2020]

# OPTION 1, based on emissions

prevalence2000 = df2000.groupby(['Sector', 'PolicyInstrument', 'CountryCPDB'])['ShareEmissionsIncl'].mean()
prevalence2005 = df2005.groupby(['Sector', 'PolicyInstrument', 'CountryCPDB'])['ShareEmissionsIncl'].mean()
prevalence2010 = df2010.groupby(['Sector', 'PolicyInstrument', 'CountryCPDB'])['ShareEmissionsIncl'].mean()
prevalence2015 = df2015.groupby(['Sector', 'PolicyInstrument', 'CountryCPDB'])['ShareEmissionsIncl'].mean()
prevalence2020 = df2020.groupby(['Sector', 'PolicyInstrument', 'CountryCPDB'])['ShareEmissionsIncl'].mean()

# OPTION 1, based on count of countries

# prevalence2000 = df2000.groupby(['Sector', 'PolicyInstrument'])['Country_x'].nunique()
# prevalence2005 = df2005.groupby(['Sector', 'PolicyInstrument'])['Country_x'].nunique()
# prevalence2010 = df2010.groupby(['Sector', 'PolicyInstrument'])['Country_x'].nunique()
# prevalence2015 = df2015.groupby(['Sector', 'PolicyInstrument'])['Country_x'].nunique()
# prevalence2020 = df2020.groupby(['Sector', 'PolicyInstrument'])['Country_x'].nunique()

frame = {'2000': prevalence2000,
         '2005': prevalence2005,
         '2010': prevalence2010,
         '2015': prevalence2015,
         '2020': prevalence2020}

results_prevalence = pd.DataFrame(frame)
results_prevalence.to_csv(r'C:\Users\HP\PycharmProjects\CPDB\data\results_prevalence.csv', encoding='utf-8', index=True)
results_prevalence.reset_index(inplace=True)

# To be able to create the table on python the data has to be tidy on the period as well
# This is step is only neccesary if one wants to create the table in Python

# select_period = results_prevalence.iloc[:, 3:8]
# select_period.reset_index(inplace=True)
# melt_period = pd.melt(select_period, id_vars='index', value_vars=['2000', '2005', '2010', '2015', '2020'])
#
# base_period = results_prevalence.iloc[:, 0:2]
# base_period.reset_index(inplace=True)
# base_period = base_period.sort_values(by=['index', 'Sector', 'PolicyInstrument'])
#
# df_ipccREStidy = pd.merge(base_period, melt_period, how='left', left_on='index', right_on='index')
# df_ipccREStidy.rename(columns={'variable': 'period', 'value': 'emissions'}, inplace=True)
# df_ipccREStidy.drop(columns='index', inplace=True)

# </editor-fold>
