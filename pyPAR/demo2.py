import multiprocessing
import time

# Define a CPU-intensive task that each process will run
def heavy_computation_task(task_id, iterations=1000000):
    print(f"Task {task_id}: Starting")
    result = 0
    for i in range(iterations):
        # Simulate heavy computation
        result += i ** 2

        # Print when the process might be rescheduled (simulate context switch)
        if i % (iterations // 10) == 0:  # Print progress every 10% of the task
            print(f"Task {task_id}: Working... (Iteration {i})")

    print(f"Task {task_id}: Completed. Result = {result}")

def main():
    # List to hold all processes
    processes = []

    # Start 4 processes with heavy computation tasks
    for i in range(4):
        # Create a process targeting the heavy_computation_task function
        process = multiprocessing.Process(target=heavy_computation_task, args=(i,))
        processes.append(process)
        process.start()  # Start the process

    # Wait for all processes to complete
    for process in processes:
        process.join()

    print("All tasks completed!")

if __name__ == "__main__":
    main()
    
    
## demo run:

# Task 0: Starting
# Task 0: Working... (Iteration 0)
# Task 1: Starting
# Task 1: Working... (Iteration 0)
# Task 2: Starting
# Task 2: Working... (Iteration 0)
# Task 3: Starting
# Task 3: Working... (Iteration 0)
# Task 0: Working... (Iteration 100000)
# Task 3: Working... (Iteration 100000)
# Task 2: Working... (Iteration 100000)
# Task 1: Working... (Iteration 100000)
# Task 0: Working... (Iteration 200000)
# Task 3: Working... (Iteration 200000)
# Task 2: Working... (Iteration 200000)
# Task 1: Working... (Iteration 200000)
# Task 3: Working... (Iteration 300000)
# Task 0: Working... (Iteration 300000)
# Task 1: Working... (Iteration 300000)
# Task 2: Working... (Iteration 300000)
# Task 3: Working... (Iteration 400000)
# Task 1: Working... (Iteration 400000)
# Task 2: Working... (Iteration 400000)
# Task 0: Working... (Iteration 400000)
# Task 3: Working... (Iteration 500000)
# Task 1: Working... (Iteration 500000)
# Task 2: Working... (Iteration 500000)
# Task 0: Working... (Iteration 500000)
# Task 3: Working... (Iteration 600000)
# Task 1: Working... (Iteration 600000)
# Task 2: Working... (Iteration 600000)
# Task 3: Working... (Iteration 700000)
# Task 0: Working... (Iteration 600000)
# Task 1: Working... (Iteration 700000)
# Task 2: Working... (Iteration 700000)
# Task 3: Working... (Iteration 800000)
# Task 1: Working... (Iteration 800000)
# Task 0: Working... (Iteration 700000)
# Task 2: Working... (Iteration 800000)
# Task 3: Working... (Iteration 900000)
# Task 1: Working... (Iteration 900000)
# Task 0: Working... (Iteration 800000)
# Task 2: Working... (Iteration 900000)
# Task 3: Completed. Result = 333332833333500000
# Task 1: Completed. Result = 333332833333500000
# Task 2: Completed. Result = 333332833333500000
# Task 0: Working... (Iteration 900000)
# Task 0: Completed. Result = 333332833333500000
# All tasks completed!