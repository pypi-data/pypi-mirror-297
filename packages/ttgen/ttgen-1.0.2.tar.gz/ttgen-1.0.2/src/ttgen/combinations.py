from typing import Iterator, TypeVar

T = TypeVar('T')

def combinations(choices: list[T], num_choices: int) -> Iterator[tuple[T, ...]]:
    multiplicities = {}
    for choice in choices:
        multiplicities[choice] = multiplicities.get(choice, 0) + 1
    
    for result_mults in combinations_from_multiplicities(list(multiplicities.values()), num_choices):
        
        if result_mults is None:
            yield None
        
        result_elements = []
        for choice, multiplicity in zip(multiplicities.keys(), result_mults):
            result_elements.extend([choice] * multiplicity)
        yield tuple(result_elements)

def combinations_from_multiplicities(multiplicities: list[int], num_choices: int) -> Iterator[tuple[int, ...]]:
    
    k = int(num_choices)
    m = [min(i, k) for i in multiplicities] # Original Pascal code breaks if any multiplicities are greater than k
    n = len(m)

    a = [0 for _ in range(n)]
    kk = k
    for i in range(n, 0, -1):
        if m[i-1] <= kk:
            a[i-1] = m[i-1]
            kk = kk - a[i-1]
        else:
            a[i-1] = kk
            break

    i0 = i

    b = [None for _ in range(n)]
    for i in range(n, 0, -1):
        b[i-1] = (b[i] if i < n else 0) + m[i-1]

    up = [i+1 for i in range(n)]
    up1 = [i+1 for i in range(n)]
    solve = [n for _ in range(n)]
    mark = [0 for _ in range(n)]

    _sum = [None for _ in range(n)]
    for i in range(n):
        _sum[i] = (_sum[i-1] + a[i-1]) if i > 0 else 0
    for i in range(i0, n):
        _sum[i] += 1

    d = [1 if i < i0 else -1 for i in range(n)]
    down = [n-1 if i < n-1 else 0 for i in range(n)]
    i = i0

    up_point = False
    for _ in range(999_999_999):
        yield tuple(a)
        if i == 0 or i == n:
            break

        lower = max(k-b[i]-_sum[i-1], 0)
        upper = min(k-_sum[i-1], m[i-1])
        
        if not ((d[i-1]>0) and a[i-1]==upper or ((d[i-1] < 0) and a[i-1] == lower)):
            a[i-1] = a[i-1] + d[i-1]
            a[solve[i-1]-1] = a[solve[i-1]-1] - d[i-1]
        up[i-1] = i

        if (d[i-1] > 0 and a[i-1] == upper) or (d[i-1] < 0 and a[i-1] == lower):
            up[i-1] = up[i-2]
            up[i-2] = i-1
            lower1 = max(k-b[i]-_sum[i-1]-d[up[i-1]-1], 0)
            upper1 = min(k-_sum[i-1]-d[up[i-1]-1], m[i-1])
            next_val = upper1 if d[i-1] > 0 else lower1
            solve[up[i-1]-1] = i if next_val != a[i-1] else solve[i-1]
            mark[up[i-1]-1] = 1
            mark[i-1] = 1
            up_point = (_sum[i-1]+a[i-1]==k) or (_sum[i-1]+a[i-1]+b[i]==k) or (i==n-1)
            if lower1 != upper1:
                _sum[i-1] = _sum[i-1] + d[up[i-1]-1]
            next_landing = (_sum[i-1]+next_val==k) or (_sum[i-1]+next_val+b[i]==k) or (i==n-1)
            up1[i-1] = up1[i-2]
            up1[i-2] = i-1
            if lower1 == upper1:
                down[up1[i-1]-1] = i
            elif next_landing:
                down[up[i-1]-1] = i
            else:
                down[up[i-1]-1] = down[i-1]
            if next_landing:
                up1[i-1] = i

            d[i-1] = -d[i-1]
        if up_point:
            ii = i
            i = up[i-1]
            up[ii-1] = ii
            up_point = False
        else:
            if mark[down[i-1]-1] == 0:
                solve[down[i-1]-1] = solve[i-1]
            mark[i-1] = 0
            i = down[i-1]