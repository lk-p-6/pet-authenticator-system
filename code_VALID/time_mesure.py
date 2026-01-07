import requests
import time

apiUrl = "http://127.0.0.1:8000/code"
data_payload = {
    "code": "012345",
}

mid_num_arr = []
mid_num_sum = 0

min_value = 0
p90 = 0
p95 = 0
p99 = 0
max_value= 0
risk_ratio = 0
avg_dif = 0

ttl = 10.0

try:
    for i in range(100):
        t1 = time.perf_counter()
        response = requests.post(apiUrl, json=data_payload, timeout=2)
        t2 = time.perf_counter()
        mid_num_arr.append(t2-t1)
        time.sleep(0.2)

    mid_num_arr.sort()
    min_value = mid_num_arr[0]
    p90 = mid_num_arr[int(len(mid_num_arr) * 0.9)-1]
    p95 = mid_num_arr[int(len(mid_num_arr) * 0.95)-1]
    p99 = mid_num_arr[int(len(mid_num_arr) * 0.99)-1]
    max_value = mid_num_arr[len(mid_num_arr)-1]
    risk_ratio = (max_value / ttl) * 100

    for i in mid_num_arr:
        mid_num_sum += i
        
    avg_dif = mid_num_sum/len(mid_num_arr)

    print("min value:", min_value)
    print("p90:", p90)
    print("p95:", p95)
    print("p99:", p99)
    print("max value:", max_value)
    print("difference between max value and ttl:", risk_ratio, "%")
    print("average number:", avg_dif)
except:
    print("HTTP error occurred:")