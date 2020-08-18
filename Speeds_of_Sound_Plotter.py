import matplotlib.pyplot as plt
import matplotlib
import pandas as pd 
import numpy as np

df = pd.read_csv('Elastic_Properties.csv')

############### list of mpIDs to be dropped #####################

l=[10,11,32,48,55,71,85,104,117,128,158,168,190,196,213,215,250,256,276,295,343,389,428,452,464,496,549,564,568,592,593,625,645,669,708,710,712,731,739,744,763,768,795,814,820,829,879,919,921,933,948,950,953,985,992,1007,1055,1101,1123,1132,1156,1220,1240,1275,1306,1402,1487,1546,1610,1620,1652,1688,1702,1708,1738,1756,1769,1785,1877,1879,1890,1971,1977,2012,2014,2050,2052,2053,2118,2120,2134,2156,2170,2182,2191,2267,2281,2297,2306,2316,2322,2323,2348,2350,2354,2384,2395,2426,2434,2516,2520,2524,2525,2540,2564,2592,2597,2637,2639,2640,2701,2724,2730,2732,2776,2807,2822,2927,3158,3247,3315,3804,3927,4120,4181,4210,4230,4247,4478,4483,4628,4897,4962,5000,5419,5473,5528,5549,5590,5597,5778,5798,5910,6954,6969,6997,7112,7263,7359,7426,7559,7755,7845,7846,7879,7882,7898,7916,7918,7961,8125,8150,8182,8368,8368,8432,8481,8577,8700,8790,9023,9027,9264,9339,9440,9460,9721,9907,9925,9960,9978]

for i in l:
	df.drop(df[df.mpID == i].index,inplace=True)

#############################  	separating data frames into metal and semiconductor dataframes 	#########################

df1=df
df2=df

df1=df1[(df1['band-gap']==0) & (df1['density']<10) & (df1['density']>4)]
df2=df2[(df2['band-gap']>0) & (df2['density']<10) & (df2['density']>4)]

###############################   extracting average speeds of sound in various density intervals ##########################

n = 6

dens_metal = []
sos_metal = np.zeros(n)
num_metal = np.zeros(n)

dens_sc = []
sos_sc = np.zeros(n)
num_sc = np.zeros(n)

for i in range(n):
	df_1=df1[(df1['band-gap']==0) & (df1['density'] < 5+i) & (df1['density'] > 4+i)]
	df_2=df2[(df2['band-gap']>0) & (df2['density'] < 5+i) & (df2['density'] > 4+i)]

	dens_metal.append(df_1['density'].mean())
	sos_metal[i] = df_1['v'].mean()
	num_metal[i] = len(df_1.index)

	dens_sc.append(df_2['density'].mean())
	sos_sc[i] = df_2['v'].mean()
	num_sc[i] = len(df_2.index)	


###########################################	Plot Details	############################################
cm = plt.cm.get_cmap('tab20b')
sc=plt.scatter(df2['density'],df2['v']**2,c= df2['band-gap'],marker='o',cmap=cm,vmin=0,s=18,vmax=1) 
sc=plt.scatter(df1['density'],df1['v']**2,c= df1['band-gap'] ,marker='o',cmap=cm,vmin=0,s=6,vmax=1) 
cbar=plt.colorbar(sc)

plt.scatter(dens_metal,sos_metal**2,s=num_metal*3, marker="p",c='midnightblue')
plt.scatter(dens_sc,sos_sc**2,s=num_sc*3, marker="p",c='palevioletred')

plt.xlim(3.6,10.4)
plt.ylim(1000000,100000000)

plt.xlabel('Density (g/cm$^{-3}$)',fontsize= 18)
plt.ylabel('$v_s^{2}$',fontsize =18)

plt.xticks(fontsize= 14)
plt.yticks(fontsize= 14)

plt.yscale('log')

cbar.set_label('band-gap (eV)', fontsize=18)

plt.rcParams['figure.figsize'] = 12, 10
plt.show()