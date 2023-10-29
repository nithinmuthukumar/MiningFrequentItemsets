import time
from collections import Counter, defaultdict
from itertools import combinations


def apriori(baskets, support):
    frequent_items = get_frequent_items(baskets, support)
    frequent_pairs = get_frequent_pairs(baskets, frequent_items, support)
    return frequent_pairs


def pcy(baskets, support):
    hash_table = defaultdict(int)

    for basket in baskets:
        pairs = set(combinations(basket, 2))
        for pair in pairs:
            key = hash(pair)
            hash_table[key] += 1

    frequent_items = get_frequent_items(baskets, support)

    frequent_pairs = dict()
    for pair in combinations(frequent_items.keys(), 2):
        key = hash(pair)
        if hash_table[key] >= support:
            pair_count = sum(
                1 for basket in baskets if all(item in basket for item in pair)
            )
            if pair_count >= support:
                frequent_pairs[pair] = pair_count
    return frequent_pairs


def get_frequent_items(baskets, support):
    occurrences = Counter()

    for basket in baskets:
        occurrences.update(basket)
    frequent_items = {k: v for (k, v) in occurrences.items() if v >= support}
    return frequent_items


def get_frequent_pairs(baskets, frequent_items, support):
    candidate_pairs = list(combinations(frequent_items.keys(), 2))
    pair_occurences = Counter()
    for basket in baskets:
        for pair in candidate_pairs:
            if all(p in basket for p in pair):
                pair_occurences[pair] += 1
    frequent_pairs = {k: v for (k, v) in pair_occurences.items() if v >= support}
    return frequent_pairs


if __name__ == "__main__":
    with open("retail.txt", "r") as file:
        baskets = [
            [int(i) for i in line.strip().split(" ")] for line in file.readlines()
        ][0:10000]
        support = round(len(baskets) * 0.01)

        start_time = time.time()
        print(len(apriori(baskets, support)))
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")

        start_time = time.time()
        print(len(pcy(baskets, support)))
        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Execution time: {execution_time} seconds")
        execution_time = end_time - start_time
