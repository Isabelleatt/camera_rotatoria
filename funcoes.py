import numpy as np
import matplotlib.image as mpimg


def criar_indices(min_i, max_i, min_j, max_j):
    import itertools
    L = list(itertools.product(range(min_i, max_i), range(min_j, max_j)))
    idx_i = np.array([e[0] for e in L])
    idx_j = np.array([e[1] for e in L])
    idx = np.vstack( (idx_i, idx_j) )
    return idx

def gira_imagem(image, ang):

    image_ = np.zeros_like(image)
    rad = np.radians(ang)

    Xd = criar_indices(0, image.shape[0], 0, image.shape[1])
    Xd = np.vstack ( (Xd, np.ones( Xd.shape[1]) ) )

    T = np.array([[1, 0, image.shape[0]/2], [0, 1, image.shape[1]/2], [0, 0, 1]])
    R = np.array([[np.cos(rad), -np.sin(rad), 0], [np.sin(rad), np.cos(rad), 0], [0, 0,1]])
    # R = np.array([[1, -np.sin(rad), 0], [np.sin(rad), 1, 0], [0, 0,1]])
    # R = np.array([[1, -np.sin(rad), 0], [np.cos(rad), 1, 0], [0, 0,1]])
    T_ = np.array([[1, 0, -image.shape[0]/2], [0, 1, -image.shape[1]/2], [0, 0, 1]])

    E = T @ R @ T_

    X = np.linalg.inv(E) @ Xd
    X = X.astype(int) # posições tem que ser inteiros
    Xd = Xd.astype(int)
    filtro = (X[0,:] >=0) & (X[0,:] < image_.shape[0]) & (X[1,:] >=0) & (X[1,:] < image_.shape[1])
    Xd = Xd[:,filtro]
    X = X[:,filtro]

    image_[Xd[0,:], Xd[1,:], :] = image[X[0,:], X[1,:], :]
    return image_

