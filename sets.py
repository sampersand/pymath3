args = 0.2
kwgs = 0.3

item = [1, 3, 4]
# [1] + [0.2, 0.3] = [1, 0.1, 0.3]
# [1, 2] + [0.2] = [1, 2, 0.3]
# [1, 2, 3] + [] = [1, 2, 3]
amnt, args, kwgs = item + [args, kwgs][len(item) -1:]
print(amnt, args, kwgs)