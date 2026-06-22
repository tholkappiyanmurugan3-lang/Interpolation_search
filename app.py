import streamlit as st

def interpolation_search(arr, target):
    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high and target >= arr[low] and target <= arr[high]:
        comparisons += 1

        if low == high:
            if arr[low] == target:
                return low, comparisons
            return -1, comparisons

        if arr[high] == arr[low]:
            break

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

st.title("Interpolation Search")

numbers = st.text_input(
    "Enter sorted numbers",
    "2 5 10 15 23 35 48 60 75 90 105 120"
)

target = st.number_input("Target", step=1, value=35)

if st.button("Search"):
    arr = list(map(int, numbers.split()))
    index, comparisons = interpolation_search(arr, target)

    st.write("Index:", index)
    st.write("Comparisons:", comparisons)
