#import packages
import matplotlib.pyplot as plt
import numpy as np

#assign variables
beta = 0.8 #beta
p = 0.4 #probability of recovery
M = 100000 #large population size
k = 10000 #number of steps

#start with empty lists for x- and y-vals
x_vals = []
y_vals = []

#set initial values
I = 10  #infected individuals on day 0
S = M - I  #susceptible individuals on day 0
q = beta * (I/M) #first probability value q_k
for j in range(0, k):
        C_lk = sum(np.random.binomial(size=S, p=q, n=1))
        B_lk = sum(np.random.binomial(size=I, p=p, n = 1))
        S = S - C_lk + B_lk #number 'S' of new susceptibles
        I = C_lk + I - B_lk #number 'I' of total infected

        #calculate new probablity value q with new value for I
        q = beta * (I/M)
        #calculate target outcome value I_k/M, named Y
        Y = I/M
        #append index value j and outcome value Y in their lists
        x_vals.append(j)
        y_vals.append(Y)

        print(j) #keep track in console

#plot line charts
plt.plot(x_vals, y_vals, linewidth=1) #line chart

# Add titles
plt.title("Proportion of Infected (I) in Population (M) over 'k' days", fontsize=12, fontweight=0)
plt.xlabel("k")
plt.ylabel("I_k/M")
plt.ylim(0,1)

#discard burn-in period of 20%
index = int(0.2 * len(y_vals))

print(sum(y_vals[index:]) / len(y_vals[index:])) #approx. 0.500