import csv
import string
import itertools
import time

def count_subdomains(domain, max_length):
    count = 0
    characters = string.ascii_lowercase + string.digits
    for length in range(1, max_length + 1):
        count += len(characters) ** length
    return count

def generate_subdomains(domain, max_length, progress_callback=None, update_interval=1):
    characters = string.ascii_lowercase + string.digits
    total_subdomains = count_subdomains(domain, max_length)
    subdomains_generated = 0
    last_progress = 0
    start_time = time.time()
    
    for length in range(1, max_length + 1):
        for subset in itertools.product(characters, repeat=length):
            subdomain = ''.join(subset)
            yield subdomain + '.' + domain
            subdomains_generated += 1
            progress = subdomains_generated / total_subdomains
            current_time = time.time()
            if progress_callback and current_time - start_time >= update_interval:
                progress_callback(progress * 100)
                start_time = current_time

def save_subdomains_to_csv(subdomains, filename, chunk_size=1000):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Subdomain"])
        chunk = []
        for subdomain in subdomains:
            chunk.append([subdomain])
            if len(chunk) == chunk_size:
                writer.writerows(chunk)
                chunk = []
        if chunk:
            writer.writerows(chunk)

def main():
    domain = input("Enter the domain: ")
    max_length = int(input("Enter the maximum length of subdomain: "))
    
    total_subdomains = count_subdomains(domain, max_length)
    print(f"Total number of subdomains to be generated: {total_subdomains}")
    
    def progress_callback(progress):
        print(f"Generating... {progress:.2f}% complete", end='\r')

    start_time = time.time()
    subdomains = generate_subdomains(domain, max_length, progress_callback)
    filename = "subdomains.csv"
    save_subdomains_to_csv(subdomains, filename)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nGenerated subdomains are saved in '{filename}'.")
    print(f"Total time taken: {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    main()
