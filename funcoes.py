import numpy as np
import cv2 as cv

''' Função | cria uma matriz de índices 2D com todas as 
    combinações possíveis de índices entre os limites 
    mínimos e máximos fornecidos para as dimensões i e j.
'''
def criar_indices(min_i, max_i, min_j, max_j):
    import itertools
    L = list(itertools.product(range(min_i, max_i), range(min_j, max_j)))
    idx_i = np.array([e[0] for e in L])
    idx_j = np.array([e[1] for e in L])
    idx = np.vstack( (idx_i, idx_j) )
    return idx

''' Função | realiza a transformação da imagem a depender do tipo
    enviado como argumento:
    caso seja expandir, diminui ou aumenta a imagem de acordo com a imagem
    e gira a imagem em um ângulo dado em graus, 
    utilizando multiplicações matriciais para encontrar a 
    posição de cada pixel na imagem girada.
    caso contrário, apenas realiza a rotação.
'''

def transforma_imagem(image, ang, escala, tipo):

    # matriz com o mesmo formato da matriz de imagem inteira de zero's
    image_ = np.zeros_like(image)

    # transforma o angulo de graus para radianos
    rad = np.radians(ang)

    Xd = criar_indices(0, image.shape[0], 0, image.shape[1])
    Xd = np.vstack ( (Xd, np.ones( Xd.shape[1]) ) )


    T = np.array([[1, 0, image.shape[0]/2], [0, 1, image.shape[1]/2], [0, 0, 1]]) # translação
    R = np.array([[np.cos(rad), -np.sin(rad), 0], [np.sin(rad), np.cos(rad), 0], [0, 0,1]]) # rotação
    T_ = np.array([[1, 0, -image.shape[0]/2], [0, 1, -image.shape[1]/2], [0, 0, 1]]) # translação
    
    if tipo == 'expandir':
        S = np.array([[escala, 0, 0], [0, escala, 0], [0, 0, 1]]) # expansão
        E = T @ R @ S @ T_
    else:
        E = T @ R @ T_
    

    X = np.linalg.inv(E) @ Xd
    
    # posições tem que ser inteiros
    X = X.astype(int) 
    Xd = Xd.astype(int)

    # filtro para a imagem não sair da delimitação do tamanho da janela
    filtro = (X[0,:] >=0) & (X[0,:] < image_.shape[0]) & (X[1,:] >=0) & (X[1,:] < image_.shape[1]) 
    Xd = Xd[:,filtro]
    X = X[:,filtro]

    image_[Xd[0,:], Xd[1,:], :] = image[X[0,:], X[1,:], :]
    return image_

def delimita_angulo(ang):
    if ang >= 365:
        ang = 0
    elif ang <= 0:
        ang = 365
    return ang

def delimita_aumento(aum):
    if abs(aum) <= 0.1:
        if aum > 0:
            aum = 0.1
        else:
            aum = -0.1
    if abs(aum) >= 60:
        if aum > 0:
            aum = 60
        else:
            aum = -60

    return aum

def delimita_escala(escala):
    if escala <= 0.1 :
        escala = 0.1
    elif escala >= 10:
        escala = 10
    return escala

