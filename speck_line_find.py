from MILPSbox import three_way_fork, getVariables_From_Constraints

class speck():
    def __init__(self, blocksize):
        self.BlockSize = blocksize

    def genVars_InVars_at_Round(self, r):
        assert r >= 1
        if r == 1:
            return ['p'+str(j) for j in range(self.BlockSize)]
        if r > 1:
            return ['p'+str(j)+'Rd'+str(r-1) for j in range(self.BlockSize)]

    def rotl(self, X, n, r):
        assert r >= 1
        temp = [None]*n
        for i in range(n-r):
            temp[i] = X[i+r]
        for i in range(n-r,n):
            temp[i] = X[i-n+r]
        return temp

    def rotr(self, X, n, r):
        assert r >= 1
        temp = [None]*n
        for i in range(r):
            temp[i] = X[n-r+i]
        for i in range(r,n):
            temp[i] = X[i-r]
        return temp


    def genVars_Objective(self, r):
        h = int(self.BlockSize + 1)
        assert r >= 1
        return ['pro'+str(i)+'Rd'+str(r-1) for i in range(h)]

    def genConstraints_of_Round(self, r):
        assert r>=1
        constraints = list()
        X = self.genVars_InVars_at_Round(r)
        Y = self.genVars_InVars_at_Round(r+1)
        h = self.BlockSize
        n = int(h/2)

        x0 = X[0 : n]
        x1 = X[n: 2*n]

        y0 = Y[0 : n]
        y1 = Y[n: 2*n]


        if n == 16:
            x2 = self.rotr(x0, n, 7)
        else:
            x2 = self.rotr(x0, n, 8)


        x4 = ['x4'+'Rd'+str(r-1)+'L'+str(i) for i in range(n)]
        x3 = ['x3'+'Rd'+str(r-1)+'L'+str(i) for i in range(n)]

        if n == 16:
            y2 = self.rotr(y1, n, 2)
        else:
            y2 = self.rotr(y1, n, 3)

        constraints += three_way_fork(x1, y2, x4, r)
        constraints += three_way_fork(x3, y1, y0, r)
        d = self.genVars_Objective(r)
        for i in range(n):
            a = [x3[i],x2[i],x4[i]]
            constraints += [d[i]+' - '+a[0]+' - '+a[1]+' + '+a[2]+' + '+d[i+1]+' >= 0']
            constraints += [d[i]+' + '+a[0]+' + '+a[1]+' - '+a[2]+' - '+d[i+1]+' >= 0']
            constraints += [d[i]+' + '+a[0]+' - '+a[1]+' - '+a[2]+' + '+d[i+1]+' >= 0']
            constraints += [d[i]+' - '+a[0]+' + '+a[1]+' - '+a[2]+' + '+d[i+1]+' >= 0']
            constraints += [d[i]+' + '+a[0]+' - '+a[1]+' + '+a[2]+' - '+d[i+1]+' >= 0']
            constraints += [d[i]+' - '+a[0]+' + '+a[1]+' + '+a[2]+' - '+d[i+1]+' >= 0']
            constraints += [a[0]+' - '+d[i]+' + '+a[1]+' + '+a[2]+' + '+d[i+1]+' >= 0']
            constraints += [d[i]+' + '+a[0]+' + '+a[1]+' + '+a[2]+' + '+d[i+1]+' <= 4']

        return constraints

    def genObjectiveFun_to_Round(self, r):
        assert (r >= 1)
        h = int(self.BlockSize / 2)
        f = list([])
        for i in range(1, r+1):
            for j in range(1,h):
                f.append(self.genVars_Objective(i)[j])
        f = ' + '.join(f)
        return f


    def genModel(self, r):
        V = set([])
        C = list([])
        for i in range(1, r+1):
            C = C + self.genConstraints_of_Round(i)
        add_constraint_1 = ' + '.join(['p'+str(i) for i in range(self.BlockSize)]) + ' >= 1'

        V = getVariables_From_Constraints(C)
        V = V.union(getVariables_From_Constraints([add_constraint_1]))

        with open('line-round-'+str(r)+'.lp','w') as o:
            o.write('Minimize\n')
            o.write(self.genObjectiveFun_to_Round(r))
            o.write('\n\nSubject To\n')
            o.write(add_constraint_1)
            o.write('\n')
            for i in range(r):
                o.write('pro0Rd'+str(i)+' = 0\n')
            for c in C:
                o.write(c + '\n')
            o.write('\n\nBinary\n')
            for v in V:
                o.write(v + '\n')

def main():
    print('Initialized...')
    m = speck(32)
    m.genModel(4)

if __name__ == '__main__':
    main()
