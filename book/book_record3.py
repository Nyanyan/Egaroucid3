from tqdm import trange

all_chars = [
    '!', '#', '$', '&', "'", '(', ')', '*', 
    '+', ',', '-', '.', '/', '0', '1', '2', 
    '3', '4', '5', '6', '7', '8', '9', ':', 
    ';', '<', '=', '>', '?', '@', 'A', 'B', 
    'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 
    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
    '[', ']', '^', '_', '`', 'a', 'b', 'c', 
    'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']

xs = 'ABCDEFGH'
ys = '12345678'

char_translate = {}
for i in range(64):
    char_translate[all_chars[i]] = xs[i % 8] + ys[i // 8]

def translate(r):
    return ''.join([char_translate[i] for i in r])

hw2 = 64

def digit(n, r):
    n = str(n)
    l = len(n)
    for i in range(r - l):
        n = '0' + n
    return n

record_all = {}

def draw_data(record, player, score):
    raw_record = ''
    for i in range(0, len(record), 2):
        p = int(record[i])
        raw_record += record[i + 1]
        if p == player:
            if not raw_record in record_all:
                record_all[raw_record] = score
            else:
                record_all[raw_record] += score

with open('data/record3/0000000.txt', 'r') as f:
    records = f.read().splitlines()
for record in records:
    score = len(record) ** 2
    draw_data(record, 0, score)
    draw_data(record, 1, score)
print(len(record_all))

book = {}

max_ln = 47

inf = 100000000

def calc_value(r):
    return record_all[r]

def create_book(record):
    if len(record) > max_ln:
        return
    policy = -1
    max_val = -inf
    for i in range(hw2):
        r = record + all_chars[i]
        if r in record_all:
            val = calc_value(r)
            if max_val < val:
                max_val = val
                policy = i
    if policy != -1:
        book[record] = all_chars[policy]
        for i in range(hw2):
            r = record + all_chars[policy] + all_chars[i]
            if r in record_all:
                create_book(r)



book = {}
create_book(all_chars[37])
print(len(book))
create_book(all_chars[37] + all_chars[43])
create_book(all_chars[37] + all_chars[45])
create_book(all_chars[37] + all_chars[29])
print(len(book))
if (input('sure?: ') == 'yes'):
    with open('learned_data/book.txt', 'w') as f:
        for record in book.keys():
            f.write(record[1:] + ' ' + book[record])