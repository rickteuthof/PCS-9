"""
gen_bifurcation.py
---------
Generates and saves different bifurcation geometries.
Use via `python3 gen_bifurcation.py <args>`.
For all the options type `python3 gen_bifurcation.py --help`.

:Authors:
    - Martijn Besamusca
    - Ralph Erkamps
    - Rick Teuthof
"""


import argparse
import os
import numpy as np
import shutil
import matplotlib.pyplot as plt
from PIL import Image

import geometry.bifurcation as bifurcation

# parse arguments
parser = argparse.ArgumentParser(
    description='Generate multiple bifurcation geom files')
parser.add_argument('--width', '-W', type=int,
                    default=400, help='Width of image')
parser.add_argument('--height', '-H', type=int,
                    default=160, help='Height of image')
parser.add_argument('--num', '-n', type=int, default=10,
                    help='Number of geometries generated')
parser.add_argument('--min', '-m', type=float, default=0.0,
                    help='Min width of the narrowing of one of the vein bifurcations')
parser.add_argument('--max', '-M', type=float, default=0.9,
                    help='Max width of the narrowing of one of the vein bifurcations')
parser.add_argument('--out', '-o', type=str, default='out',
                    help='The name of the output folder')
parser.add_argument('--clear', '-c', action='store_true',
                    help='Clear the output folder')
parser.add_argument('--draw', '-d', action='store_true',
                    help='Draw probes at end')
args = parser.parse_args()

# make folder
if not args.out:
    print('No out path')
    exit(1)
folder = args.out
if args.clear and os.path.exists(folder):
    shutil.rmtree(folder)
if not os.path.exists(folder):
    os.mkdir(folder)

# generate
widths = np.linspace(args.min, args.max, num=args.num)
split_vein, v0, v1, v2 = None, None, None, None
for width in widths:
    split_vein, v0, v1, v2 = bifurcation.build(
        args.width, args.height, args.width/5, angle=20)
    v1.add_narrowing(loc=0.5, length=0.4, scale=width)
    image = split_vein.get_image()
    filename = f'bifurcation_{width:.4f}.png'
    new_im = Image.fromarray(image)
    new_im.save(os.path.join(folder, filename))

if not v0:
    print('Nothing generated')
    exit(1)

# display
split_vein, v0, v1, v2 = bifurcation.build(
    args.width, args.height, args.width/5, angle=20)
image = split_vein.get_image()

probe_in = v0.get_probe_point(0.3)
probe_normal = v2.get_probe_point(0.8)
probe_nar_before = v1.get_probe_point(0.2)
probe_nar_after = v1.get_probe_point(0.8)

with open(os.path.join(folder, 'probe.txt'), 'w') as f:
    s = '{},{},{}\n'
    f.write(s.format('inlet', *probe_in))
    f.write(s.format('normal vein', *probe_normal))
    f.write(s.format('start narrow vein', *probe_nar_before))
    f.write(s.format('end narrow vein', *probe_nar_after))

if args.draw:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(image, cmap=plt.cm.gray)
    ax.scatter(
        *zip(*[probe_in, probe_normal, probe_nar_before, probe_nar_after]), s=20)
    names = ['inlet', 'normal vein', 'start narrow vein', 'end narrow vein']
    for name, pos in zip(names, [probe_in, probe_normal, probe_nar_before, probe_nar_after]):
        ax.annotate(name, pos, c='C1')
    plt.show()
