#Write a program that finds the longest adjacent sequence of colors in a matrix(2D grid). Colors are represented by
#‘R’, ‘G’, ‘B’ characters (respectively Red, Green and Blue).

# Solution:

class MatrixRGB:
    def __init__(self):
        self.width = None
        self.height = None
        self.values = None
        self.max_path_R = None
        self.max_path_G = None
        self.max_path_B = None

def gen_input(readFile = False):
    if readFile:
        with open("input.txt", "r", newline='') as file_json:
            inputString = file_json.readlines()
        rows = int(inputString[0].split(' ')[0])
        cols = int(inputString[0].split(' ')[1])
        matrixValues = [inputString[i].replace("\xa0"," ").replace("\r\n","").split() for i in range(1, rows + 1)]
    else:
        input_string = str(input())
        results = input_string.split(' ')
        rows = int(results[0])
        cols = int(results[1])
        matrixValues = [list(map(str,input().split())) for i in range(rows)]
    mat = MatrixRGB()
    mat.width = rows
    mat.height = cols
    mat.values = matrixValues
    return mat

# All Possible Directions we can go
def get_directions(p1, p2):
    return {(1,0):"n", (-1,0):"s", (0,1):"w", (0,-1):"e"}[(p1[0] - p2[0], p1[1] - p2[1])]

# Main Algorithm to find path
def find_path(start, mat):
    preferredCharacter = mat[start[0]][start[1]]
    m, paths = get_max(mat, get_neighbours(mat), start, list(), preferredCharacter)
    #print(paths)
    if len(paths) == 1:
        return []
    directions = ""
    prev = get_directions(paths[0], paths[1])
    current = ""
    ctr = 1
    for i in range(1, len(paths) - 1):
        current = get_directions(paths[i], paths[i + 1])
        if current == prev:
            ctr += 1
        else:
            directions, prev, ctr = directions + prev + " " + str(ctr) + ",", current, 1
    return paths

#Neighbor is (-1,-1) if indices are out of range. For top and bottom rows for example
def get_neighbours(mat):
    neighbours = dict()
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            n = (i - 1, j) if i - 1 >= 0 else (-1, -1)
            s = (i + 1, j) if i + 1 < len(mat) else (-1, -1)
            w = (i, j - 1) if j - 1 >= 0 else (-1, -1)
            e = (i, j + 1) if j + 1 < len(mat[i]) else (-1, -1)
            neighbours[(i,j)] = {'n':n, 's':s, 'w':w, 'e':e}
    return neighbours

# Get max path from a a list of neighbours
def get_max(mat, neighbours, coordinates, visited, character):
    if coordinates == (-1,-1):
        return -1, []
    elif mat[coordinates[0]][coordinates[1]] != character:
        return -1, []
    elif coordinates in visited:
        return -1, []
    else:
        visited.append(coordinates)
        n, nlist = get_max(mat, neighbours, neighbours[coordinates]['n'], visited[:], character)
        s, slist = get_max(mat, neighbours, neighbours[coordinates]['s'], visited[:], character)
        w, wlist = get_max(mat, neighbours, neighbours[coordinates]['w'], visited[:], character)
        e, elist = get_max(mat, neighbours, neighbours[coordinates]['e'], visited[:], character)
        if max(n,s,w,e) == -1:
            return 0, visited
        if max(n,s,w,e) == n:
            visited = nlist     
        elif max(n,s,w,e) == s:
            visited = slist     
        elif max(n,s,w,e) == w:
            visited = wlist     
        elif max(n,s,w,e) == e:
            visited = elist     
        return 1 + max(n,s,w,e), visited
 
def main():
    # Set gen_input to False to read from console, 
    # Set gen_input to True to read from 'input.txt', located in the project folder
    mat = gen_input(False) 
    pathList = []
    for i in range(mat.width):
        for j in range(mat.height):
            pathList.append(len(find_path((i,j),mat.values)))
    print(max(pathList))

if __name__ == "__main__":
    main()