import os
import subprocess
import numpy as np
import random
import matplotlib.pyplot as plt
# from matplotlib import rc
from os import mkdir, path

np.random.seed(44)

plt.style.use('dark_background')
save = True
n_trajectories = 80
list_colors = ['#72bcd4', 'yellow', '#f95e04', 'orange', 'red']
n_colors = len(list_colors)


centers = [np.array([0, 0]),
           np.array([45, 50]),
           np.array([-30, -50]),
           np.array([20, -28]),
           np.array([-30, 21]),
           np.array([-20, -20]),
           np.array([50, -30]),
           # np.array([0, 40])
           ]

n_sources = len(centers)

n_times = 1000
n_times_tab = (np.linspace(n_times, 1.5 * n_times, num=n_sources + 1)).astype(int)


list_colors_used = random.choices(list_colors, k=n_sources + 1)

starting = np.sort(np.random.randint(0, n_trajectories, n_sources))
# centers = [np.zeros(2,)]
scales = [1.5]


dirname = "gifs/"
if not path.exists(dirname):
    mkdir(dirname)


plt.close('all')

width = np.sqrt(n_sources) * np.sqrt(n_times)


f, ax = plt.subplots(1, 1)
f.set_size_inches(30, 30)


ax.set_aspect('equal')
ax.set_xlim(-width, width)
ax.set_ylim(-width, width)

plt.show()


arrange_tab = np.sqrt(np.arange(n_times) + 1)

files = ''

idx_video = 0

n_to_display = 0
for i in range(n_trajectories):
    print(i)
    if i in starting:
        # centers.append(4 * np.sqrt(n_times) * (np.random.rand(2,) - 0.5))
        scales.append(1 * np.random.randint(1, 7))

    for idx_center, scale in enumerate(scales):
        # print(idx_center)
        n_times = n_times_tab[idx_center]
        trajectories = np.cumsum(scales[idx_center] * ((np.random.rand(n_times, 2)) - 0.5), axis=0) + centers[idx_center]
        # print(scales[idx_center])
        color = list_colors[idx_center % n_colors]
        print(color, centers[idx_center], scales[idx_center])

        ax.set_aspect('equal')
        ax.set_xlim(-width, width)
        ax.set_ylim(-width, width)
        # ax.plot(trajectories[0: j, 0], trajectories[0: j, 1], '-', color='orange', linewidth=0.8, alpha=0.9)

        # trajectories_fast = np.cumsum(np.random.rand(n_times, 2 * n_times) - 0.5, axis=0)

        # ax.plot(trajectories[:, 0], trajectories[:, 1], '.', color=list_colors[0], alpha=0.01)
        ax.plot(trajectories[:, 0], trajectories[:, 1], '.', color=color, alpha=0.03 * (0.99 ** i))
        ax.set_axis_off()

        if save:
            plt.savefig("gifs/Fireworks_%s.png" % str(idx_video).zfill(5))
            files = files + ' gifs/Fireworks_{}.png'.format(str(idx_video).zfill(5))
            idx_video += 1
            print('----')
            print(idx_video)

# # # job = 'convert -layers optimize -resize 400 -delay 6 {} -loop 3 gifs/TCL.gif'.format(files)
# job = 'convert -layers optimize -resize 800 -delay 2 {} -loop 3 gifs/Fireworks.gif'.format(files)
# os.system(job)

# subprocess.run('''
# cd  gifs

# ffmpeg \
#   -framerate 60 \
#   -pattern_type glob \
#   -i '*.png' \
#   -vf scale=500:500:flags=lanczos \
#   Fireworks.gif \
# ;

# cd ..
# ''', shell=True, check=True, executable='/bin/bash')


subprocess.run('''
cd  gifs
files=(*.png )

batch=75

## Read the array in batches of $batch
for (( i=0; $i<${#files[@]}; i+=$batch ))
do
    ## Convert this batch
    convert -limit memory 1GB -limit map 4GB -define registry:temporary-path=/tmp -layers optimize -resize 800 -delay 1 {} -loop 1 "${files[@]:$i:$batch}" animated.$i.gif
done
cd ..
''', shell=True, check=True, executable='/bin/bash')


path = "./gifs/"
for filename in os.listdir(path):
    # print(os.path.splitext(filename[1][:5])
    if os.path.splitext(filename)[1] == '.gif':
        print('True')
        print(filename)
        int(os.path.splitext(filename)[0][9:])
        # os.rename(path + '/' + filename, path + '/' + str(filename[0]).zfill(5) + '.gif')

        os.rename(path + '/' + filename, path + '/' + 'animated' + str(int(os.path.splitext(filename)[0][9:])).zfill(5) + '.gif')


subprocess.run('''
cd gifs
## Now, merge them into a single file
convert -loop 3 animated*.gif all.gif
cd ..
''', shell=True, check=True, executable='/bin/bash')

# os.system(cmd)
