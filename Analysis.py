from DataPreparation import df_PolWide
from DataPreparation import df_countries
import numpy as np
import pandas as pd

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

# <editor-fold desc="ANALYSIS PREVALENCE">

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
                                                                    'Policy[Country]',
                                                                    'Policy[Date of decision]',
                                                                    '2010in',
                                                                    '2010certain',
                                                                    '2000in',
                                                                    '2000certain']]

df_PolCountry = pd.merge(df_PolTidy, df_countries, how='left', left_on='Policy[Country]', right_on='Name in CPDB')

# ANALYSIS PREVALENCE FOR THE IPCC

df2000 = df_PolCountry[df_PolCountry['Policy[Date of decision]'] <= 2000]
df2005 = df_PolCountry[df_PolCountry['Policy[Date of decision]'] <= 2005]
df2010 = df_PolCountry[df_PolCountry['Policy[Date of decision]'] <= 2010]
df2015 = df_PolCountry[df_PolCountry['Policy[Date of decision]'] <= 2015]
df2020 = df_PolCountry[df_PolCountry['Policy[Date of decision]'] <= 2020]

# OPTION 1, based on emissions

prevalence2000 = df2000.groupby(['Sector', 'PolicyInstrument', 'Policy[Country]'])['Share emissions Incl.'].mean()
prevalence2005 = df2005.groupby(['Sector', 'PolicyInstrument', 'Policy[Country]'])['Share emissions Incl.'].mean()
prevalence2010 = df2010.groupby(['Sector', 'PolicyInstrument', 'Policy[Country]'])['Share emissions Incl.'].mean()
prevalence2015 = df2015.groupby(['Sector', 'PolicyInstrument', 'Policy[Country]'])['Share emissions Incl.'].mean()
prevalence2020 = df2020.groupby(['Sector', 'PolicyInstrument', 'Policy[Country]'])['Share emissions Incl.'].mean()

frame = {'2000': prevalence2000,
         '2005': prevalence2005,
         '2010': prevalence2010,
         '2015': prevalence2015,
         '2020': prevalence2020}

r_prevalence = pd.DataFrame(frame)
r_prevalence.to_csv(r'results\results_prevalence.csv', encoding='utf-8', index=True)
r_prevalence.reset_index(inplace=True)

# </editor-fold>
