import multiprocessing
import psutil
import time

# Define the worker task that runs indefinitely
def worker_task(task_id, shutdown_event):
    print(f"Worker {task_id}: Starting")

    while not shutdown_event.is_set():
        print(f"Worker {task_id}: Working on CPU {psutil.Process().cpu_num()}")
        time.sleep(1)

    print(f"Worker {task_id}: Shutting down gracefully")

# Set CPU affinity for a process
def set_cpu_affinity(worker, cpus):
    p = psutil.Process(worker.pid)
    p.cpu_affinity(cpus)  # Bind the process to specific CPUs
    print(f"Worker {worker.pid} is now set to run on CPUs: {cpus}")

# Start and manage workers
def start_workers_with_affinity(num_workers, cpu_affinities):
    workers = []
    shutdown_events = []

    for i in range(num_workers):
        shutdown_event = multiprocessing.Event()
        shutdown_events.append(shutdown_event)

        worker = multiprocessing.Process(target=worker_task, args=(i, shutdown_event))
        worker.start()
        workers.append(worker)

        # Set CPU affinity for this worker
        set_cpu_affinity(worker, cpu_affinities[i])
        
        ## other way to set cpu affinity
        # os.sched_setaffinity(pid, cpus)

    return workers, shutdown_events

def stop_workers(workers, shutdown_events):
    for event in shutdown_events:
        event.set()

    for worker in workers:
        worker.join()

if __name__ == "__main__":
    # Define CPU affinities for each worker (each worker on a separate CPU core)
    cpu_affinities = [
        [0],  # Worker 0 on CPU 0
        [1],  # Worker 1 on CPU 1
        [2],  # Worker 2 on CPU 2
        [3],  # Worker 3 on CPU 3
    ]

    # Start 4 workers with specific CPU affinities
    workers, shutdown_events = start_workers_with_affinity(4, cpu_affinities)

    # Let the workers run for a while
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        print("Shutting down workers...")

    # Gracefully stop workers
    stop_workers(workers, shutdown_events)
    print("All workers shut down.")
