# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 11:10:26 2024

@author: Ana Luiza Haas
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta

#Ler arquivo csv e fazer dataframe
#file_carga = 'databases/dados_carga.csv'
file_diasespeciais = 'databases/dados_carga_diasespeciais_v3.xlsx'

#df = pd.read_csv(file_carga,sep = ';',index_col=2)
#df.index = pd.to_datetime(df.index)

df = pd.read_excel(file_diasespeciais,index_col = 1)

df=df.astype(str)
df.iloc[:,[1,2,3,4,5,6,7,8]]=df.iloc[:,[1,2,3,4,5,6,7,8]].applymap(lambda x: x.replace(',', '.')).astype(float)
df.index = pd.to_datetime(df.index)

#Tratamento referência utc
df.index = df.index - timedelta(hours=3)

#Tratamento de excluir dias especiais
df = df[df['Data especial']=='nan']


#Condições de estações
df = df[df['cod_areacarga']=='SECO'] #Selecionando o sudeste
df = df[df.index.year == 2023] #Selecionando 2023

df = df.drop(['cod_areacarga'], axis = 1)

dias_num = range(7)
dias_nome = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
dias_ptbr = ['Segunda','Terca','Quarta','Quinta','Sexta','Sabado','Domingo']

df_estacoes = {}
for n in dias_num:
    dia = dias_ptbr[n]
    df_estacoes[dia]={}
    #outono
    df_estacoes[dia]['outono']=df.loc[df.index[df.index.month>3][0]:df.index[df.index.month<=6][-1]]
    df_estacoes[dia]['outono']=df_estacoes[dia]['outono'][df_estacoes[dia]['outono']['day_of_week'] == dias_nome[n]]
    #inverno
    df_estacoes[dia]['inverno']=df.loc[df.index[df.index.month>6][0]:df.index[df.index.month<=9][-1]]
    df_estacoes[dia]['inverno']=df_estacoes[dia]['inverno'][df_estacoes[dia]['inverno']['day_of_week'] == dias_nome[n]]
    #primavera
    df_estacoes[dia]['primavera']=df.loc[df.index[df.index.month>9][0]:df.index[df.index.month<=12][-1]]
    df_estacoes[dia]['primavera']=df_estacoes[dia]['primavera'][df_estacoes[dia]['primavera']['day_of_week'] == dias_nome[n]]
    #verao
    df_estacoes[dia]['verao']=df.loc[df.index[df.index.month==1][0]:df.index[df.index.month<=3][-1]]
    df_estacoes[dia]['verao']=df_estacoes[dia]['verao'][df_estacoes[dia]['verao']['day_of_week'] == dias_nome[n]]
    
#df_estacoes['outono']=df.loc[df.index[df.index.month>3][0]:df.index[df.index.month<=6][-1]]
#df_estacoes['inverno']=df.loc[df.index[df.index.month>6][0]:df.index[df.index.month<=9][-1]]
#df_estacoes['primavera']=df.loc[df.index[df.index.month>9][0]:df.index[df.index.month<=12][-1]]
#df_estacoes['verao']=df.loc[df.index[df.index.month==1][0]:df.index[df.index.month<=3][-1]]


#Teste das curvas semi-horária de carga verificada
df_teste = df_estacoes['Sabado']['verao'][df_estacoes['Sabado']['verao'].index.date.astype(str) == '2023-01-07']

plt.plot(df_teste.index,df_teste['val_cargaglobal'],label = 'Carga Global')
plt.plot(df_teste.index,df_teste['val_cargaglobalsmmgd'],label = 'Carga Global Líquida MMGD')
plt.plot(df_teste.index,df_teste['val_cargammgd'],label = 'Carga atendida MMGD')
plt.plot(df_teste.index,df_teste['val_cargaglobal']-df_teste['val_cargammgd'],label = 'Carga global gerada')
plt.xticks(rotation=45)
plt.xlabel('Tempo')
plt.ylabel('Valor Carga Global(MWmed)')
plt.title('Curva de Carga em Sábado no verao de 2023')
plt.legend()
plt.show()

#Média pra cada estação (TEM QUE EVOLUIR PRA TER PRA CADA DIA TBM USANDO ARQUIVO DOS MENINOS)
df_estacoesmed = {}
for dia in df_estacoes:
    df_estacoesmed[dia]={}
    for est in df_estacoes[dia]:
        df_estacoesmed[dia][est] = pd.DataFrame(columns=df_estacoes[dia][est].columns).drop(['Data especial','day_of_week'],axis=1)
        tempos1 = np.unique(df_estacoes[dia][est].index.time)
        tempos_i = np.unique(df_estacoes[dia][est].index.hour + df_estacoes[dia][est].index.minute/60)
        for i in range(48):
            df_estacoesmed[dia][est].loc[tempos_i[i]]=df_estacoes[dia][est][df_estacoes[dia][est].index.time == tempos1[i]].drop(['Data especial','day_of_week'],axis=1).mean()

for dia in df_estacoes:
    for est in df_estacoesmed[dia]:
        plt.plot(df_estacoesmed[dia][est].index,df_estacoesmed[dia][est]['val_cargaglobal'],label = est)
    
    plt.xlabel('Tempo (h)')
    plt.ylabel('Valor Carga Global(MWmed)')
    plt.title('Curva global média típica SECO no dia de '+ str(dia)+ ' em 2023')
    plt.legend()
    plt.show()


df_estacoesmed['Sabado']['verao'].to_excel('databases/curva_media_sabado_verao.xlsx')


#Código antigo
'''
#Média do outono

df_outono=df_outono.drop(['cod_areacarga','dat_referencia'], axis = 1)
df_outono = df_outono.astype(str)
df_outono = df_outono.applymap(lambda x: x.replace(',', '.')).astype(float)
dfmed_out = pd.DataFrame(columns=df_outono.columns)
for hora in range(24):
    dfmed_out.loc[hora]=df_outono[df_outono.index.hour == hora].mean()
    
#Plot matplotlib
plt.plot(dfmed_out.index,dfmed_out['val_cargaglobal'])
plt.xlabel('Tempo (h)')
plt.ylabel('Valor Carga Global(MWmed)')
plt.title('Curva de Carga líquida média em dia de outono 2023')
#plt.ylim(0, 60000)
plt.show()

#Média do verão

df_verao=df_verao.drop(['cod_areacarga','dat_referencia'], axis = 1)
df_verao = df_verao.astype(str)
df_verao = df_verao.applymap(lambda x: x.replace(',', '.')).astype(float)
dfmed_ver = pd.DataFrame(columns=df_outono.columns)
for hora in range(24):
    dfmed_ver.loc[hora]=df_verao[df_verao.index.hour == hora].mean()

#Plot matplotlib
plt.plot(dfmed_ver.index,dfmed_ver['val_cargaglobal'])
plt.xlabel('Tempo (h)')
plt.ylabel('Valor Carga Global(MWmed)')
plt.title('Curva de Carga líquida média em dia de verão 2023')
#plt.ylim(0, 60000)
plt.show()

#Média do inverno

df_inverno=df_inverno.drop(['cod_areacarga','dat_referencia'], axis = 1)
df_inverno = df_inverno.astype(str)
df_inverno = df_inverno.applymap(lambda x: x.replace(',', '.')).astype(float)
dfmed_inv = pd.DataFrame(columns=df_inverno.columns)
for hora in range(24):
    dfmed_inv.loc[hora]=df_inverno[df_inverno.index.hour == hora].mean()

#Plot matplotlib
plt.plot(dfmed_inv.index,dfmed_inv['val_cargaglobal'])
plt.xlabel('Tempo (h)')
plt.ylabel('Valor Carga Global(MWmed)')
plt.title('Curva de Carga líquida média em dia de inverno 2023')
#plt.ylim(0, 60000)
plt.show()

#Média da primavera

df_primavera=df_primavera.drop(['cod_areacarga','dat_referencia'], axis = 1)
df_primavera = df_primavera.astype(str)
df_primavera = df_primavera.applymap(lambda x: x.replace(',', '.')).astype(float)
dfmed_pri = pd.DataFrame(columns=df_primavera.columns)
for hora in range(24):
    dfmed_pri.loc[hora]=df_primavera[df_primavera.index.hour == hora].mean()

#Plot matplotlib
plt.plot(dfmed_pri.index,dfmed_pri['val_cargaglobal'])
plt.xlabel('Tempo (h)')
plt.ylabel('Valor Carga Global(MWmed)')
plt.title('Curva de Carga líquida média em dia de primavera 2023')
#plt.ylim(0, 60000)
plt.show()
'''