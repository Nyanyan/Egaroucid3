#pragma GCC target("avx2")
#pragma GCC optimize("O3")
#pragma GCC optimize("unroll-loops")
#pragma GCC target("sse,sse2,sse3,ssse3,sse4,popcnt,abm,mmx")

// Egaroucid3

// black: 0, white: 1

#include <iostream>
#include <fstream>
#include <algorithm>
#include <vector>
#include <chrono>
#include <string>
#include <unordered_map>
#include <random>

using namespace std;

#define tl 145

#define hw 8
#define hw_m1 7
#define hw_p1 9
#define hw2 64
#define hw22 128
#define hw2_m1 63
#define hw2_mhw 56
#define hw2_p1 65
#define n_line 6561
#define inf 2000000000.0
#define window 1e-10
#define b_idx_num 38

#define book_hash_table_size 16384
#define book_hash_mask (book_hash_table_size - 1)
#define book_stones 17
#define ln_repair_book 27

#define search_hash_table_size 1048576
#define search_hash_mask (search_hash_table_size - 1)

struct board{
    int b[b_idx_num];
    int p;
    int policy;
};

struct book_node{
    int k[hw];
    int policy;
    book_node* p_n_node;
};

struct search_node{
    int k[b_idx_num];
    pair<double, double> v;
    search_node* p_n_node;
};

struct search_result{
    int policy;
    int value;
    int depth;
};

const int idx_n_cell[b_idx_num] = {8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 3, 4, 5, 6, 7, 8, 7, 6, 5, 4, 3, 3, 4, 5, 6, 7, 8, 7, 6, 5, 4, 3};
const int move_offset[b_idx_num] = {1, 1, 1, 1, 1, 1, 1, 1, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7};
const int global_place[b_idx_num][hw] = {
    {0, 1, 2, 3, 4, 5, 6, 7},{8, 9, 10, 11, 12, 13, 14, 15},{16, 17, 18, 19, 20, 21, 22, 23},{24, 25, 26, 27, 28, 29, 30, 31},{32, 33, 34, 35, 36, 37, 38, 39},{40, 41, 42, 43, 44, 45, 46, 47},{48, 49, 50, 51, 52, 53, 54, 55},{56, 57, 58, 59, 60, 61, 62, 63},
    {0, 8, 16, 24, 32, 40, 48, 56},{1, 9, 17, 25, 33, 41, 49, 57},{2, 10, 18, 26, 34, 42, 50, 58},{3, 11, 19, 27, 35, 43, 51, 59},{4, 12, 20, 28, 36, 44, 52, 60},{5, 13, 21, 29, 37, 45, 53, 61},{6, 14, 22, 30, 38, 46, 54, 62},{7, 15, 23, 31, 39, 47, 55, 63},
    {5, 14, 23, -1, -1, -1, -1, -1},{4, 13, 22, 31, -1, -1, -1, -1},{3, 12, 21, 30, 39, -1, -1, -1},{2, 11, 20, 29, 38, 47, -1, -1},{1, 10, 19, 28, 37, 46, 55, -1},{0, 9, 18, 27, 36, 45, 54, 63},{8, 17, 26, 35, 44, 53, 62, -1},{16, 25, 34, 43, 52, 61, -1, -1},{24, 33, 42, 51, 60, -1, -1, -1},{32, 41, 50, 59, -1, -1, -1, -1},{40, 49, 58, -1, -1, -1, -1, -1},
    {2, 9, 16, -1, -1, -1, -1, -1},{3, 10, 17, 24, -1, -1, -1, -1},{4, 11, 18, 25, 32, -1, -1, -1},{5, 12, 19, 26, 33, 40, -1, -1},{6, 13, 20, 27, 34, 41, 48, -1},{7, 14, 21, 28, 35, 42, 49, 56},{15, 22, 29, 36, 43, 50, 57, -1},{23, 30, 37, 44, 51, 58, -1, -1},{31, 38, 45, 52, 59, -1, -1, -1},{39, 46, 53, 60, -1, -1, -1, -1},{47, 54, 61, -1, -1, -1, -1, -1}
};
vector<vector<int>> place_included;
int pow3[hw], pow17[hw];
int move_arr[2][n_line][hw][2];
bool legal_arr[2][n_line][hw];
int flip_arr[2][n_line][hw];
int put_arr[2][n_line][hw];
int local_place[b_idx_num][hw2];
int turn_board[4][hw2];
const double cell_weight[hw2] = {
    0.2880, -0.1150, 0.0000, -0.0096, -0.0096, 0.0000, -0.1150, 0.2880,
    -0.1150, -0.1542, -0.0288, -0.0288, -0.0288, -0.0288, -0.1542, -0.1150,
    0.0000, -0.0288, 0.0000, -0.0096, -0.0096, 0.0000, -0.0288, 0.0000,
    -0.0096, -0.0288, -0.0096, -0.0096, -0.0096, -0.0096, -0.0288, -0.0096,
    -0.0096, -0.0288, -0.0096, -0.0096, -0.0096, -0.0096, -0.0288, -0.0096,
    0.0000, -0.0288, 0.0000, -0.0096, -0.0096, 0.0000, -0.0288, 0.0000,
    -0.1150, -0.1542, -0.0288, -0.0288, -0.0288, -0.0288, -0.1542, -0.1150,
    0.2880, -0.1150, 0.0000, -0.0096, -0.0096, 0.0000, -0.1150, 0.2880
};
int count_arr[n_line];

vector<int> vacant_lst;

unordered_map<char, int> char_keys;
book_node *book[book_hash_table_size];
const string book_chars = "!#$&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abc";
string param_compressed1;

search_node *search_replace_table[2][search_hash_table_size];
int searched_nodes;
int f_search_table_idx;

inline long long tim(){
    return chrono::duration_cast<chrono::milliseconds>(chrono::high_resolution_clock::now().time_since_epoch()).count();
}

inline unsigned long long calc_hash(const int *p){
    unsigned long long seed = 0;
    // int seed = 0;
    //for (int i = 0; i < hw; ++i)
    //    seed ^= p[i] << (i / 4);
    for (int i = 0; i < hw; ++i)
        seed += p[i] * pow17[i];
    return seed;
}

inline bool compare_key(const int *a, const int *b){
    for (int i = 0; i < hw; ++i){
        if (a[i] != b[i])
            return false;
    }
    return true;
}

inline void print_board_line(int tmp){
    int j;
    string res = "";
    for (j = 0; j < hw; ++j){
        if (tmp % 3 == 0)
            res = "X " + res;
        else if (tmp % 3 == 1)
            res = "O " + res;
        else
            res = ". " + res;
        tmp /= 3;
    }
    cerr << res;
}

inline void print_board(const int* board){
    int i, j, tmp;
    string res;
    for (i = 0; i < hw; ++i){
        tmp = board[i];
        res = "";
        for (j = 0; j < hw; ++j){
            if (tmp % 3 == 0)
                res = "X " + res;
            else if (tmp % 3 == 1)
                res = "O " + res;
            else
                res = ". " + res;
            tmp /= 3;
        }
        cerr << res << endl;
    }
    cerr << endl;
}

inline int create_one_color(int idx, const int k){
    int res = 0;
    for (int i = 0; i < hw; ++i){
        if (idx % 3 == k){
            res |= 1 << i;
        }
        idx /= 3;
    }
    return res;
}

inline int trans(const int pt, const int k) {
    if (k == 0)
        return pt << 1;
    else
        return pt >> 1;
}

inline int move_line_half(const int p, const int o, const int place, const int k) {
    int mask;
    int res = 0;
    int pt = 1 << (hw_m1 - place);
    if (pt & p || pt & o)
        return res;
    mask = trans(pt, k);
    while (mask && (mask & o)) {
        ++res;
        mask = trans(mask, k);
        if (mask & p)
            return res;
    }
    return 0;
}

inline void init_pow(){
    int idx;
    pow3[0] = 1;
    for (idx = 1; idx < hw; ++idx)
        pow3[idx] = pow3[idx- 1] * 3;
    pow17[0] = 1;
    for (idx = 1; idx < hw; ++idx)
        pow17[idx] = pow17[idx - 1] * 17;
}

inline void init_move(){
    int idx, b, w, place;
    for (idx = 0; idx < n_line; ++idx){
        b = create_one_color(idx, 0);
        w = create_one_color(idx, 1);
        count_arr[idx] = 0;
        for (place = 0; place < hw; ++place){
            count_arr[idx] += 1 & (b >> place);
            count_arr[idx] -= 1 & (w >> place);
        }
        for (place = 0; place < hw; ++place){
            move_arr[0][idx][place][0] = move_line_half(b, w, place, 0);
            move_arr[0][idx][place][1] = move_line_half(b, w, place, 1);
            if (move_arr[0][idx][place][0] || move_arr[0][idx][place][1])
                legal_arr[0][idx][place] = true;
            else
                legal_arr[0][idx][place] = false;
            move_arr[1][idx][place][0] = move_line_half(w, b, place, 0);
            move_arr[1][idx][place][1] = move_line_half(w, b, place, 1);
            if (move_arr[1][idx][place][0] || move_arr[1][idx][place][1])
                legal_arr[1][idx][place] = true;
            else
                legal_arr[1][idx][place] = false;
            /*
            if (legal_arr[1][idx][place]){
                print_board_line(idx);
                cerr << idx << " " << place << " " << move_arr[1][idx][place][0] << " " << move_arr[1][idx][place][1] << endl;
            }
            */
        }
        for (place = 0; place < hw; ++place){
            flip_arr[0][idx][place] = idx;
            flip_arr[1][idx][place] = idx;
            put_arr[0][idx][place] = idx;
            put_arr[1][idx][place] = idx;
            if (b & (1 << (hw_m1 - place)))
                flip_arr[1][idx][place] += pow3[hw_m1 - place];
            else if (w & (1 << (hw_m1 - place)))
                flip_arr[0][idx][place] -= pow3[hw_m1 - place];
            else{
                put_arr[0][idx][place] -= pow3[hw_m1 - place] * 2;
                put_arr[1][idx][place] -= pow3[hw_m1 - place];
            }
        }
    }
}

inline void init_local_place(){
    int idx, place, l_place;
    for (idx = 0; idx < b_idx_num; ++idx){
        for (place = 0; place < hw2; ++place){
            local_place[idx][place] = -1;
            for (l_place = 0; l_place < hw; ++l_place){
                if (global_place[idx][l_place] == place)
                    local_place[idx][place] = l_place;
            }
        }
    }
}

inline void init_included(){
    int idx, place, l_place;
    for (place = 0; place < hw2; ++place){
        vector<int> included;
        for (idx = 0; idx < b_idx_num; ++idx){
            for (l_place = 0; l_place < hw; ++l_place){
                if (global_place[idx][l_place] == place)
                    included.push_back(idx);
            }
        }
        place_included.push_back(included);
    }
}

inline void init_turn_board(){
    int i, j;
    for (i = 0; i < hw; ++i){
        for (j = 0; j < hw; ++j){
            turn_board[0][i * hw + j] = i * hw + j;
            turn_board[1][i * hw + j] = j * hw + i;
            turn_board[2][i * hw + j] = (hw_m1 - i) * hw + (hw_m1 - j);
            turn_board[3][i * hw + j] = (hw_m1 - j) * hw + (hw_m1 - i);
        }
    }
}

inline board move(const board *b, const int global_place){
    board res;
    int j, place, g_place;
    for (int i = 0; i < b_idx_num; ++i)
        res.b[i] = b->b[i];
    for (const int &i: place_included[global_place]){
        place = local_place[i][global_place];
        for (j = 1; j <= move_arr[b->p][b->b[i]][place][0]; ++j){
            g_place = global_place - move_offset[i] * j;
            for (const int &idx: place_included[g_place])
                res.b[idx] = flip_arr[b->p][res.b[idx]][local_place[idx][g_place]];
        }
        for (j = 1; j <= move_arr[b->p][b->b[i]][place][1]; ++j){
            g_place = global_place + move_offset[i] * j;
            for (const int &idx: place_included[g_place])
                res.b[idx] = flip_arr[b->p][res.b[idx]][local_place[idx][g_place]];
        }
    }
    for (const int &idx: place_included[global_place])
        res.b[idx] = put_arr[b->p][res.b[idx]][local_place[idx][global_place]];
    res.p = 1 - b->p;
    res.policy = global_place;
    return res;
}

inline void book_hash_table_init(book_node** hash_table){
    for(int i = 0; i < book_hash_table_size; ++i)
        hash_table[i] = NULL;
}

inline book_node* book_node_init(const int *key, int policy){
    book_node* p_node = NULL;
    p_node = (book_node*)malloc(sizeof(book_node));
    for (int i = 0; i < hw; ++i)
        p_node->k[i] = key[i];
    p_node->policy = policy;
    p_node->p_n_node = NULL;
    return p_node;
}

inline void register_book(book_node** hash_table, const int *key, int hash, int policy){
    if(hash_table[hash] == NULL){
        hash_table[hash] = book_node_init(key, policy);
    } else {
        book_node *p_node = hash_table[hash];
        book_node *p_pre_node = NULL;
        p_pre_node = p_node;
        while(p_node != NULL){
            if(compare_key(key, p_node->k)){
                p_node->policy = policy;
                return;
            }
            p_pre_node = p_node;
            p_node = p_node->p_n_node;
        }
        p_pre_node->p_n_node = book_node_init(key, policy);
    }
}

inline int get_book(const int *key){
    book_node *p_node = book[calc_hash(key) & book_hash_mask];
    while(p_node != NULL){
        if(compare_key(key, p_node->k)){
            return p_node->policy;
        }
        p_node = p_node->p_n_node;
    }
    return -1;
}

inline void init_book(){
    int i;
    for (i = 0; i < hw2; ++i)
        char_keys[book_chars[i]] = i;
    ifstream ifs("book/param/book.txt");
    if (ifs.fail()){
        cerr << "book file not exist" << endl;
        exit(1);
    }
    getline(ifs, param_compressed1);
    int ln = param_compressed1.length();
    int coord;
    board fb;
    const int first_board[b_idx_num] = {6560, 6560, 6560, 6425, 6326, 6560, 6560, 6560, 6560, 6560, 6560, 6425, 6344, 6506, 6560, 6560, 6560, 6560, 6560, 6560, 6344, 6425, 6398, 6560, 6560, 6560, 6560, 6560, 6560, 6560, 6560, 6479, 6344, 6398, 6074, 6560, 6560, 6560};
    book_hash_table_init(book);
    int data_idx = 0;
    int n_book = 0;
    while (data_idx < ln){
        fb.p = 1;
        for (i = 0; i < b_idx_num; ++i)
            fb.b[i] = first_board[i];
        while (true){
            if (param_compressed1[data_idx] == ' '){
                ++data_idx;
                break;
            }
            coord = char_keys[param_compressed1[data_idx++]];
            fb = move(&fb, coord);
            //cerr << coord << endl;
            //print_board(fb.b);
        }
        coord = char_keys[param_compressed1[data_idx++]];
        register_book(book, fb.b, calc_hash(fb.b) & book_hash_mask, coord);
        ++n_book;
    }
    cerr << n_book << " boards in book" << endl;
}

inline void search_hash_table_init(const int table_idx){
    for(int i = 0; i < search_hash_table_size; ++i)
        search_replace_table[table_idx][i] = NULL;
}

inline search_node* search_node_init(const int *key, double l, double u){
    search_node* p_node = NULL;
    p_node = (search_node*)malloc(sizeof(search_node));
    for (int i = 0; i < hw; ++i)
        p_node->k[i] = key[i];
    p_node->v.first = l;
    p_node->v.second = u;
    p_node->p_n_node = NULL;
    return p_node;
}

inline void register_search(const int table_idx, const int *key, int hash, double l, double u){
    if(search_replace_table[table_idx][hash] == NULL){
        search_replace_table[table_idx][hash] = search_node_init(key, l, u);
    } else {
        search_node *p_node = search_replace_table[table_idx][hash];
        search_node *p_pre_node = NULL;
        p_pre_node = p_node;
        while(p_node != NULL){
            if(compare_key(key, p_node->k)){
                p_node->v.first = l;
                p_node->v.second = u;
                return;
            }
            p_pre_node = p_node;
            p_node = p_node->p_n_node;
        }
        p_pre_node->p_n_node = search_node_init(key, l, u);
    }
}

inline pair<double, double> get_search(const int *key, const int hash, const int table_idx){
    search_node *p_node = search_replace_table[table_idx][hash];
    while(p_node != NULL){
        if(compare_key(key, p_node->k)){
            return p_node->v;
        }
        p_node = p_node->p_n_node;
    }
    pair<double, double> empty = {-inf, -inf};
    return empty;
}

inline double end_game(const board *b){
    int count = 0;
    for (int idx = 0; idx < hw; ++idx)
        count += count_arr[b->b[idx]];
    if (b->p == 1)
        count = -count;
    if (count > 0)
        return 1.0;
    else if (count < 0)
        return -1.0;
    return 0.0;
}

inline double evaluate(const board *b){
    return end_game(b);
}

int move_ordering(const board p, const board q){
    pair<double, double> plu = get_search(p.b, calc_hash(p.b) & search_hash_mask, f_search_table_idx);
    pair<double, double> qlu = get_search(q.b, calc_hash(q.b) & search_hash_mask, f_search_table_idx);
    if (plu.first != -inf){
        if (qlu.first != inf)
            return plu.first > qlu.first;
        else
            return 1;
    } else{
        if (qlu.first != inf)
            return 0;
        else
            return evaluate(&p) > evaluate(&q);
    }
}

double nega_scout(board *b, const long long strt, int skip_cnt, int depth, double alpha, double beta){
    if (tim() - strt > tl)
        return -inf;
    ++searched_nodes;
    if (skip_cnt == 2)
        return end_game(b);
    if (depth == 0)
        return evaluate(b);
    int hash = (int)(calc_hash(b->b) & search_hash_mask);
    pair<double, double> lu = get_search(b->b, hash, 1 - f_search_table_idx);
    if (lu.first != -inf){
        if (lu.first == lu.second)
            return lu.first;
        alpha = max(alpha, lu.first);
        if (alpha >= beta)
            return alpha;
    }
    if (lu.second != -inf){
        beta = min(beta, lu.second);
        if (alpha >= beta)
            return beta;
    }
    vector<board> nb;
    for (const int &cell: vacant_lst){
        for (const int &idx: place_included[cell]){
            if (move_arr[b->p][b->b[idx]][local_place[idx][cell]][0] || move_arr[b->p][b->b[idx]][local_place[idx][cell]][1]){
                nb.push_back(move(b, cell));
                break;
            }
        }
    }
    int canput = nb.size();
    if (canput == 0){
        b->p = 1 - b->p;
        return -nega_scout(b, strt, skip_cnt + 1, depth, -beta, -alpha);
    }
    if (canput > 2)
        sort(nb.begin(), nb.end(), move_ordering);
    double v, g;
    g = -nega_scout(&nb[0], strt, 0, depth - 1, -beta, -alpha);
    if (fabs(g) == inf)
        return -inf;
    if (beta <= g){
        if (lu.first < g)
            register_search(1 - f_search_table_idx, b->b, hash, g, lu.second);
        return g;
    }
    v = g;
    alpha = max(alpha, g);
    for (int i = 1; i < canput; ++i){
        g = -nega_scout(&nb[i], strt, 0, depth - 1, -alpha - window, -alpha);
        if (fabs(g) == inf)
            return -inf;
        if (beta <= g){
            if (lu.first < g)
                register_search(1 - f_search_table_idx, b->b, hash, g, lu.second);
            return g;
        }
        if (alpha < g){
            alpha = g;
            g = -nega_scout(&nb[i], strt, 0, depth - 1, -beta, -alpha);
            if (beta <= g){
                if (lu.first < g)
                    register_search(1 - f_search_table_idx, b->b, hash, g, lu.second);
                return g;
            }
            alpha = max(alpha, g);
        }
        v = max(v, g);
    }
    if (v <= alpha)
        register_search(1 - f_search_table_idx, b->b, hash, lu.first, v);
    else
        register_search(1 - f_search_table_idx, b->b, hash, v, v);
    return v;

}

inline search_result search(const board b){
    long long strt = tim();
    vector<board> nb;
    for (const int &cell: vacant_lst){
        for (const int &idx: place_included[cell]){
            if (move_arr[b.p][b.b[idx]][local_place[idx][cell]][0] || move_arr[b.p][b.b[idx]][local_place[idx][cell]][1]){
                nb.push_back(move(&b, cell));
                break;
            }
        }
    }
    int canput = nb.size();
    double alpha = -1.1, beta = 1.1;
    int depth = 5;
    int res_depth;
    int policy = -1;
    int tmp_policy, i;
    double g, value;
    searched_nodes = 0;
    while (tim() - strt < tl){
        search_hash_table_init(1 - f_search_table_idx);
        if (canput > 2)
            sort(nb.begin(), nb.end(), move_ordering);
        for (i = 0; i < canput; ++i){
            g = -nega_scout(&nb[i], strt, 0, depth, -beta, -alpha);
            if (fabs(g) == inf)
                break;
            if (alpha < g){
                alpha = g;
                tmp_policy = nb[i].policy;
            }
        }
        f_search_table_idx = 1 - f_search_table_idx;
        policy = tmp_policy;
        value = alpha;
        res_depth = depth;
        ++depth;
    }
    cerr << "depth: " << res_depth + 1 << " searched nodes: " << searched_nodes << " nps: " << searched_nodes * 1000 / (tim() - strt) << endl;
    search_result res;
    res.policy = policy;
    res.value = value;
    res.depth = res_depth;
    return res;
}

inline string coord_str(int policy, int direction){
    string res;
    //res += (char)(turn_board[direction][policy] % hw + 97);
    //res += to_string(turn_board[direction][policy] / hw + 1);
    res += to_string(turn_board[direction][policy] / hw);
    res += " ";
    res += to_string(turn_board[direction][policy] % hw);
    return res;
}

int cmp_vacant(int p, int q){
    return cell_weight[p] > cell_weight[q];
}

inline int input_board(int (&board)[b_idx_num], int direction){
    int i, j;
    unsigned long long b = 0, w = 0;
    char elem;
    int n_stones = 0;
    vacant_lst.clear();
    for (i = 0; i < hw; ++i){
        string raw_board;
        cin >> raw_board; cin.ignore();
        cerr << raw_board << endl;
        for (j = 0; j < hw; ++j){
            elem = raw_board[j];
            if (elem != '.'){
                b |= (unsigned long long)(elem == '0') << turn_board[direction][i * hw + j];
                w |= (unsigned long long)(elem == '1') << turn_board[direction][i * hw + j];
                ++n_stones;
            } else{
                vacant_lst.push_back(turn_board[direction][i * hw + j]);
            }
        }
    }
    if (n_stones < hw2_m1)
        sort(vacant_lst.begin(), vacant_lst.end(), cmp_vacant);
    for (i = 0; i < b_idx_num; ++i){
        board[i] = n_line - 1;
        for (j = 0; j < idx_n_cell[i]; ++j){
            if (1 & (b >> global_place[i][j]))
                board[i] -= pow3[hw_m1 - j] * 2;
            else if (1 & (w >> global_place[i][j]))
                board[i] -= pow3[hw_m1 - j];
        }
    }
    return n_stones;
}

int main(){
    int direction, ai_player, policy, n_stones;
    board b;
    cin >> ai_player;
    long long strt = tim();
    search_result result;
    cerr << "initializing" << endl;
    init_pow();
    init_move();
    init_local_place();
    init_included();
    init_turn_board();
    init_book();
    f_search_table_idx = 0;
    search_hash_table_init(f_search_table_idx);
    cerr << "iniitialized in " << tim() - strt << " ms" << endl;
    if (ai_player == 0){
        direction = 0;
        string raw_board;
        for (int i = 0; i < hw; ++i){
            cin >> raw_board; cin.ignore();
        }
        policy = 37;
        cerr << "FIRST direction " << direction << endl; 
        cerr << "book policy " << policy << endl;
        cout << coord_str(policy, direction) << endl;
    } else {
        string board_turns[4] = {
            "...........................10......000..........................",
            "...........................10......00.......0...................",
            "..........................000......01...........................",
            "...................0.......00......01..........................."
        };
        string board_str;
        string tmp;
        for (int i = 0; i < hw;++i){
            cin >> tmp; cin.ignore();
            board_str += tmp;
        }
        for (int i = 0; i < 4; ++i){
            if (board_str == board_turns[i])
                direction = i;
        }
        int first_board[b_idx_num] = {6560, 6560, 6560, 6425, 6326, 6560, 6560, 6560, 6560, 6560, 6560, 6425, 6344, 6506, 6560, 6560, 6560, 6560, 6560, 6560, 6344, 6425, 6398, 6560, 6560, 6560, 6560, 6560, 6560, 6560, 6560, 6479, 6344, 6398, 6074, 6560, 6560, 6560};
        policy = get_book(first_board);
        cerr << "FIRST direction " << direction << endl;
        cerr << "book policy " << policy << endl;
        cout << coord_str(policy, direction) << " " << 0 << endl;
    }
    while (true){
        n_stones = input_board(b.b, direction);
        b.p = ai_player;
        if (n_stones < book_stones){
            policy = get_book(b.b);
            cerr << "book policy " << policy << endl;
            if (policy != -1){
                b = move(&b, policy);
                ++n_stones;
                cout << coord_str(policy, direction) << " " << 0 << endl;
                continue;
            }
        }
        result = search(b);
        cerr << "policy " << result.policy << endl;
        cout << coord_str(result.policy, direction) << " " << result.value << endl;
    }
    return 0;
}