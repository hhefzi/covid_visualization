#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from math import ceil,floor

state_df = pd.read_csv('./data/states.csv')
state_df.date = pd.to_datetime(state_df.date, yearfirst = True, format = '%Y%m%d')
state_df.date = state_df.date.dt.strftime('%m/%d')
state_df.sort_values('date',inplace=True)

population_dict = {}
with open('./data/populations.tsv','r') as f:
    for line in f:
        line = line.strip().split('\t')
        population_dict[line[0]] = int(line[1])

def plot_individual_state(state, output_file = None, rollingwindow = 7, df = state_df, pop_dict = population_dict):
    fig,ax = plt.subplots(figsize = (20,10))
    ax2 = ax.twinx()
    state_pop = pop_dict[state]

    tmp = df.loc[df.state==state,:].copy()
    tmp.loc[:,'deltapos'] = tmp['positive'].diff()
    tmp.loc[:,'deltapos.rolling'] = tmp['deltapos'].rolling(rollingwindow).mean()
    tmp.loc[:,'deltatest'] = tmp['totalTestResults'].diff()
    tmp.loc[:,'deltatest.rolling'] = tmp['deltatest'].rolling(rollingwindow).mean()
    rate = tmp['deltapos.rolling']/tmp['deltatest.rolling']
    ax.plot(tmp.date, rate , lw = 2, color = '#aaaaaa',zorder = 1, marker = 'o', ms = 8, markeredgecolor = 'k', markerfacecolor = '#00ffff')
    #ax.scatter(tmp.date, rate , color = ['#00ffff' if x<0.05 else '#00ffff' for x in rate], s = 40, zorder = 3, edgecolor = 'k')
    ax.set_ylim([0,0.3])
    ax2.bar(tmp.date,tmp['deltapos.rolling']/state_pop*1000,color = 'k',zorder = 3)
    ax2.bar(tmp.date,tmp['deltatest.rolling']/state_pop*1000, color = '#FFC900', edgecolor = 'k')
    ax2.tick_params(axis = 'y', direction = 'in', labelsize = 16)
    ax.set_title(state, fontsize = 24)
    ax2.set_ylim([0,4])
    ax.set_yticks([0,0.1,0.2,0.3,0.3])
    ax.set_yticklabels(['0%','10%','20%','30%'])
    ax.tick_params(axis = 'both', direction = 'in', labelsize = 16)

    (xmin,xmax) = ax.get_xlim()
    ax.plot([xmin,xmax],[0.05,0.05],lw = 4, ls = '-', color = '#cc0000')
    ax.set_xticks(range(ceil(xmax)+1,floor(xmin),-7))
    ax2.set_xlim([xmin,xmax])
    ax.set_zorder(1)
    ax.patch.set_visible(False)
    ax.set_ylabel('% Positive Tests', fontsize = 24)
    ax2.set_ylabel('Tests and Cases per 1000', fontsize = 24, rotation = 270, labelpad = 25)
    ax.legend(['Positive Rate'], fontsize = 20, loc = 'upper left')
    ax2.legend(['Cases','Tests'], fontsize = 20)
    if output_file:
        plt.savefig(output_file)

states_dc = sorted([x for x in state_df.state.unique() if x not in ['PR','GU','AS','MP','VI']])

for state in states_dc:
    plot_individual_state(state, output_file = './imgs/{}.png'.format(state))
