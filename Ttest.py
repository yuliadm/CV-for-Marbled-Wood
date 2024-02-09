# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 14:50:22 2024

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


# number of simulations for the monte carlo simulation
number_simulations = 100

# reference sample
mean_bending_strength = np.mean(fmA) # [MPa]
CoV = 0.25
std_bending_strength = CoV * mean_bending_strength
print(mean_bending_strength)


# reduction of bending strength
REDs = [5,10,20,30] # %
sample_sizes = [2,5,10,15,20,30] # [-]

colors = ['aqua','dodgerblue','blue','darkviolet','fuchsia']


fig = plt.figure(figsize=(5, 5), dpi=600)
ax1 = fig.add_subplot(111)
ax1.set_ylabel(r'significant difference [%]')
ax1.set_xlabel(r'sample size [-]')
plt.title('number of simulations = ' + str(number_simulations))
ax1.grid(True)


Data ={}

# for all sample sizes...
for i, n in enumerate(sample_sizes):
    
    # create randomly generate normal distributed sample for reference sample
    normal_data = np.random.normal(mean_bending_strength, std_bending_strength, n)
    # create logs
    lognormal_data_reference = np.exp(normal_data)
    
    Data[i] = lognormal_data_reference
    
    # print(np.mean(lognormal_data_reference))
    
    
# for all reductions of bending strength...
for k, red in enumerate(REDs):
    
    n_difference = np.array([])
    
    mu = mean_bending_strength * (1-red/100.0)
    # sigma = CoV * mu
    sigma = CoV * std_bending_strength
    
    print(red, mu)
    
    # for all sample sizes...
    for i, n in enumerate(sample_sizes):
        
        difference = 0
        no_difference = 0

        # perform Monte Carlo simulation
        for j in range(number_simulations):

            
            # create randomly generate normal distributed sample for reference sample
            normal_data = np.random.normal(mu, sigma, n)
            # create logs
            lognormal_data_MC = np.exp(normal_data)
            
            
            t_statistic, p_value = stats.ttest_ind(Data[i], lognormal_data_MC)
    
            alpha = 0.05  # Set your significance level
            if p_value < alpha:
                difference = difference + 1
                # print("Reject the null hypothesis. There is a significant difference between the two groups.")
            else:
                no_difference = no_difference + 1
                # print("Fail to reject the null hypothesis. There is no significant difference between the two groups.")
                
        n_difference = np.append(n_difference, no_difference/(difference+no_difference))

    ax1.plot(sample_sizes,
             100*n_difference,
             label = 'red=' + str(red) + '%',
             linestyle = '-',
             color = colors[k])


ax1.legend(loc='lower right')
figure_name = 'T-test_n='+str(number_simulations)+'.jpg'
plt.savefig(figure_name,
            dpi=600)
plt.show()