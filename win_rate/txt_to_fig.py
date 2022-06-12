
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def export(data, models, save_path, model_sort=False, check=True, vector=False):
    if model_sort:
        models = sorted(models)
    n_models = len(models)
    wr_mat = -1.0 * np.ones((n_models, n_models), dtype=np.float32)
    for m in range(n_models):
        wr_mat[m, m] = 0.5
        
    for d in data:
        row = models.index(d[0])
        col = models.index(d[1])
        wr_mat[row, col] = d[2]
    
    # check and repair
    if check:
        for i in range(n_models):
            for j in range(n_models):
                if wr_mat[i, j] == -1.0:
                    if wr_mat[j, i] != -1.0:
                        wr_mat[i, j] = 1.0 - wr_mat[j, i]
                    else:
                        print(f"{models[i]} vs {models[j]} Data Missing.")
    
    res = pd.DataFrame(wr_mat, columns=models, index=models)
    plt.figure(figsize=(10,8))
    plt.title('Row v.s. Col')
    ax = sns.heatmap(res, annot=True, fmt='.2f')
    if vector:
        plt.savefig(np.save+',eps', dpi=600, format='eps')
    else:
        plt.savefig(save_path)
    plt.show()



def main():
    # models = None
    models = ['0601a_10', '0601a_30', '0601a_50', '0601a_70', '0601a_90', '0601a_110', '0601a_130', '0601a_150']
        
    left_models = []
    right_models = []
    wr = [] 
    file=open('win_rate/data/exp2.txt')
    save_path = 'win_rate/fig/exp2'

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

    export(data, models, save_path, model_sort=False, check=True, vector=False)
    

if __name__ == "__main__":
    main()
