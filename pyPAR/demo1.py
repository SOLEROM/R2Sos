import threading
import time
import random

# Define a CPU-intensive task that each thread will run
def heavy_computation_task(task_id, iterations=1000000):
    print(f"Task {task_id}: Starting")
    result = 0
    for i in range(iterations):
        # Simulate heavy computation
        result += i ** 2

        # Print when the thread might be rescheduled (simulate context switch)
        if i % (iterations // 10) == 0:  # Print progress every 10% of the task
            print(f"Task {task_id}: Working... (Iteration {i})")

    print(f"Task {task_id}: Completed. Result = {result}")

def main():
    # List to hold all threads
    threads = []

    # Start 4 threads with heavy computation tasks
    for i in range(4):
        # Create a thread targeting the heavy_computation_task function
        thread = threading.Thread(target=heavy_computation_task, args=(i,))
        threads.append(thread)
        thread.start()  # Start the thread

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("All tasks completed!")

if __name__ == "__main__":
    main()



## run demo:

# Task 0: Starting
# Task 0: Working... (Iteration 0)
# Task 1: Starting
# Task 1: Working... (Iteration 0)
# Task 2: Starting
# Task 1: Working... (Iteration 100000)
# Task 2: Working... (Iteration 0)
# Task 3: Starting
# Task 0: Working... (Iteration 100000)
# Task 1: Working... (Iteration 200000)
# Task 2: Working... (Iteration 100000)
# Task 1: Working... (Iteration 300000)
# Task 0: Working... (Iteration 200000)
# Task 2: Working... (Iteration 200000)
# Task 3: Working... (Iteration 0)
# Task 1: Working... (Iteration 400000)
# Task 0: Working... (Iteration 300000)
# Task 3: Working... (Iteration 100000)
# Task 2: Working... (Iteration 300000)
# Task 0: Working... (Iteration 400000)
# Task 2: Working... (Iteration 400000)
# Task 3: Working... (Iteration 200000)
# Task 0: Working... (Iteration 500000)
# Task 2: Working... (Iteration 500000)
# Task 1: Working... (Iteration 500000)
# Task 0: Working... (Iteration 600000)
# Task 2: Working... (Iteration 600000)
# Task 3: Working... (Iteration 300000)
# Task 0: Working... (Iteration 700000)
# Task 1: Working... (Iteration 600000)
# Task 2: Working... (Iteration 700000)
# Task 0: Working... (Iteration 800000)
# Task 3: Working... (Iteration 400000)
# Task 1: Working... (Iteration 700000)
# Task 2: Working... (Iteration 800000)
# Task 3: Working... (Iteration 500000)
# Task 1: Working... (Iteration 800000)
# Task 2: Working... (Iteration 900000)
# Task 0: Working... (Iteration 900000)
# Task 3: Working... (Iteration 600000)
# Task 2: Completed. Result = 333332833333500000
# Task 1: Working... (Iteration 900000)
# Task 3: Working... (Iteration 700000)
# Task 0: Completed. Result = 333332833333500000
# Task 1: Completed. Result = 333332833333500000
# Task 3: Working... (Iteration 800000)
# Task 3: Working... (Iteration 900000)
# Task 3: Completed. Result = 333332833333500000
# All tasks completed!