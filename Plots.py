# import seaborn as sns
# import matplotlib.pyplot as plt
# import numpy as np
#
# from AnalysisIPCC import df_ipccREStidy
# from DataPreparation import df_temp
# res = df_ipccREStidy[df_ipccREStidy['Sector'] != 'GeneralSector']
#
# sns.set(style="whitegrid",
#         palette='Blues_d',
#         font='Arial',
#         font_scale=2)
#
# grid = sns.FacetGrid(data=res.query(('period  not in ["2005", "2015"]')),
#                      col='Sector',
#                      col_order=['ElectricitySector', 'IndustrySector',
#                                 'BuildingsSector', 'TransportSector', 'LandSector'],
#                      row='period',
#                      height=4, aspect=1.5,
#                      margin_titles=False,
#                      sharex=True)
#
# map = grid.map(sns.barplot, 'emissions', 'PolicyInstrument', estimator=sum, ci=None,
#          palette='Blues_d',
#          order=['AnyPolicyInstrument','DirectInvestment','FiscalorFinancialIncentives', 'Market-basedInstruments',
#                                    'CodesStandards', 'VoluntaryApproaches'])
#
# grid.set_axis_labels(x_var='Share of G20 emissions', y_var="")
# grid.set_titles("{col_name} | {row_name}")
# grid.set(xticks=[0.0,0.25,0.50,0.75,1.0],xlim=(0,1))
#
# plt.show()
#
# # <editor-fold desc="Check of created variables">
#
# stats_sector = df_temp[df_temp.columns[26:32]].describe()
# sectors = stats_sector.columns
# coverage_sector = 1 - stats_sector.iloc[3] / stats_sector.iloc[0]
#
# # Analysing policy instruments
#
# stats_PI = df_temp[df_temp.columns[32:44]].describe()
# PIs = stats_PI.columns
# coverage_PI = 1 - stats_PI.iloc[3] / stats_PI.iloc[0]
#
# # plot
# # creating a reusable bar plot
#
# # defining the figure
# fig1, axs = plt.subplots(1, 2)
#
# # Chart content
# axs[0].bar(sectors, coverage_sector)
# axs[1].bar(PIs, coverage_PI, width=0.35, color='grey')
#
# # Chart titles
# axs[0].set_title('Sectors')
# axs[1].set_title('Policy instruments')
#
# # Chart labels
# # axs[0].set_xlabel('Placeholder')
# # axs[1].set_xlabel('Placeholder')
#
# # Chart ticklabels
# axs[0].set_xticklabels(sectors, rotation=45, horizontalalignment='right')
# axs[1].set_xticklabels(PIs, rotation=45, horizontalalignment='right')
#
# fig1.show()
# # </editor-fold>