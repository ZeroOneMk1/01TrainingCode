import random as rd
from math import log10, log, log2
from statistics import stdev, mean
import numpy as np
from scipy.stats import norm

bignumber = 2**8
partnerslen = 1000 # ! test this

comparison = 2

attempts = 100
for k in range(1, 11):
    percenntile = k/10
    zthreshold = norm.ppf(1-percenntile/100) # ! test this
    percentiles = []
    for i in range(attempts):
        stdevE = -log(rd.random()+0.0000000000001) * bignumber

        partners = np.random.normal(0, stdevE, partnerslen)
        # partners = np.flip(np.sort(partners)) SORTED

        datedpartners = []

        for j in range(len(partners)):
            datedpartners.append(partners[j])
            if(j >= comparison): # ! Test this?
                std = stdev(datedpartners)
                mea = mean(datedpartners)
                currZ = (partners[j]-mea)/std
                if(currZ > zthreshold):
                    finalpartner = (j, partners[j])
                    break
                elif(j == len(partners) - 1):
                    finalpartner = (j, partners[j])
                    break
            
        percentile = 0
        betterpartners = [partner>=finalpartner[1] for partner in partners]
        percentile = 100*betterpartners.count(True) / len(partners)
        percentiles.append(percentile)

    print(f"Trying for: {percenntile}%\nAverage Percentile: {np.average(percentiles)}%\nWorst Performance: {max(percentiles)}%\nBest Performace: {min(percentiles)}%")

# print(f"The final partner is: {finalpartner}.\nThey were in the top {percentile}%.\nThe best partner would've been {(np.where(partners == max(partners))[0][0], max(partners))}.\n")
