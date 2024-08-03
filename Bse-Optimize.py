import time
import pandas as pd
import re
from bsedata.bse import BSE
import os
import logging
from plyer import notification
from datetime import datetime


notification.notify(
    title="Script started",
    message="Your scheduled Python script has finished running.",
    timeout=10
)

log_file = r"C:\Users\sumeet\Desktop\LargeDeals\script_log.txt"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

logging.info("Script started")



# Load the CSV file
n = pd.read_csv(r"C:\Users\sumeet\Desktop\LargeDeals\MarketCap\BseStocks.csv")
n['code'] = n['code'].astype(str)


# Initialize BSE API
b = BSE()

# Function to get data for one stock code
def get_stock_info(x, b):
    try:
        q = b.getQuote(x)
        return {
            'updatedOn': q.get('updatedOn', 'n/a'),
            'marketCapFull': q.get('marketCapFull', 'n/a'),
            'marketCapFreeFloat': q.get('marketCapFreeFloat', 'n/a')
        }
    except Exception as e:
        return {
            'updatedOn': 'n/a',
            'marketCapFull': 'n/a',
            'marketCapFreeFloat': 'n/a'
        }

# Function to remove "Cr." from text
def substitute_example(input_text):
    if isinstance(input_text, str):
        return input_text.replace("Cr.", "")
    else:
        return None

# Function to keep only numeric characters and dots in text
def regex_replace_example(input_text):
    if isinstance(input_text, str):
        return re.sub(r"[^0-9.]", "", input_text)
    else:
        return None

# Tracking time
start_time = time.time()
num_items = len(n)  # Total number of iterations
completed_items = 0  # Counter for completed iterations

# List to store results
results = []

# Loop through each stock code
for index, row in n.iterrows():
    # Perform the operation (e.g., API call)
    result = get_stock_info(row['code'], b)
    results.append(result)
    
    # # Increment completed items
    # completed_items += 1
    
    # # Calculate elapsed time
    # elapsed_time = time.time() - start_time
    
    # # Calculate average time per item
    # avg_time_per_item = elapsed_time / completed_items
    
    # # Estimate remaining time
    # remaining_items = num_items - completed_items
    # estimated_remaining_time = avg_time_per_item * remaining_items
    
    #No need to use the below one as the cmd prompt is opening
    # # Print progress and estimated remaining time
    # print(f"Processed {completed_items}/{num_items} items. "
    #       f"Estimated remaining time: {estimated_remaining_time:.2f} seconds")


end_time = time.time()

# Calculate total time taken
total_time = end_time - start_time

logging.info(f"Total time taken: {total_time:.2f} seconds")


# Convert results to DataFrame

result_df = pd.DataFrame(results)

# Update original DataFrame with the new data
n = pd.concat([n, result_df], axis=1)

# Clean up the market cap data
n['marketCapFull'] = n['marketCapFull'].apply(substitute_example)
n['marketCapFull'] = n['marketCapFull'].apply(regex_replace_example)

# # Save the result to a new CSV file
# n.to_csv(r"C:\Users\sumeet\Desktop\LargeDeals\MarketCap\TotalMcap.csv", index=False)

# #hellohi

# Define the output file path
today = datetime.today()
filename = f"TotalMcap_{today}.csv"
output_path = r"C:\Users\sumeet\Desktop\LargeDeals\MarketCap"
output_file = os.path.join(output_path, filename)

# Check if the output file already exists
# if os.path.exists(output_file):
#     # If the file exists, read it into a DataFrame and append the new data
#     existing_df = pd.read_csv(output_file)
#     n = pd.concat([existing_df, n], ignore_index=True)

# Save the updated DataFrame to the output CSV file
n.to_csv(output_file, index=False)
logging.info("Script finished successfully")


# After your script logic
notification.notify(
    title="Script Finished",
    message="Your scheduled Python script has finished running.",
    timeout=10
)