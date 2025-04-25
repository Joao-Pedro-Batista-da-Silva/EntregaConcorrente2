import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def separa_por_tam(doc,tam):
    df = pd.read_csv(doc)
    
    df_grupos = df.groupby("tamanhoN")
    
    df = df_grupos.get_group(tam)
    return df

def gera_tempo_medio(doc,tam):
    df = separa_por_tam(doc,tam)
    
    mean_mult = df.groupby('nthreads')['processamento'].mean()
    return mean_mult

def gera_aceleração(doc,tam):
    mean_mult = gera_tempo_medio(doc,tam)
    aceleração = {}
    for i in mean_mult.keys():
        aceleração[i] = mean_mult[1]/mean_mult[i]
    return aceleração

def gera_eficiencia(doc,tam):
    mean_mult = gera_tempo_medio(doc,tam)
    aceleração = gera_aceleração(doc,tam)
    eficiencia = {}
    for i in mean_mult.keys():
        eficiencia[i] = aceleração[i]/i
    return eficiencia

def gera_plot(doc,tam):
    mean_mult = gera_tempo_medio(doc,tam)
    aceleracao = gera_aceleração(doc,tam)
    eficiencia = gera_eficiencia(doc,tam)
    num_threads = [f"{k} threads" for k in mean_mult.keys()]
    fig, ax = plt.subplots(figsize=(10,6))
    height_bar = 0.3
    y = np.arange(len(num_threads))
    #print(mean_mult.values)
    #print(np.array(aceleracao.values()))

    ax.barh(y - height_bar, mean_mult.values,height=height_bar, color='blue', alpha = 0.6, label='Tempo')
    ax.barh(y, aceleracao.values(),height=height_bar, color='green', alpha=0.6, label='Aceleração')
    ax.barh(y+height_bar, eficiencia.values(),height=height_bar, color='red', alpha=0.6, label='Eficiência')

    ax.set_yticks(y)
    ax.set_yticklabels(num_threads)
    ax.set_xlabel('Valores')
    ax.set_ylabel('Número de threads')
    ax.set_title(f'Tempo, Aceleração e Eficiência por Número de Threads')
    ax.legend()
    
    plt.tight_layout()
    plt.show()

gera_plot('dados.csv', 1000000)

