# Name: Daniel Thien
# OSU Email: Thienda@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: 8/15/2023
# Description: Hashmap



from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Puts a key and a value into the hashmap
        """
        
        #checks lf, resize if necessary
        lf = self.table_load()
        if lf >= 1.0:
            self.resize_table(self._capacity*2)

        kn = self._hash_function(key)
        kn = kn % self.get_capacity()

        if self.get_capacity() < kn:
            self.resize_table(kn)
        #if list is empty, insert 
        l = self._buckets[kn]
        if l._head is None:
            l.insert(key,value)
            self._size = self._size + 1
            return
        #if list is not empty, look through nodes to make sure key doesn't already exist;
        #if it does, simply overwrite the existing value with the new one
        for SLNode in l:
            n = SLNode
            if SLNode.key == key:
                t = 1
                SLNode.value = value                
                return
        l.insert(key,value)
        self._size = self._size + 1         
        return

    def empty_buckets(self) -> int:
        """
        returns # of empty buckets
        """
        tally = 0
        for i in range (self._buckets.length()):
            if self._buckets[i]._head is None:
                tally = tally + 1
        return tally

        

    def table_load(self) -> float:
        """
        Calculates load factor of table
        """
        buckets = self._buckets.length()
        si = self._size
        lf = self._size/self._buckets.length()
        return lf

    def clear(self) -> None:
        """
        Clears contents of hash map
        """
        for i in range(self._capacity):
            if self._buckets is not None:
                self._buckets[i] = LinkedList()
        self._size = 0
        return

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the table to new capacity
        """

        if new_capacity < 1:
            return 
        #create new array
        newarr = DynamicArray()
        oldcap = self.get_capacity()
        # capacity must be a prime number
        self._size = 0
        self._capacity = new_capacity
        newarr._capacity = new_capacity
        if self._is_prime(newarr._capacity) is False:
            newarr._capacity = self._next_prime(newarr._capacity)
        new_capacity = newarr._capacity
        self._capacity = newarr._capacity
        #populate new array with empty linked lists 
        for _ in range(newarr._capacity):
            newarr.append(LinkedList())
        oldarr = self._buckets
        self._buckets = newarr
        #place values from old list into new one
        for i in range(oldcap):
            for SLNode in oldarr[i]:
                self.put(SLNode.key, SLNode.value)
            
        return

    #upto here

    def get(self, key: str):
        """
        Returns value associated with given key
        """
        #hash key and check nodes in index for key
        kn = self._hash_function(key)
        kn = kn % self.get_capacity()
        l = self._buckets[kn]    
        for SLNode in l:
            if SLNode.key == key:
                return SLNode.value
        return



    def contains_key(self, key: str) -> bool:
        """
        Searches for given key
        """
        kn = self._hash_function(key)
        kn = kn % self.get_capacity()
        l = self._buckets[kn]           
        for SLNode in l:
            if SLNode.key == key:
                return True
        return False

    def remove(self, key: str) -> None:
        """
        Remove given key/value
        """

        kn = self._hash_function(key)
        kn = kn % self.get_capacity()
        l = self._buckets[kn]         
        #find matching key and remove it from list
        for SLNode in l:
            if SLNode.key == key:
                l.remove(key) 
                self._size = self._size - 1
                return
             
        return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns array of pairs of keys and values
        """
        newarr = DynamicArray()
        for i in range(self._capacity):
            for SLNode in self._buckets[i]:
                t = [SLNode.key,SLNode.value]
                newarr.append(t)
        return newarr


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Finds mode of dynamic array
    """
    
    map = HashMap()
    #iterates through array; if object is already in map, increments the value (frequency) of that item by one; otherwise add it to the map with a value (freq) of 1.
    #each string acts as a key; it's associated value is the frequency of that string within the argued dynamic array.
    for i in range(da.length()):
        if map.contains_key(da[i]) is True: 
            num = map.get(da[i])
            map.put(da[i],num + 1)
        else:
            map.put(da[i],1)

    #finds the mode and frequency
    mode = DynamicArray()
    freq = 0
    #use get_keys_and_values() to get an array containing the keys(objects) and values(frequencies of objects)
    freq_array = map.get_keys_and_values()
    #iterate through array, finding the largest frequency/modes.
    for i in range(freq_array.length()):
        #if frequency is larger than current max, create a new array with the new most common object
        if freq_array[i][1] > freq:
            freq = freq_array[i][1]
            mode = DynamicArray()            
            mode.append(freq_array[i][0])
        #if frequency is equal to current max, simply add it to existing array
        elif freq_array[i][1] == freq:
            mode.append(freq_array[i][0])

    return (mode, freq)

                    
                    
              

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    
    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
