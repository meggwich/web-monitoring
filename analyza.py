import csv
import datetime

def process_csv(file_path):
    
    data = []
    
    with open(file_path, mode='r') as file:
        
        reader = csv.DictReader(file)
        
        for row in reader:
            
            row['timestamp'] = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
            row['available'] = row['available'] == 'True'
            row['load_time'] = float(row['load_time'])
            row['info'] = int(row['info'])
            
            data.append(row)
    
    return data

def calculate_metrics(data):
    
    metrics = {
        'total_measurements': 0,
        'total_available': 0,
        'total_load_time': 0,
        'total_long_loads': 0,
        'total_errors': 0,
        'total_size': 0,
        'start_time': min(row['timestamp'] for row in data),
        'end_time': max(row['timestamp'] for row in data),
        'urls': {}
    }

    for row in data:
        
        url = row['url']
        
        if url not in metrics['urls']:
            
            metrics['urls'][url] = {
                'measurements': 0,
                'available': 0,
                'load_time': 0,
                'long_loads': 0,
                'errors': 0
            }
        
        metrics['total_measurements'] += 1
        metrics['urls'][url]['measurements'] += 1
        
        if row['available']:
            
            metrics['total_available'] += 1
            metrics['urls'][url]['available'] += 1
            
        else:
            
            metrics['total_errors'] += 1
            metrics['urls'][url]['errors'] += 1
        
        metrics['total_load_time'] += row['load_time']
        metrics['urls'][url]['load_time'] += row['load_time']
        
        if row['load_time'] > 10:
            
            metrics['total_long_loads'] += 1
            metrics['urls'][url]['long_loads'] += 1
        
        metrics['total_size'] += row['info']

    for url in metrics['urls']:
        
        metrics['urls'][url]['availability'] = (metrics['urls'][url]['available'] / metrics['urls'][url]['measurements']) * 100
        metrics['urls'][url]['average_load_time'] = metrics['urls'][url]['load_time'] / metrics['urls'][url]['measurements']
    
    metrics['availability'] = (metrics['total_available'] / metrics['total_measurements']) * 100
    metrics['average_load_time'] = metrics['total_load_time'] / metrics['total_measurements']
    
    return metrics


csv_file_path = 'monitoring_log.csv'
data = process_csv(csv_file_path)
metrics = calculate_metrics(data)

print(metrics)
