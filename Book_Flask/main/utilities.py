from itertools import combinations


def making_combination(lst):  # making combination for items in cart
    res = []
    for i in range(len(lst)):
        el = [set(x) for x in combinations(lst, i+1)]
        res.append(el)
    return res[::-1]  # reverse for priority (larger cases)


# chosing the recommendation from rules and items in cart
def making_recommendation(cart, rule):
    res = []
    for i in cart:
        for i2 in i:
            #[print(x) for x in rule if i2.issubset(x)]
            for r in rule:
                if i2.issubset(r):
                    if i2 in res:
                        pass
                    else:
                        res.append(i2)

    res_2 = []  # remove the redundancy to fit the database

    if len(res) > 0:
        for i in res:
            ex = str(i)
            ex = ex.strip('{/}')
            ex = ex.replace(' ', '')
            ex = ex.replace("'", '')
            res_2.append(ex)

    return res_2
