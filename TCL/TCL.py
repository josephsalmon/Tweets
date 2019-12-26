import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib import rc
from os import mkdir, path

plt.style.use('dark_background')
save = True
n_times = 30
n_trajectories = 70

dirname = "gifs/"
if not path.exists(dirname):
    mkdir(dirname)

plt.close('all')

width = np.sqrt(n_times)

f, axes = plt.subplots(2, 2)
f.set_size_inches(16, 16)

for i in range(2):
    for j in range(2):
        axes[i, j].set_aspect('equal')
        axes[i, j].set_xlim(-width, width)
        axes[i, j].set_ylim(-width, width)
        axes[i, j].set_xticks([])
        axes[i, j].set_yticks([])


plt.show()

arrange_tab = np.sqrt(np.arange(n_times) + 1)

files = ''

idx_video = 0

list_times = np.arange(1, n_times, 4)

for i in range(n_trajectories):

    trajectories = np.cumsum(np.random.rand(n_times, 2 * n_times) - 0.5, axis=0)
    for j in list_times:
        axes[0, 0].cla()
        axes[0, 0].set_aspect('equal')
        axes[0, 0].set_xlim(-width, width)
        axes[0, 0].set_ylim(-width, width)
        axes[0, 0].plot(trajectories[0: j, 0], trajectories[0: j, 1], '-', color='#f95e04', linewidth=0.8, alpha=0.9)
        axes[0, 0].set_xticks([])
        axes[0, 0].set_yticks([])

        trajectories_fast = np.cumsum(np.random.rand(n_times, 2 * n_times) - 0.5, axis=0)

        axes[1, 0].cla()
        axes[1, 0].set_aspect('equal')
        axes[1, 0].set_xlim(-width, width)
        axes[1, 0].set_ylim(-width, width)
        axes[1, 0].plot(trajectories_fast[:, 0], trajectories_fast[:, 1], '-',
                        color='#f95e04', linewidth=0.8, alpha=0.9)
        axes[1, 0].plot(trajectories_fast[-1, 0], trajectories_fast[-1, 1], '.',
                        color='#f95e04', ms=20, alpha=1)
        axes[1, 0].set_xticks([])
        axes[1, 0].set_yticks([])
        if i > 0:
            axes[0, 0].plot(point_to_keep[0], point_to_keep[1], '.',
                            color='#f95e04', ms=20, alpha=1-j/n_times)

        axes[1, 1].plot(trajectories_fast[n_times - 1, 0],
                        trajectories_fast[n_times - 1, 1],
                        '.', color='#f95e04', ms=20, alpha=0.3)

        if save:
            plt.savefig("gifs/TCL_%s.png" % str(idx_video).zfill(5))
            files = files + ' gifs/TCL_{}.png'.format(str(idx_video).zfill(5))
            idx_video += 1

    axes[0, 0].plot(trajectories[0: n_times - 1, 0],
                    trajectories[0: n_times - 1, 1],
                    '-', color='#f95e04', linewidth=0.8, alpha=0.9)
    point_to_keep = trajectories[n_times - 1, 0], trajectories[n_times - 1, 1]
    axes[0, 0].plot(point_to_keep[0], point_to_keep[1],
                    '.', color='#f95e04', ms=20, alpha=1)
    axes[0, 1].plot(trajectories[n_times - 1, 0], trajectories[n_times - 1, 1],
                    '.', color='#f95e04', ms=20, alpha=0.3)

    if save:
        plt.savefig("gifs/TCL_%s.png" % str(idx_video).zfill(5))
        files = files + ' gifs/TCL_{}.png'.format(str(idx_video).zfill(5))
        idx_video += 1
        print(i)

# job = 'convert -limit memory 1GB -limit map 4GB -define registry:temporary-path=/tmp -layers optimize -resize 600 -delay 6 {} -loop 2 gifs/TCL.gif'.format(files)
# os.system(job)

### Solution bash?
# https://askubuntu.com/questions/573712/convert-thousands-of-pngs-to-animated-gif-convert-uses-too-much-memory


subprocess.run('''
cd  gifs
files=(*.png )

batch=75

## Read the array in batches of $batch
for (( i=0; $i<${#files[@]}; i+=$batch ))
do
    ## Convert this batch
    convert -limit memory 1GB -limit map 4GB -define registry:temporary-path=/tmp -layers optimize -resize 800 -delay 6 {} -loop 1 "${files[@]:$i:$batch}" animated.$i.gif
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
