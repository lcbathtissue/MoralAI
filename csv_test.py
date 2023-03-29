import csv

def save_csv_file(data, filename):
    with open(filename, mode='w', newline='') as csv_file:
        fieldnames = [
            'Scenario number (1,2 or 3)', 
            'Iteration number', 
            'Agent number', 
            'd: Number of collected targets by the agent', 
            'e: Number of steps taken by the agent at the end of iteration', 
            'f: Agent happiness: f=d/(e+1)', 
            'g: Maximum happiness in each iteration', 
            'h: Minimum happiness in each iteration', 
            'Average happiness in each iteration', 
            'Standard deviation of happiness in each iteration', 
            'k: Agent competitiveness: k=(f-h)/(g-h)'
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in data:
            row['f: Agent happiness: f=d/(e+1)'] = row['d: Number of collected targets by the agent'] / (row['e: Number of steps taken by the agent at the end of iteration'] + 1)  # Calculate happiness
            writer.writerow(row)
        
        iter_data = {} 
        for row in data:
            iter_num = row['Iteration number']
            if iter_num not in iter_data:
                iter_data[iter_num] = []
            iter_data[iter_num].append(row['f: Agent happiness: f=d/(e+1)'])
        
        for iter_num in sorted(iter_data.keys()):
            happiness_values = iter_data[iter_num]
            max_happiness = max(happiness_values)
            min_happiness = min(happiness_values)
            avg_happiness = sum(happiness_values) / len(happiness_values)
            std_dev_happiness = (sum((x - avg_happiness) ** 2 for x in happiness_values) / len(happiness_values)) ** 0.5
            
            # Write happiness statistics row for current iteration
            writer.writerow({
                'Scenario number (1,2 or 3)': '',
                'Iteration number': iter_num,
                'Agent number': '',
                'd: Number of collected targets by the agent': '',
                'e: Number of steps taken by the agent at the end of iteration': '',
                'f: Agent happiness: f=d/(e+1)': max_happiness,
                'g: Maximum happiness in each iteration': '',
                'h: Minimum happiness in each iteration': min_happiness,
                'Average happiness in each iteration': avg_happiness,
                'Standard deviation of happiness in each iteration': std_dev_happiness,
                'k: Agent competitiveness: k=(f-h)/(g-h)': '',
            })

data = [
    {
        'Scenario number (1,2 or 3)': 1, 
        'Iteration number': 1, 
        'Agent number': 1, 
        'd: Number of collected targets by the agent': 10, 
        'e: Number of steps taken by the agent at the end of iteration': 20
    },
    {
        'Scenario number (1,2 or 3)': 1, 
        'Iteration number': 1, 
        'Agent number': 1, 
        'd: Number of collected targets by the agent': 10, 
        'e: Number of steps taken by the agent at the end of iteration': 20
    },
]

save_csv_file(data, "test_csv.csv")