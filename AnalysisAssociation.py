from AnalysisIPCC import results_prevalence
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

df_association_input = results_prevalence.fillna(0)
df_association_base = df_association_input.iloc[:, 0:3]

df_association_data = df_association_input.iloc[:, 3:8]
df_association_data[df_association_data > 0] = 1
df_association_data.astype(int)

df_association = pd.concat([df_association_base, df_association_data], axis=1)

# Analysis for 2020 using policy instruments for association rule

df_present = df_association.drop(columns=['2000', '2005', '2020', '2015'])
df_present_ready = pd.pivot_table(df_present,
                                  values='2010',
                                  index=['Sector', 'CountryCPDB'],
                                  columns='PolicyInstrument',
                                  fill_value=0)

df_present_ready.drop(columns='AnyPolicyInstrument', inplace=True)

frequent_itemsets = apriori(df_present_ready, min_support=0.05, use_colnames=True)
rules = association_rules(frequent_itemsets,metric='lift', min_threshold=1)
rules = rules.sort_values(by='lift', ascending=False)

market_rules = rules[rules['consequents'] == frozenset({'Market-basedInstruments'})]
