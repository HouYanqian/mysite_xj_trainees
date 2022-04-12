cur_count = 50
target_count = 255 * 4 + 70 * 2 + 375 + 195 * 2


def level_cost(level):
    return int(level / 5) + 3


cur_level = 19
pass_level = 0
while cur_count < target_count:
    pass_level += 1
    cur_count += level_cost(cur_level+cur_level)

if __name__ == '__main__':
    print('所需白虎令"%s"， 需要再通"%s"关' % (target_count, pass_level))
