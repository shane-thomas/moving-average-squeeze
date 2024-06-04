import os
import constants as c
import pandas as pd
from pandas import DataFrame


def excel_file(directory: str) -> None:
    sheet_name = directory.split('/')[1]
    time_period = int(sheet_name.split(' ')[0])

    files_list = [file for file in os.listdir(
        directory) if file.endswith('.csv')]

    current = pd.read_csv(os.path.join(directory, files_list[-1]))

    sma_dictionary = sma(directory)
    current = current.query("SERIES == 'EQ'")
    current.insert(len(current.columns), f'{
                   time_period} SMA', value=current['SYMBOL'].map(sma_dictionary))
    file_name = f"{sheet_name}.xlsx"

    write_results(current, time_period, directory)


def write_results(dataframe: DataFrame, range: int, directory: str) -> None:
    del_columns = ['TOTTRDVAL', 'TIMESTAMP', 'TOTALTRADES', 'ISIN', 'Unnamed: 13',
                   'LAST', 'OPEN', 'HIGH', 'LOW', 'PREVCLOSE', 'SERIES', 'TOTTRDQTY']
    sheet_name = directory.split('/')[1]
    print(sheet_name)
    for col in del_columns:
        dataframe.pop(col)
    if range != 5:
        # Read the last sheet from the existing Excel file
        excel = pd.read_excel(io=c.RESULTS_FILE, sheet_name=None)
        last_sheet_name = list(excel.keys())[-1]
        last_sheet = excel[last_sheet_name]

        # Merge the dataframes on 'SYMBOL'
        dataframe = last_sheet.merge(dataframe, on=['SYMBOL', 'CLOSE'], how='right')

        # Determine the index of the last two columns for comparison
        col_count = len(dataframe.columns)
        col_2 = col_count - 2
        col_1 = col_count - 1

        # Apply the filter condition
        dataframe = dataframe[(1.005 * dataframe.iloc[:, col_2] > dataframe.iloc[:, col_1]) & (dataframe.iloc[:, col_1] > 0.995 * dataframe.iloc[:, col_2])]

        print("Writing")
    with pd.ExcelWriter(c.RESULTS_FILE, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        dataframe.to_excel(writer, f"{range} SMA", index=False)


def sma(directory: str):
    dataframes = []
    files_list = [file for file in os.listdir(
        directory) if file.endswith('.csv')]

    for file in files_list:
        file_path = os.path.join(directory, file)
        df = pd.read_csv(file_path)
        df = df.query('SERIES == "EQ"')
        dataframes.append(df[['SYMBOL', 'CLOSE']])

    combined_df = pd.concat(dataframes)
    combined_df = combined_df.groupby('SYMBOL')['CLOSE'].mean()
    return combined_df.to_dict()


if __name__ == "__main__":
    excel_file(c.FIVE_DAYS_PATH)
