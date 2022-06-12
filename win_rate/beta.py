import seaborn as sns
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd


def export(data, models=None):

    if models is not None:
        n_models = len(models)
        wr_mat = -1.0 * np.ones((n_models, n_models), dtype=np.float32)
        for m in range(n_models):
            wr_mat[m, m] = 0.5
            
        for d in data:
            row = models.index(d[0])
            col = models.index(d[1])
            wr_mat[row, col] = d[2]
        
        # check and repair
        for i in range(n_models):
            for j in range(n_models):
                if wr_mat[i, j] == -1.0:
                    if wr_mat[j, i] != -1.0:
                        wr_mat[i, j] = 1.0 - wr_mat[j, i]
                    else:
                        print(f"{models[i]} vs {models[j]} Data Missing.")
        
        res = pd.DataFrame(wr_mat,columns=models, index=models)
        plt.figure(figsize=(10,8))
        ax = sns.heatmap(res)
        plt.show()
    
    else:
        # Todo: extract model info from source data
        pass


def main():
    # models = None
    models = []
        
    left_models = []
    right_models = []
    wr = [] 
    file=open('win_rate/data/real.txt')

    for line in file.readlines():  
        curLine=line.split(",")
        lm = curLine[0].strip("'()")
        rm = curLine[1].strip(" ')")
        left_models.append(lm)
        right_models.append(rm)

        if lm not in models:
            models.append(lm)
        if rm not in models:
            models.append(rm)
        
        wr.append(curLine[2].strip(" win_rate: "))

    data = zip(left_models, right_models, wr)

    export(data, sorted(models))
    

if __name__ == "__main__":
    main()
