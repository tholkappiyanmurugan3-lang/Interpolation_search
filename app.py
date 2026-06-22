from flask import Flask, render_template
import time
import random

app = Flask(__name__)


# Interpolation Search
def interpolation_search(arr, target):
    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high and arr[low] <= target <= arr[high]:
        comparisons += 1

        if low == high:
            if arr[low] == target:
                return low, comparisons
            return -1, comparisons

        pos = low + int(
            ((target - arr[low]) * (high - low))
            / (arr[high] - arr[low])
        )

        if arr[pos] == target:
            return pos, comparisons
        elif arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1

    return -1, comparisons


# Binary Search
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high:
        comparisons += 1
        mid = (low + high) // 2

        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1, comparisons


# Performance Analysis
def performance_analysis():
    sizes = [1000, 5000, 10000, 50000, 100000]
    results = []

    for size in sizes:
        arr = sorted(random.sample(range(size * 10), size))
        target = random.choice(arr)

        start = time.perf_counter()
        for _ in range(100):
            _, comp_is = interpolation_search(arr, target)
        is_time = (time.perf_counter() - start) / 100 * 1000

        start = time.perf_counter()
        for _ in range(100):
            _, comp_bs = binary_search(arr, target)
        bs_time = (time.perf_counter() - start) / 100 * 1000

        results.append({
            "size": size,
            "is_time": round(is_time, 6),
            "bs_time": round(bs_time, 6),
            "is_comp": comp_is,
            "bs_comp": comp_bs
        })

    return results


@app.route("/")
def home():
    arr = [2, 5, 10, 15, 23, 35, 48, 60, 75, 90, 105, 120]
    target = 35

    index, comparisons = interpolation_search(arr, target)
    comparison = performance_analysis()

    return render_template(
        "index.html",
        array=arr,
        target=target,
        index=index,
        comparisons=comparisons,
        comparison=comparison
    )


if __name__ == "__main__":
    app.run(debug=True)