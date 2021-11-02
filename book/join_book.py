import sys


all_data = ''
for fil in sys.argv[1:]:
    with open('learned_data/' + fil, 'r') as f:
        data = f.read()
    all_data += data

with open('learned_data/book.txt', 'w') as f:
    f.write(all_data)