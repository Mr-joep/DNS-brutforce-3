import csv
import asyncio
import aiomultiprocess
import socket
import tqdm

# Function to perform DNS lookup for a domain
async def lookup_domain(domain):
    try:
        ip_address = await loop.getaddrinfo(domain, None)
        return domain, ip_address[0][4][0] if ip_address else None
    except Exception as e:
        return domain, str(e)

# Function to process a batch of domains
async def process_batch(batch):
    results = []
    for domain in batch:
        result = await lookup_domain(domain)
        results.append(result)
    return results

# Main function to read domains from input CSV, perform DNS lookup, and write results to output CSV
async def main(input_file, output_file):
    loop = asyncio.get_event_loop()
    
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        domains = [row[0] for row in reader]

    batch_size = 5000  # You can adjust this batch size based on your preference
    batches = [domains[i:i + batch_size] for i in range(0, len(domains), batch_size)]

    with tqdm.tqdm(total=len(domains)) as pbar:
        async with aiomultiprocess.Pool() as pool:
            tasks = []
            for batch in batches:
                tasks.append(process_batch(batch))
            results = await asyncio.gather(*tasks)
            for result_batch in results:
                for result in result_batch:
                    with open(output_file, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(result)
                    pbar.update(1)

if __name__ == "__main__":
    input_csv = "subdomains.csv"
    output_csv = "dns_results.csv"

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(input_csv, output_csv))
    loop.close()
