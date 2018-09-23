import pandas as pd
from itertools import permutations, repeat, tee, zip_longest


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


def distance_two_cities(city_a, city_b, data_frame):
    city_names = data_frame.columns.values
    city_dict = {}
    for index, city in enumerate(city_names):
        city_dict[city] = index
    return data_frame.iloc[city_dict[city_a]][city_dict[city_b]]


def exhaustive_search(data_frame, search_depth):
    selected_data_frame = data_frame.loc[:, :'Budapest'][:search_depth]
    distance_two_cities('Barcelona', 'Belgrade', data_frame)

    min_distance = float("inf")
    min_route = []

    for one_travel in permutations(selected_data_frame.columns.values):
        each_trip_dist_array = []
        for city_pair in pairwise_circle(one_travel):
            each_trip_dist_array.append(distance_two_cities(city_pair[0], city_pair[1], selected_data_frame))
        distance_calculated = sum(each_trip_dist_array)

        if distance_calculated < min_distance:
            min_distance = distance_calculated
            min_route = one_travel
            
    print(min_distance, min_route)


if __name__ == "__main__":
    europe_cities_data_frame = pd.read_csv("european_cities.csv", sep=';')
    exhaustive_search(europe_cities_data_frame, 6)
