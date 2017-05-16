Plan to update the tax create program to use the pandasdmx module
to get data from the OECD and implement and installable package

McDaniel_tax_create.py is the old python program that creates tax



Old README
Updated 12/6/2014

For easier interpretation, abbreviations are not used
Necessary to run: python with numpy and pandas
Create directory with McDaniel_tax_create.py and mulamda.py

- Query 13. Simplified non-financial accounts, all years all countries all values
-- Save file SNA_TABLE_13.csv in directory with McDaniel_tax_create and mulamda.py

- Query OECD revenue statistics.  Refine query to include only total government revenues in local currency.
  Variable = Tax revenue in national currency
  Government = Total
--save file Rev.csv

-Run McDaniel_tax_create.py
--csv tax files saved in directory

-If you want to update old series, save the old series as in the folder old/csv with the name tau*.csv then run McDaniel_tax update function tax_update(inp)

-To update the original series, save the original tax series in old/csv as tau*orig.csv
then run McDaniel_tax update function tax_orig_update(imp)
