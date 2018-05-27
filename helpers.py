def flatten(ll):
    return [x for l in ll for x in l]

def xs(ll):
    return [x for x, _ in ll]

def ys(ll):
    return [y for _, y in ll]

def mean(ll):
    assert len(xs(ll)) == len(ys(ll))
    return sum(xs(ll))/len(ll), sum(ys(ll))/len(ll)


def alpha_beta(a, b):
    (p1, q1) = a
    (p2, q2) = b
    if p1 == p2:
        alpha = float('inf')
    else:
        alpha = (q2 - q1) / (p2 - p1)
    beta = q1 - alpha * p1
    return alpha, beta

def isup(a, b):
    (x, y) = a
    ((p1, q1), (p2, q2)) = b
    if p1 == p2:
        return x < p1
    alpha, beta = alpha_beta(b[0], b[1])
    return y > alpha * x + beta

def isdown(a, b):
    return not isup(a, b)

def different_sides(a1, a2, b):
    return (isup(a1, b) and isdown(a2, b)) or isup(a2, b) and isdown(a1, b)

def intersect(l1, l2):
    (a1, a2) = l1
    (b1, b2) = l2
    return different_sides(a1, a2, l2) and different_sides(b1, b2, l1)

def solution(a, b):
    (a1, a2) = a
    (b1, b2) = b
    assert intersect(a, b)
    alpha1, beta1 = alpha_beta(a1, a2)
    alpha2, beta2 = alpha_beta(b1, b2)
    xsol =  (beta2 - beta1) / (alpha1 - alpha2)
    ysol = alpha1 * xsol + beta1
    return xsol, ysol