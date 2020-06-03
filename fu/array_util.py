def flat(ar):
    # 把一个多维列表展平
    if type(ar) == list:
        a = []
        for i in ar:
            a.extend(flat(i))
        return a
    else:
        return [ar]
