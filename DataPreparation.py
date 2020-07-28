import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame

# <editor-fold desc="Imports data">

# All data is available in the project folder

df_policies = pd.read_csv(r"data\DatabaseJun2020.csv")
df_sectors = pd.read_csv(r"data\Sectors.csv")
df_instruments = pd.read_csv(r"data\PolicyInstruments.csv")
df_code = pd.read_csv(r"data\Code.csv")
df_countries = pd.read_csv(r"data\Countries.csv")

df_temp = df_policies.copy(deep=True)  # defining the work dataset
df_temp.index.name = 'PolicyID'  # defining the policy ID, which is the unique identifier for each policy

# </editor-fold>

# <editor-fold desc="Replaces strings to make data more treatable">

# Correcting strings

# Updading string names with odd characters
df_temp['Typeofpolicyinstrument'] = df_temp['Typeofpolicyinstrument'].str.replace("public/private", "public or private")
df_temp['Sectorname'] = df_temp['Sectorname'].str.replace("public/private", "public or private")
df_temp['Typeofpolicyinstrument'] = df_temp['Typeofpolicyinstrument'].str.replace("Research & Development and "
                                                                                  "Deployment (RD&D)",
                                                                                  "RD&D")

# Updating Policy sector to include most recent conventions
df_temp['Sectorname'] = df_temp['Sectorname'].str.replace("Electro-mobility", "Low-emissions mobility")
df_temp['Sectorname'] = df_temp['Sectorname'].str.replace("Waste (CH4)", "Waste CH4")

# Updating EU name to something useful
df_temp['Country'] = df_temp['Country'].str.replace(
    "European Union, Austria, Belgium, Bulgaria, Croatia, Cyprus, Czech Republic, Denmark, Estonia, Finland, France, "
    "Germany, Greece, Hungary, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, Netherlands, Poland, Portugal, "
    "Romania, Slovakia, Slovenia, Spain, Sweden, United Kingdom",
    "European Union (28)")

# Updating Policy type to include most recent conventions
df_temp['Policytype'] = df_temp['Policytype'].str.replace("Changing activity",
                                                          "Energy service demand reduction and resource efficiency")
df_temp['Policytype'] = df_temp['Policytype'].str.replace("Nuclear or CCS or fuel switch",
                                                          "Other low-carbon technologies and fuel switch")

# Updating EU jurisdiction from Supranational region to country to make filtering straightforward
df_temp['Jurisdiction'] = np.where(df_temp['Country'] == 'European Union (28)',
                                   df_temp['Jurisdiction'].str.replace("Supranational region", "Country"),
                                   df_temp['Jurisdiction'])

# </editor-fold> wit with

# <editor-fold desc="Creates sector and policy instrument columns">

# Creating boolean sector columns to allow for analysis that require 'wide' data
# This step also extracts information from the col Sectorname, which is now not really accessible
df_temp['GeneralSector'] = df_temp['Sectorname'].str.contains(
    "General")

df_temp['ElectricitySector'] = df_temp['Sectorname'].str.contains(
    r"Electricity\s+and\s+heat|"
    r"Nuclear|"
    r"Coal|"
    r"CCS|"
    r"Gas|"
    r"Oil|"
    r"Renewables", case=False)

df_temp['IndustrySector'] = df_temp['Sectorname'].str.contains(
    r"Industry|"
    r"Negative\s+emissions|"
    r"Industrial\s+process\s+CO2|"
    r"Industrial\s+energy\s+related|"
    r"Fossil\s+fuel\s+exploration\s+and\s+production|"
    r"Industrial\s+N2O|"
    r"Fluorinated\s+gases|"
    r"Waste\s+CH4", case=False)

df_temp['BuildingsSector'] = df_temp['Sectorname'].str.contains(
    r"Buildings|"
    r"Construction|"
    r"Appliances|"
    r"Hot\s+water\s+and\s+cooking|"
    r"Heating\s+and\s+cooling", case=False)

df_temp['TransportSector'] = df_temp['Sectorname'].str.contains(
    r"Transport|"
    r"Low-emissions\s+mobility|"
    r"Public\s+transport|"
    r"Light\s+duty\s+vehicles|"
    r"Shipping|"
    r"Heavy\s+duty\s+vehicles|"
    r"Air|"
    r"Rail", case=False)

df_temp['LandSector'] = df_temp['Sectorname'].str.contains(
    r"Forestry|"
    r"Agriculture\s+and\s+forestry|"
    r"Agricultural\s+CH4|"
    r"Agricultural\s+N2O|"
    r"Agricultural\s+CO2")

# Creating boolean PolicyInstrument columns to allow for analysis that require 'wide' data
# This step also extracts information from the col Sectorname, which is now not really accessible

df_temp['DirectInvestment'] = df_temp['Typeofpolicyinstrument'].str.contains(
    r"Direct\s+investment|"
    r"Funds\s+to\s+sub-national\s+governments|"
    r"Infrastructure\s+investments|"
    r"Procurement\s+rules|"
    r"RD&D\s+funding", case=False)

df_temp['FiscalorFinancialIncentives'] = df_temp['Typeofpolicyinstrument'].str.contains(
    r"Fiscal\s+or\s+financial\s+incentives|"
    r"CO2\s+taxes|"
    r"Energy\s+and\s+other\s+taxes|"
    r"Feed-in\s+tariffs\s+or\s+premiums|"
    r"Grants\s+and\s+subsidies|"
    r"Loans|"
    r"Tax\s+relief|"
    r"User\s+changes|"
    r"Tendering\s+schemes|"
    r"Retirement\s+premium|"
    r"User\s+charges", case=False)

df_temp['Market-basedInstruments'] = df_temp['Typeofpolicyinstrument'].str.contains(
    r"Market-based\s+instruments|"
    r"GHG\s+emissions\s+allowances|"
    r"GHG\s+emission\s+reduction\s+crediting\s+and\s+offsetting\s+mechanism|"
    r"Green\s+certificates|"
    r"White\s+certificates", case=False)

df_temp['CodesStandards'] = df_temp['Typeofpolicyinstrument'].str.contains(
    r"Codes\s+and\s+standards|"
    r"Building\s+codes\s+and\s+standards|"
    r"Product\s+Standards|"
    r"Sectoral\s+Standards|"
    r"Vehicle\s+fuel-economy\s+and\s+emissions\s+standards", case=False)

df_temp['OtherRegulatoryInstruments'] = df_temp['Typeofpolicyinstrument'].str.contains(
    r"Auditing|"
    r"Monitoring|"
    r"Obligation\s+schemes|"
    r"Other\s+mandatory\s+requirements", case=False)

df_temp['RDD'] = df_temp['Typeofpolicyinstrument'].str.contains(
    r"RD&D|"
    r"Research\s+programme|"
    r"Technology\s+deployment\s+and\s+diffusion|"
    r"Technology\s+development|"
    r"Demonstration\s+project", case=False)

df_temp['InformationEducation'] = df_temp['Typeofpolicyinstrument'].str.contains(
    r"Information\s+and+\s+education|"
    r"Performance\s+label|"
    r"Comparison\s+label|"
    r"Endorsement\s+label|"
    r"Advice\s+or\s+aid\s+in\s+implementation|"
    r"Information\s+provision|"
    r"Professional\s+training\s+and\s+qualification", case=False)

df_temp['PolicySupport'] = df_temp['Typeofpolicyinstrument'].str.contains(
    r"Policy\s+support|"
    r"Institutional\s+creation|"
    r"Strategic\s+planning", case=False)

df_temp['VoluntaryApproaches'] = df_temp['Typeofpolicyinstrument'].str.contains(
    r"Voluntary\s+Approaches|"
    r"Negotiated\s+agreements|"
    r"Public\s+voluntary\s+schemes|"
    r"Unilateral\s+commitments", case=False)

df_temp['BarrierRemoval'] = df_temp['Typeofpolicyinstrument'].str.contains(
    r"Net\s+metering|"
    r"Removal\s+of\s+fossil\s+fuel\s+subsidies|"
    r"Removal\s+of\s+split\s+incentives|"
    r"Grid\s+access\s+and\s+priority\s+for\s+renewables", case=False)

df_temp['ClimateStrategy'] = df_temp['Typeofpolicyinstrument'].str.contains(
    r"Formal\s+&\s+legally\s+binding\s+climate\s+strategy|"
    r"Political\s+&\s+non-binding\s+climate\s+strategy|"
    r"Coordinating\s+body\s+for\s+climate\s+strategy", case=False)

df_temp['Target'] = df_temp['Typeofpolicyinstrument'].str.contains(
    r"Target|"
    r"Energy\s+efficiency\s+target|"
    r"GHG\s+reduction\s+target|"
    r"Renewable\s+energy\s+target", case=False)

# </editor-fold>

# filtering data to include only implemented policies, with national jurisdiction
# we also filter policies with Sector and/or PolicyInstrument = NaN
# Pol = Policies

# Counting number of missing values per columns
share_missing_before = df_temp.isna().sum() / df_temp.count().max()
# Now we will remove all relevant missing
# This could be delegated to an intern, to check the actual values of these missings

df_PolWide: DataFrame = df_temp[
    (df_temp['Jurisdiction'] == 'Country') &
    (df_temp['Dateofdecision'] != 0) &
    (df_temp['Typeofpolicyinstrument'].notnull()) &
    (df_temp['Sectorname'].notnull()) &
    (df_temp['Implementationstate'] == 'Implemented')]

# removing EU member states
df_PolWide = df_PolWide[~df_PolWide['Country'].isin(['Germany',
                                                     'France',
                                                     'Italy',
                                                     'United Kingdom'])]

# Dropping unnecessary columns
df_PolWide = df_PolWide.drop(columns=['Enddateofimplementation',
                                      'Highlight',
                                      'Policystringency',
                                      'Source',
                                      'Supranationalregion',
                                      'Title',
                                      'Cityorlocal',
                                      'Subnationalregionorstate',
                                      'Policydescription',
                                      'ImpactIndicatorSubObject[Comments]',
                                      'ImpactIndicatorSubObject[Nameofimpactindicator]',
                                      'ImpactIndicatorSubObject[Value]',
                                      'ImpactIndicatorSubObject[Base_year]',
                                      'ImpactIndicatorSubObject[Target_year]',
                                      'Startdateofimplementation'
                                      ])

# I use this to add the index as a column, personal preference
df_PolWide.reset_index(inplace=True)

# Changing data types as currently it is a mess
# All created variables as Booleans
for col in ['GeneralSector',
            'ElectricitySector', 'IndustrySector', 'BuildingsSector',
            'TransportSector', 'LandSector', 'DirectInvestment',
            'FiscalorFinancialIncentives', 'Market-basedInstruments',
            'CodesStandards', 'OtherRegulatoryInstruments', 'InformationEducation',
            'PolicySupport', 'VoluntaryApproaches', 'BarrierRemoval',
            'ClimateStrategy', 'Target', 'RDD']:
    df_PolWide[col] = df_PolWide[col].astype(bool)

# All categories as categories
df_PolWide['Country'] = df_PolWide['Country'].astype('category')
df_PolWide['Typeofpolicyinstrument'] = df_PolWide['Typeofpolicyinstrument'].astype('category')
df_PolWide['Sectorname'] = df_PolWide['Sectorname'].astype('category')
df_PolWide['Policytype'] = df_PolWide['Policytype'].astype('category')

# Testing for policy document not considered in any policy instrument type

df_PolWide['AnyPolicyInstrument'] = np.where(((df_PolWide['DirectInvestment'] == True) |
                                              (df_PolWide['FiscalorFinancialIncentives'] == True) |
                                              (df_PolWide['Market-basedInstruments'] == True) |
                                              (df_PolWide['CodesStandards'] == True) |
                                              (df_PolWide['VoluntaryApproaches'] == True) |
                                              (df_PolWide['OtherRegulatoryInstruments'] == True) |
                                              (df_PolWide['RDD'] == True) |
                                              (df_PolWide['InformationEducation'] == True) |
                                              (df_PolWide['PolicySupport'] == True) |
                                              (df_PolWide['BarrierRemoval'] == True) |
                                              (df_PolWide['ClimateStrategy'] == True) |
                                              (df_PolWide['Target'] == True)),
                                             True,
                                             False)

tst_nopolicyinstrument = df_PolWide[df_PolWide['AnyPolicyInstrument'] == False]
tst_nopolicyinstrument.to_csv(r'C:\Users\HP\PycharmProjects\CPDB\data\tst_nopolicyinstrument.csv',
                              encoding='utf-8',
                              index=True)