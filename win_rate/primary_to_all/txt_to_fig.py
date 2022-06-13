import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


DIGIT = 3


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
    tips = sns.load_dataset('tips')
    plt.figure(figsize=(10,8))
    plt.title('Row v.s. Col')
    # ax = sns.heatmap(res, annot=True, fmt='.2f')
    ax = sns.violinplot(data=res)
    if vector:
        plt.savefig(np.save+',eps', dpi=600, format='eps')
    else:
        plt.savefig(save_path)
    plt.show()


def auto_model_name(model_id, s, t, k, n_digit=None):
    models = []
    for i in range(s, t + k, k):
        if n_digit is not None:
            ind = str(i).zfill(n_digit)
        else:
            ind = str(i)
        models.append(model_id + '_' + ind)
    return models


def auto_focus(model_id, focus_list, n_digit=None):
    f_models = []
    for i in focus_list:
        if n_digit is not None:
            ind = str(i).zfill(n_digit)
        else:
            ind = str(i)
        f_models.append(model_id + '_' + ind)
    return f_models
        

def main():
    model_id = '0601a'
    # optional
    models = auto_model_name(model_id, 10, 150, 20, n_digit=DIGIT)
    focus = auto_focus(model_id, [30, 90, 150], n_digit=DIGIT)
    vector = False

    left_models = []
    right_models = []
    wr = [] 
    l_wr = []
    r_wr = []
    file=open('win_rate/primary_to_all/data/exp2.txt')
    save_path = 'win_rate/primary_to_all/fig/exp2'

    for line in file.readlines():  
        curLine=line.split(",")

        lm = curLine[0].strip("'()")
        ind_lm = lm.split('_')[1].zfill(DIGIT)
        lm = lm.split('_')[0] + '_' + ind_lm

        rm = curLine[1].strip(" ')")
        ind_rm = rm.split('_')[1].zfill(DIGIT)
        rm = rm.split('_')[0] + '_' + ind_rm

        l_win = float(curLine[2].strip(" win_rate: "))
        r_win = 1 - l_win
        if lm in focus:
            left_models.append(lm)
            l_wr.append(l_win)
        if rm in focus:
            right_models.append(rm)
            r_wr.append(r_win)

        if lm not in models:
            models.append(lm)
        if rm not in models:
            models.append(rm)

    left_side = ['left' for _ in range(len(l_wr))]
    right_side = ['right' for _ in range(len(r_wr))]
    data = list(zip(left_models + right_models, l_wr + r_wr, left_side + right_side))
    df = pd.DataFrame(data, columns=['model', 'win_rate', 'side'])

    plt.figure(figsize=(10, 8))
    plt.title('primary vs all')
    sns.set_palette("muted")
    sns.violinplot(
        x=df['model'].astype('category'),
        y=df['win_rate'], hue=df['side'].astype('category'),
        split=True,
        # scale='count'
        )

    if vector:
        plt.savefig(save_path+'.eps', dpi=600, format='eps')
    else:
        plt.savefig(save_path)

    plt.show()
    

if __name__ == "__main__":
    main()
