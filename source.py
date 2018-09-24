import pandas as pd
import random
from math import factorial
from itertools import permutations, tee, zip_longest


def pairwise(iterable):
    # s -> (s0,s1), (s1,s2), (s2, s3), ...
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def pairwise_circle(iterable):
    # s -> (s0,s1), (s1,s2), (s2, s3), ... (s<last>,s0)
    a, b = tee(iterable)
    first_value = next(b, None)
    return zip_longest(a, b, fillvalue=first_value)


def number_permutations(n, k):
    '''
    return the number of ordered permutations of
    k items taken from a population of size n
    uses algorithm n!/(n-k)!
    '''
    return factorial(n)/factorial(n-k)


def distance_two_cities(city_a, city_b, data_frame):
    city_names = data_frame.columns.values
    city_dict = {}
    for index, city in enumerate(city_names):
        city_dict[city] = index
    return data_frame.iloc[city_dict[city_a]][city_dict[city_b]]


def distance_of_whole_trip(one_whole_trip_array, data_frame):
    each_trip_dist_array = [distance_two_cities(city_pair[0], city_pair[1], data_frame) for city_pair in
                            pairwise_circle(one_whole_trip_array)]
    return sum(each_trip_dist_array)


def exhaustive_search(data_frame, search_depth):
    selected_cities = data_frame.columns.values[0:search_depth]

    min_distance = float("inf")
    min_route = []
    for one_whole_trip in permutations(selected_cities):
        distance_calculated = distance_of_whole_trip(one_whole_trip, data_frame)
        if distance_calculated < min_distance:
            min_distance = distance_calculated
            min_route = one_whole_trip

    return min_distance, list(min_route)


def hill_climbing(data_frame, search_depth):
    # need to consider 1. choice of initial state 2. successor function (2-opt move in below case)
    selected_cities = data_frame.columns.values[0:search_depth]
    ran_num = random.randint(1, number_permutations(search_depth, search_depth))
    initial_state = list([*permutations(selected_cities)][ran_num])

    # print("Original route : ", initial_state, " distance : ", distance_of_whole_trip(initial_state, data_frame))
    best_distance = float("inf")
    best_route = []
    improved = True
    while improved:
        improved = False
        for i in range(1, search_depth - 2):
            for j in range(i + 1, search_depth):
                if j - i == 1: continue
                new_route = initial_state
                new_route[i:j] = initial_state[j-1:i-1:-1]
                distance_calculated = distance_of_whole_trip(new_route, data_frame)
                if distance_calculated < best_distance:
                    best_distance = distance_calculated
                    best_route = new_route
                    improved = True
    return best_distance, best_route


if __name__ == "__main__":
    europe_cities_data_frame = pd.read_csv("european_cities.csv", sep=';')

    print("Exhaustive Search Result : ", exhaustive_search(europe_cities_data_frame, 6))
    print("hill Climbing result : ", hill_climbing(europe_cities_data_frame, 6))
