from multiprocessing import Pool
from tqdm import tqdm
import time

# Function to be processed
def process_item(item):
    time.sleep(0.1)  # Simulate work
    return item * 2

# Callback to update the progress bar
def update_progress_bar(_, pbar):
    pbar.update()

def pmap(items, n_processes = 8):
    with Pool(n_processes) as pool:
        # Create a tqdm progress bar
        with tqdm(total=len(items)) as pbar:
            for item in items:
                pool.apply_async(
                    process_item, 
                    args=(item,), 
                    callback=lambda x: update_progress_bar(x, pbar)
                )

            # Close the pool and wait for the work to finish
            pool.close()
            pool.join()
