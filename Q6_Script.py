#import packages
import matplotlib.pyplot as plt
import random
import scipy.stats
import numpy as np
from scipy.stats import binom

#function to calculate transition probability
def trans_prob(m, n, beta, pop=100, p=0.4):
    prob_sum = 0 #sum of probabilities from the terms
    q = beta * (m/pop)

    #check whether number of infected increases, stabilizes, or decreases
    if n-m >= 0: #if equal or more are infected after state transition
        m_poss = list(range(m+1)) #all possibilities of number of people healed
        diff = n - m
        n_poss = [] #list to find matching number of infected to get to state n
        for i in range(0, len(m_poss)):
            n_poss.append(m_poss[i]+diff) #list is now populated
            prob_I_beta = (binom.pmf(m_poss[i],m,p)*binom.pmf(n_poss[i],pop-m,q))
            prob_sum += prob_I_beta

    elif n-m < 0: #if less get infected
        diff = n-m
        m_poss = list(range(m-n, m+1))
        for i in range(0, len(m_poss)):
            prob_I_beta = (binom.pmf(m_poss[i],m,p)*binom.pmf(m_poss[i]+diff,pop-m,q))
            prob_sum += prob_I_beta

    return prob_sum

#function to compute 95% CI
def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h

#prepare lists
beta_list = [] #store drawn sample values of beta from Uniform(0,1) distribution
prob_list_toI1 = [] #list for probability of state transition I_0 to I_1
prob_list_toI2 = [] #list for probability of state transition I_1 to I_2
prob_list_toI3 = [] #list for probability of state transition I_2 to I_3
prob_list_toI4 = [] #list for probability of state transition I_3 to I_4
prob_list_toI5 = [] #list for probability of state transition I_4 to I_5

#Monte-Carlo simulation
for i in range(10000):
    beta = random.uniform(0, 1) #draw value for beta
    beta_list.append(beta) #append to list to keep track of history of drawn betas

    prob_list_toI1.append(trans_prob(1,4,beta)) #append probability of I_0 to I_1
    prob_list_toI2.append(trans_prob(4,7,beta)) #I_1 to I_2
    prob_list_toI3.append(trans_prob(7,6,beta)) #I_2 to I_3
    prob_list_toI4.append(trans_prob(6,16,beta)) #I_3 to I_4
    prob_list_toI5.append(trans_prob(16,14,beta)) #I_4 to I_5
    print(i) #to keep track in console

#normalising constants for each state transition
constant_toI1 = sum(prob_list_toI1) / len(prob_list_toI1)
constant_toI2 = sum(prob_list_toI2) / len(prob_list_toI2)
constant_toI3 = sum(prob_list_toI3) / len(prob_list_toI3)
constant_toI4 = sum(prob_list_toI4) / len(prob_list_toI4)
constant_toI5 = sum(prob_list_toI5) / len(prob_list_toI5)

print(mean_confidence_interval(prob_list_toI1),
      mean_confidence_interval(prob_list_toI2),
      mean_confidence_interval(prob_list_toI3),
      mean_confidence_interval(prob_list_toI4),
      mean_confidence_interval(prob_list_toI5), sep="\n")

#create list of lists of all state transition probabilities
master_list = [prob_list_toI1, prob_list_toI2, prob_list_toI3, prob_list_toI4, prob_list_toI5]
constant_list = [constant_toI1, constant_toI2, constant_toI3, constant_toI4, constant_toI5]

#for-loop to create plots of posterior distribution after every observation
master_scaled_list = [] #store re-scaled probabilities for each state transition
for i in range(0, len(master_list)): #for each state transition
    prob_scaled = []
    for j in range(0, len(master_list[i])): #for each probability value within state transition
        prob_scaled.append(master_list[i][j]/constant_list[i])
    master_scaled_list.append(prob_scaled)

#to achieve a consistent line plot
#ascending order of beta in list with list of density values shuffled corresponding
beta_list_0, prob_list_0 = zip(*sorted(zip(beta_list, master_scaled_list[0])))
beta_list_1, prob_list_1 = zip(*sorted(zip(beta_list, master_scaled_list[1])))
beta_list_2, prob_list_2 = zip(*sorted(zip(beta_list, master_scaled_list[2])))
beta_list_3, prob_list_3 = zip(*sorted(zip(beta_list, master_scaled_list[3])))
beta_list_4, prob_list_4 = zip(*sorted(zip(beta_list, master_scaled_list[4])))


#creating grid of posterior distribution plots
#use master_list for conditional probabilities
#use master_scaled_list for conditional densities
fig, axs = plt.subplots(3, 2)

axs[0, 0].plot(beta_list_0, prob_list_0)
axs[0, 0].set_title('I_0 to I_1')
axs[0, 1].plot(beta_list_1, prob_list_1)
axs[0, 1].set_title('I_1 to I_2')
axs[1, 0].set_title('I_2 to I_3')
axs[1, 0].plot(beta_list_2, prob_list_2)
axs[1, 1].set_title('I_3 to I_4')
axs[1, 1].plot(beta_list_3, prob_list_3)
axs[2, 0].set_title('I_4 to I_5')
axs[2, 0].plot(beta_list_4, prob_list_4)

for ax in axs.flat:
    ax.set(xlabel='Beta', ylabel='Conditional Density')
fig.tight_layout()