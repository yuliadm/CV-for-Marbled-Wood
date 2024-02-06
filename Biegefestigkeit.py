# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 19:24:59 2024

@author: wyjo
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import lognorm
import math

def plot_histogram(data, bins=10, title='Histogram', xlabel='Values', ylabel='Frequency'):
    """
    Plot a histogram of the given data.

    Parameters:
        data (array_like): Input data to be plotted.
        bins (int or sequence, optional): Number of bins or bin edges. Default is 10.
        title (str, optional): Title of the plot. Default is 'Histogram'.
        xlabel (str, optional): Label for the x-axis. Default is 'Values'.
        ylabel (str, optional): Label for the y-axis. Default is 'Frequency'.

    Returns:
        None
    """
    plt.hist(data, bins=bins, density=True, alpha=0.6, color='b', label='Histogram')  # Plot histogram
    # Fit a lognormal distribution to the data
    sigma_hat, loc_hat, scale_hat = lognorm.fit(data, floc=0)
    x = np.linspace(data.min(), data.max(), 100)
    pdf = lognorm.pdf(x, sigma_hat, loc=loc_hat, scale=scale_hat)
    plt.plot(x, pdf, 'r-', lw=2, label='Lognormal Fit')  # Plot fitted distribution
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

# Example usage:
# Generate lognormal distributed data

mean_bending_strength = 84.0 # [MPa]
CoV = 0.1

mu = math.log(mean_bending_strength)
sigma = math.log(CoV * mean_bending_strength)
num_samples = 1000
normal_data = np.random.normal(mu, sigma, num_samples)
lognormal_data = np.exp(normal_data)

# Plot the histogram with lognormal fit
plot_histogram(lognormal_data, bins=30, title='Lognormal Distribution with Fit', xlabel='Values', ylabel='Frequency')




z=1.96
number_simulations = 10000
sample_sizes = [5,6,7,8,9,10,15,20,50,100,150,200]
CoVs = [10,15,20,25,30]

colors = ['aqua','dodgerblue','blue','darkviolet','fuchsia']

fig = plt.figure(figsize=(5, 5), dpi=600)
ax1 = fig.add_subplot(111)
ax1.set_ylabel(r'$|t_{5\%}*s/\sqrt{n}|/f_{m,reference}$ [%]')
ax1.set_xlabel(r'sample size [-]')
plt.title('number of simulations = ' + str(number_simulations))
ax1.grid(True)


for k, cov in enumerate(CoVs):
    
    bounds = np.array([])
    b0     = np.array([])
    
    stds = np.array([])
    ns = np.array([])
    
    sigma = math.log(cov/100.0 * mean_bending_strength)

    for i, n in enumerate(sample_sizes):
        
        Bla = np.array([])
    
        
        for j in range(number_simulations):
            
            normal_data = np.random.normal(mu, sigma, n)
            lognormal_data = np.exp(normal_data)
            
            bound = math.log(z * np.std(lognormal_data) / math.sqrt(n))
            
            
            Bla = np.append(Bla, bound)
    
        
        bounds = np.append(bounds, np.mean(Bla))
        b0     = np.append(b0,     z * np.std(Bla) / math.sqrt(number_simulations))



    ax1.plot(sample_sizes,
             mean_bending_strength/100*(bounds-b0),
             # label = 'CoV=' + str(cov) + '%',
             linestyle = '--',
             color = colors[k])
    ax1.plot(sample_sizes,
             mean_bending_strength/100*bounds,
             label = 'CoV=' + str(cov) + '%',
             color = colors[k])
    ax1.plot(sample_sizes,
             mean_bending_strength/100*(bounds+b0),
             # label = 'CoV=' + str(cov) + '%',
             linestyle = '--',
             color = colors[k])
    ax1.fill_between(sample_sizes, mean_bending_strength/100*(bounds-b0), mean_bending_strength/100*(bounds+b0), color=colors[k], alpha=0.3)

ax1.legend(loc='lower right')
figure_name = 'simulations_'+str(number_simulations)+'.jpg'
plt.savefig(figure_name,
            dpi=600)
plt.show()