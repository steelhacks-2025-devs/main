import asyncio
import json
import aiohttp
import requests
import time
import pandas as pd
from client import WPRDC_Client

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Load parcel IDs from the dataset file
def load_parcel_ids():
    parcel_ids = set()
    with open("../datasets/parcels_stripdistrict.txt", "r") as file:
        for line in file:
            parcel_id = line.strip()
            if parcel_id:  # Skip empty lines
                parcel_ids.add(parcel_id)
    return parcel_ids

# Load the parcel IDs
parcel_ids = load_parcel_ids()
print(f"Loaded {len(parcel_ids)} parcel IDs")

async def get_parcel_data(client, parcel_id):
    response = await client._make_request(parcel_id)
    return response

async def main():
    async with WPRDC_Client() as client:
        tasks = []
        for parcel_id in parcel_ids:
            tasks.append(get_parcel_data(client, parcel_id))
        print("starting tasks...")
        results = await asyncio.gather(*tasks, return_exceptions=True)
        print(results[15:20])
        print("tasks completed")
        df = pd.DataFrame(results)
        df.to_csv("parcel_data.csv", index=False)
        print("data saved to parcel_data.csv")

start_time = time.time()
asyncio.run(main())
end_time = time.time()
print(f"Time taken: {end_time - start_time} seconds")