# Sources:
# - ht #/jsfiddle.net/vjeux/vkdxv/2/
# - https://www.jasondavies.com/factorisation-diagrams/

# %%
import numpy as np
import matplotlib.pylab as plt
from functools import partial
import cmath
# %%

def smallestFactor(n):
    if (n < 2):
        raise NameError("Argument error")
    if (n % 4 == 0):
        return 4  # vjeux hack
    if (n % 2 == 0):
        return 2
    end = int(np.floor(np.sqrt(n)))
    for i in range(3, end + 1, 2):
        if (n % i == 0):
            return i
    return n


def primeFactorList(n):
    if (n == 1):
        return [1]
    result = []
    while (n != 1):
        factor = smallestFactor(n)
        result.append(factor)
        n //= factor
    result.sort(reverse=False)
    return result


def polygon_complex(n):
    if n == 1:
        return [0]
    return np.exp(1j * 2 * np.pi * np.arange(n) / n)


def factor_to_points(primes, alpha_2=1.03):
    n_k = primes[-1]
    if n_k == 1:
        return np.zeros(1)
    if n_k == 2:
        return polygon_complex(2) * alpha_2
    alpha_outer = 0.99 * 1 / (n_k-1.4)
    if len(primes) <= 1:
        points = polygon_complex(n_k)
    else:
        points_intermed = polygon_complex(n_k)
        smaller = factor_to_points(primes[:-1])
        points = np.kron(points_intermed, (1 + smaller * alpha_outer))
    return points / np.max(np.abs(points))


# %%
radius = 1
number = 3
epsilon = 0.2
# %%
ncol = 9
nrow = 13


fig, ax = plt.subplots(nrow, ncol,
                       figsize=(ncol+1, nrow+1),
                       constrained_layout=True)

# radius = 5
for i in range(nrow):
    for j in range(ncol):
        number = i * ncol + j + 1
        print(number)
        ax[i, j].set_title(str(number), fontsize=7, horizontalalignment='center', loc='center')
        ax[i, j].set_aspect('equal', 'box')
        ax[i, j].set_xlim([-radius * (1+epsilon), radius* (1+epsilon)])
        ax[i, j].set_ylim([-radius* (1+epsilon), radius* (1+epsilon)])
        ax[i, j].set_xticks([])
        ax[i, j].set_yticks([])
        ax[i, j].set_axis_off()
        # print(number)
        primes = primeFactorList(number)
        points = factor_to_points(primes)
        ax[i, j].plot(points.real, points.imag, ".", color='k', ms=int(1.5 / number **0.5 * (ncol * nrow)**0.5), markeredgewidth=0)
fig.tight_layout()
plt.show()
fig.savefig("test_" + str(nrow) + "_" + str(ncol) + ".svg")

# %%

# %%

# %%

# %%

# %%
