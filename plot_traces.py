if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np
    import sys
    data = np.load(sys.argv[-1], allow_pickle=True).tolist()
    traces = data['responses']
    title = data['key']
    
    ncol = int(np.sqrt(len(traces)))
    nrow = int(np.ceil(len(traces) / ncol))

    plt.figure(figsize=(15, 15))
    plt.title(str(title))
    for i, (k, tr) in enumerate(traces.items()):
        plt.subplot(ncol, nrow, i+1)
        plt.title(k)
        plt.plot(tr['time'], tr['voltage'])

    plt.show()
