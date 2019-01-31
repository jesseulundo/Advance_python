import pandas as pd
import numpy as np
import matplotlib as plt

energy = pd.read_excel('Energy Indicators.xls')
energy = energy[16:243]
energy = energy.drop(energy.columns[[0, 1]], axis=1)
energy.rename(columns={'Environmental Indicators: Energy': 'Country','Unnamed: 3':'Energy Supply','Unnamed: 4':'Energy Supply per Capita','Unnamed: 5':'% Renewable'}, inplace=True)
energy.replace('...', np.nan,inplace = True)
energy['Energy Supply'] *= 1000000
def remove_digits(data):
    nData = ''.join([i for i in data if not i.isdigit()])
    i = nData.find('(')
    if i>-1:
        nData = nData[:i]
    return nData.strip()
energy['Country'] = energy['Country'].apply(remove_digits)
re_name_countries = {"Republic of Korea": "South Korea",
                     "United States of America": "United States",
                     "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                     "China, Hong Kong Special Administrative Region": "Hong Kong"}
energy.replace({"Country": re_name_countries},inplace = True)
#in 4
GDP = pd.read_csv('world_bank.csv', skiprows=4)
GDP.rename(columns ={'Country Name': 'Country'}, inplace=True)
GDP.replace({"Country": {"Korea, Rep.": "South Korea",
                              "Iran, Islamic Rep.": "Iran",
                              "Hong Kong SAR, China": "Hong Kong"}},inplace=True)
#GDP_data.replace({"Country": new_name_countries},inplace=True)

#in 5                   
ScimEn = pd.read_excel('scimagojr-3.xlsx')
print(energy.head())
print(energy.Country.unique())
print(GDP.head())
print(len(GDP.Country.unique()))
print(ScimEn.head())
df = pd.merge(pd.merge(energy, GDP, on='Country'), ScimEn, on='Country')

df.set_index('Country',inplace=True)
df = df[['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
df = (df.loc[df['Rank'].isin([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])])
df.sort('Rank',inplace=True)
df
#in 6
def answer_one():
    return df

def answer_two():
    union = pd.merge(pd.merge(energy, GDP, on='Country', how='outer'), ScimEn, on='Country', how='outer')
    intersection = pd.merge(pd.merge(energy, GDP, on='Country'), ScimEn, on='Country')
    return len(union)-len(intersection)

def answer_three():
    Top15 = answer_one()
    years = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    return (Top15[years].mean(axis=1)).sort_values(ascending=False).rename('avgGDP')


def answer_four():
    Top15 = answer_one()
    Top15['avgGDP'] = answer_three()
    Top15.sort_values(by='avgGDP', inplace=True, ascending=False)
    return abs(Top15.iloc[5]['2015']-Top15.iloc[5]['2006'])


def answer_five():
    Top15 = answer_one()
    return Top15['Energy Supply per Capita'].mean()


def answer_six():
    Top15 = answer_one()
    country = Top15.sort_values(by='% Renewable', ascending=False).iloc[0]
    return (country.name, country['% Renewable'])


def answer_seven():
    Top15 = answer_one()
    Top15['Citation_ratio'] = Top15['Self-citations']/Top15['Citations']
    country = Top15.sort_values(by='Citation_ratio', ascending=False).iloc[0]
    return country.name, country['Citation_ratio']


def answer_eight():
    Top15 = answer_one()
    Top15['Population'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    return Top15.sort_values(by='Population', ascending=False).iloc[2].name


def answer_nine():
    Top15 = answer_one()
    Top15['Estimate Population'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['avgCiteDocPerPerson'] = Top15['Citable documents'] / Top15['Estimate Population']
    return Top15[['Energy Supply per Capita', 'avgCiteDocPerPerson']].corr().ix['Energy Supply per Capita', 'avgCiteDocPerPerson']

def plot9():
    %matplotlib inline
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])
	
plot9() # Be sure to comment out plot9() before submitting the assignment!


def answer_ten():
    Top15 = answer_one()
    mid = Top15['% Renewable'].median()
    Top15['HighRenew'] = Top15['% Renewable']>=mid
    Top15['HighRenew'] = Top15['HighRenew'].apply(lambda x:1 if x else 0)
    Top15.sort_values(by='Rank', inplace=True)
    return Top15['HighRenew']



def answer_eleven():
    Top15 = answer_one()
    continents =  {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    groups = pd.DataFrame(columns = ['size', 'sum', 'mean', 'std'])
    Top15['Estimate Population'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    for group, frame in Top15.groupby(continents):
         groups.loc[group] = [len(frame), frame['Estimate Population'].sum(),frame['Estimate Population'].mean(),frame['Estimate Population'].std()]
    return groups


def answer_twelve():
    Top15 = answer_one()
    continents =  {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    Top15 = Top15.reset_index()
    Top15['Continent'] = [continents[country] for country in Top15['Country']]
    Top15['bins'] = pd.cut(Top15['% Renewable'],5)
    return Top15.groupby(['Continent','bins']).size()



def answer_thirteen():
    Top15 = answer_one()
    Top15['PopEst'] = (Top15['Energy Supply'] / Top15['Energy Supply per Capita']).astype(float)
    return Top15['PopEst'].apply(lambda x: '{0:,}'.format(x))




def plot_optional():
    import matplotlib as plt
    %matplotlib inline
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. \
This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' \
2014 GDP, and the color corresponds to the continent.")


plot_optional() # Be sure to comment out plot_optional() before submitting the assignment!

