import os
import xlsxwriter
import constants as c
from data_operations import reload
from watchlist_operations import excel_file, filtering

def main():
    os.system('cls')
    reload()
    results_path = os.path.join(os.getcwd(), c.RESULTS_FILE)
    if os.path.isfile(results_path):
        os.remove(results_path)
    
    workbook = xlsxwriter.Workbook(c.RESULTS_FILE)
    workbook.add_worksheet('5 SMA')
    workbook.close()

    for directory in c.DIRECTORIES:
        excel_file(directory)
    filtering()
    os.system('cls')

if __name__ == "__main__":
    main()