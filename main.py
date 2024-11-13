import requests
import time
import datetime
import csv

# URL na monitorovanie
urls = {
    "homepage": "https://www.buxus.sk/co-je-buxus",
    "info_page": "https://www.buxus.sk/o-firme-ui42"  
}

# Funkcia na kontrolu dostupnosti
def check_availability(url):
    
    try:
        
        response = requests.get(url, timeout=10)
        load_time = response.elapsed.total_seconds()

        if response.status_code == 200:

            return True, load_time, len(response.content)

        else:

            return False, load_time, response.status_code

    except requests.RequestException as e:

        return False, None, str(e)

# Hlavný cyklus na monitorovanie
start_time = datetime.datetime.now()
end_time = start_time + datetime.timedelta(days=7)
log_data = []

print("Starting monitoring...")

while datetime.datetime.now() < end_time:
    
    print("Checking availability...")

    for page, url in urls.items():

        available, load_time, info = check_availability(url)

        log_entry = {
            "url": url,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "available": available,
            "load_time": load_time,
            "info": info
        }

        log_data.append(log_entry)
        print(log_entry)
    
    # Uloženie logov do súboru po každom cykle
    with open('monitoring_log.csv', 'w', newline='') as csvfile:

        fieldnames = ['url', 'timestamp', 'available', 'load_time', 'info']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for entry in log_data:

            writer.writerow(entry)
        print("CSV file updated successfully.")
    
    time.sleep(300)  # Čakaj 5 minút

print("Finished monitoring.")



