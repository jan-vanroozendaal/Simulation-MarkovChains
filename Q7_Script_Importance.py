#import packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats
from scipy.stats import binom
import statistics

#assign variables
p = 0.4 #probability of recovery
M = 100 #list of population sizes

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
            prob_I_beta = (binom.pmf(m_poss[i], m, p) * binom.pmf(n_poss[i], pop-m, q))
            prob_sum += prob_I_beta

    elif n-m < 0: #if less get infected
        diff = n-m
        m_poss = list(range(m-n, m+1))
        for i in range(0, len(m_poss)):
            prob_I_beta = (binom.pmf(m_poss[i], m, p) * binom.pmf(m_poss[i]+diff, pop - m, q))
            prob_sum += prob_I_beta

    return prob_sum

#function to compute 95% CI
def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h

#prepare lists to store drawn beta's and probability of Markov Chain
beta_list = []
prob_list = []

for i in range(10000):
    beta = np.random.beta(5.2, 1) #draw beta from Beta distribution
    beta_v2 = scipy.stats.beta(5.2, 1) #needed to compute probability density function
    beta_list.append(beta) #store value in list
    prob_i01 = trans_prob(1, 4,beta) #state transition probability of I_0 to I_1
    prob_i12 = trans_prob(4, 7, beta) #I_1 to I_2
    prob_i23 = trans_prob(7, 6, beta) #I_2 to I_3
    prob_i34 = trans_prob(6, 16, beta) #I_3 to I_4
    prob_i45 = trans_prob(16, 14, beta) #I_4 to I_5

    value = prob_i01 * prob_i12 * prob_i23 * prob_i34 * prob_i45 * (1 / beta_v2.pdf(beta)) #likelihood function
    #term (1/beta_v2.pdf(beta)) is weighing factor for importance sampling

    prob_list.append(value)
    print(i) #to keep track in console

constant = sum(prob_list) / len(prob_list) #normalizing constant
print(constant)
print(statistics.variance(prob_list)) #variance

df = pd.DataFrame({'beta': beta_list, 'Post. Prob.': prob_list})

#rescaling probabilily figures into densities
prob_new = []
for j in range(0, len(prob_list)):
    prob_new.append(prob_list[j]/constant)

#to achieve a consistent line plot
#ascending order of beta in list with list of density values shuffled corresponding
beta_list, prob_new = zip(*sorted(zip(beta_list, prob_new)))

plt.plot(beta_list, prob_new)
plt.title("Posterior Distribution of Beta after All Observations", fontsize=12, fontweight=0)
plt.xlabel("Beta")
plt.ylabel("Conditional Density")
plt.xlim(0,1)

#compute 95% CI, smaller CI expected due to variance reduction
print(mean_confidence_interval(prob_list))