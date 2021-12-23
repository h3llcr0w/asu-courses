import math
import pprint
import random
import baseline
import numpy as np
from time import time
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from collections import OrderedDict
import matplotlib.patches as patches

unif  = np.random.uniform

def rect_area(p1, p2): return abs((p1[0]-p2[0])*(p1[1]-p2[1]))

def get_points(func, limits, num_segments, area_tol=10e-12):
    def get_next_point(func, limits, start_x, ref_area, area_tol=10e-16):
        xmin, xmax = start_x, limits[1]
        midpoint = (xmin+xmax)/2
        mid_area = rect_area((limits[0], func(start_x)), (midpoint, func(midpoint)))
        while abs(ref_area-mid_area)>area_tol:
            midpoint = (xmin+xmax)/2
            mid_area = rect_area((limits[0], func(start_x)), (midpoint, func(midpoint)))
            if ref_area>mid_area: xmin = midpoint
            elif ref_area<mid_area: xmax = midpoint

            if midpoint == limits[1]: return None, None

        return (xmin+xmax)/2, mid_area

    total_area = integrate.quad(func, *limits)[0]
    ref_area = total_area/num_segments
    area_max = total_area
    area_min = 0
    nth_area = 0
    nth_rect_probability = 0

    x_list = [limits[0]]
    area_list = list()
    
    while abs(nth_area-ref_area)>area_tol:
        x_list = [limits[0]]
        area_list = []
        for _ in range(num_segments-1):
            x_point, area = get_next_point(func, limits, x_list[-1], ref_area)
            if not x_point: continue
            x_list.append(x_point)
            area_list.append(area)
        nth_area = rect_area((limits[0], 0), (x_list[-1], func(x_list[-1]))) + integrate.quad(func, x_list[-1], limits[1])[0]
        nth_rect_probability = rect_area((limits[0], 0), (x_list[-1], func(x_list[-1]))) / nth_area 
        area_list.append(nth_area)

        if nth_area>ref_area:
            area_min = ref_area
        elif ref_area>nth_area:
            area_max = ref_area
        ref_area = (area_min+area_max)/2

    y_list = [func(x) for x in x_list]
    return x_list, y_list, nth_rect_probability


def ziggurat(func, func_limits=(0,float('inf')), num_samples=1, num_segments=4, area_tolerance=10e-12):
    samples = list()

    ## Precompute stage
    x_list, y_list, nth_rect_probability = get_points(func, func_limits, num_segments, area_tolerance)

    time_start = time()
    time_random = 0

    stats = OrderedDict.fromkeys(['X is accepted because X<xk', 
                                  'X>xk but X is accepted because Y<g(X)', 
                                  'Y>g(X) so X is rejected', 
                                  'Sample drawn from rectangular part of nth region', 
                                  'Tail algorithm is run'], 0)

    ## Sampling stage
    while(len(samples)<num_samples):
        time_s = time()
        k = int(random.random()*num_segments)
        time_random += (time()-time_s)
        if k<num_segments-1:
            time_s = time()
            x = unif(x_list[0], x_list[k+1])
            time_random += (time()-time_s)
            if x<x_list[k]:
                stats['X is accepted because X<xk'] += 1
                samples.append(x)
                continue
            else:
                time_s = time()
                y = unif(y_list[k], y_list[k+1])
                time_random += (time()-time_s)
                if y<func(x):
                    stats['X>xk but X is accepted because Y<g(X)'] += 1
                    samples.append(x)
                    continue
                else:
                    stats['Y>g(X) so X is rejected'] += 1
        else:
            rect_select = unif(0,1)
            if rect_select<nth_rect_probability:
                stats['Sample drawn from rectangular part of nth region'] += 1
                samples.append(unif(x_list[0], x_list[-1]))
            else:
                stats['Tail algorithm is run'] += 1
                samples.append(baseline.baseline(func, (x_list[-1], func_limits[1]), 1))
                #samples.append(ziggurat(func, (x_list[-1], func_limits[1]), 1, num_segments))

    time_end = time()
    print(f"Time taken for {num_samples} samples using N={num_segments}:", time_end-time_start)
    #print("Time taken for random number generation: ", time_random)
    [print(key, ":", value) for key,value in stats.items()]
    return samples, list(zip(x_list, y_list))



if __name__ == '__main__':
    
    ## Experiment settings
    show_rects = False
    segment_list = [4]
    sample_list = [10**6]
    #segment_list = [4, 32, 256]              ## Uncomment to run for all combinations
    #sample_list = [10**5, 10**6, 10**7]      ## Uncomment to run for all combinations
    area_tolerance = 10e-12
    
    ## PDF function (monotonically decreasing, not normalized
    gx = lambda x: math.exp(x-2*math.exp(x))
    func_limits = (0,3)

    ## Calculate normalized PDF
    c = integrate.quad(gx, *func_limits)[0]
    func = lambda x: gx(x)/c

    fig = plt.figure(1)
    ## Generate Ziggurat samples for all experiment settings
    for seg_i, num_segments in enumerate(segment_list):
        for sample_i, num_samples in enumerate(sample_list):
            samples, rects = ziggurat(func, func_limits, num_samples=num_samples, num_segments=num_segments, area_tolerance=area_tolerance)

            ax = fig.add_subplot(len(segment_list), len(sample_list), len(sample_list)*(seg_i)+sample_i+1)
            ax.hist(samples, bins=1000, density=True, label='Histogram of generated samples')
            x = np.linspace(*func_limits, 50000)
            ax.plot(x, [func(x_) for x_ in x], label='PDF')
            ax.set_title(f'Ziggurat sampling with N={num_segments} for {num_samples} samples')
            
            if show_rects:
                for rect_ind in range(1, len(rects)):
                    ax.add_patch(patches.Rectangle((rects[0][0], rects[rect_ind][1]), rects[rect_ind][0]-rects[0][0], rects[rect_ind-1][1]-rects[rect_ind][1], edgecolor='red', facecolor='none', linewidth=2),)

            ax.legend()
    
    plt.show()

