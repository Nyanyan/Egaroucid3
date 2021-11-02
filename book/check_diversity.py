import matplotlib.pyplot as plt
from tqdm import trange

def digit(n, r):
    n = str(n)
    l = len(n)
    for i in range(r - l):
        n = '0' + n
    return n

records = []
for num in trange(117):
    try:
        with open('self_play/' + digit(num, 7) + '.txt', 'r') as f:
            raw_records = f.readlines()
        for i in range(len(raw_records)):
            records.append(raw_records[i].split()[0])
    except:
        continue

len_records = len(records)

y = []

max_ln = 0

for i in range(2, 60):
    dct = {}
    for record in records:
        if record[:i] in dct:
            dct[record[:i * 2]] += 1
        else:
            dct[record[:i * 2]] = 0
    y.append(len(dct) / len_records)
    max_ln = len(dct)
    print(y[-1])

print('all', len_records)
print('individual', max_ln)
x = range(2, 60)

plt.plot(x, y)
plt.plot(x, [1.0 for _ in range(len(x))])
plt.plot(x, [0.9 for _ in range(len(x))])
plt.show()

