
#TODO: initialize default data, such as chess board and initial location
input_XY = input('Enter start position X and Y (please add \",\" to split X and Y): ')
XY = input_XY.split(',')
x,y = int(XY[0]), int(XY[1])
print('Got initial value, X=', x, ', Y=',y)
#print(type(input_size),type(x),type(y))

deg_map = [[2,3,4,4,4,4,3,2],
           [3,4,6,6,6,6,4,3],
           [4,6,8,8,8,8,6,4],
           [4,6,8,8,8,8,6,4],
           [4,6,8,8,8,8,6,4],
           [4,6,8,8,8,8,6,4],
           [3,4,6,6,6,6,4,3],
           [2,3,4,4,4,4,3,2]]

GoX = [ 1, 2, 2, 1,-1,-2,-2,-1]
GoY = [-2,-1, 1, 2, 2, 1,-1,-2]
result_map = [[0 for a in range(8)] for b in range(8)]

def print_result(result_map_in):
       for i in range(0,len(result_map_in)):
              for j in range(0, len(result_map_in[i])):
                     print('%3d'%result_map_in[i][j], end='')
              print('\n')

def GoCheck():
       global x, y, GoX, GoY
       goList = []
       for a in range(0,8):
              if 7 >= (x + GoX[a]) >= 0 and 7 >= (y + GoY[a]) >= 0:
                     #? check each possible further steps, if it is possible then add it to the list
                     goList.append([ GoX[a], GoY[a] ])
       return goList

def dynamic():
       global x, y, deg_map
       #? initialize lists to save further steps (one for direction and one for map)
       further_path_list = []
       further_path_map = []
       for go in GoCheck():
              deg_map[x + go[0]][y + go[1]] -= 1
              further_path_list.append([ go[0], go[1] ])
              further_path_map.append(deg_map[x + go[0]][y + go[1]])
       while min(further_path_map) < 0:
              del further_path_list[ further_path_map.index(min(further_path_map)) ]
              del further_path_map[ further_path_map.index(min(further_path_map)) ]
       
       selected_move = further_path_list[ further_path_map.index(min(further_path_map)) ]

       x += selected_move[0]
       y += selected_move[1]



for i in range(0,64):
       deg_map[x][y] = 0
       result_map[x][y] = i+1
       if result_map[x][y] == 64:
              break
       dynamic()
print_result(result_map)
