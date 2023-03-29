import csv

def generate_summary_csv(input_file, output_file):
    scenarios = set()
    with open(input_file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        rows = list(csv_reader)
        for row in rows:
            scenarios.add(row['Scenario number (1,2 or 3)'])

    with open(output_file, mode='w', newline='') as summary_csv_file:
        fieldnames = ['Scenario number (1,2 or 3)', 'Average happiness in each iteration', 'Average competitiveness in each iteration']
        csv_writer = csv.DictWriter(summary_csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        for scenario in scenarios:
            happiness_sum = 0
            competitiveness_sum = 0
            iteration_count = 0
            for row in rows:
                if row['Scenario number (1,2 or 3)'] == scenario and row['Average happiness in each iteration']:
                    happiness_sum += float(row['Average happiness in each iteration'])
                    competitiveness_sum += float(row['k: Agent competitiveness: k=(f-h)/(g-h)'])
                    iteration_count += 1
            if iteration_count > 0:
                avg_happiness = happiness_sum / iteration_count
                avg_competitiveness = competitiveness_sum / iteration_count
                csv_writer.writerow({'Scenario number (1,2 or 3)': scenario, 
                                    'Average happiness in each iteration': avg_happiness, 
                                    'Average competitiveness in each iteration': avg_competitiveness})

generate_summary_csv("example_test_csv.csv", "test_csv_summary.csv")
