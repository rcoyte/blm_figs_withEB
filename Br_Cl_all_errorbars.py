# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 15:00:24 2024

@author: rmcoy
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats.mstats import gmean
custom_pal = ['#1af041', '#053480', '#f0c0bd',  '#f2aa1b', '#a65628', '#984ea3', '#999999']
    
SMALL_SIZE = 10
MEDIUM_SIZE = 16
BIGGER_SIZE = 20
plt.rc('font', family='serif')
plt.rc('xtick', labelsize= SMALL_SIZE)
plt.rc('ytick', labelsize='x-small')
plt.rc('axes', titlesize= BIGGER_SIZE, labelweight = 'bold')     # fontsize of the axes title
plt.rc('axes', labelsize= BIGGER_SIZE, labelweight='bold')    # fontsize of the x and y labels
plt.rc('ytick.major', size=10,)
plt.rc('ytick.minor', size = 5)
plt.rc('xtick.major', size=10,)
plt.rc('xtick.minor', size = 5)
plt.rc('xtick', labelsize= BIGGER_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize= BIGGER_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize= MEDIUM_SIZE)    # legend fontsize
plt.rc('figure', titlesize= BIGGER_SIZE)  # fontsize of the figure title

#read data and make output folders
datadir = os.path.join('..', 'data')
outdir = os.path.join('..', 'output')
if not os.path.exists(outdir):
    os.mkdir(outdir)
    
file1 = os.path.join(datadir, 'data_2.xlsx')
df = pd.read_excel(file1, na_values='n/a', sheet_name="MAIN_ALL")
df_north = df[df['Group'] == 'North']
df_south = df[df['Group'] == 'South']
df_central = df[df['Group'] == 'Center']
    
# Calculate mean and standard deviation for each Well_ID
agg_df = df.groupby('Well_ID').agg(
    mean_Br=('m_Br', 'mean'),
    std_Br=('m_Br', 'std'),
    mean_Cl=('m_Cl', 'mean'),
    std_Cl=('m_Cl', 'std'),
    Group=('Group', 'first')
).reset_index()

# Create the scatterplot with error bars
plt.figure(figsize=(10, 6))

# Plot error bars first
plt.errorbar(
    x=agg_df['mean_Cl'],
    y=agg_df['mean_Br'],
    xerr=agg_df['std_Cl'],
    yerr=agg_df['std_Br'],
    fmt='o',
    ecolor='gray',
    elinewidth=1,
    capsize=3,
    alpha=0.5,
    zorder=1  # Plot error bars with a lower zorder
)

# Plot the scatterplot on top
sns.scatterplot(
    data=agg_df,
    x='mean_Cl',
    y='mean_Br',
    hue='Group',
    palette='colorblind',  # Using custom palette
    s=100,
    edgecolor='black',
    zorder=2  # Plot scatter points with a higher zorder
)
# Define the ratio of Br/Cl = 0.0015
ratio = 0.0015

# Generate a range of Cl values
cl_values = np.linspace(df['m_Cl'].min(), df['m_Cl'].max(), 100)

# Calculate corresponding Na values
na_values = ratio * cl_values

# Plot the line
plt.plot(cl_values, na_values, label='Br/Cl = 0.0015', color='red', linestyle='--')
# Set title and labels
# plt.title('Scatterplot of m_Br vs m_Cl with Error Bars by Group')
plt.xlabel('Chloride (mol/L)')
plt.ylabel('Bromide (mol/L)')  # Using LaTeX formatting for subscript and superscript
plt.xscale('log')
plt.yscale('log')
# Show the plot
plt.legend(title='Group')
plt.show()