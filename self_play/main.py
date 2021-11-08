import subprocess
import os
import shutil
import datetime

def digit(n, r):
    n = str(n)
    l = len(n)
    for i in range(r - l):
        n = '0' + n
    return n

self_play_num = 4000
parallel_num = 8
one_self_play_num = self_play_num // parallel_num

while True:
    p = []
    strt_idx = 0
    for i in range(parallel_num):
        p.append(subprocess.Popen(('python self_play.py ' + str(one_self_play_num) + ' ' + str(strt_idx)).split()))
        strt_idx += one_self_play_num // 100
    for pp in p:
        pp.wait()
    

    for strt in [20, 30, 40, 50]:
        end = strt + 10
        q = subprocess.run(('python learn.py ' + str(self_play_num) + ' ' + str(strt) + ' ' + str(end)).split())

    for i, strt in enumerate([20, 30, 40, 50]):
        end = strt + 10
        r = subprocess.run(('python output_model.py ' + str(strt) + '_' + str(end) + '.h5 ' + str(i + 1) + '.txt').split())

    s = subprocess.run('python join_model.py param_add.txt 1.txt 2.txt 3.txt 4.txt'.split())
    
    t = subprocess.run(('python load_additional_data.py ' + str(self_play_num)).split())

    for i, strt in enumerate([20, 30, 40, 50]):
        end = strt + 10
        u = subprocess.run(('python learn_all_data.py ' + str(self_play_num) + ' ' + str(strt) + ' ' + str(end)).split())

    for i, strt in enumerate([20, 30, 40, 50]):
        end = strt + 10
        v = subprocess.run(('python output_model.py all_' + str(strt) + '_' + str(end) + '.h5 ' + str(i + 6) + '.txt').split())

    s = subprocess.run('python join_model.py param.txt 1.txt 2.txt 3.txt 4.txt 6.txt 7.txt 8.txt 9.txt'.split())

    now = datetime.datetime.today()
    now_str = str(now.year) + digit(now.month, 2) + digit(now.day, 2) + '_' + digit(now.hour, 2) + digit(now.minute, 2)
    shutil.copyfile('./eval/param.txt', os.path.join('./eval', now_str + '.txt'))

    dir_num = sum(os.path.isdir(os.path.join('./data', name)) for name in os.listdir('./data'))
    print(dir_num)
    new_dir = digit(dir_num, 7)
    os.mkdir('./data/' + new_dir)
    file_dir_lst = os.listdir('./data')
    for elem in file_dir_lst:
        if os.path.isfile(os.path.join('./data', elem)):
            shutil.move(os.path.join('./data', elem), os.path.join('./data', new_dir))
    file_lst = os.listdir('./data_player')
    for elem in file_lst:
        os.remove(os.path.join('./data_player', elem))
    file_lst = os.listdir('./data_additional')
    for elem in file_lst:
        os.remove(os.path.join('./data_additional', elem))
    os.mkdir('./learned_data/' + now_str)
    for strt in [20, 30, 40, 50]:
        end = strt + 10
        os.remove(os.path.join('./learned_data', 'bef_' + str(strt) + '_' + str(end) + '.h5'))
        os.rename(os.path.join('./learned_data', str(strt) + '_' + str(end) + '.h5'), os.path.join('./learned_data', 'bef_' + str(strt) + '_' + str(end) + '.h5'))
        shutil.copyfile(os.path.join('./learned_data', 'bef_' + str(strt) + '_' + str(end) + '.h5'), os.path.join(os.path.join('./learned_data', now_str), 'bef_' + str(strt) + '_' + str(end) + '.h5'))