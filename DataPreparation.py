import numpy as np
import pandas as pd
from pandas import DataFrame

# <editor-fold desc="Imports data">

# All data is available in the project folder

df_policies = pd.read_csv(r"data\DatabaseFinal.csv")
df_sectors = pd.read_csv(r"data\Sectors.csv")
df_instruments = pd.read_csv(r"data\PolicyInstruments.csv")
df_code = pd.read_csv(r"data\Code.csv")
df_countries = pd.read_csv(r"data\Countries.csv")

df_temp = df_policies.copy(deep=True)  # defining the work dataset
# </editor-fold>

# <editor-fold desc="Replaces strings to make data more treatable">

# Updating string names with odd characters
df_temp['Policy[Type of policy instrument]'] = \
    df_temp['Policy[Type of policy instrument]'].str.replace("public/private", "public or private")

df_temp['Policy[Type of policy instrument]'] = \
    df_temp['Policy[Type of policy instrument]'].str.replace("Research & Development and Deployment (RD&D)", "RD&D")

df_temp['Policy[Sector name]'] = \
    df_temp['Policy[Sector name]'].str.replace("Waste (CH4)", "Waste CH4")

df_temp['Policy[Sector name]'] = \
    df_temp['Policy[Sector name]'].str.replace("public/private", "public or private")

# </editor-fold> wit with

# <editor-fold desc="Creates sector and policy instrument columns">

# Creating boolean sector columns to allow for analysis that require 'wide' data
# This step also extracts information from the 'Sector name'
df_temp['GeneralSector'] = df_temp['Policy[Sector name]'].str.contains(
    "General")

df_temp['ElectricitySector'] = df_temp['Policy[Sector name]'].str.contains(
    r"Electricity\s+and\s+heat|"
    r"Nuclear|"
    r"Coal|"
    r"CCS|"
    r"Gas|"
    r"Oil|"
    r"Renewables", case=False)

df_temp['IndustrySector'] = df_temp['Policy[Sector name]'].str.contains(
    r"Industry|"
    r"Negative\s+emissions|"
    r"Industrial\s+process\s+CO2|"
    r"Industrial\s+energy\s+related|"
    r"Fossil\s+fuel\s+exploration\s+and\s+production|"
    r"Industrial\s+N2O|"
    r"Fluorinated\s+gases|"
    r"Waste\s+CH4", case=False)

df_temp['BuildingsSector'] = df_temp['Policy[Sector name]'].str.contains(
    r"Buildings|"
    r"Construction|"
    r"Appliances|"
    r"Hot\s+water\s+and\s+cooking|"
    r"Heating\s+and\s+cooling", case=False)

df_temp['TransportSector'] = df_temp['Policy[Sector name]'].str.contains(
    r"Transport|"
    r"Low-emissions\s+mobility|"
    r"Public\s+transport|"
    r"Light\s+duty\s+vehicles|"
    r"Shipping|"
    r"Heavy\s+duty\s+vehicles|"
    r"Air|"
    r"Rail", case=False)

df_temp['LandSector'] = df_temp['Policy[Sector name]'].str.contains(
    r"Forestry|"
    r"Agriculture\s+and\s+forestry|"
    r"Agricultural\s+CH4|"
    r"Agricultural\s+N2O|"
    r"Agricultural\s+CO2")

# Creating boolean PolicyInstrument columns to allow for analysis that require 'wide' data
# This step also extracts information from the col Sectorname, which is now not really accessible

df_temp['DirectInvestment'] = df_temp['Policy[Type of policy instrument]'].str.contains(
    r"Direct\s+investment|"
    r"Funds\s+to\s+sub-national\s+governments|"
    r"Infrastructure\s+investments|"
    r"Procurement\s+rules|"
    r"RD&D\s+funding", case=False)

df_temp['FiscalorFinancialIncentives'] = df_temp['Policy[Type of policy instrument]'].str.contains(
    r"Fiscal\s+or\s+financial\s+incentives|"
    r"Economic\s+Instruments|"
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

df_temp['Market-basedInstruments'] = df_temp['Policy[Type of policy instrument]'].str.contains(
    r"Market-based\s+instruments|"
    r"GHG\s+emissions\s+allowances|"
    r"GHG\s+emission\s+reduction\s+crediting\s+and\s+offsetting\s+mechanism|"
    r"Green\s+certificates|"
    r"White\s+certificates", case=False)

df_temp['CodesStandards'] = df_temp['Policy[Type of policy instrument]'].str.contains(
    r"Codes\s+and\s+standards|"
    r"Building\s+codes\s+and\s+standards|"
    r"Product\s+Standards|"
    r"Sectoral\s+Standards|"
    r"Industrial\s+air\s+pollution\s+standards|"
    r"Vehicle\s+fuel-economy\s+and\s+emissions\s+standards|"
    r"Vehicle\s+air\s+pollution\s+standards", case=False)

df_temp['OtherRegulatoryInstruments'] = df_temp['Policy[Type of policy instrument]'].str.contains(
    r"Regulatory Instruments|"
    r"Auditing|"
    r"Monitoring|"
    r"Obligation\s+schemes|"
    r"Other\s+mandatory\s+requirements", case=False)

df_temp['RDD'] = df_temp['Policy[Type of policy instrument]'].str.contains(
    r"RD&D|"
    r"Research\s+programme|"
    r"Technology\s+deployment\s+and\s+diffusion|"
    r"Technology\s+development|"
    r"Demonstration\s+project", case=False)

df_temp['InformationEducation'] = df_temp['Policy[Type of policy instrument]'].str.contains(
    r"Information\s+and+\s+education|"
    r"Performance\s+label|"
    r"Comparison\s+label|"
    r"Endorsement\s+label|"
    r"Advice\s+or\s+aid\s+in\s+implementation|"
    r"Information\s+provision|"
    r"Professional\s+training\s+and\s+qualification", case=False)

df_temp['PolicySupport'] = df_temp['Policy[Type of policy instrument]'].str.contains(
    r"Policy\s+support|"
    r"Institutional\s+creation|"
    r"Strategic\s+planning", case=False)

df_temp['VoluntaryApproaches'] = df_temp['Policy[Type of policy instrument]'].str.contains(
    r"Voluntary\s+Approaches|"
    r"Negotiated\s+agreements|"
    r"Public\s+voluntary\s+schemes|"
    r"Unilateral\s+commitments", case=False)

df_temp['BarrierRemoval'] = df_temp['Policy[Type of policy instrument]'].str.contains(
    r"Net\s+metering|"
    r"Removal\s+of\s+fossil\s+fuel\s+subsidies|"
    r"Removal\s+of\s+split\s+incentives|"
    r"Grid\s+access\s+and\s+priority\s+for\s+renewables", case=False)

df_temp['ClimateStrategy'] = df_temp['Policy[Type of policy instrument]'].str.contains(
    r"Formal\s+&\s+legally\s+binding\s+climate\s+strategy|"
    r"Political\s+&\s+non-binding\s+climate\s+strategy|"
    r"Coordinating\s+body\s+for\s+climate\s+strategy|"
    r"Climate\s+strategy", case=False)

df_temp['Target'] = df_temp['Policy[Type of policy instrument]'].str.contains(
    r"Target|"
    r"Energy\s+efficiency\s+target|"
    r"GHG\s+reduction\s+target|"
    r"Renewable\s+energy\s+target", case=False)

# </editor-fold>

# filtering data to include policies with national jurisdiction
# Policies that are no longer implemented but should be considered in the years 2000 and 2010 or are implemented
# we also filter policies with Sector and/or PolicyInstrument = NaN
# Pol = Policies

# Counting number of missing values per columns
share_missing_before = df_temp.isna().sum() / df_temp.count().max()

df_PolWide: DataFrame = df_temp[
    (df_temp['Policy[Jurisdiction]'] == 'Country') &
    (df_temp['Policy[Date of decision]'] != 0) &
    (df_temp['Policy[Date of decision]'] < 2020) &
    (df_temp['Policy[Type of policy instrument]'].notnull()) &
    (df_temp['Policy[Sector name]'].notnull()) &
    ((df_temp['Policy[Implementation state]'] == 'Implemented') |
     ((df_temp['2010in'] == True) & (df_temp['2010certain'] == "yes")) |
     ((df_temp['2000in'] == True) & (df_temp['2000certain'] == "yes")))]

# removing EU member states
df_PolWide = df_PolWide[~df_PolWide['Policy[Country]'].isin(['Germany',
                                                             'France',
                                                             'Italy',
                                                             'United Kingdom'])]

# Dropping unnecessary columns
df_PolWide = df_PolWide.drop(columns=['Title',
                                      'Policy[Jurisdiction]',
                                      'Policy[Name of policy]',
                                      'Policy[Supranational region]',
                                      'Policy[Subnational region or state]',
                                      'Policy[City or local]',
                                      'Policy[Policy description]',
                                      'Policy[Policy stringency]',
                                      'Policy[Start date of implementation]',
                                      'Policy[End date of implementation]',
                                      'Policy[High Impact]',
                                      'Policy[Policy Objective]',
                                      'Policy[Source or references]',
                                      'ImpactIndicatorSubObject[Comments]',
                                      'ImpactIndicatorSubObject[Name of impact indicator]',
                                      'ImpactIndicatorSubObject[Value]',
                                      'ImpactIndicatorSubObject[Base_year]',
                                      'ImpactIndicatorSubObject[Target_year]'])

# Changing data types
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
df_PolWide['Policy[Country]'] = df_PolWide['Policy[Country]'].astype('category')
df_PolWide['Policy[Type of policy instrument]'] = df_PolWide['Policy[Type of policy instrument]'].astype('category')
df_PolWide['Policy[Sector name]'] = df_PolWide['Policy[Sector name]'].astype('category')
df_PolWide['Policy[Policy type]'] = df_PolWide['Policy[Policy type]'].astype('category')

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
tst_nopolicyinstrument.to_csv(r'results\tst_nopolicyinstrument.csv',
                              encoding='utf-8',
                              index=True)