import os
import matplotlib.pyplot as plt

def smith_predictor(trace_file, b):
    counter = (1 << (b - 1)) if b in [5, 6] else 0
    mask = (1 << b) - 1
    total_branches = 0
    mispredictions = 0

    with open(trace_file, 'r') as f:
        for line in f:
            if line.strip() == '':
                continue

            address, outcome = line.strip().split()
            outcome = 1 if outcome == 't' else 0

            prediction = 1 if counter > (mask // 2) else 0
            if prediction != outcome:
                mispredictions += 1

            if outcome:
                counter = min(counter + 1, mask)
            else:
                counter = max(counter - 1, 0)

            total_branches += 1

    return mispredictions / total_branches

trace_files = [r'traces\gcc_trace.txt', r'traces\jpeg_trace.txt', r'traces\perl_trace.txt']  
bs = list(range(1, 7))

for trace_file in trace_files:
    misprediction_rates = [smith_predictor(trace_file, b) for b in bs]
    plt.plot(bs, misprediction_rates, marker='o', linestyle='-')
    plt.xlabel('b')
    plt.ylabel('Branch Misprediction Rate')
    plt.title(f'{os.path.basename(trace_file)}, smith')
    plt.xticks(bs)
    plt.grid()
    plt.show()
