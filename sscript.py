# %%
from nepse import AsyncNepse 
import asyncio
import pandas as pd
from datetime import datetime

# %%
nepse = AsyncNepse()
nepse.setTLSVerification(False) #This is temporary, until nepse sorts its ssl certificate problem
# abc=nepse.getCompanyList()

# %%

# Assuming `nepse.getCompanyList` and `nepse.getCompanyDetails` are asynchronous functions

async def fetch_company_details():
    # Fetch the list of companies
    company_list = nepse.getCompanyList()

    # Fetch details for each company concurrently
    tasks = [nepse.getCompanyDetails(company['symbol']) for company in company_list if company['status'] == 'A']

    company_details = await asyncio.gather(*tasks)

    # Combine symbol and details for better output
    result = [{**company, **details} for company, details in zip(company_list, company_details)]

    return result

# %%
async def main():
    results = await fetch_company_details()
    now = datetime.now()
    filename = now.strftime("%Y-%m-%d_%H-%M-%S")
    pd.DataFrame.from_dict(results).to_excel(f"files/{filename}.xlsx", index=False)

# Execute the main async function
asyncio.run(main())

# %%
