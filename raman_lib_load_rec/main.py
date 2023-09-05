from misc import load_data

#data_path = r"/Users/Praktikum/Documents/E_Coli/Steininger_E_Coli_By_Substrate_State_Week/Ag1/Non_Induced"
data_path = r"/Users/Praktikum/Documents/E_Coli/Steininger_E_Coli_By_Substrate_State_Time/Ag1/Induced"

data = load_data(data_path)

data.describe()
