import subprocess

self_play_num = 3200
parallel_num = 8

one_self_play_num = self_play_num // parallel_num
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
