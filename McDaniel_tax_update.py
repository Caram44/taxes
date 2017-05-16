#This program takeso old csv taxfiles and updates
#Move old tax files to dir old/csv
#Run McDaniel tax create
#Run McDaniel tax update
inp = ['tauinc', 'tauss', 'tauk', 'tauc', 'taux']
import pandas as pd
import numpy as np
import xlsxwriter


def tax_update(inp):
    writer = pd.ExcelWriter('McDaniel_tax_02_01_2017.xlsx', engine='xlsxwriter')
    for tax in inp:
        oldtax = pd.read_csv('old/csv/' + tax + '.csv', index_col=0, header=0)
        oldtax = oldtax.dropna(axis=1, how='all')
        newtax = pd.read_csv(tax + '.csv', index_col=0, header=0)
        years = list(set(list(oldtax.axes[0]) + list(newtax.axes[0])))
        countries = list(set(list(oldtax.axes[1]) + list(newtax.axes[1])))
        update = pd.DataFrame(index=years, columns=countries)
        for c in countries:
            if c in oldtax.axes[1]:
                coldtax = oldtax[c]
            else:
                coldtax = pd.Series(np.nan, index=years)
            if c in newtax.axes[1]:
                cnewtax = newtax[c]
            else:
                cnewtax = pd.Series(np.nan, index=years)
                cnewtax[coldtax.axes[0]] = coldtax
            #find the earliest newtax year
            nonnanold = coldtax[np.isnan(coldtax) == False].axes[0]
            nonnannew = cnewtax[np.isnan(cnewtax) == False].axes[0]
            relyears = nonnanold[nonnanold.isin(nonnannew) == False]
            oyr = nonnannew[0]
            #if the new same year is not nan, then update
            if cnewtax[oyr] > 0:
                factor = cnewtax[oyr] / coldtax[oyr]
                #put data in update
                cnewtax[relyears] = coldtax[relyears] * factor
            else:
                cnewtax[coldtax.axes[0]] = coldtax
            update[c] = cnewtax
        #sort the country columns
        scols = sorted(update.columns.tolist())
        update = update[scols]
        update.to_excel(writer, sheet_name=tax)
        update.to_csv('update' + tax + '.csv', na_rep='nan')
    return update


def tax_orig_update(inp):
    #run this AFTER tax update
    writer = pd.ExcelWriter('McDaniel_tax_02_01_2017_orig.xlsx', engine='xlsxwriter')
    for tax in inp:
        origtax = pd.read_csv('old/csv/' + tax + 'orig' + '.csv', index_col=0, header=0)
        newtax = pd.read_csv('update' + tax + '.csv', index_col=0, header=0)
        years = list(set(list(origtax.axes[0]) + list(newtax.axes[0])))
        countries = list(list(origtax.axes[1]))
        update = pd.DataFrame(index=years, columns=countries)
        for c in countries:
            #latest year for orig taxes
            corigtax = origtax[c]
            cnewtax = newtax[c]
            nonnanorig = corigtax[np.isnan(corigtax) == False].axes[0]
            nonnannew = cnewtax[np.isnan(cnewtax) == False].axes[0]
            relyears = nonnanorig[nonnanorig.isin(nonnannew) == False]
            oyr = nonnannew[0]
            #if the new same year is not nan, then update
            factor = cnewtax[oyr] / corigtax[oyr]
            #put data in update
            cnewtax[relyears] = corigtax[relyears] * factor
            update[c] = cnewtax
        #sort the country columns
        scols = sorted(update.columns.tolist())
        update = update[scols]
        update.to_excel(writer, sheet_name=tax)
        update.to_csv('updateorig' + tax + '.csv', na_rep='nan')
    return update
