# %%
from nepse import AsyncNepse 
import asyncio
import os
from datetime import datetime, timedelta
import json

# %%
nepse = AsyncNepse()
nepse.setTLSVerification(False)  # Temporary, until NEPSE sorts its SSL certificate problem

async def fetch_market_depth():
    # Fetch the list of companies
    company_list = await nepse.getSecurityList()
    active_symbols = [company['symbol'] for company in company_list if company['activeStatus'] == 'A']
    tasks = [nepse.getSymbolMarketDepth(symbol) for symbol in active_symbols]

    # Fetch market depths concurrently
    company_depths = await asyncio.gather(*tasks, return_exceptions=True)

    # Create a dictionary to map symbols to their market depth or error codes
    symbol_depth_mapping = {
    symbol: (depth if not isinstance(depth, Exception) else f"error code {depth}")
    for symbol, depth in zip(active_symbols, company_depths)
    }
    return symbol_depth_mapping

# Define the main function to execute the workflow
async def main():
    results = await fetch_market_depth()

    # Calculate the current timestamp and adjust for Nepal's timezone
    now = datetime.now() + timedelta(hours=5, minutes=45)
    timestamp = now.isoformat()

    # Create directory structure: files/<year>/
    year = now.strftime("%Y")
    date = now.strftime("%Y-%m-%d")
    directory = f"files/{year}"
    os.makedirs(directory, exist_ok=True)

    # Define the file path: files/<year>/yyyy-mm-dd.json
    file_path = f"{directory}/{date}.json"

    # Prepare the run data with timestamp
    run_data = {"timestamp": timestamp, "data": results}

    # If the file exists, append the new run data
    if os.path.exists(file_path):
        with open(file_path, 'r+', encoding='utf-8') as f:
            try:
                # Load existing data
                daily_data = json.load(f)
            except json.JSONDecodeError:
                daily_data = []

            # Append the new run data
            daily_data.append(run_data)

            # Write back to the file
            f.seek(0)
            json.dump(daily_data, f, indent=4)
            f.truncate()
    else:
        # If the file doesn't exist, create it with the new run data
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump([run_data], f, indent=4)
asyncio.run(main())

# %%
