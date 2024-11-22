import pandas as pd

file_path = 'sorted_nepse_data.csv'
df = pd.read_csv(file_path)

df = df.drop(columns=['S.N.'])

columns = ['Date'] + [col for col in df.columns if col != 'Date']
df = df[columns]

output_path = 'C:/Users/Sapko/Desktop/the-python/modified_nepse_data.csv'
df.to_csv(output_path, index=False)

print("The file has been modified and saved as 'modified_nepse_data.csv'")
