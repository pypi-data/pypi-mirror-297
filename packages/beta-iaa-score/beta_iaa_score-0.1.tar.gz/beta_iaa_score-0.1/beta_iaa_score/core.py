# beta_iaa_score/core.py

def nr_agreements(v1, v2):
    ''''
    Computes the number of agreements between two vectors.'''
    acc = 0
    for i in range(7):
        if v1[i] == v2[i]:
            acc+=1
        else:
            continue
    return acc

def coef2(v1, v2, v3):
    ''''
    Computes the agreement between three adnotators.'''
    x = (nr_agreements(v1, v2) + nr_agreements(v1, v3) + nr_agreements(v2, v3)) / 21
    return x