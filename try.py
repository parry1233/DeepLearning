degree_map = [[2,3,4,4,4,4,3,2],
              [3,4,6,6,6,6,4,3],
              [4,6,8,8,8,8,6,4],
              [4,6,8,8,8,8,6,4],
              [4,6,8,8,8,8,6,4],
              [4,6,8,8,8,8,6,4],
              [3,4,6,6,6,6,4,3],
              [2,3,4,4,4,4,3,2]]

## 8個移動方位
dx = [1, 2, 2, 1,-1,-2,-2,-1]
dy = [-2,-1, 1, 2, 2, 1,-1,-2]

input_num = input('請輸入位置(介在0~7)(用空格隔開):')
input_num = list(input_num.split())
[a, b] = [int(input_num[0]), int(input_num[1])]

while a < 0 or a > 7 or b < 0 or b > 7:
    input_num = input('請輸入位置(介在0~7)(用空格隔開):')
    input_num = list(input_num.split())
    [a, b] = [int(input_num[0]), int(input_num[1])]
    
print(a)
print(b)

cbx = 8; cby = 8 # width and height of the chessboard
cb = [[0 for x in range(cbx)] for y in range(cby)] # chessboard

## 路徑及搜尋
for i in range(0, 64):
    degree_map[a][b] = 0
    cb[a][b] = i+1
    
    ## 在最後一步不跳出error
    if cb[a][b] == 64:
        break
    
    ## 找出合法路徑
    available_path = []
    for j in range(0,8):
        if a+dx[j] >= 0 and a+dx[j] <= 7 and b+dy[j] >= 0 and b+dy[j] <= 7:
            available_path.append([dx[j], dy[j]])
        else:
            continue

    ## 減去可行路徑的degree(dynamic)
    possible_path = []
    possible_path_degree = []
    for k in range(0, len(available_path)):
        degree_map[a+available_path[k][0]][b+available_path[k][1]] -= 1
        possible_path.append([available_path[k][0], available_path[k][1]])
        possible_path_degree.append(degree_map[a+available_path[k][0]][b+available_path[k][1]])
    
    while min(possible_path_degree) < 0:
        min_index = possible_path_degree.index(min(possible_path_degree))
        del possible_path[min_index]
        del possible_path_degree[min_index]
    
    min_index = possible_path_degree.index(min(possible_path_degree))
    move = possible_path[min_index]
        
    a += move[0]
    b += move[1]

for i in range(0, len(cb)):
    for j in range(0, len(cb[i])):
        print('%3d' % cb[i][j], end='')
    print('\n')