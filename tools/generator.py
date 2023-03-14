import random

def dearrangement(arr):
    init_arr, d_arr = arr[:], arr[:]

    if len(arr) == 1:
        return arr

    while True:
        found_match = False
        for i in range(len(d_arr)):
            if d_arr[i] == init_arr[i]:
                random.shuffle(d_arr)
                found_match = True
                break

        if not found_match:
            break

    return d_arr