import os
from main import set_number_of_threads


def select_optimal_number_of_threads():
    max_cpus = os.cpu_count()
    if 3 <= max_cpus <= 5:
        set_number_of_threads(max_cpus - 1, cahce_warm=True)
    elif 6 <= max_cpus <= 10:
        set_number_of_threads(max_cpus - 2, cahce_warm=True)
    elif 11 <= max_cpus <= 15:
        set_number_of_threads(max_cpus - 3, cahce_warm=True)
    else:
        set_number_of_threads(max_cpus - 4, cahce_warm=True)


def main():
    select_optimal_number_of_threads()


if __name__ == "main":
    main()