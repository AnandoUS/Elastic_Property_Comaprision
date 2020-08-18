from pymatgen.ext.matproj import MPRester
import pandas as pd 

a = MPRester("6vuOTNU35SWJmEsk")
n = 10000 										#First n mp-IDs to check for elastic properties

df = pd.DataFrame(columns=['mpID','Chemical Formula','no. of elements','Total no. of atoms','Space Group','Space Group Number','Shear_Modulus','Bulk_Modulus','density','band-gap','stability','icsd_ID'])

for i in range(n):
	data = a.get_data("mp-"+str(i))
	if not data:
		print("Property list for mp-ID "+ str(i) + " is empty.")
	elif data[0]['elasticity'] == None:
		print("Elastic properties for mp-ID "+str(i) + " is not calculated.")
	elif data[0]['elasticity']['G_VRH'] > 2:
		data = data[0]
		df = df.append({'mpID': str(i), 'Chemical Formula': data['full_formula'], 'no. of elements': data['nelements'], 'Total no. of atoms': data['nsites'],'Space Group':data['spacegroup']['symbol'],'Space Group Number':data['spacegroup']['number'], 'Shear_Modulus':data['elasticity']['G_VRH'],'Bulk_Modulus':data['elasticity']['K_VRH'],'density':data['density'],'band-gap':data['band_gap'],'stability':data['e_above_hull'],'icsd_ID':data['icsd_id']}, ignore_index=True)

'''
Adding Speeds of Sound columns to the dataframe using the elastic properties extracted
'''

df['v_L']=(((df['Bulk_Modulus']+1.333*df['Shear_Modulus'])/df['density'])**0.5)*1000 
df['v_T']=((df['Shear_Modulus']/df['density'])**0.5)*1000
df['v']=( ( (2/(df['v_T']**3)) + (1/(df['v_L']**3)) )/3 )**-0.33333333

print(df)
df.to_csv('Elastic_Properties.csv')