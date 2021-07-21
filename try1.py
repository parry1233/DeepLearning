def knightTour(ni, nj, xi, xj):
    # Creating a degree map by the WARNSDORFF rules...
    degree_map = [2,3,4,4,4,4,3,2,
                  3,4,6,6,6,6,4,3,
                  4,6,8,8,8,8,6,4,
                  4,6,8,8,8,8,6,4,
                  4,6,8,8,8,8,6,4,
                  4,6,8,8,8,8,6,4,
                  3,4,6,6,6,6,4,3,
                  2,3,4,4,4,4,3,2]
    # knight_map = degree_map
    
    for i in range(ni*nj):
        if i%8 < 7:
            print(degree_map[i], end=' ')
        else: 
            print(degree_map[i])

    # Creating the 8 possible moves...
    eight_moves = [(1,-2),(2,-1),(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2)]
    for i in range(8):
        print(eight_moves[i], end=' ')
    print('\n')
    
    # Initiating the start position of Knight...
    knight_move = ni*nj

    # Looping for finding the Hamiltonian Path for Knight’s Tour...
    for _ in range(knight_move-1):
        if knight_move == ni*nj:
            degree_map[xi*8+xj] = knight_move

        # Checking if the moves within the board boundaries or not...
        OK_moves = []
        for i in range(8):
            (test_i, test_j) = (xi + eight_moves[i][0], xj + eight_moves[i][1])
            if test_i >= 0 and test_j >= 0 and test_i <= 7 and test_j <= 7:
                OK_moves.append((test_i, test_j))
        # print(OK_moves)

        # Finding the next position for Knight's movement...
        count = 0
        for ti,tj in OK_moves:
            # print(degree_map[ti*8+tj], end=' ')
            if degree_map[ti*8+tj] >= ni*nj:
                continue
            elif count == 0:
                temp = ti, tj, degree_map[ti*8+tj]
                count += 1
            elif degree_map[ti*8+tj] < temp[2]:
                temp = ti, tj, degree_map[ti*8+tj]
        # print(temp)
        
        # Updating the degree map and the new move...
        for ti,tj in OK_moves:
            if degree_map[ti*8+tj] >= ni*nj:
                continue
            else: 
                degree_map[ti*8+tj] -= 1

        knight_move += 1
        degree_map[temp[0]*8+temp[1]] = knight_move
        xi, xj = temp[0], temp[1]
        # print(degree_map[temp[0]*8+temp[1]], xi, xj, temp[2])
    
    # Print out the Hamiltonian Path for Knight’s Tour...
    for i in range(ni*nj):
        if i%8 < 7:
            print('{0:3d}'.format(degree_map[i]-ni*nj+1), end=' ')
        else: 
            print('{0:3d}'.format(degree_map[i]-ni*nj+1))    
    
knightTour(8,8,0,0)