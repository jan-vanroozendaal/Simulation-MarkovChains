# import packages
import matplotlib.pyplot as plt
import random
from scipy.stats import binom
import math
from scipy.stats import triang

#function to calculate transition probability
def trans_prob(m, n, beta, pop=100, p=0.4):
    prob_sum = 0  # sum of probabilities from the terms
    q = beta * (m / pop)

    # check whether number of infected increases, stabilizes, or decreases
    if n - m >= 0:  # if equal or more are infected after state transition
        m_poss = list(range(m + 1))  # all possibilities of number of people healed
        diff = n - m
        n_poss = []  #list to find matching number of infected to get to state n
        for i in range(0, len(m_poss)):
            n_poss.append(m_poss[i] + diff)  # list is now populated
            prob_I_beta = (binom.pmf(m_poss[i], m, p) * binom.pmf(n_poss[i], pop - m, q))
            prob_sum += prob_I_beta

    elif n - m < 0:  # if less get infected
        diff = n - m
        m_poss = list(range(m - n, m + 1))
        for i in range(0, len(m_poss)):
            prob_I_beta = (binom.pmf(m_poss[i], m, p) * binom.pmf(m_poss[i] + diff, pop - m, q))
            prob_sum += prob_I_beta

    return prob_sum

# assign variables
p = 0.4  # probability of recovery
M = 100  # list of population sizes

#prepare lists
beta_list = [] #list of drawn samples of beta from Truncated Normal Distribution
prob_list = [] #list of probability values of Markov Chain after all observations
trace_index_list = [] #list of run ID's

beta_list.append(0.5)  # initial value for beta
prob_list.append(3.545752984641526e-10) #probability given initial beta

for i in range(1, 10001):
    #select beta from 'q' triagular normal distribution based on old value of beta
    beta = triang.rvs(beta_list[i-1])

    # compute state transition probabilities of new drawn beta
    prob_i01 = trans_prob(1, 4, beta)
    prob_i12 = trans_prob(4, 7, beta)
    prob_i23 = trans_prob(7, 6, beta)
    prob_i34 = trans_prob(6, 16, beta)
    prob_i45 = trans_prob(16, 14, beta)

    value = prob_i01 * prob_i12 * prob_i23 * prob_i34 * prob_i45 #likelihood function

    # compute state transition probabilities of previous value of beta
    prob_i01_old = trans_prob(1, 4, beta_list[i-1])
    prob_i12_old = trans_prob(4, 7, beta_list[i-1])
    prob_i23_old = trans_prob(7, 6, beta_list[i-1])
    prob_i34_old = trans_prob(6, 16, beta_list[i-1])
    prob_i45_old = trans_prob(16, 14, beta_list[i-1])

    value_old = prob_i01_old * prob_i12_old * prob_i23_old * prob_i34_old * prob_i45_old #likelihood function

    # Metropolis-Hastings
    # compute ratio
    ratio = value / value_old
    # find acceptance value
    accept_value = min(1, ratio)
    # draw from Uniform(0,1)
    draw = random.uniform(0, 1)

    if draw < accept_value:
        # accept beta, add it to list
        beta_list.append(beta)
        prob_list.append(value)

    else:
        # reject beta, beta of state k-1 is repeated again
        beta_list.append(beta_list[i - 1])
        prob_list.append(prob_list[i - 1])

    trace_index_list.append(i)  # keep run ID
    print(i)  # to keep track in console

constant = sum(prob_list) / len(prob_list)

#rescaling probability values into densities
prob_new = []
for j in range(0, len(prob_list)):
    prob_new.append(prob_list[j]/constant)

#trace-plot
plt.plot(beta_list)
plt.xlabel("Run ID")
plt.ylabel("Beta")
plt.ylim(0,1)

#Posterior Distribution of Beta using Conditional Density
#ascending order of beta in list with prob_list shuffled corresponding
beta_list_copy = beta_list
beta_list_copy, prob_new = zip(*sorted(zip(beta_list_copy, prob_new)))
#plt.plot(beta_list_copy, prob_new)
#plt.title("Posterior Distribution of Beta after All Observations", fontsize=12, fontweight=0)
#plt.xlabel("Beta")
#plt.ylabel("Conditional Density")
#plt.xlim(0,1)

#Batch Means Method
#1000 first observations (10%) omitted
#9000 observations left, divided in 30 batches of 300 observations
batch_means = []
for j in range(1000, 10001, 300): #step size of 300
    batch = prob_list[j:j+299] #subset list of probability values of Markov Chain
    batch_means.append(sum(batch)/len(batch)) #calculate mean of batch, append to list

all_batch_means = sum(batch_means) / len(batch_means) #find mean of all batch means

batch_variances = [] #prep list of variances

for k in range(0, len(batch_means)): #iterate over each batch
    batch_var = (batch_means[k] - all_batch_means) ** 2 #calculate variance of each batch
    batch_variances.append(batch_var) #append variance to list

all_batch_variances = sum(batch_variances) / (len(batch_variances)-1) #S^2 calculated

lower_CI = all_batch_means - 1.96*(math.sqrt(all_batch_variances)/math.sqrt(len(batch_means)))
upper_CI = all_batch_means + 1.96*(math.sqrt(all_batch_variances)/math.sqrt(len(batch_means)))

print(all_batch_means, lower_CI, upper_CI)
print(all_batch_variances)