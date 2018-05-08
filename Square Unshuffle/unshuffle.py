def bisect(w):
    ''' simply splits a string down the middle '''
    return w[:len(w)//2], w[len(w)//2:]

def shrink(a, b):
    ''' Chops off last two chars from w=ab, then bisects '''
    return a[:-1], a[-1]+b[:-2]

def unshuffle_square(w):
    ''' Seems to have a worst case of O(n^2) when given a perfect shuffle as input
        and a best case of O(1) when given w=u^2 as input 
    '''
    
    string1 = ''
    string2 = ''
    
    # initialize to given string w
    u = w
    
    # u shrinks as we iterate through
    while len(u) > 0:
        sub1, sub2 = bisect(u)
        print('remaining:', u)
        
        # once the substrings are equal we can move on
        while sub1 != sub2:
            if sub1 == '' or sub2 == '': # otherwise we never move on
                return False
        
            # reduce substring sizes by one and reindex them
            sub1, sub2 = shrink(sub1, sub2)
            print('substrings:', sub1, sub2)
        
        # mostly here for printing purposes
        string1 = string1 + sub1
        string2 = string2 + sub2
    
        u = w[2*len(string1):] # reindex substrings to the right
        
    print('strings:', string1, string2)
    return True
