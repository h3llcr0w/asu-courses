###################################################
# Homework #5 : EEE554 - Random Signal Theory     #
# * Author: Mishel Paul                           #
# * Date : 11/08/2021                             #
###################################################

from scipy.stats import bernoulli as Ber
import matplotlib.pyplot as plt

## General simulation parameters
num_simulations = 10**4
num_samples_per_sim = 100
ber_p = 0.6
epsilon = 0.1 # For P[p^ > p+epsilon] bound calculation

bounds_theoretical = (0.24,0.86) # Bounds from Chebyshev's & Markov's inequality; calculated manually

## Params to measure
bounds_estimator = (1,0)         # (min,max) values of estimator
num_greater = 0                  # Num sample sets with p^ > p+eplsilon
list_data = list()               # List of data points for n, p^ > p+epsilon
dist_data = list()               # Distribution of p^


for sim_no in range(num_simulations):
    ## Create a Bernoulli random generator
    x_gen = Ber(ber_p)
    x = x_gen.rvs(num_samples_per_sim)
    
    mean = x.mean()
    if mean >= ber_p+epsilon: num_greater += 1
    
    epsilon_probability = round(num_greater/float(sim_no+1),3)
    if epsilon_probability < bounds_estimator[0]: bounds_estimator = (epsilon_probability, bounds_estimator[1])
    if epsilon_probability > bounds_estimator[1]: bounds_estimator = (bounds_estimator[0], epsilon_probability)
      
    list_data.append((sim_no+1, epsilon_probability))
    dist_data.append((sim_no+1, mean))
    
    
print("Avg p^:", round(sum([mean for _,mean in dist_data])/float(len(dist_data)),4))
print("Bounds of p^:", bounds_estimator)
print("p^ > p+epsilon probability:", round(num_greater/float(num_simulations), 4))
plt.scatter(*zip(*list_data), color='r', s=0.1)
plt.plot([0,num_simulations], [bounds_theoretical[0],bounds_theoretical[0]], color = 'blue', label="Upper bound by Chebyshev's inequality")
plt.plot([0,num_simulations], [bounds_theoretical[1],bounds_theoretical[1]], color = 'green', label="Upper bound by Markov's inequality")
plt.title('Plot of #coin flips vs P[p^>p+epsilon]')
plt.xlabel('x100 coin flips')
plt.ylabel('P[p^>p+epsilon]')
#plt.scatter(*zip(*dist_data))
plt.legend()
plt.show()
