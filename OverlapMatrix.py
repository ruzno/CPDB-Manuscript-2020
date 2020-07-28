# from DataPreparation import df_PolWide
# import pandas as pd
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt
#
# # Create an overlap matrix of sectors
#
# sector_input = df_PolWide.iloc[:,np.r_[0,12:18]]
# sector_input.set_index('PolicyID',inplace=True)
#
# for col in sector_input.columns:
#     sector_input[col] = sector_input[col]*1
#
# sector_overlap = sector_input.T.dot(sector_input)
# normalized_sector = (sector_overlap)/sector_overlap.max()
#
# sns.heatmap(normalized_sector, linewidths=.5, annot=True,vmin=0, vmax=0.5)
# plt.show()
#
# # Create an overlap matrix of policy instruments
#
# pi_input = df_PolWide.iloc[:,np.r_[0,18:30]]
# pi_input.set_index('PolicyID',inplace=True)
#
# for col in pi_input.columns:
#     pi_input[col] = pi_input[col]*1
#
# pi_overlap = pi_input.T.dot(pi_input)
# normalized_pi = (pi_overlap)/pi_overlap.max()
#
# sns.set(style="whitegrid",
#         palette='Blues_d',
#         font='Arial',
#         font_scale=1)
# fig, ax = plt.subplots(figsize=(10,8))
#
# sns.heatmap(normalized_pi, linewidths=.5, annot=True, ax=ax,square=True)
# plt.show()