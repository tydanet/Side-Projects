class FixedQueue:
    ''' Queue that pops the oldest element every time a push operation occurs 
    '''
    
    def __init__(self, elems):
        self.queue = elems
        
    def pushpop(self, elem):
        popped = self.queue.pop(0)
        self.queue.append(elem)

        return popped
