# python parallel


* For I/O-bound tasks: Multithreading can be useful, but it's limited by the GIL.
* For CPU-bound tasks: Multiprocessing is more effective because it bypasses the GIL and achieves parallelism.


### Multithreading:

Python has a threading module that allows you to run multiple threads within the same process. However, due to the Global Interpreter Lock (GIL), only one thread can execute Python bytecode at a time in a single process. This makes Python threading less efficient for CPU-bound tasks (e.g., heavy calculations) but useful for I/O-bound tasks (like network operations, file I/O).

### Multiprocessing:

Python's multiprocessing module allows the creation of separate processes, each with its own memory space and GIL. This means that true parallelism can be achieved, making it ideal for CPU-bound tasks. Each process runs in its own Python interpreter, so they can run concurrently on multiple cores.


## best practice:

 * critical multithreaded task system 
 * prevent starvation, 
 * set task priorities, 
 * ensure task resilience (respawning downed tasks)



Task Pool with Thread Prioritization: Use a priority queue to manage task priorities and dynamically assign tasks to threads. Higher-priority tasks get executed first.

Worker Pool: Use a thread pool (or worker pool) where each worker thread fetches tasks from the priority queue and executes them. If a worker fails, you need a way to detect failure and respawn the thread.

Task Monitoring and Resilience: Implement task health checks, so if a task fails, it can be automatically respawned or retried.

Task Preemption: While Python doesn’t have preemption for threads directly, you can structure tasks to yield time (using time.sleep()) for fair CPU time distribution.

Handling Exceptions: Capture exceptions in tasks to ensure they don’t crash your worker threads. If a thread crashes, handle restarting it or re-enqueue the task.

```python

import threading
import time
import queue
import random

# Define task priorities (lower number = higher priority)
class TaskPriorities:
    HIGH = 1
    MEDIUM = 2
    LOW = 3

# Define a task that has a priority and performs a job
class Task:
    def __init__(self, priority, task_id, job):
        self.priority = priority
        self.task_id = task_id
        self.job = job

    def run(self):
        print(f"Task {self.task_id}: Starting with priority {self.priority}")
        try:
            self.job()  # Perform the task's job
        except Exception as e:
            print(f"Task {self.task_id} failed with exception: {e}")
            raise e
        print(f"Task {self.task_id}: Completed")

# Thread worker that fetches tasks from the priority queue
def worker_thread(task_queue, shutdown_event):
    while not shutdown_event.is_set():
        try:
            priority, task = task_queue.get(timeout=1)
            task.run()
        except queue.Empty:
            continue  # No task to run, loop again
        except Exception as e:
            print(f"Worker failed with task {task.task_id}, restarting...")
            # Handle task failure (e.g., re-enqueue or log)
        finally:
            task_queue.task_done()

# Function to spawn worker threads and manage task execution
def start_task_pool(num_workers, task_queue):
    shutdown_event = threading.Event()
    workers = []

    for i in range(num_workers):
        t = threading.Thread(target=worker_thread, args=(task_queue, shutdown_event))
        t.daemon = True
        t.start()
        workers.append(t)

    return workers, shutdown_event

# Respawn downed worker threads (monitoring mechanism)
def monitor_workers(workers, shutdown_event):
    while not shutdown_event.is_set():
        for i, worker in enumerate(workers):
            if not worker.is_alive():
                print(f"Worker {i} died. Respawning...")
                t = threading.Thread(target=worker_thread, args=(task_queue, shutdown_event))
                t.daemon = True
                t.start()
                workers[i] = t
        time.sleep(5)  # Monitor every 5 seconds

# Sample jobs (replace with your actual workload)
def high_priority_job():
    time.sleep(random.uniform(0.5, 1.0))  # Simulate workload

def medium_priority_job():
    time.sleep(random.uniform(1.0, 2.0))  # Simulate workload

def low_priority_job():
    time.sleep(random.uniform(2.0, 3.0))  # Simulate workload

# Main function to manage task pool and scheduling
if __name__ == "__main__":
    # Create a priority queue to hold tasks
    task_queue = queue.PriorityQueue()

    # Define some tasks
    tasks = [
        Task(TaskPriorities.HIGH, "High_1", high_priority_job),
        Task(TaskPriorities.MEDIUM, "Medium_1", medium_priority_job),
        Task(TaskPriorities.LOW, "Low_1", low_priority_job),
        Task(TaskPriorities.HIGH, "High_2", high_priority_job),
        Task(TaskPriorities.MEDIUM, "Medium_2", medium_priority_job),
    ]

    # Enqueue tasks with priorities
    for task in tasks:
        task_queue.put((task.priority, task))

    # Start a pool of 3 workers
    workers, shutdown_event = start_task_pool(3, task_queue)

    # Monitor and respawn downed workers
    monitor_thread = threading.Thread(target=monitor_workers, args=(workers, shutdown_event))
    monitor_thread.daemon = True
    monitor_thread.start()

    # Let the workers process the tasks for a while
    try:
        time.sleep(20)  # Simulate the system running
    except KeyboardInterrupt:
        print("Shutdown requested...")

    # Shutdown the system gracefully
    shutdown_event.set()
    task_queue.join()  # Wait for all tasks to complete
    print("All tasks completed and workers shut down.")


```