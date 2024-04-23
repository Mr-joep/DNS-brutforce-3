import csv
import asyncio
import aiomultiprocess
import tqdm

# Function to perform DNS lookup for a domain
async def lookup_domain(domain):
    try:
        ip_address = await loop.getaddrinfo(domain, None)
        return domain, ip_address[0][4][0] if ip_address else None
    except Exception as e:
        return domain, str(e)

# Function to process a chunk of domains
async def process_chunk(chunk, pbar):
    results = []
    for domain in chunk:
        result = await lookup_domain(domain)
        results.append(result)
        pbar.update(1)
    return results

# Main function to read domains from input CSV, perform DNS lookup, and write results to output CSV
async def main(input_file, output_file, chunk_size=500):
    loop = asyncio.get_event_loop()

    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header
        domains = [row[0] for row in reader]

    with tqdm.tqdm(total=len(domains)) as pbar:
        for i in range(0, len(domains), chunk_size):
            chunk = domains[i:i + chunk_size]
            async with aiomultiprocess.Pool() as pool:
                results = await process_chunk(chunk, pbar)
                write_results(output_file, results)

def write_results(output_file, results):
    with open(output_file, 'a', newline='') as f:
        writer = csv.writer(f)
        for result in results:
            writer.writerow(result)

if __name__ == "__main__":
    input_csv = "subdomains.csv"
    output_csv = "dns_results.csv"
    chunk_size = 500  # Adjust as needed

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(input_csv, output_csv, chunk_size))
    loop.close()
