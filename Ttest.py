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
number_simulations = 10000

# reference sample
mean_bending_strength = np.mean(fmA) # [MPa]
CoV = 0.1
std_bending_strength = CoV * mean_bending_strength

# sigfificane level of 5 %
z=1.96

# reduction of bending strength
REDs = [1,2,3,4,5,10] # %
sample_sizes = [5,6,7,8,9,10,15,20,30,40,50,60,70,80,90,100] # [-]


colors = ['aqua','dodgerblue','blue','darkviolet','fuchsia','deeppink']


fig = plt.figure(figsize=(5, 5), dpi=600)
ax1 = fig.add_subplot(111)
ax1.set_ylabel(r'p [%]')
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
    
    Data[i] = normal_data
    

    
    
# for all reductions of bending strength...
for k, red in enumerate(REDs):
    
    n_difference = np.array([])
    p_values = np.array([])
    b_0s = np.array([])
    
    mu = mean_bending_strength * (1-red/100.0)
    # sigma = CoV * mu
    sigma = std_bending_strength
    
    print(red, mu)
    
    # for all sample sizes...
    for i, n in enumerate(sample_sizes):
        
        difference = 0
        no_difference = 0
        
        p_pre = np.array([])

        # perform Monte Carlo simulation
        for j in range(number_simulations):
            
            
            # create randomly generate normal distributed sample for reference sample
            # normal_data_reference = np.random.normal(np.log(mean_bending_strength), np.log(std_bending_strength), n)
            normal_data_reference = np.random.normal(mean_bending_strength, std_bending_strength, n)
            # create logs
            lognormal_data_reference = np.exp(normal_data_reference)
            
            
            # create randomly generate normal distributed sample for reference sample
            # normal_data_MC = np.random.normal(np.log(mu), np.log(sigma), n)
            normal_data_MC = np.random.normal(mu, sigma, n)
            # create logs
            lognormal_data_MC = np.exp(normal_data_MC)
            
            
            t_statistic, p_value = stats.ttest_ind(normal_data_reference, normal_data_MC)
    
            alpha = 0.05  # Set your significance level
            if p_value < alpha:
                difference = difference + 1
                # print("Reject the null hypothesis. There is a significant difference between the two groups.")
            else:
                no_difference = no_difference + 1
                # print("Fail to reject the null hypothesis. There is no significant difference between the two groups.")
            
            p_pre = np.append(p_pre, p_value)
                
        n_difference = np.append(n_difference, difference/(difference+no_difference))
        p_values     = np.append(p_values,     np.mean(p_pre))
        b_0s         = np.append(b_0s,     z * np.std(p_pre) / math.sqrt(number_simulations))
    
    
    ax1.plot(sample_sizes,
              100*(p_values+b_0s),
              linestyle = '--',
              color = colors[k])
    ax1.plot(sample_sizes,
              100*(p_values),
              label = 'red=' + str(red) + '%',
              color = colors[k])
    ax1.plot(sample_sizes,
              100*(p_values-b_0s),
              linestyle = '--',
              color = colors[k])
    ax1.fill_between(sample_sizes,
                     100*(p_values+b_0s),
                     100*(p_values-b_0s), color=colors[k], alpha=0.3)

ax1.plot(sample_sizes,
          5.0 * np.ones(len(sample_sizes)),
          label = 'a=5%',
          linestyle = '-',
          color = 'black')

t_statistic, p_value = stats.ttest_ind(fmA, fmB)

ax1.scatter(nB, p_value, marker='v', label='Gruppe B', color = 'blue')


ax1.legend(loc='upper right')
figure_name = 'T-test_n='+str(number_simulations)+'.jpg'
plt.savefig(figure_name,
            dpi=600)
plt.show()