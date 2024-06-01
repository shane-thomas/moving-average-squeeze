import os
import xlsxwriter
import constants as c
from watchlist_operations import sma

def main():
    os.system('cls')

    results_path = os.path.join(os.getcwd(), c.RESULTS_FILE)
    if not os.path.isfile(results_path):
        workbook = xlsxwriter.Workbook(c.RESULTS_FILE)
        workbook.add_worksheet('5 SMA')
        workbook.add_worksheet('10 SMA')
        workbook.add_worksheet('20 SMA')
        workbook.add_worksheet('50 SMA')
        workbook.close()

    for directory in c.DIRECTORIES:
        sma(directory)

    os.system('cls')