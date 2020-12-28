with open("input.txt") as f:
    nums = [int(line) for line in f]

for ii, x in enumerate(nums):
    for jj, y in enumerate(nums):
        if x + y == 2020:
            print(x * y)

        for kk, z in enumerate(nums):
            if ii == jj or jj == kk or ii == kk:
                continue
            elif x + y + z == 2020:
                print(x*y*z)
