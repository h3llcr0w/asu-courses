import math
from time import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

unif = np.random.uniform

def cdf(func, x, low_lim):
    return integrate.quad(func, low_lim, x)[0]

def baseline(gx, limits, num_samples, tol=10e-12):
    def inv_cdf(func, u, limits):
        xmin, xmax = limits
        midpoint = (xmin+xmax)/2
        cdf_val = cdf(func, midpoint, limits[0])
        while abs(cdf_val-u)>tol:
            if cdf_val>u:
                xmax=midpoint
            else:
                xmin=midpoint
            midpoint = (xmin+xmax)/2
            cdf_val = cdf(func, midpoint, limits[0])
        return midpoint 

    c = integrate.quad(gx, *limits)[0]
    func = lambda x: gx(x)/c

    time_start = time()
    samples = list()
    while len(samples)<num_samples:
        u = unif(0,1)
        samples.append(inv_cdf(func, u, limits))
    time_end = time()
    if __name__ == '__main__': print(f"Time taken for {num_samples}: ", time_end-time_start)
    if num_samples==1: return samples[0]
    return samples

if __name__ == '__main__':
        
    gx = lambda x: math.exp(x-2*math.exp(x))
    
    for num_samples in [10**5]:
        samples = baseline(gx, (0,3), num_samples)
    plt.hist(samples, bins=100, density=True, label='Histogram of generated samples')
    x = np.linspace(0,3,50000)
    c = integrate.quad(gx, 0, 100)[0]
    plt.plot(x, [gx(x_)/c for x_ in x], label='PDF')
    plt.title('Baseline sampling for 100,000 samples')
    plt.legend()
    plt.show()
