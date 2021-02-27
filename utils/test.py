__author__ = "Ldaze"

obstacleGrid = [[0,0],[0,0]]
row = len(obstacleGrid)
col = len(obstacleGrid[0])
count = 0;
countAdj = 0;
for i, j in enumerate(obstacleGrid):
    for k, v in enumerate(j):
        if v == 1:
            count += 1
            if j[k + 1] == 1:
                countAdj += 1
            if obstacleGrid[i + 1][k] == 1:
                countAdj += 1
size = row * col - row - col + 1
res = pow(2, (size - (count - countAdj) * 2 - countAdj ))
print(res)