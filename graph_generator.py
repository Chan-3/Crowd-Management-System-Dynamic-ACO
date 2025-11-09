"""Graph generator"""
import sys
import os
import csv
import matplotlib.pyplot as plt

def read_csv(filepath):
    data = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def plot_convergence(run_dir):
    convergence_file = os.path.join(run_dir, 'convergence.csv')
    if not os.path.exists(convergence_file):
        print(f"Convergence file not found: {convergence_file}")
        return
    data = read_csv(convergence_file)
    if not data:
        print("No convergence data")
        return
    iterations = [int(row['iteration']) for row in data]
    path_lengths = [float(row['best_path_length']) for row in data]
    plt.figure(figsize=(10, 6))
    plt.plot(iterations, path_lengths, 'b-', linewidth=2)
    plt.xlabel('Iteration', fontsize=12)
    plt.ylabel('Best Path Length', fontsize=12)
    plt.title('ACO Convergence', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    output_file = os.path.join(run_dir, 'convergence_graph.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Convergence graph saved: {output_file}")
    plt.close()

def plot_evacuation(run_dir):
    evacuation_file = os.path.join(run_dir, 'evacuation.csv')
    if not os.path.exists(evacuation_file):
        print(f"Evacuation file not found: {evacuation_file}")
        return
    data = read_csv(evacuation_file)
    if not data:
        print("No evacuation data")
        return
    time_steps = [int(row['time_step']) for row in data]
    evacuated = [int(row['evacuated']) for row in data]
    remaining = [int(row['remaining']) for row in data]
    fire_cells = [int(row['fire_cells']) for row in data]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    ax1.plot(time_steps, evacuated, 'g-', linewidth=2, label='Evacuated')
    ax1.plot(time_steps, remaining, 'b-', linewidth=2, label='Remaining')
    ax1.set_xlabel('Time Steps', fontsize=12)
    ax1.set_ylabel('Number of People', fontsize=12)
    ax1.set_title('Evacuation Progress', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax2.plot(time_steps, fire_cells, 'r-', linewidth=2)
    ax2.set_xlabel('Time Steps', fontsize=12)
    ax2.set_ylabel('Fire Cells', fontsize=12)
    ax2.set_title('Fire Spread', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    output_file = os.path.join(run_dir, 'evacuation_graph.png')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Evacuation graph saved: {output_file}")
    plt.close()

def generate_all_graphs(run_dir):
    print(f"Generating graphs for: {run_dir}")
    plot_convergence(run_dir)
    plot_evacuation(run_dir)
    print("Done!")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python graph_generator.py <run_directory>")
        print("Example: python graph_generator.py runs/20241109_143022")
        sys.exit(1)
    run_dir = sys.argv[1]
    if not os.path.exists(run_dir):
        print(f"Directory not found: {run_dir}")
        sys.exit(1)
    generate_all_graphs(run_dir)