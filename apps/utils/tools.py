def cost_convert(n):
    """
    转大写
    :param n:
    :return:
    """
    units = ['', '万', '亿']
    nums = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
    decimal_label = ['角', '分']
    small_int_label = ['', '拾', '佰', '仟']
    int_part, decimal_part = str(int(n)), str(n - int(n))[2:]  # 分离整数和小数部分

    res = []
    if decimal_part:
        res.append(''.join([nums[int(x)] + y for x, y in zip(decimal_part, decimal_label) if x != '0']))

    if int_part != '0':
        res.append('圆')
        while int_part:
            small_int_part, int_part = int_part[-4:], int_part[:-4]
            tmp = ''.join([nums[int(x)] + (y if x != '0' else '') for x, y in
                           list(zip(small_int_part[::-1], small_int_label))[::-1]])
            tmp = tmp.rstrip('零').replace('零零零', '零').replace('零零', '零')
            unit = units.pop(0)
            if tmp:
                tmp += unit
                res.append(tmp)
    return ''.join(res[::-1])


def id_split(ids):
    """
    id列表分割
    :param ids:
    :return:
    """
    res_list = []
    initial_split = ids.split(',')
    for initial in initial_split:
        twice_split = initial.split('-')
        try:
            if len(twice_split) == 1:
                res_list.append(int(twice_split[0]))
            else:
                if twice_split[1]:
                    res_list += list(range(int(twice_split[0]), int(twice_split[1]) + 1))
        except ValueError:
            pass
    return res_list

