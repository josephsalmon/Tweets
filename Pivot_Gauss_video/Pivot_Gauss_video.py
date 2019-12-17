# import itertools
# from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
# from subprocess import call
import os

save = True

if not os.path.exists("./gifs"):
    os.mkdir("./gifs")


def pivot(m, m_evol, i):
    n, _ = np.shape(m)
    max = np.finfo(np.float64).eps
    for r in range(i, n):
        max_to_test = np.abs(m[r, i])
        # print(max_to_test, max)
        if max < max_to_test:
            max_row = r
            max = max_to_test
        # print(max_row)
    m[[i, max_row]] = m[[max_row, i]]  # raw swapping
    m_evol[[i, max_row]] = m_evol[[max_row, i]]


def gaussian_elimination_with_pivot(m):
    """
    Parameters
    ----------
    m  : list of list of floats (matrix)

    Returns
    -------
    list of floats
      solution to the system of linear equation

    Raises
    ------
    ValueError
      no unique solution
    """
    # forward elimination
    n, _ = m.shape
    liste_evol = []
    liste_mat = []
    m_evol = np.eye(n)
    for i in range(n):
        # ACTIVATE IF you want pivot.
        # pivot(m, m_evol, i)
        liste_mat.append(m.copy())
        # liste_evol.append(m_evol.copy())
        for j in range(i + 1, n):
            alpha = m[j, i] / m[i, i]
            m[j, :] = m[j, :] - m[i, :] * alpha
            m_evol[j, :] = m_evol[j, :] - m_evol[i, :] * alpha
            liste_mat.append(m.copy())
            liste_evol.append(m_evol.copy())
        liste_evol.append(m_evol.copy())

    # if np.abs(m[n - 1, n - 1]) < np.finfo(np.float64).eps:
    #     raise ValueError('No unique solution')

    for i in range(n)[::-1]:
        for j in range(0, i)[::-1]:
            alpha = m[j, i] / m[i, i]
            m[j, :] = m[j, :] - m[i, :] * alpha
            m_evol[j, :] = m_evol[j, :] - m_evol[i, :] * alpha
            liste_evol.append(m_evol.copy())
            liste_mat.append(m.copy())

    # # backward substitution
    # x = np.zeros(n, )
    # for i in range(n - 1, -1, -1):
    #     s = sum(m[i,j] * x[j] for j in range(i, n))
    #     x[i] = (m[i,n] - s) / m[i,i]
    return liste_mat, liste_evol

'''
# shorter way to pivot but cannot run in trinket
def pivot(m, n, i):
  max_row = max(range(i, n), key=lambda r: abs(m[r,i]))
  m[i], m[max_row] = m[max_row], m[i]
'''


def imaging(m):
    m_init = m.copy()
    liste_mat, liste_evol = gaussian_elimination_with_pivot(m)
    fig = plt.figure(figsize=(4, 4))
    ax12 = fig.add_subplot(2, 2, 2)
    ax21 = fig.add_subplot(2, 2, 3)
    ax22 = fig.add_subplot(2, 2, 4)
    plt.show(block=False)
    for i, matrix in enumerate(liste_mat):
        ax21.set_axis_off()
        ax21.imshow(liste_evol[i], vmin=-3, vmax=3, cmap='RdBu')

        ax22.set_axis_off()
        ax22.imshow(matrix, vmin=-3, vmax=3, cmap='RdBu')

        ax12.set_axis_off()
        ax12.imshow(m_init, vmin=-3, vmax=3, cmap='RdBu')

        plt.savefig("gifs/gauss_pivot_%s.png" % str(i).zfill(3))

        # plt.close()
        print(i)
    if save is True:
        # files = []
        files = ''
        for i, matrix in enumerate(liste_mat):
            # files.append('gifs/gauss_pivot_{}.png'.format(str(i).zfill(3)))
            files = files + ' gifs/gauss_pivot_{}.png'.format(str(i).zfill(3))

        # print(files)
        print(files)
        # command = 'convert -delay 5 {} -loop 100 gifs/gauss_pivot.gif'.format(' '.join(files))
        job = 'convert -layers optimize -resize 400 -delay 6 {} -loop 3 gifs/gauss_pivot.gif'.format(files)
        os.system(job)

# n = 19
n = 19
# m = np.abs(np.random.randn(n, n) + np.eye(n))
m = (np.random.randn(n, n) + np.eye(n))

print(m)
# print(gaussian_elimination_with_pivot(m))
imaging(m)
