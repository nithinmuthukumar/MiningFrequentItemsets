import time
from collections import Counter
from itertools import combinations


def apriori(baskets, support):
    frequent_items = get_frequent_items(baskets, support)
    frequent_pairs = get_frequent_pairs(baskets, frequent_items, support)
    return frequent_pairs


def pcy(baskets, support, bucket_size):
    bucket = [0] * bucket_size

    for basket in baskets:
        pairs = set(combinations(basket, 2))
        for pair in pairs:
            key = hash_pair_1(pair) % bucket_size
            bucket[key] += 1
    bit_vector = get_bit_vector(bucket, support)
    del bucket

    frequent_items = get_frequent_items(baskets, support)

    frequent_pairs = dict()
    for pair in combinations(frequent_items.keys(), 2):
        key = hash_pair_1(pair) % bucket_size
        if bit_vector[key]:
            pair_count = sum(
                1 for basket in baskets if all(item in basket for item in pair)
            )
            if pair_count >= support:
                frequent_pairs[pair] = pair_count
    return frequent_pairs


def get_bit_vector(buckets, support):
    return [i >= support for i in buckets]  # size of bool is also 1


def hash_pair_1(pair):
    return (pair[0] + pair[1]) % 80021


def hash_pair_2(pair):
    return (pair[0] + pair[1]) % 80039


def multistage_pcy(baskets, support, bucket_size):
    bucket_1 = [0] * bucket_size

    for basket in baskets:
        pairs = set(combinations(basket, 2))
        for pair in pairs:
            key = hash_pair_1(pair) % bucket_size
            bucket_1[key] += 1
    bit_vector_1 = get_bit_vector(bucket_1, support)
    del bucket_1

    frequent_items = get_frequent_items(baskets, support)

    bucket_2 = [0] * bucket_size

    for basket in baskets:
        pairs = combinations([i for i in basket if i in set(frequent_items.keys())], 2)
        for pair in pairs:
            key = hash_pair_2(pair) % bucket_size
            bucket_2[key] += 1
    bit_vector_2 = get_bit_vector(bucket_2, support)
    del bucket_2

    candidate_pairs = [
        p
        for p in combinations(frequent_items, 2)
        if bit_vector_1[hash_pair_1(p) % bucket_size]
        and bit_vector_2[hash_pair_2(p) % bucket_size]
    ]
    frequent_pairs = dict()
    for pair in candidate_pairs:
        pair_count = sum(
            1 for basket in baskets if all(item in basket for item in pair)
        )
        if pair_count >= support:
            frequent_pairs[pair] = pair_count

    return frequent_pairs


def multihash_pcy(baskets, support, bucket_size):
    bucket_1 = [0] * bucket_size
    bucket_2 = [0] * bucket_size

    for basket in baskets:
        pairs = set(combinations(basket, 2))
        for pair in pairs:
            key = hash_pair_1(pair) % bucket_size
            bucket_1[key] += 1

            key = hash_pair_2(pair) % bucket_size
            bucket_2[key] += 1

    bit_vector_1 = get_bit_vector(bucket_1, support)
    bit_vector_2 = get_bit_vector(bucket_2, support)
    del bucket_1
    del bucket_2
    frequent_items = get_frequent_items(baskets, support)

    candidate_pairs = [
        p
        for p in combinations(frequent_items, 2)
        if bit_vector_1[hash_pair_1(p) % bucket_size]
        and bit_vector_2[hash_pair_2(p) % bucket_size]
    ]
    frequent_pairs = dict()
    for pair in candidate_pairs:
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
        ]
        support = round(len(baskets) * 0.01)
        bucket_size = 40000

        start_time = time.time()
        print(len(apriori(baskets, support)))
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")

        start_time = time.time()
        print(len(pcy(baskets, support, bucket_size)))
        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Execution time: {execution_time} seconds")

        start_time = time.time()
        print(len(multistage_pcy(baskets, support, bucket_size)))
        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Execution time: {execution_time} seconds")

        start_time = time.time()
        print(len(multihash_pcy(baskets, support, bucket_size)))
        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Execution time: {execution_time} seconds")
