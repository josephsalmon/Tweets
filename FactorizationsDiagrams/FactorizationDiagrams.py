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


def dot(ax, x, y, size):
    ax.add_patch(plt.Circle((x, y), size, color='k'))


def polygon_complex(n, center, radius):
    rot = 1
    if n == 1:
        return [center]
    if n==2:
        rot = cmath.exp(1j * np.pi / 2)
    # elif n == 4:
    #     rot = cmath.exp(4*1j * np.pi / 8)
    return [center + rot * radius * cmath.exp(1j * 2 * np.pi * i / n) for i in range(n)]


def polygon(ax, n, size, x, y, f):
    step = 2 * np.pi / n
    sizish = 1.5
    if n == 2:
        init = np.pi
        sizish = 1.1
    elif n == 4:
        init = np.pi / 4
        sizish = 1.4
    else:
        init = 0
    dot_radius = (sizish * size) / (n + sizish)
    radius = (n * size) / (n + sizish)
    growth = 1
    if n % 2 == 0:
        delta_x = 0
        growth = 1
    else:
        delta_x = (radius * 0.5) * (1 - np.cos(np.pi / n))

    for i in range(n):
        f(ax,
          x + np.cos(init + step * i) * radius * growth - delta_x,
          y + np.sin(init + step * i) * radius * growth,
          dot_radius)

def draw(ax, x, y, size, depth, primes):
    if (depth < 0):
        dot(ax, x, y, 0.8 * size)
    else:
        g = partial(draw, depth=depth-1, primes=primes)
        polygon(ax, primes[depth], size, x, y, g)


def make(ax, number, size, alpha=0.95):
    primes = primeFactorList(number)
    draw(ax, 0, 0, size * alpha, len(primes) - 1, primes)




# %%
def plot_points(points, ax, color='k', ms=20, alpha=1):
    """Return iterative lists of midpoints.

    Parameters
    ----------
    points: list,
        list of points with complex format
    Returns
    -------
       none, modify ax.
    """
    for i, idx in enumerate(points):
        # print(points[i])
        x1, y1 = points[i].real, points[i].imag
        ax.plot(x1, y1, 'o', color=color, ms=ms, alpha=alpha)


def factor_to_points(primes, radius=1):
    if len(primes) <= 1:
        points = polygon_complex(primes[0], 0, radius)
    else:
        n_k = primes[-1]
        alpha_outer = 2 / 3 #(n_k-1) / (n_k)
        alpha_inner = 1 / 3 #(n_k-2) / (n_k-1)

        points_intermed = polygon_complex(n_k, 0, alpha_outer * radius)
        smaller = factor_to_points(primes[:-1], radius=radius * alpha_inner)
        points = []
        # points_intermed = [pt for pt in points_intermed]
        for point in smaller:
            points.extend([s + s * point for s in points_intermed])
    return points
# %%

number = 9
primes = primeFactorList(number)
print(primes)


# %%
fig, ax = plt.subplots(1, 1,
                       figsize=(1, 1),
                       constrained_layout=True)
plot_points(factor_to_points(primes), ax=ax, ms=1)
ax.set_xticks([])
ax.set_yticks([])
radius = 1.1
ax.set_xlim([-radius, radius])
ax.set_ylim([-radius, radius])

# %%
ncol = 8
nrow = 4


fig, ax = plt.subplots(nrow, ncol,
                       figsize=(ncol+1, nrow+1),
                       constrained_layout=True)

for i in range(nrow):
    for j in range(ncol):
        number = i * ncol + j + 1
        ax[i, j].set_title(str(number), fontsize=7, horizontalalignment='left', loc='left')
        ax[i, j].set_aspect('equal', 'box')
        radius = 1.1
        ax[i, j].set_xlim([-radius, radius])
        ax[i, j].set_ylim([-radius, radius])
        ax[i, j].set_xticks([])
        ax[i, j].set_yticks([])
        print(number)
        primes = primeFactorList(number)

        plot_points(factor_to_points(primes), ax=ax[i, j], ms=1)
        # make(ax[i, j], n_tot, radius * 0.9)
fig.tight_layout()
plt.show()
fig.savefig("test_" + str(nrow) + "_" + str(ncol) + ".svg")
# %%

# %%
fig, ax = plt.subplots(1, 1,
                       figsize=(1, 1),
                       constrained_layout=True)
make(ax, number, 1, alpha=0.95)
# plot_points(factor_to_points(primes), ax=ax, ms=1)
ax.set_xticks([])
ax.set_yticks([])
radius = 1.1
ax.set_xlim([-radius, radius])
ax.set_ylim([-radius, radius])
# %%

# %%

# %%

# %%

# %%

# %%
