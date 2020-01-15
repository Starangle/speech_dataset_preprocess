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
    cmd_copy,cmd_remove=cmd_arr
    os.system(cmd_copy)
    os.system(cmd_remove)

for root,dirs,files in os.walk(dst):
    for file in files:
        base_name,ext=os.path.splitext(file)
        if ext in ['.wv1','.wv2']:
            full_name=os.path.join(root,file)
            converted_name=os.path.join(root,base_name+'.wav')
            cmd_copy="ffmpeg -i {} {} -y".format(full_name,converted_name)
            cmd_remove='rm {}'.format(full_name)
            cmds.append([cmd_copy,cmd_remove])

pool=ThreadPoolExecutor()
pool.map(run,cmds)