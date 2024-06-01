import os 
import constants as c
import pandas as pd

def sma(directory: str) -> None:
    sheet_name = directory.split('/')[1]
    time_period = int(sheet_name.split(' ')[0])

    dataframes = []

    files_list = [file for file in os.listdir(directory) if file.endswith('.csv')]

    for file in files_list:
        file_path = os.path.join(directory, file)
        df = pd.read_csv(file_path)
        df = df.query('SERIES == "EQ"')
        dataframes.append(df[['SYMBOL', 'CLOSE']])
    
    combined_df = pd.concat(dataframes)

    combined_df = combined_df.groupby('SYMBOL').mean()
    # print(combined_df)

if __name__ == "__main__":
    sma(c.FIVE_DAYS_PATH)