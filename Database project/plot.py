import matplotlib.pyplot as plt
import json

def plot_execution_times():
    # Load execution times from JSON file
    with open('execution_times.json', 'r') as f:
        execution_times = json.load(f)

    # Prepare data for plotting
    file_sizes = ['1MB', '10MB', '100MB']
    queries = list(execution_times.keys())

    # Create a separate plot for each query
    for i, query in enumerate(queries):
        times = execution_times[query]
        
        plt.figure()  # Create a new figure for each query
        plt.plot(file_sizes, times, marker='o', label=query[:30])  # Plot only the first 30 characters of the query for clarity
        plt.title(f'Execution Time for Query {i + 1}: {query[:30]}...')  # Title for each query
        plt.xlabel('File Size')
        plt.ylabel('Execution Time (seconds)')
        plt.xticks(file_sizes)
        plt.grid(True)

        # Save the plot as a file
        plt.savefig(f'query_{i + 1}_execution_time.png')
        plt.close()  # Close the figure after saving

if __name__ == "__main__":
    plot_execution_times()
