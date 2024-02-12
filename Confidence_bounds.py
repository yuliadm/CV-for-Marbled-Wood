# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 14:50:26 2024

@author: wyjo
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import lognorm
import math
import pandas as pd
from scipy import stats

#### ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
####
#%%  IMPORT Blaukäfer Versuche
####
#### ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

excel_file_path = 'Auswertung_Biegeproben_Blauholz.xlsx'
sheet_name = 'Results_Serie_1_2'

df = pd.read_excel(excel_file_path, sheet_name, skiprows=1, nrows=166, usecols='C', header=0)
fm = np.ravel(np.array(df))


fmA = fm[0:68]
fmA = fmA[~np.isnan(fmA)]
nA = len(fmA)



fmB = fm[68:136]
log_fmB = np.exp(fmB)
nB = len(fmB)
meanB = np.mean(fmB)
stdB = np.std(fmB)
covB = stdB/meanB


# assumed bending strength of the reference group
mean_bending_strength = np.mean(fmA) # [MPa]



# standard deviation
mu = mean_bending_strength

# number of simulations for the monte carlo simulation
number_simulations = 1000

# sigfificane level of 5 %
z=1.96

# calculate deviations (?) for different numbers of sample sizes
sample_sizes = [5,6,7,8,9,10,15,20,30,40,50,60,70,80,90,100]

# calculate deviations (?) for different CoV's
CoVs = [1,5,10,15,20]

colors = ['aqua','dodgerblue','blue','darkviolet','fuchsia']

fig = plt.figure(figsize=(5, 5), dpi=600)
ax1 = fig.add_subplot(111)
ax1.set_ylabel(r'$|t_{5\%}*s/\sqrt{n}|/MOR_{A,mean}~[\%]$')
ax1.set_xlabel(r'sample size [-]')
plt.title('number of simulations = ' + str(number_simulations))
# ax1.set_ylim(0.0,3.0)
ax1.set_xlim(0.0,max(sample_sizes))
ax1.grid(True)

# for all CoVs...
for k, cov in enumerate(CoVs):
    
    # deviations (?) with confidence bounds b0
    devs = np.array([])
    b0     = np.array([])

    # standard deviation
    # sigma = math.log(cov/100.0 * mean_bending_strength)
    sigma = cov/100.0 * mean_bending_strength
    
    # for all sample sizes...
    for i, n in enumerate(sample_sizes):
        
        # initialize array for deviations (?)
        Deviations = np.array([])
    
        # perform Monte Carlo simulation
        for j in range(number_simulations):
            
            # create randomly generate normal distributed sample
            # normal_data = np.random.normal(np.log(mu), np.log(sigma), n)
            normal_data = np.random.normal(mu, sigma, n)
            # create logs
            lognormal_data = np.exp(normal_data)
            
            # calculate confidence bounds based on generated sample
            # dev = math.log(z * np.log(np.std(lognormal_data)) / math.sqrt(n))
            dev = (z * np.std(normal_data) / math.sqrt(n))
            
            # append confidence bound to array
            Deviations = np.append(Deviations, dev)
    
        # append mean of confidence bound and calculate according confidence bound b0
        devs = np.append(devs, np.mean(Deviations))
        b0     = np.append(b0,     z * np.std(Deviations) / math.sqrt(number_simulations))
    
    
    

    # plot data
    ax1.plot(sample_sizes,
              mean_bending_strength/100*(devs-b0),
              # label = 'CoV=' + str(cov) + '%',
              linestyle = '--',
              color = colors[k])
    ax1.plot(sample_sizes,
              mean_bending_strength/100*devs,
              label = 'CoV=' + str(cov) + '%',
              color = colors[k])
    ax1.plot(sample_sizes,
              mean_bending_strength/100*(devs+b0),
              # label = 'CoV=' + str(cov) + '%',
              linestyle = '--',
              color = colors[k])
    ax1.fill_between(sample_sizes, mean_bending_strength/100*(devs-b0), mean_bending_strength/100*(devs+b0), color=colors[k], alpha=0.3)


dev_exp = mean_bending_strength/100*z * np.std(fmB) / math.sqrt(nB)
ax1.scatter(nB, dev_exp, marker='v', label='Gruppe B', color = 'purple')


ax1.legend(loc='upper right')
figure_name = 'confidents_bounds_n='+str(number_simulations)+'.jpg'
plt.savefig(figure_name,
            dpi=600)
plt.show()