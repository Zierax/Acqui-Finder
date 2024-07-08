Run the script with the following command:

```
python script.py company_name [--sleep SLEEP] [--verbose] [--threads THREADS]
```
company_name: Name of the company to search acquisitions for.
--sleep SLEEP: Delay in seconds between requests (default: 0).
--verbose: Enable verbose output.
--threads THREADS: Number of threads for concurrent processing (default: 1).
Example usage:
```
python script.py "Company Inc." --sleep 1.5 --verbose --threads 3
```
