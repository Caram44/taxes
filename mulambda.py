
import pandas as pd
import numpy as np


def read_tax():
    rev = pd.read_csv('rev.csv', header=0, na_values=['..', ''])
    countries = sorted(list(rev['Country'].unique()))
    # maximum years available
    years = sorted(list(rev['Year'].unique()))
    # make sure rev includes only local currency and total gov
    rev = rev[rev['Variable'] == 'Tax revenue in national currency']
    rev = rev[rev['Government'] == 'Total']

    tax4120 = pd.DataFrame(index=years, columns=countries)
    tax4100 = pd.DataFrame(index=years, columns=countries)
    tax4110 = pd.DataFrame(index=years, columns=countries)
    tax5110 = pd.DataFrame(index=years, columns=countries)
    tax5121 = pd.DataFrame(index=years, columns=countries)
    tax5123 = pd.DataFrame(index=years, columns=countries)
    tax5126 = pd.DataFrame(index=years, columns=countries)
    tax5200 = pd.DataFrame(index=years, columns=countries)

    taxes = {4120: tax4120, 4100: tax4100, 4110: tax4110, 5110: tax5110,
             5121: tax5121, 5123: tax5123, 5126: tax5126, 5200: tax5200}

    for t in taxes.keys():
        tx_tbl = rev[rev['TAX'] == t]
        outtbl = taxes[t]
        for c in countries:
            if c in list(tx_tbl['Country']):
                df = tx_tbl[tx_tbl['Country'] == c]
                outtbl.loc[list(df['Year']), c] = list(df['Value'])
            else:
                outtbl.loc[years, c] = np.nan
    return (tax4120, tax4100, tax4110, tax5110, tax5121, tax5123, tax5126, tax5200)


def mu_lambda(TPI):
    (tax4120, tax4100, tax4110, tax5110, tax5121,
     tax5123, tax5126, tax5200) = read_tax()
    # see paper "Country notes, Canada for explanation
    # only adjust countries where 4100/TPI is greater than 5%
    countries = tax4100.axes[1]
    nosplit = countries[tax4120.count(axis = 0,level = None, numeric_only = False) < 1]
    tax4120[nosplit] = .58 * tax4100[nosplit]
    tax4110[nosplit] = .42 * tax4100[nosplit]
    # countries included in the tax tables

    #print type(countries)
    # create mu values
    mu = pd.Series(0., countries)
    lmda = pd.Series(0., countries)
    Ctax = tax4110 + tax5121 + tax5126
    CItax = tax5110 + tax5123 + tax5200

    for country in countries:
        if country in TPI.axes[1]:
            #TPI is in millions, tax rev in billions
            #check this before running
            mu[country] = np.mean(tax4120[country] / TPI[country])*1000
            # lmda[country] = mean(Ctax[country]/(TPI[country]*(1-mu[country]))
            lmda[country] = np.mean(
                Ctax[country] / (Ctax[country] + CItax[country]))

    # if can't be calculated, mu = 0
    mu[np.isnan(mu) == True] = 0
    # no calculate lambda
    return (mu, lmda)


# GOV                   9694  non-null values
# Government               9694  non-null values
# TAX                      9694  non-null values
# Tax                      9694  non-null values
# VAR                      9694  non-null values
# Variable                 9694  non-null values
# COU                      9694  non-null values
# Country                  9694  non-null values
# YEA                      9694  non-null values
# Year                     9694  non-null values
# Unit Code                9694  non-null values
# Unit                     9694  non-null values
# PowerCode Code           9694  non-null values
# PowerCode                9694  non-null values
# Reference Period Code    0  non-null values
# Reference Period         0  non-null values
# Value                    9690  non-null values
# Flag Codes               0  non-null values
# Flags                    0  non-null values
