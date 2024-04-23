import csv
import asyncio
import aiodns
import tqdm
import os

# Set event loop policy to use SelectorEventLoop on Windows
if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Function to perform DNS lookup for a domain
async def lookup_domain(domain, resolver):
    try:
        result = await resolver.query(domain, 'A')
        return domain, [response.host for response in result] if result else None
    except Exception as e:
        return domain, str(e)

# Function to process a chunk of domains
async def process_chunk(chunk, resolver, pbar):
    async_results = [lookup_domain(domain, resolver) for domain in chunk]
    results = await asyncio.gather(*async_results)
    pbar.update(len(chunk))
    return results

# Main function to read domains from input CSV, perform DNS lookup, and write results to output CSV
async def main(input_file, output_file, chunk_size=300):
    resolver = aiodns.DNSResolver()

    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header
        domains = [row[0] for row in reader]

    with tqdm.tqdm(total=len(domains)) as pbar:
        for i in range(0, len(domains), chunk_size):
            chunk = domains[i:i + chunk_size]
            results = await process_chunk(chunk, resolver, pbar)
            write_results(output_file, results)

def write_results(output_file, results):
    with open(output_file, 'a', newline='') as f:
        writer = csv.writer(f)
        for result in results:
            writer.writerow(result)

if __name__ == "__main__":
    input_csv = "subdomains.csv"
    output_csv = "dns_results.csv"
    chunk_size = 300  # Adjust as needed

    asyncio.run(main(input_csv, output_csv, chunk_size))
