#import packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#assign variables
beta = 0.8 #beta
p = 0.4 #probability of recovery
M = [100, 1000, 10000] #list of population sizes
k = 100 #number of steps

list_x = [] #will store three lists of x-vals of size k, for each setting of M
list_y = [] #idem for y-vals

for i in range(0, len(M)):
    #start with empty lists for x- and y-vals
    x_vals = []
    y_vals = []
    #set initial values
    I = 10  #infected individuals on day 0
    S = M[i] - I  #susceptible individuals on day 0
    q = beta * (I/M[i]) #first probability value q_k
    for j in range(0, k):
        C_lk = sum(np.random.binomial(size=S, p=q, n=1))
        B_lk = sum(np.random.binomial(size=I, p=p, n = 1))
        S = S - C_lk + B_lk #number 'S' of new susceptibles
        I = C_lk + I - B_lk #number 'I' of total infected

        #calculate new probablity value q with new value for I
        q = beta * (I/M[i])
        #calculate target outcome value I_k/M, named Y
        Y = I/M[i]
        #append index value j and outcome value Y in their lists
        x_vals.append(j)
        y_vals.append(Y)

        #if loop is completed, append x-vals and y-vals to master lists
        if len(x_vals) == 100:
            list_x.append(x_vals)
            list_y.append(y_vals)

#create dataframe using pandas
df = pd.DataFrame({'x_100': list_x[0], 'x_1000': list_x[1], 'x_10000': list_x[2],
                   'y_100': list_y[0], 'y_1000': list_y[1], 'y_10000': list_y[2]})

#plot line charts
# multiple line plot
plt.plot('x_100', 'y_100', data=df, linewidth=1) #line chart for M=100
plt.plot('x_1000', 'y_1000', data=df, linewidth=1) #line chart for M=1000
plt.plot('x_10000', 'y_10000', data=df, linewidth=1) #line chart for M=10000
plt.legend(["M=100", "M=1000", "M=10000"])

# Add titles
plt.title("Proportion of Infected (I) in Population (M) over 'k' days", fontsize=12, fontweight=0)
plt.xlabel("k")
plt.ylabel("I_k/M")