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
        assert r >= 1
        h = self.BlockSize
        n = int(h/2)
        return ['pro'+str(i)+'Rd'+str(r-1) for i in range(n-1)]

    def genConstraints_of_Round(self, r):
        assert r >= 1
        constraints = []
        X = self.genVars_InVars_at_Round(r)
        Y = self.genVars_InVars_at_Round(r+1)
        h = self.BlockSize
        n = int(h/2)
        x0 = X[0 :   n]
        x1 = X[n : 2*n]
        y0 = Y[0 :   n]
        y1 = Y[n : 2*n]
        if n == 16:
            x2 = self.rotr(x0, 16, 7)
            x3 = self.rotl(x1, 16, 2)
        else:
            x2 = self.rotr(x0, n, 8)
            x3 = self.rotl(x1, n, 3)

        constraints += three_way_fork(x3, y1, y0, r)

        d = self.genVars_Objective(r)

        for i in range(n-1):
            b = [x2[i], x1[i], y0[i]]
            a = [x2[i+1], x1[i+1], y0[i+1]]
            constraints += [a[1]+' - '+a[2]+' + '+d[i]+' >= 0 ']
            constraints += [a[0]+' - '+a[1]+' + '+d[i]+' >= 0 ']
            constraints += [a[2]+' - '+a[0]+' + '+d[i]+' >= 0 ']
            constraints += [a[0]+' + '+a[1]+' + '+a[2]+' + '+d[i]+' <= 3 ']
            constraints += [a[0]+' + '+a[1]+' + '+a[2]+' - '+d[i]+' >= 0 ']
            constraints += [b[0]+' + '+b[1]+' + '+b[2]+' + '+d[i]+' - '+a[1]+' >= 0 ']
            constraints += [a[1]+' + '+b[0]+' - '+b[1]+' + '+b[2]+' + '+d[i]+' >= 0 ']
            constraints += [a[1]+' - '+b[0]+' + '+b[1]+' + '+b[2]+' + '+d[i]+' >= 0 ']
            constraints += [a[0]+' + '+b[0]+' + '+b[1]+' - '+b[2]+' + '+d[i]+' >= 0 ']
            constraints += [a[2]+' - '+b[0]+' - '+b[1]+' - '+b[2]+' + '+d[i]+' >= -2 ']
            constraints += [b[0]+' - '+a[1]+' - '+b[1]+' - '+b[2]+' + '+d[i]+' >= -2 ']
            constraints += [b[1]+' - '+a[1]+' - '+b[0]+' - '+b[2]+' + '+d[i]+' >= -2 ']
            constraints += [b[2]+' - '+a[1]+' - '+b[0]+' - '+b[1]+' + '+d[i]+' >= -2 ']

        constraints += [x2[n-1]+' + '+x1[n-1]+' + '+y0[n-1]+' <= 2 ']
        constraints += [x2[n-1]+' + '+x1[n-1]+' + '+y0[n-1]+' - 2 temp'+str(r-1)+' >= 0 ']
        constraints += ['temp'+str(r-1)+' - '+x2[n-1]+' >= 0 ']
        constraints += ['temp'+str(r-1)+' - '+x1[n-1]+' >= 0 ']
        constraints += ['temp'+str(r-1)+' - '+y0[n-1]+' >= 0 ']

        return constraints

    def genObjectiveFun_to_Round(self, r):
        assert (r >= 1)
        h = self.BlockSize
        n = int(h/2)
        f = list([])
        for i in range(1, r+1):
            for j in range(n-1):
                f.append(self.genVars_Objective(i)[j])

        f = ' + '.join(f)
        return f

    def genModel(self, r):
        C = list([])
        for i in range(1, r+1):
            C = C + self.genConstraints_of_Round(i)
        add_constraint_1 = ' + '.join(['p'+str(i) for i in range(self.BlockSize)]) + ' >= 1'

        V = getVariables_From_Constraints(C)
        V = V.union(getVariables_From_Constraints([add_constraint_1]))

        with open('diff-round-'+str(r)+'.lp', 'w') as o:
            o.write('Minimize\n')
            o.write(self.genObjectiveFun_to_Round(r))
            o.write('\n\nSubject To\n')
            o.write(add_constraint_1)
            o.write('\n')
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
