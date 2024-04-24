class Hashtable:
    def __init__(self):
        self.MAX = 10
        self.arr = [[] for i in range(self.MAX) ]
    
    def get_hash(self, key):
        hash = 0
        for char in key:
            hash += ord(char)
        return hash % self.MAX
    
    def __setitem__(self , key, val):
        h = self.get_hash(key)
        found = False
        for indx , element in enumerate(self.arr[h]):
            if len(element) == 2 and element[0]==key:
                self.arr[h][indx] = (key , val)
                found = True
                break
        if not found:
            self.arr[h].append((key,val))
    
    def __getitem__(self, key):
        h = self.get_hash(key)
        print(h)
        for element in self.arr[h]:
            print(element)
            if element[0] == key:
                return element[1]

    
    def __delitem__(self , key):
        h = self.get_hash(key)
        for index , element in enumerate(self.arr[h]):
            if element[0] == key:
                del self.arr[h][index]
    
h = Hashtable()

h["march 6"] = 70
h["march 17"] = 80
print(h.arr)
print(h["march 17"])



