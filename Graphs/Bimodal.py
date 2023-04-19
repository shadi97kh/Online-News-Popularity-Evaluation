import os
import matplotlib.pyplot as plt

def bimodal_predictor(trace_file, m):
    table_size = 1 << m
    table = [0] * table_size
    mask = table_size - 1
    total_branches = 0
    mispredictions = 0

    with open(trace_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line == '':
                continue

            try:
                address, outcome = line.split()
            except ValueError:
                continue

            outcome = 1 if outcome == 't' else 0
            index = int(address, 16) & mask

            prediction = 1 if table[index] > 1 else 0
            if prediction != outcome:
                mispredictions += 1

            if outcome:
                table[index] = min(table[index] + 1, 3)
            else:
                table[index] = max(table[index] - 1, 0)

            total_branches += 1

    return mispredictions / total_branches

trace_files = [r'traces\gcc_trace.txt', r'traces\jpeg_trace.txt', r'traces\perl_trace.txt'] 
ms = list(range(7, 13))

for trace_file in trace_files:
    misprediction_rates = [bimodal_predictor(trace_file, m) for m in ms]
    plt.plot(ms, misprediction_rates, marker='o', linestyle='-')
    plt.xlabel('m')
    plt.ylabel('Branch Misprediction Rate')
    plt.title(f'{os.path.basename(trace_file)}, bimodal')
    plt.xticks(ms)
    plt.grid()
    plt.show()
