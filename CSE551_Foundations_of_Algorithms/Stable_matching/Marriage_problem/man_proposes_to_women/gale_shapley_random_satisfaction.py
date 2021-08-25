################################################################
#      Gale-Shapley algorithm for Stable Marriage Problem      #
#      --------------------------------------------------      #
# * Time complexity : O(n^2)                                   #
#                                                              #
# * Preference matrices are generated randomly                 #
# * Satisfaction metric is defined based on pref vs assignment #
#                                                              #
# - Python3 implementation, Mishel Paul, 08/25/2021            #
################################################################

import random

## Number of men & women (in pairs)
num_pairs = 3

## List of people
men_list = ['Xavier', 'Yancey', 'Zeus']
women_list = ['Amy', 'Bertha', 'Claire']

## Sample preference tables
men_pref   = [random.sample(list(range(num_pairs)), num_pairs) for i in range(num_pairs)]
women_pref = [random.sample(list(range(num_pairs)), num_pairs) for i in range(num_pairs)]

print(men_pref)
print(women_pref)

women_inv_pref = []
for woman_pref in women_pref:
    inv_pref = [-1]*num_pairs
    for i in range(num_pairs):
        inv_pref[woman_pref[i]] = i
    women_inv_pref.append(inv_pref)

## Queue for free men; initialized to everyone free
free_men = list(range(num_pairs))
random.shuffle(free_men)

## Array for number of women proposed to by a man
proposal_count = [0]*num_pairs

## Matching result data (initialized to -1 for unmatched since indexing starts from 0)
husband = [-1]*num_pairs
wife = [-1]*num_pairs

## Gale-Shapley / propose-and-reject algorithm

# algorithm stable_matching is
#     Initialize m belongs to M and w belongs W to free
#     while there exists free man m who has a woman w to propose to do
#         w := first woman on m's list to whom m has not yet proposed
#         if there exists some pair (m', w) then
#             if w prefers m to m' then
#                 m' becomes free
#                 (m, w) become engaged
#             end if
#         else
#             (m, w) become engaged
#         end if
#     repeat
#
# Source: https://en.wikipedia.org/wiki/Gale%E2%80%93Shapley_algorithm

while(len(free_men)!=0):
    m = free_men.pop(0)
    print("Matching man {0}".format(men_list[m]))
    wife[m] = -1
    if proposal_count[m] > num_pairs:
        print(f'Man {m} has exhausted max number of proposals. GS somehow failed (0_0) or there is something wrong with the implementation.')
        break
    while(wife[m]==-1 and proposal_count[m]<=num_pairs):
        w = men_pref[m][proposal_count[m]]
        print("Proposing to {0}".format(women_list[w]))
        m_prime = husband[w]
        if m_prime == -1:
            husband[w] = m
            wife[m] = w
        elif m_prime != -1 and women_inv_pref[w][m_prime]>women_inv_pref[w][m]:
            husband[w] = m
            wife[m] = w
            wife[m_prime] = -1
            free_men.append(m_prime)
        proposal_count[m] += 1

print("Final stable perfect matching:")
for i in range(num_pairs):
    print(men_list[i], women_list[wife[i]])

## Calculating satisfaction metric:

men_inv_pref = []
for man_pref in men_pref:
    inv_pref = [-1]*num_pairs
    for i in range(num_pairs):
        inv_pref[man_pref[i]] = i
    men_inv_pref.append(inv_pref)

men_satisfaction = [(3-men_inv_pref[m][wife[m]])*100/3 for m in range(num_pairs)]
women_satisfaction = [(3-women_inv_pref[w][husband[w]])*100/3 for w in range(num_pairs)]

print("Average matching satisfaction for men: {0}".format(sum(men_satisfaction)/num_pairs))
print("Average matching satisfaction for women: {0}".format(sum(women_satisfaction)/num_pairs))
