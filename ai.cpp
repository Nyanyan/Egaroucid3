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
#define b_idx_num 38

struct board{
    int b[b_idx_num];
    int p;
    double v;
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
int pow3[hw];
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

vector<int> vacant_lst;

inline long long tim(){
    return chrono::duration_cast<chrono::milliseconds>(chrono::high_resolution_clock::now().time_since_epoch()).count();
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

inline void init_move(){
    int idx, b, w, place;
    pow3[0] = 1;
    for (idx = 1; idx < hw; ++idx)
        pow3[idx] = pow3[idx- 1] * 3;
    for (idx = 0; idx < n_line; ++idx){
        b = create_one_color(idx, 0);
        w = create_one_color(idx, 1);
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
            turn_board[0][i * hw + j] = i * hw + (hw_m1 - j);
            turn_board[1][i * hw + j] = (hw_m1 - j) * hw + i;
            turn_board[2][i * hw + j] = (hw_m1 - i) * hw + j;
            turn_board[3][i * hw + j] = j * hw + (hw_m1 - i);
        }
    }
}

inline board move(board b, const int global_place){
    board res;
    int j, place, g_place;
    for (int i = 0; i < b_idx_num; ++i)
        res.b[i] = b.b[i];
    for (const int &i: place_included[global_place]){
        place = local_place[i][global_place];
        for (j = 1; j <= move_arr[b.p][b.b[i]][place][0]; ++j){
            g_place = global_place - move_offset[i] * j;
            for (const int &idx: place_included[g_place])
                res.b[idx] = flip_arr[b.p][res.b[idx]][local_place[idx][g_place]];
        }
        for (j = 1; j <= move_arr[b.p][b.b[i]][place][1]; ++j){
            g_place = global_place + move_offset[i] * j;
            for (const int &idx: place_included[g_place])
                res.b[idx] = flip_arr[b.p][res.b[idx]][local_place[idx][g_place]];
        }
    }
    for (const int &idx: place_included[global_place])
        res.b[idx] = put_arr[b.p][res.b[idx]][local_place[idx][global_place]];
    res.p = 1 - b.p;
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
    for (i = 0; i < hw2; ++i){
        cin >> elem;
        if (elem != '.'){
            b |= (unsigned long long)(elem == '0') << turn_board[direction][i];
            w |= (unsigned long long)(elem == '1') << turn_board[direction][i];
            ++n_stones;
        } else
            vacant_lst.push_back(turn_board[direction][i]);
    }
    if (n_stones < hw2_m1)
        sort(vacant_lst.begin(), vacant_lst.end(), cmp_vacant);
    for (i = 0; i < b_idx_num; ++i){
        board[i] = 0;
        for (j = 0; j < idx_n_cell[i]; ++j){
            if (1 & (b >> global_place[i][j]))
                board[i] += 0;
            else if (1 & (w >> global_place[i][j]))
                board[i] += pow3[j];
            else
                board[i] += pow3[j] * 2;
        }
    }
    return n_stones;
}

inline string coord_str(int policy, int direction){
    string res;
    res += (char)(board_c::turn_board[direction][policy] % hw + 97);
    res += to_string(board_c::turn_board[direction][policy] / hw + 1);
    return res;
}

int main(){
    long long strt = tim();
    int direction;
    init_move();
    init_local_place();
    init_included();
    init_turn_board();
    cerr << "iniitialized in " << tim() - strt << " ms" << endl;
    board b;
    cerr << input_board(b.b, 0) << endl;
    print_board(b.b);
    b.p = 0;
    board nb = move(b, 34);
    print_board(nb.b);
    return 0;
}