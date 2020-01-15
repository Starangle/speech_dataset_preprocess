import shutil
import argparse
import os
from concurrent.futures import ThreadPoolExecutor
parser=argparse.ArgumentParser()
parser.add_argument('src')
parser.add_argument('--dst')
parser.add_argument('-m','--merge_disk',action='store_true')
args=parser.parse_args()
dst=args.dst if args.dst else args.src+'-converted'

if args.merge_disk==False:
    shutil.copytree(args.src,dst)
else:
    os.mkdir(dst)
    os.system("cp -r {}/*/wsj* {}".format(args.src,dst))

cmds=[]
def run(cmd_arr):
    for cmd in cmd_arr:
        os.system(cmd)

for root,dirs,files in os.walk(dst):
    for file in files:
        base_name,ext=os.path.splitext(file)
        if ext in ['.wv1','.wv2']:
            full_name=os.path.join(root,file)
            converted_name=full_name+'.wav'
            cmd_copy="ffmpeg -i {} {} -y".format(full_name,converted_name)
            cmd_remove='rm {}'.format(full_name)
            cmd_move='mv {} {}'.format(converted_name,full_name)
            cmds.append([cmd_copy,cmd_remove,cmd_move])

pool=ThreadPoolExecutor()
pool.map(run,cmds)