import matplotlib.pyplot as plt
import numpy as np
import timeit

# Time Complexity: O(n), Space Complexity: O(1)
def sum_directly(arr):
    total_sum = 0
    for num in arr:
        total_sum += num
    return total_sum

# Time Complexity: O(n), Space Complexity: O(n)
def sum_with_cumulative_array(arr):
    cumulative_sum = np.cumsum(arr)  # This creates a new array of size n
    total_sum = cumulative_sum[-1]
    return total_sum

# A function to plot the time complexities
def plot_time_complexities(array_sizes):
    direct_times = []
    cumulative_times = []

    for size in array_sizes:
        arr = np.random.randint(100, size=size)
        
        # Setup for timeit
        setup_code = f"from __main__ import sum_directly, sum_with_cumulative_array; import numpy as np; arr = np.random.randint(100, size={size})"

        # Timing for direct sum
        direct_time = timeit.timeit("sum_directly(arr)", setup=setup_code, number=1000)
        direct_times.append(direct_time)

        # Timing for cumulative sum
        cumulative_time = timeit.timeit("sum_with_cumulative_array(arr)", setup=setup_code, number=1000)
        cumulative_times.append(cumulative_time)

    plt.plot(array_sizes, direct_times, label='Direct Sum')
    plt.plot(array_sizes, cumulative_times, label='Cumulative Sum Array')
    plt.xlabel('Array Size')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.title('Time Complexity')
    plt.show()

# Define array sizes for the experiment
array_sizes = np.linspace(100, 10000, 20, dtype=int)
plot_time_complexities(array_sizes)
