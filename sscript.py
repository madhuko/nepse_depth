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

    # Ensure the "files/" directory exists
    os.makedirs("files", exist_ok=True)

    # Generate filename with timestamp
    now = datetime.now() - timedelta(hours=5, minutes=45)
    filename = now.strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"files/{filename}.json", "w") as f:
        json.dump(results, f, indent=4)
# Execute the main function
asyncio.run(main())

# %%
