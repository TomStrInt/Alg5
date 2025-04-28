def insertion_sort(arr):
    comparisons = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            comparisons += 1
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        if j >= 0:
            comparisons += 1  
    return arr, comparisons


def merge(left, right):
    merged = []
    i = j = comparisons = 0

    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, comparisons


def merge_sort(arr, run_size):
    if len(arr) <= run_size:
        return insertion_sort(arr)  # sortowanie małych fragmentow 

    mid = len(arr) // 2
    left, left_comparisons = merge_sort(arr[:mid], run_size)
    right, right_comparisons = merge_sort(arr[mid:], run_size)

    merged, merge_comparisons = merge(left, right)
    total_comparisons = left_comparisons + right_comparisons + merge_comparisons
    return merged, total_comparisons


def test_algorithm():
    sizes = [10, 50, 100]
    run_sizes = [4, 8, 16]
    datasets = {
        "posortowane": [i for i in range(1, 101)],
        "wstepnie_posortowane": [i if i % 10 != 0 else i - 1 for i in range(1, 101)],
        "przypadkowa kolejnosc": [45, 78, 12, 89, 33, 67, 56, 88, 21, 34],
        "odwrocone": [i for i in range(100, 0, -1)]
    }

    for run_size in run_sizes:
        print(f"Run size: {run_size}")
        for dataset_type, dataset in datasets.items():
            print(f"Typ danych:   {dataset_type}")
            sorted_array, comparisons = merge_sort(dataset, run_size)
            print(f"Liczba porownan:   {comparisons}\n")

test_algorithm()
