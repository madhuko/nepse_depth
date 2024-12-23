# %%
from nepse import AsyncNepse 
import asyncio
import pandas as pd
from datetime import datetime
import os

# %%
nepse = AsyncNepse()
nepse.setTLSVerification(False)  # Temporary, until NEPSE sorts its SSL certificate problem

async def fetch_company_details():
    # Fetch the list of companies
    company_list = await nepse.getCompanyList()

    # Fetch details for each company concurrently
    tasks = [
        nepse.getCompanyDetails(company['symbol']) 
        for company in company_list 
        if company['status'] == 'A'
    ]

    company_details = await asyncio.gather(*tasks)

    # Combine company and details
    result = []
    for company, details in zip(company_list, company_details):
        # If details is a list, handle it appropriately
        if isinstance(details, list):
            # Add details as a key-value pair
            result.append({**company, "details": details})
        elif isinstance(details, dict):
            # Merge dictionaries directly
            result.append({**company, **details})
        else:
            # Handle unexpected formats (optional)
            result.append({**company, "details": str(details)})

    return result

# Define the main function to execute the workflow
async def main():
    results = await fetch_company_details()

    # Ensure the "files/" directory exists
    os.makedirs("files", exist_ok=True)

    # Generate filename with timestamp
    now = datetime.now()
    filename = now.strftime("%Y-%m-%d_%H-%M-%S")
    pd.DataFrame.from_dict(results).to_excel(f"files/{filename}.xlsx", index=False)

# Execute the main function
asyncio.run(main())
