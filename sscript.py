# %%
from nepse import AsyncNepse 
import asyncio
import os
from datetime import datetime
import json

# %%
nepse = AsyncNepse()
nepse.setTLSVerification(False)  # Temporary, until NEPSE sorts its SSL certificate problem

async def fetch_market_depth():
    # Fetch the list of companies
    company_list = await nepse.getSecurityList()

    # Fetch market depth for each company concurrently
    tasks = [
        nepse.getSymbolMarketDepth(company['symbol']) 
        for company in company_list 
        if company['activeStatus'] == 'A'
    ]

    company_depths = await asyncio.gather(*tasks, return_exceptions=True)

    # Combine company and market depth
    result = []
    for company, depth in zip(company_list, company_depths):
        if isinstance(depth, Exception):
            # Handle exceptions by adding the error message
            result.append({**company, "error": str(depth)})
        elif isinstance(depth, list):
            # Add depth as a key-value pair
            result.append({**company, "depth": depth})
        elif isinstance(depth, dict):
            # Merge dictionaries directly
            result.append({**company, **depth})
        else:
            # Handle unexpected formats (optional)
            result.append({**company, "depth": str(depth)})

    return result

# Define the main function to execute the workflow
async def main():
    results = await fetch_market_depth()

    # Ensure the "files/" directory exists
    os.makedirs("files", exist_ok=True)

    # Generate filename with timestamp
    now = datetime.now()
    filename = now.strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"files/{filename}.json", "w") as f:
        json.dump(results, f, indent=4)
# Execute the main function
asyncio.run(main())

# %%
