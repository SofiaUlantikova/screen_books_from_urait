inp = input().split()
h = int(inp[0])
w = int(inp[1])
map = []
for i in range(h):
    map.append(input())
def find_corner(start_point):
    n = start_point[0]
    v = start_point[1]
    if n == 0:
        n_step = 1
    else:
        n_step = -1
    if v == 0:
        v_step = 1
    else:
        v_step = -1
    if (n ==0 and v ==0) or (n !=0 and v != 0):
        for j in range(w):
            n_cur = n
            for i in range(h):
                if map[n_cur][v] == ".":
                    print('end')
                    return [n_cur, v]
                n_cur += n_step
            v += v_step
    else:
        for j in range(h):
            v_cur = v
            for i in range(w):
                if map[n][v_cur] == ".":
                    return [n, v_cur]
                v_cur += v_step
            n += n_step

vert_1 = find_corner([0, 0])
vert_2 = find_corner([0, w-1])
vert_3 = find_corner([h-1, 0])
vert_4 = find_corner([h-1, w-1])

v_min = min([vert_1[1], vert_2[1], vert_3[1], vert_4[1]])
v_max = max([vert_1[1], vert_2[1], vert_3[1], vert_4[1]])
n_min = min([vert_1[0], vert_2[0], vert_3[0], vert_4[0]])
n_max = max([vert_1[0], vert_2[0], vert_3[0], vert_4[0]])

for i in range(h):
    if i == n_min-1 or i == n_max+1:
        print("#"*w)
    elif (i >= n_min) and (i <= n_max):
        print(("."*(v_min-2))+"#"+("."*(v_max-v_min+1))+"#"+("."*(w-v_max-2)))
    else:
        print("."*w)