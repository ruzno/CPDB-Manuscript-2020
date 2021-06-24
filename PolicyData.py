# CLIMATE POLICY DATABASE DATA PREPARATION
# This script prepares the Climate Policy Database data
# It includes filtering, adjusting data types and creating boolean columns for sectors and instruments

# Author:   Leonardo Nascimento
# Date:     June 2021
# Contact:  l.nascimento@newclimate.org

import numpy as np
import pandas as pd

from pandas import DataFrame
from functions_policy_indicators import *

# all data is available in the project folder
policies_import = pd.read_csv('data/policy_database/source_database_23_06_2021.csv')

# defines latest analysis year, this refers to policy adoption cut-off date
range_end = 2019
range_start = 1990

# creates a copy so changes can be compared to the import
df_temp = policies_import.copy(deep=True)

# --------------------------------------------------------------------
# DATA CLEANING: drops columns and adjust data types
# --------------------------------------------------------------------

# removes columns that are  irrelevant to the analysis
df_temp = df_temp.drop(columns=['policy_title', 'policy_name',
                                'policy_supranational_region',
                                'policy_subnational_region_or_state', 'policy_city',
                                'policy_description', 'policy_stringency',
                                'policy_objective', 'policy_source_or_references',
                                'impact_indicator_comments',
                                'impact_indicator_name_of_impact_indicator', 'impact_indicator_value',
                                'impact_indicator_base_year', 'impact_indicator_target_year'])

# removes entries that are irrelevant to the analysis
df_temp = df_temp[
    (df_temp['policy_jurisdiction'] == 'Country') &
    (df_temp['policy_type_of_policy_instrument'].notnull()) &
    (df_temp['policy_sector_name'].notnull())]

# --------------------------------------------------------------------
# DATA PREPARATION: creates new columns necessary for the analysis
# --------------------------------------------------------------------

# Estimates the first year for the policy to be considered in the analysis
# For policies with adoption date, the first year is the start date
# For policies without the adoption date but with implementation date, the start date is the implementation date

condition = [df_temp['policy_date_of_decision'].notna(),
             df_temp['policy_start_date_of_implementation'].notna()]

result = [df_temp['policy_date_of_decision'],
          df_temp['policy_start_date_of_implementation']]

df_temp['policy_start_date_analysis'] = np.select(condition, result, default=0)

df_temp = df_temp[df_temp['policy_start_date_analysis'] != 0]
assert df_temp[df_temp['policy_start_date_analysis'] == 0].empty

# Estimates the last year for the policy to be considered in the analysis
# For policies with end date, the last year is the end date
# For policies in force, the final date to be considered is the last analysis year

condition = [df_temp['policy_end_date_of_implementation'].notna(),
             df_temp['policy_implementation_state'] == 'In force']

result = [df_temp['policy_end_date_of_implementation'],
          range_end]

df_temp['policy_end_date_analysis'] = np.select(condition, result, default=0)

df_temp = df_temp[df_temp['policy_end_date_analysis'] != 0]
assert df_temp[df_temp['policy_end_date_analysis'] == 0].empty

# adjusts data types
list_category_columns = ['policy_country', 'policy_country_iso_code', 'policy_jurisdiction',
                         'policy_type_of_policy_instrument', 'policy_sector_name', 'policy_type',
                         'policy_implementation_state', 'policy_high_impact']

list_numeric_columns = ['policy_date_of_decision', 'policy_end_date_of_implementation',
                        'policy_start_date_of_implementation', 'policy_id', 'policy_end_date_analysis',
                        'policy_start_date_analysis']

for col in list_category_columns:
    df_temp[col] = df_temp[col].astype('category')

for col in list_numeric_columns:
    df_temp[col] = df_temp[col].astype('Int32')

# ---------------------------------------
# INDICATORS: creates main categorisation indicators
# See all functions in python module functions_policy_indicators.py
# ---------------------------------------

# creates boolean PolicyInstrument columns
# this step extracts information from the column 'policy instrument'
df_temp = add_pi(df_temp)

# Calls function that adds policy options to the table
df_temp = add_policy_options(df_temp)

# creates boolean sector columns
# this step extracts information from the 'sector name'
df_temp = add_sec(df_temp)

# calculates fuzziness for each individual policy
df_temp = add_f(df_temp)

# calculates sector specificity for each individual policy
df_temp = add_sp(df_temp)

# changes column types
list_boolean_columns = ['GeneralSector', 'ElectricitySector',
                        'IndustrySector', 'BuildingsSector', 'TransportSector', 'LandSector',
                        'DirectInvestment', 'FiscalFinancialIncentives',
                        'Market-basedInstruments', 'CodesStandards',
                        'OtherRegulatoryInstruments', 'RDD', 'InformationEducation',
                        'PolicySupport', 'VoluntaryApproaches', 'BarrierRemoval',
                        'ClimateStrategy', 'Target']

for col in list_boolean_columns:
    df_temp[col] = df_temp[col].astype(bool)

policies_tidy_clean: DataFrame = df_temp.copy(deep=True)
policies_tidy_clean.to_csv(r'results/treated_policy_database.csv', index=False)

# ---------------------------------------
# INDICATORS: creates main categorisation indicators
# See all functions in python module functions_policy_indicators.py
# ---------------------------------------

policies_aggYear_withIndicators = pd.DataFrame()

# this loop will aggregate the policy information per country and per year
# this is necessary because some variables, such as number of policies, only make sense when aggregated by country
# I use the opportunity to add the time element, aggregating only policies that fit the year of interest


for year in range(range_start, range_end + 1):
    df_temp1 = df_temp[((df_temp['policy_start_date_analysis'] >= range_start) &  # change here, check if error
                        (df_temp['policy_end_date_analysis'] >= year) &
                        (df_temp['policy_start_date_analysis'] <= year))]

    # -----------------------------------------------------------------------------------------
    # GENERAL INDICATORS - N, Sp, F
    # -----------------------------------------------------------------------------------------

    # Aggregates these three variables per country, as they can be directly calculated
    df_results = df_temp1.groupby('policy_country_iso_code').agg({
        'policy_id': 'nunique',
        'F': 'mean',
        'Sp': 'mean'})

    df_results = df_results.rename(columns={'policy_id': 'N'})

    # -----------------------------------------------------------------------------------------
    # COVERAGE - C
    # -----------------------------------------------------------------------------------------

    # each country will adopt a share of the policy menu, we calculate coverage using this share
    # total number of policy options is 50
    # coverage is number of policy options in place divided by the total

    # Creates list with information on the columns used to aggregate the data
    # Creates list with all columns that contains boolean information about the prevalence of policy options

    id_vars = ['policy_id', 'policy_country_iso_code']
    value_vars = ['g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'eh1', 'eh2', 'eh3', 'eh4', 'eh5', 'eh6',
                  'eh7', 'eh8', 'eh9', 'eh10', 'i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7',
                  'i8', 'i9', 'i10', 'i11', 'i12', 'i13', 'i14', 'b1', 'b2', 'b3', 'b4',
                  'b5', 'b6', 'lt1', 'lt2', 'lt3', 'lt4', 'lt5', 'lt6', 'lt7', 'af1',
                  'af2', 'af3', 'af4', 'af5', 'af6']

    df_C = pd.melt(df_temp1, id_vars=id_vars, value_vars=value_vars)

    df_C['value'] = df_C['value'].astype('Int32')
    df_C = df_C[df_C['value'] != 0]

    df_C = df_C.groupby(['policy_country_iso_code']).agg({
        'policy_id': 'nunique',
        'variable': 'nunique'
    })

    # N_options is the number of policy options covered by the country
    # N_policies_matrix is # of policies that fit the policy matrix (lower than total N)
    # C is the share of policy options covered by the country divided by the total

    df_C['C'] = df_C['variable'] / len(value_vars)
    df_C = df_C.rename(columns={"policy_id": "N_policies_matrix", "variable": "N_options"})

    # updates the results to include coverage
    df_results = pd.merge(df_results, df_C, how='outer', left_index=True, right_index=True)

    # -----------------------------------------------------------------------------------------
    # BALANCE - B
    # -----------------------------------------------------------------------------------------

    # Represents the probability that randomly picked policies from a policy mix are of the same instrument type

    # TODO: probably better to reshape database and aggregated instead of doing column calculations

    id_vars = ['policy_id', 'policy_country_iso_code']

    # I removed policy support here. This variable is currently meaningless
    value_vars = ['FiscalFinancialIncentives', 'Market-basedInstruments',
                  'CodesStandards', 'OtherRegulatoryInstruments', 'RDD',
                  'InformationEducation', 'VoluntaryApproaches',
                  'BarrierRemoval', 'ClimateStrategy', 'Target', 'DirectInvestment']

    # df_B = pd.melt(policies_tidy, id_vars=id_vars, value_vars=value_vars)

    df_1 = df_temp1[id_vars]
    df_2 = df_temp1[value_vars]

    df_B = pd.concat([df_1, df_2], axis=1)

    df_B = df_B.groupby(['policy_country_iso_code']).agg({
        'FiscalFinancialIncentives': 'sum',
        'Market-basedInstruments': 'sum',
        'CodesStandards': 'sum',
        'OtherRegulatoryInstruments': 'sum',
        'RDD': 'sum',
        'InformationEducation': 'sum',
        'VoluntaryApproaches': 'sum',
        'BarrierRemoval': 'sum',
        'ClimateStrategy': 'sum',
        'Target': 'sum',
        'DirectInvestment': 'sum'

    })

    df_B['SUM_instruments'] = (df_B['FiscalFinancialIncentives'] + df_B['Market-basedInstruments'] +
                               df_B['CodesStandards'] + df_B['OtherRegulatoryInstruments'] + df_B['RDD'] +
                               df_B['InformationEducation'] + df_B['VoluntaryApproaches'] +
                               df_B['BarrierRemoval'] + df_B['ClimateStrategy'] + df_B['Target'] +
                               df_B['DirectInvestment'])

    df_B['numerator'] = ((df_B['FiscalFinancialIncentives'] * (df_B['FiscalFinancialIncentives'] - 1)) + (
            df_B['Market-basedInstruments'] * (df_B['Market-basedInstruments'] - 1)) + (
                                 df_B['CodesStandards'] * (df_B['CodesStandards'] - 1)) + (
                                 df_B['OtherRegulatoryInstruments'] * (df_B['OtherRegulatoryInstruments'] - 1)) + (
                                 df_B['RDD'] * (df_B['RDD'] - 1)) + (
                                 df_B['InformationEducation'] * (df_B['InformationEducation'] - 1)) + (
                                 df_B['VoluntaryApproaches'] * (df_B['VoluntaryApproaches'] - 1)) + (
                                 df_B['BarrierRemoval'] * (df_B['BarrierRemoval'] - 1)) + (
                                 df_B['ClimateStrategy'] * (df_B['ClimateStrategy'] - 1)) + (
                                 df_B['Target'] * (df_B['Target'] - 1)) + (
                                 df_B['DirectInvestment'] * (df_B['DirectInvestment'] - 1)))

    df_B['denominator'] = (df_B['SUM_instruments'] * (df_B['SUM_instruments'] - 1))

    df_B['B'] = 1 - df_B['numerator'] / df_B['denominator']

    df_results = pd.merge(df_results, df_B, how='outer', left_index=True, right_index=True)
    df_results['year'] = year

    policies_aggYear_withIndicators = pd.concat([policies_aggYear_withIndicators, df_results])

policies_aggYear_withIndicators = policies_aggYear_withIndicators[
    ['year', 'N', 'F', 'Sp', 'B', 'C', 'N_policies_matrix', 'N_options',
     'FiscalFinancialIncentives', 'Market-basedInstruments',
     'CodesStandards', 'OtherRegulatoryInstruments', 'RDD',
     'InformationEducation', 'VoluntaryApproaches',
     'BarrierRemoval', 'ClimateStrategy', 'Target', 'DirectInvestment',
     'SUM_instruments']]

# Reduce the number of policy instrument types based on IPCC AR6 categorisation
# Economic Instruments // Regulatory Instruments // Other Instruments

# Based on policy database categories we define:
# Economic as Fiscal and Financial Instruments + Market-based instruments
# Regulatory as Codes and Standards + Other regulatory
# The remaining instruments are grouped under other
# We remove policy support because this is a default categorisation that at this stage does not support analysis

policy_data = policies_aggYear_withIndicators.copy(deep=True)

policy_data['Economic instruments'] = ((policy_data['FiscalFinancialIncentives']) |
                                       (policy_data['Market-basedInstruments']))

policy_data['Regulatory instruments'] = ((policy_data['OtherRegulatoryInstruments']) |
                                         (policy_data['CodesStandards']))

policy_data['Other instruments'] = ((policy_data['DirectInvestment']) |
                                    (policy_data['InformationEducation']) |
                                    (policy_data['VoluntaryApproaches']) |
                                    (policy_data['ClimateStrategy']) |
                                    (policy_data['Target']))

policy_data['SUM_instruments_IPCC'] = policy_data['Economic instruments'] + policy_data['Regulatory instruments'] + \
                                      policy_data['Other instruments']

list_instruments = ['FiscalFinancialIncentives', 'Market-basedInstruments',
                    'CodesStandards', 'OtherRegulatoryInstruments', 'RDD',
                    'InformationEducation', 'VoluntaryApproaches', 'BarrierRemoval',
                    'ClimateStrategy', 'Target', 'DirectInvestment']

list_instruments_IPCC = ['Economic instruments', 'Regulatory instruments', 'Other instruments']

for col in list_instruments:
    policy_data[col] = policy_data[col] / policy_data['SUM_instruments']

for col in list_instruments_IPCC:
    policy_data[col] = policy_data[col] / policy_data['SUM_instruments_IPCC']

policy_data.reset_index(inplace=True)
policy_data.to_csv(r'results/policy_data.csv', index=False)

