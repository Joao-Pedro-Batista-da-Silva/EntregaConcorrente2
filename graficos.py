import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt

def separa_por_tam(doc,tam):
    df = pd.read_csv(doc)
    
    df_grupos = df.groupby("tamanhoN")
    
    df = df_grupos.get_group(tam)
    return df

def gera_tempo_medio(doc,tam):
    df = separa_por_tam(doc,tam)
    
    mean_tempo = df.groupby('nthreads')['processamento'].mean()
    return mean_tempo

def gera_aceleração(doc,tam):
    mean_tempo = gera_tempo_medio(doc,tam)
    aceleração = {}
    for i in mean_tempo.keys():
        aceleração[i] = mean_tempo[1]/mean_tempo[i]
    return aceleração

def gera_eficiencia(doc,tam):
    mean_tempo = gera_tempo_medio(doc,tam)
    aceleração = gera_aceleração(doc,tam)
    eficiencia = {}
    for i in mean_tempo.keys():
        eficiencia[i] = aceleração[i]/i
    return eficiencia

def gera_plot(doc):
    tams = pd.read_csv('dados.csv')['tamanhoN'].unique()
    cols = math.ceil(math.sqrt(len(tams)))
    rows = math.ceil(len(tams)/cols)
    fig, axs = plt.subplots(rows, cols, figsize=(6*cols, 5*rows))
    axs = np.array(axs).reshape(-1)
    for idx, tam in enumerate(tams):
        mean_tempo = gera_tempo_medio(doc,tam)
        tempo_seq = mean_tempo[1]
        mean_tempo_percent = (mean_tempo/tempo_seq)
        aceleracao = gera_aceleração(doc,tam)
        eficiencia = gera_eficiencia(doc,tam)
        num_threads = [f"{k} threads" for k in mean_tempo.keys()]
        ax = axs[idx]
        height_bar = 0.3
        y = np.arange(len(num_threads))
        #print(mean_tempo.values)
        #print(np.array(aceleracao.values()))

        bar_tempo = ax.barh(y - height_bar, mean_tempo_percent.values,height=height_bar, color='blue', alpha = 0.6, label='Tempo')
        bar_acel = ax.barh(y, aceleracao.values(),height=height_bar, color='green', alpha=0.6, label='Aceleração')
        bar_efic =ax.barh(y+height_bar, eficiencia.values(),height=height_bar, color='red', alpha=0.6, label='Eficiência')

        
        ax.bar_label(bar_tempo, labels=[f'{v:.5f} s' for v in mean_tempo.values], label_type='edge', padding= 5)
        ax.bar_label(bar_acel, fmt='%.5f', label_type='edge', padding= 5)
        ax.bar_label(bar_efic, fmt='%.5f', label_type='edge', padding= 5)
        ax.set_yticks(y)
        ax.set_yticklabels(num_threads)
        ax.set_xlabel('Valores')
        ax.set_ylabel('Número de threads')
        ax.set_title(f'Tamanho {tam}')
        ax.xaxis.set_visible(False)
        if(idx == 0):
            ax.legend()
        max_value = max(
            max(mean_tempo_percent.values),
            max(aceleracao.values()),
            max(eficiencia.values())
        )
        ax.set_xlim(0, max_value * 1.5)
    
    plt.tight_layout(pad=3.0)
    plt.show()
gera_plot('dados.csv')

