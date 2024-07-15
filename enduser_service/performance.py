# curl -o /dev/null -s -w "\n\
# Time Namelookup:  %{time_namelookup}\n\
# Time Connect:  %{time_connect}\n\
# Time Appconnect:  %{time_appconnect}\n\
# Time Pretransfer:  %{time_pretransfer}\n\
# Time Redirect:  %{time_redirect}\n\
# Time Starttransfer:  %{time_starttransfer}\n\
# Time Total:  %{time_total}\n" "http://localhost:5001/mq" -d '{"query": "write poem on demons"}'

# curl -o /dev/null -s -w "\n\
# Time Namelookup:  %{time_namelookup}\n\
# Time Connect:  %{time_connect}\n\
# Time Appconnect:  %{time_appconnect}\n\
# Time Pretransfer:  %{time_pretransfer}\n\
# Time Redirect:  %{time_redirect}\n\
# Time Starttransfer:  %{time_starttransfer}\n\
# Time Total:  %{time_total}\n" "http://localhost:5001/llm" -d '{"query": "write poem on demons"}'

import requests
import time

# Define your endpoints
mq_url = "http://llm_service:5001/mq"
llm_url = "http://llm_service:5001/llm"
query = {"query": "write poem on demons"}

# Number of requests to send
n = 100  # Adjust the number of requests as needed

# Initialize counters
mq_times = []
llm_times = []
mq_faster_count = 0
llm_faster_count = 0

# Perform latency tests
for _ in range(n):
    # Test /mq endpoint
    start_time = time.time()
    requests.post(mq_url, json=query)
    end_time = time.time()
    mq_duration = end_time - start_time
    mq_times.append(mq_duration)

    # Test /llm endpoint
    start_time = time.time()
    requests.post(llm_url, json=query)
    end_time = time.time()
    llm_duration = end_time - start_time
    llm_times.append(llm_duration)

    # Compare the response times
    if mq_duration < llm_duration:
        mq_faster_count += 1
    elif llm_duration < mq_duration:
        llm_faster_count += 1

# Calculate average latencies
average_mq_time = sum(mq_times) / len(mq_times)
average_llm_time = sum(llm_times) / len(llm_times)

# Print out the results
print(f"Average latency for /mq: {average_mq_time:.4f} seconds")
print(f"Average latency for /llm: {average_llm_time:.4f} seconds")
print(f"/mq was faster {mq_faster_count} times")
print(f"/llm was faster {llm_faster_count} times")
print(f"Total requests: {n}")
