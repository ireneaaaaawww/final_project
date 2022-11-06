import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn')

st.title('Mineral Ores Around The World')
df = pd.read_csv('Mineral Ores Around The World Cleaned.csv')

df = df.dropna(thresh = len(df)*0.8, axis = 1)
df = df.dropna(subset = ['commod1'])

# create a multi select
development_status = st.sidebar.multiselect(
     'Choose Development Status',
     df.dev_stat.unique(),  # options
     df.dev_stat.unique())  # defaults

# filter by development status
df1 = df[df.dev_stat.isin(development_status)]

# create a radio
mineral_type = st.sidebar.radio(
    'Choose Mineral Type:',
    ('ALL', 'Gold', 'Copper', 'Iron', 'Phosphorus-Phosphates',
       'Aluminum', 'Mercury', 'Chromium', 'Tungsten','Silver','Zinc'))

# filter by mineral type
if mineral_type == 'ALL':
    df2 = df1
elif mineral_type == 'Gold':
    df2 = df1[df1['commod1'] == 'Gold']
elif mineral_type == 'Copper':
    df2 = df1[df1['commod1'] == 'Copper']
elif mineral_type == 'Iron':
    df2 = df1[df1['commod1'] == 'Iron']
elif mineral_type == 'Phosphorus-Phosphates':
    df2 = df1[df1['commod1'] == 'Phosphorus-Phosphates']
elif mineral_type == 'Aluminum':
    df2 = df1[df1['commod1'] == 'Aluminum']
elif mineral_type == 'Mercury':
    df2 = df1[df1['commod1'] == 'Mercury']
elif mineral_type == 'Chromium':
    df2 = df1[df1['commod1'] == 'Chromium']
elif mineral_type =='Tungsten':
    df2 = df1[df1['commod1'] == 'Tungsten']
elif mineral_type =='Silver':
    df2 = df1[df1['commod1'] == 'Silver']
else:
    df2 = df1[df1['commod1'] == 'Zinc']

# show on map
df3 = pd.DataFrame(df2[['latitude','longitude']],columns=['latitude','longitude'])
st.map(df3)

# show the plot1 of the percentage of mineral resources of the country in the world
st.subheader('Percentage of different country')
fig, ax = plt.subplots(figsize= (20, 5))
pd1 = df.country.value_counts().head(10).plot.pie(
    autopct='%1.2f%%',
    explode=(0, 0, 0, 0, 0, 0, 0, 0, 0.3, 0),
    colors=["#FA8072", "#FFA500", "#FAC205", "#FFD700", "#FFFF14"])
pd1.set_xlabel('country')
pd1.set_ylabel(' ')
st.pyplot(fig)

# show the plot2 of the operation type between the world and US
st.subheader('Compare the operaion type between the world and US')

us = df[df['country'] == 'United States']
us = us.oper_type.value_counts()
world = df.oper_type.value_counts()
world = world.to_frame(name = 'World').sort_values(by = 'World', ascending = False)
us = us.to_frame('US').sort_values(by = 'US', ascending= False)
compare = pd.concat([world, us] , axis = 1)
fig, ax = plt.subplots(1, 2, figsize = (10, 5))
compare.World.plot.bar(ax = ax[0], xlabel= 'kinds').set_xticks(range(0, len(list(compare.index))))
ax[0].set_xticklabels(list(compare.index), rotation= 60)
ax[0].set_xlabel('kinds')
compare.US.plot.bar(ax = ax[1], xlabel= 'kinds').set_xticks(range(0, len(list(compare.index))))
ax[1].set_xticklabels(list(compare.index), rotation= 60)
ax[1].set_xlabel('kinds')
st.pyplot(fig)

# show the plot3 of the tail's operation type between the world and US
st.subheader('Compare the tail\'s operaion type between the world and US')

us = df[df['country'] == 'United States']
us = us.oper_type.value_counts()
world = df.oper_type.value_counts()
world = world.to_frame(name= 'World').sort_values(by= 'World', ascending= False).tail()
us = us.to_frame('US').sort_values(by= 'US', ascending= False).tail()
compare = pd.concat([world, us], axis = 1)
fig, ax = plt.subplots(1, 2, figsize = (10, 5))
compare.World.plot.bar(ax= ax[0], xlabel= 'kinds').set_xticks(range(0, len(list(compare.index))))
ax[0].set_xticklabels(list(compare.index), rotation= 60)
ax[0].set_xlabel('kinds')
ax[0].set_yticks(range(0, 20))
compare.US.plot.bar(ax = ax[1], xlabel= 'kinds').set_xticks(range(0, len(list(compare.index))))
ax[1].set_xticklabels(list(compare.index), rotation= 60)
ax[1].set_yticks(range(0, 20))
ax[1].set_xlabel('kinds')

st.pyplot(fig)

# show the plot4 of distrinution of different type of mineral
st.subheader('Kinds of mineral')
commod1_count = df['commod1'].value_counts()
gold = df[(df['commod1'] == 'Gold') | (df['commod1'] == 'Gold, Silver') | (df['commod1'] == 'Silver, Gold')].value_counts().sum()
silver = df[(df['commod1'] == 'Silver') | (df['commod1'] == 'Gold, Silver') | (df['commod1'] == 'Silver, Gold')].value_counts().sum()
zinc = df[(df['commod1'] == 'Zinc') | (df['commod1'] == 'Zinc, Lead') | (df['commod1'] == 'Lead, Zinc')].value_counts().sum()
lead = df[(df['commod1'] == 'Lead') | (df['commod1'] == 'Zinc, Lead') | (df['commod1'] == 'Lead, Zinc')].value_counts().sum()

commod1_count = df['commod1'].value_counts()
commod1_count = commod1_count.drop(labels = ['Gold, Silver', 'Silver, Gold', 'Zinc, Lead', 'Lead, Zinc'])
commod1_count.loc['Gold'] = gold
commod1_count.loc['Silver'] = silver
commod1_count.loc['Zinc'] = zinc
commod1_count.loc['Lead'] = lead
fig, ax = plt.subplots(figsize= (12, 10))
plt.style.use('seaborn')
ax = sns.countplot(y = "commod1", data = df, order = commod1_count[:10].index, palette = 'Dark2')
ax.set_yticklabels(ax.get_yticklabels(),fontsize= 15)
ax.set_ylabel('mineral',fontsize= 20)  
ax.set_xlabel('Count',fontsize= 20)

st.pyplot(fig)

# show the plot4 of Comparing how many mine lot producing gold between the world and US
st.subheader('Compare how many mine lot producing gold between the world and US')
 
world=df[df['commod1']=='Gold'].country.value_counts(normalize=True)
fig, ax = plt.subplots(figsize = (20, 5))
world.head(5).plot.pie(
    autopct = '%1.2f%%',
    colors = ["#FA8072", "#FFA500", "#FAC205", "#FFD700", "#FFFF14"],
    ax = ax,
    )
st.pyplot(fig)