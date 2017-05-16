#!/usr/bin/env python
# This program creates tax rates from csv files in directory csv.
# See README.txt for required files

import pandas as pd
from mulambda import mu_lambda
import numpy as np


def read_data():
    tbl = pd.read_csv('SNA_TABLE13.csv', header=0, na_values=['..', ''])
    countries = sorted(list(tbl['Country'].unique()))
    # maximum years available
    years = sorted(list(tbl['Year'].unique()))

    # Total economy tables
    GDP = pd.DataFrame(index=years, columns=countries)
    TPI = pd.DataFrame(index=years, columns=countries)
    Sub = pd.DataFrame(index=years, columns=countries)
    OS = pd.DataFrame(index=years, columns=countries)
    W = pd.DataFrame(index=years, columns=countries)
    I = pd.DataFrame(index=years, columns=countries)
    Dep = pd.DataFrame(index=years, columns=countries)

    # Houshold tables

    HT = pd.DataFrame(index=years, columns=countries)
    OSPUE = pd.DataFrame(index=years, columns=countries)
    C = pd.DataFrame(index=years, columns=countries)

    # Government tables

    OSGOV = pd.DataFrame(index=years, columns=countries)
    SS = pd.DataFrame(index=years, columns=countries)
    Igov = pd.DataFrame(index=years, columns=countries)
    TIW = pd.DataFrame(index=years, columns=countries)

    # Corp tables
    CT = pd.DataFrame(index=years, columns=countries)

    # map variable names to data frames
    totecon = {
        'Gross domestic product (expenditure approach)': GDP,
        'Taxes on production and imports; paid': TPI,
        'Subsidies; received': Sub,
        'Operating surplus and mixed income; gross': OS,
        'Compensation of employees; received': W,
        'Gross fixed capital formation': I,
        'Consumption of fixed capital': Dep
    }

    hh = {'Current taxes on income; wealth; etc.; paid': HT,
          'Operating surplus and mixed income; gross': OSPUE,
          'Final consumption expenditure': C}

    gov = {'Operating surplus and mixed income; gross': OSGOV,
           'Social contributions and benefits other than social transfers in kind; rec.': SS,
           'Gross fixed capital formation': Igov,
           'Current taxes on income; wealth; etc.; received': TIW}

    corp = {'Current taxes on income; wealth; etc.; paid': CT}

    sectors = {'Total economy': totecon,
               'Households and non-profit institutions serving households': hh,
               'General government': gov, 'Corporations': corp}

    # def reduce_tbl(tbl):
    # This function returns a list of data frames containing
    # only the tranactions needed to calcualte the taxes
    # create a fresh working data frame
    for s in sectors.keys():
        sect_tbl = tbl[tbl['Sector'] == s]
        for trans in sectors[s].keys():
            trans_tbl = sect_tbl[sect_tbl['Transaction'] == trans]
            for c in countries:
                # first check to see if series exists
                if c in list(trans_tbl['Country']):
                    df = trans_tbl[trans_tbl['Country'] == c]
                    sectors[s][trans].loc[list(df['Year'])[0]:list(df['Year'])[-1], c] = list(df['Value'])
                else:
                    sectors[s][trans].loc[years, c] = np.nan

    return (GDP, TPI, Sub, W, OS, OSPUE, OSGOV, C, I, Dep, HT, SS, CT)


# Tax comp calcualtes tax rates and writes to csv file
def taxcomp(argv=None):
    (GDP, TPI, Sub, W, OS, OSPUE, OSGOV, C, I, Dep, HT, SS, CT) = read_data()
    (mu, lmda) = mu_lambda(TPI)
    # actually calculate the tax rates here.  Then write them to file
    INC = GDP - TPI + Sub
    tauinc = HT / INC
    theta = 1 - W / (INC - OSPUE)
    tauss = SS / (1 - theta) / INC
    tauh = tauinc + tauss
    TPItilde = (1 - mu) * TPI
    TPIc = (lmda + (1 - lmda) * (C / (C + I))) * (TPItilde - Sub)
    tauc = TPIc / (C - TPIc)
    TPIx = TPItilde - Sub - TPIc
    taux = TPIx / (I - TPIx)
    tauk = (tauinc * (theta * INC - OSGOV - CT) + CT + mu * TPI) / (theta * INC - OSGOV)
    #no social security taxes in Australia
    tauss['Australia'] = 0
    taxes = {'tauinc.csv': tauinc, 'tauc.csv': tauc, 'taux.csv': taux,
             'tauk.csv': tauk, 'tauh.csv': tauh, 'tauss.csv': tauss}
    for t in taxes:
        #drop the columns that have no data
        taxes[t] = taxes[t].dropna(axis=1, how='all')
        #write to file
        taxes[t].to_csv(t, na_rep='nan')
    return (tauinc, tauss, tauc, taux, tauk)

(tauinc, tauss, tauc, taux, tauk) = taxcomp()

#


# Country                  68109  non-null values
# TRANSACT                 68109  non-null values
# Transaction              68109  non-null values
# SECTOR                   68109  non-null values
# Sector                   68109  non-null values
# MEASURE                  68109  non-null values
# Measure                  68109  non-null values
# TIME                     68109  non-null values
# Year                     68109  non-null values
# Unit Code                68109  non-null values
# Unit                     68109  non-null values
# PowerCode Code           68109  non-null values
# PowerCode                68109  non-null values
# Reference Period Code    0  non-null values
# Reference Period         0  non-null values
# Value                    68109  non-null values
# Flag Codes               715  non-null values
# Flags                    715  non-null values
# dtypes: float64(3), int64(3), object(12)
