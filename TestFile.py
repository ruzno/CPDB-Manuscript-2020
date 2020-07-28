from DataPreparation import data_ready

x = data_ready[data_ready['VoluntaryApproaches'] == True]

result = x.groupby(['Country', 'Sector']).count()


sns.catplot(x='PolicyID', y='Sector', data=df, height=5,aspect=2)
plt.show()

# <editor-fold desc="Learning scatter catplots">
# tips = sns.load_dataset("tips")
# sns.catplot(x='day', y= 'total_bill', data=tips)
# plt.show()
#
# sns.catplot(x='day', y= 'total_bill', jitter=False, data=tips)
# plt.show()
#
# sns.catplot(x='day', y= 'total_bill', kind='swarm', data=tips)
# plt.show()
#
# sns.catplot(x='day', y= 'total_bill', kind='swarm', hue='sex', data=tips)
# plt.show()
#
# sns.catplot(x='size', y= 'total_bill', kind='swarm', data=tips.query("size != 3"))
# plt.show()
#
# sns.catplot(x='sex', y= 'total_bill', order=['Female','Male'], kind='swarm', data=tips.query("size != 3"))
# plt.show()
#
# sns.catplot(x='total_bill', y= 'day', kind='swarm', hue='sex', legend=False , data=tips)
# plt.legend(loc='upper right', ncol=1)
# plt.show()
# </editor-fold>

# <editor-fold desc="Learning box catplots">
tips = sns.load_dataset('tips')

sns.catplot(x='day', y='total_bill', kind='box',data=tips,height=5,aspect=1.5)
plt.show()

sns.catplot(x='day', y='total_bill', kind='box', data=tips, height=5, aspect=1.5, hue='sex', legend=False)
plt.show()

# tips["weekend"] = tips['day'].isin(['Sat', 'Sun'])
# sns.catplot(x='day', y='total_bill', kind='box', data=tips, height=5, aspect=1.5, hue='weekend', dodge=False)
# plt.show()

sns.catplot(x='day', y='total_bill', kind='boxen', data=tips, height=5, aspect=1.5, dodge=False)
plt.show()

sns.catplot(x='Dateofdecision',
            y='Sector',
            kind='violin',
            cut=0,
            bw=0.15,
            data=df,
            height=15,
            aspect=0.5,
            hue='PolicyInstrument',
            legend=False)
plt.show()

sns.catplot(x='total_bill', y='day', hue='sex', data=tips, kind='violin', legend=False, split=True, inner=None)
plt.show()
# </editor-fold>

# <editor-fold desc="Learning box catplots">
titanic = sns.load_dataset('titanic')
sns.catplot(x='sex', y='survived', data=titanic, kind='bar', hue='class', legend_out=False)
plt.show()

sns.catplot(x='deck', kind='count', data=titanic, palette='ch:.25', hue='class')
plt.show()

sns.catplot(y='Sector', kind='count', data=df, hue='CountryCPDB', height=10,aspect=0.8, legend_out=True)
plt.show()
# </editor-fold>

sns.catplot(x='day', y='total_bill', hue='smoker', data=tips,
            col='time', row='sex')
plt.show()


sns.catplot(y='PolicyInstrument', kind='count', data=df, hue='Sector', col='CountryCPDB', col_wrap=4,
            height=10, aspect=0.8, legend_out=True)
plt.show()