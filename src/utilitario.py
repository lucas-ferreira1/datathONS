# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 19:00:31 2021

@author: renan
"""

import cmath
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sympy
from sympy import symbols, Eq, solve
from scipy.optimize import curve_fit

plt.rcParams['figure.figsize'] = [23,10]
plt.rcParams['font.size'] = 24
plt.style.use('classic')
# from _biblioteca_ import *

# Definição de valor imaginário

j=cmath.sqrt(-1)

# Definição de funções importantes

def rad(x):
    return math.radians(x)

def euler_ang(x):
    return cmath.exp(j*rad(x))

def sqrt(x):
    return cmath.sqrt(x)

def fase(x):
    return np.degrees(np.angle(x))

def modulo(x):
    return abs(x)

def mod(x):
    return abs(x)

def limpa():
    print("\n"*40)

def rect(modulo,fase):
    return cmath.rect(modulo,np.radians(fase))
    
def polar(x):
    print('fase em radianos')
    return cmath.polar(x)

def paralelo(a,b): #define o paralelo de duas impedâncias
    return a*b/(a+b) 

def raiz(x):
    return np.sqrt(x)

# constante de giro

a=rect(1,120)

# Matriz de transformação para componentes simétricas trifásicas

T = np.array([[1, 1, 1], [1, a**2,a], [1,a,a**2]])

T_inv= np.array([[1, 1, 1], [1, a,a**2], [1,a**2,a]])



# Solução de sistemas

def sis_2x2(eq1,eq2,x,y):
    equacao1 = Eq(eq1,0)
    equacao2 = Eq(eq2,0)
    solucao_dict = solve((equacao1,equacao2),(x,y))
    print(list(solucao_dict.keys())[0],"=",list(solucao_dict.values())[0])
    print(list(solucao_dict.keys())[1],"=",list(solucao_dict.values())[1])
    return 
    
def sis_3x3(eq1,eq2,eq3,x,y,z):
    equacao1 = Eq(eq1,0)
    equacao2 = Eq(eq2,0)
    equacao3 = Eq(eq3,0)
    solucao_dict = solve((equacao1,equacao2,equacao3),(x,y,z))
    print(list(solucao_dict.keys())[0],"=",list(solucao_dict.values())[0])
    print(list(solucao_dict.keys())[1],"=",list(solucao_dict.values())[1])
    print(list(solucao_dict.keys())[2],"=",list(solucao_dict.values())[2])
    return 

# Input de matriz 3x1

def m_4x1(eq1,eq2,eq3,eq4):
    return np.array([[eq1], [eq2], [eq3],[eq4]])

def m_3x1(eq1,eq2,eq3): # cada equação é uma linha da matriz 3x1
    return np.array([[eq1], [eq2], [eq3]])

def m_2x1(eq1,eq2):
    return np.array([[eq1], [eq2]])
    
# Solver de componentes simétricas (seq zero,positiva e negativa)

def solve_012(matriz):# entra com a matriz abc 
    return (1/3)*np.matmul(T_inv,matriz) # retorna a matriz 012


# solver de componentes simétricas (a,b,c)

def solve_abc(matriz): #entra com a matriz 012
    return np.matmul(T,matriz) # retorna a matriz abc

def delta_estrela(z1,z2,z3):
    D=z1+z2+z3
    print("Za =",z1*z3/D)
    print("Zb =",z1*z2/D)
    print("Zc =",z2*z3/D)
    return 

def estrela_delta(z1,z2,z3):
    D=z1*z2+z2*z3+z3*z1
    print("Za =",D/z3)
    print("Zb =",D/z1)
    print("Zc =",D/z2)
    return 

neutro = bool 
def solve_i012(matriz,Zeq0,Zeq1,Zeq2,neutro): # entra com a matriz de tensão abc, 
                                              # imp seq0, imp seq1, imp se2,
                                              # neutro = 1 se tiver
                                              # neutro = 0 caso nao tenha
    return m_3x1((matriz[0][0]/(Zeq0))*neutro,matriz[1][0]/(Zeq1),matriz[2][0]/(Zeq2))

# multiplicação de matrizes

def mult(a,b):
    return np.matmul(a,b)


seq_abc = m_3x1(127,127*a**2,127*a)

seq_acb = m_3x1(127,127*a*2,127*a**2)

