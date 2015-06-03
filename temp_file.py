def posterior (x, clusters):
    x_shape = x.shape
    N = x_shape[0]
    D = x_shape[1]
    K = cluster_shape.shape[0]
    z = np.zeros([K,N])
    for k in xrange(K):
        for i in xrange(N):
            product1 = 1
            for d in xrange(D):
                if x[i,d]==1:
                    product1*=max(1e-100,cluster[k,d])
                else:
                    product1*=max(1e-100,1-cluster[k,d])
            sum1 = 0
            for j in xrange(K):
                product2 = 1
                for d in xrange(D):
                    if x[i,d]==1:
                        product2*=max(1e-100,cluster[j,d])
                    else:
                        product2*=max(1e-100,1-cluster[j,d])
                sum1+=product2
            z[k,i] = product1/float(sum1)
    return z
