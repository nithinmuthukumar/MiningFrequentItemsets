from collections import defaultdict

import matplotlib.pyplot as plt

from count_frequent_pairs import *


def calc_time(baskets, support, bucket_size):
    start_time = time.time()
    apriori(baskets, support)
    apriori_time = time.time() - start_time

    start_time = time.time()
    pcy(baskets, support, bucket_size)
    pcy_time = time.time() - start_time

    start_time = time.time()
    multistage_pcy(baskets, support, bucket_size)
    multistage_pcy_time = time.time() - start_time

    start_time = time.time()
    multihash_pcy(baskets, support, bucket_size)
    multihash_pcy_time = time.time() - start_time

    return apriori_time, pcy_time, multistage_pcy_time, multihash_pcy_time


if __name__ == "__main__":
    thresholds = [0.01, 0.05, 0.1]
    chunks = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    bucket_size = 40000
    run_times = {
        threshold: {chunk: None for chunk in chunks} for threshold in thresholds
    }
    for threshold in thresholds:
        for chunk in chunks:
            print(f"{threshold=}, {chunk=}")
            with open("retail.txt", "r") as file:
                baskets = [
                    [int(i) for i in line.strip().split(" ")]
                    for line in file.readlines()
                ]
                num_baskets = int(round(chunk * len(baskets)))

                support = int(round(num_baskets * threshold))
                run_times[threshold][chunk] = calc_time(
                    baskets[:num_baskets], support, bucket_size
                )
    print(run_times)
    for threshold in thresholds:
        for i, algorithm in enumerate(
            ["Apriori", "PCY", "Multistage PCY", "Multihash PCY"]
        ):
            y = [run_times[threshold][chunk][i] for chunk in chunks]

            plt.plot(
                chunks,
                y,
                label=algorithm,
            )

        plt.title(f"Support Threshold: {threshold*100}%")
        plt.xlabel("Dataset Size")
        plt.ylabel("Run time (seconds)")
        plt.legend()
        plt.show()
