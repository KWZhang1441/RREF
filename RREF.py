from copy import deepcopy

def vadd(v1, v2):
    mat = [v1[i] + v2[i] for i in range(len(v1))]
    return mat

def vsmul(v, x):
    mat = [v[i]*x for i in range(len(v))]
    return mat

def swaprows(A, r1, r2):
    B = deepcopy(A)
    row1 = A[r1-1]
    row2 = A[r2-1]
    B[r1-1] = row2
    B[r2-1] = row1
    return B

def findNonZero(A, ColumnStart, ColumnEnd, Rows):
    """
    Takes a matrix and finds the first non-zero entry
    Returns a tuple (row, column)
    """
    B = deepcopy(A)
    for i in range(ColumnStart, ColumnEnd):
        #check down the columns
        #use z-1 to make sure we ignore the rows that we've already moved to the top
        for j in range(ColumnStart, Rows):
            #repeat the loop until we find a non-zero entry
            if B[j][i] != 0:
                return (j, i)
    return ('stop', 'stop')


def RREF(A, augmented = True):
    """
    Input: Matrix A. The second argument decides whether your matrix is augmented or not.
    Output: RREF of the matrix
    """
    #set m as the number of rows and n and columns
    #z is incremented so we do not go over rows we have already put into RREF
    m = len(A)
    n = len(A[0])
    
    #Early exit condition if matrix is not the correct size
    for i in range(m):
        if len(A[i]) != n:
            raise ValueError("Matrix is not well defined")
    
    #z is the row we swap our non zero row to
    #In this case we start counting the rows from 1 due to mathematical convention indexing from 1
    #Python indexes from 0 so we use z-1 later
    z = 1
    #Make a copy so A is not affected with the function
    B = deepcopy(A)
    #the max times we do the loop is m times (the number of rows)
    for times in range(m):
        #find first non-zero entry, first going down columns
        #we can skip the columns where there is guranteed to be a leading 1
        
        #If it is an augmented matrix we do not want to check the right most column for non-zeros
        if augmented == True:
            (row, column) = findNonZero(B, z-1, n-1, m)
        elif augmented == False:
            (row, column) = findNonZero(B, z-1, n, m)
        else:
            raise ValueError("The 'augmented' argument must either be True or False")
            
        #early exit condition
        if (row, column) == ('stop', 'stop'):
            return B
        
        #make the row we found the 1st row (2nd row for 2nd attempt etc.)
        B = swaprows(B, row+1, z)
        #make the zth row start with a 1
        B[z-1] = vsmul(B[z-1], 1/B[z-1][column])
        #Clear the other rows, including the ones that we've put to the top
        rangeLst = [i for i in range(m)]
        rangeLst.remove(z-1)
        for k in rangeLst:
            addVec1 = vsmul(B[z-1], -1)
            addVec2 = vsmul(addVec1, B[k][column])
            B[k] = vadd(addVec2, B[k])
        #go back to top of for loop and find the next column with a non-zero entry
        #increment z so next row is put below
        z = z + 1
    return B

TestMatrix1 = [[2,3,8],[5,1,0.5]]
TestMatrix2 = [[-5,4,-1,8],[-2,4,5,6],[-9,12,9,5],[1,2,3,4]]
print(RREF(TestMatrix1))
print(RREF(TestMatrix2, False))
print(RREF(TestMatrix1, 5))
    
