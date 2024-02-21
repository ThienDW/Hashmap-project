# Name: Daniel Thien
# OSU Email: Thienda@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: 8/15/2023
# Description: Hashmap

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        Puts a new value into the hashmap
        """
        #check table load, resize if needed
        lf = self.table_load()
        if lf >= 0.5:
            self.resize_table(self._capacity*2)
        #set initial i
        i = self._hash_function(key)
        i = i % self.get_capacity()
        j = 1
        init = i
        #keep probing i until a non-filled slot is reached
        while self._buckets[i] is not None:
            #if key already exists, simply overwrite value
            if self._buckets[i].key == key:
                if self._buckets[i].is_tombstone == True:
                    self._size = self._size + 1
                self._buckets[i] = HashEntry(key, value)

                return
            i = init + (j*j)
            i = i % self.get_capacity()
            j = j + 1


        self._buckets[i] = HashEntry(key, value)
        self._size = self._size + 1
            
       
        return
        

    def table_load(self) -> float:
        """
        Gets the load factor of the table, based on number of elements and capacity
        """
        buckets = self._buckets.length()
        si = self._size
        lf = self._size/self._buckets.length()
        return lf

    def empty_buckets(self) -> int:
        """
        Returns number of empty buckets
        """
        tally = self._capacity - self._size
        return tally
        

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes table
        """
        if new_capacity < 1:
            return 
        if new_capacity < self._size:
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
        #create empty slots in array equal to capacity
        for _ in range(newarr._capacity):
            newarr.append(None)
        oldarr = self._buckets
        self._buckets = newarr
        #fill new array with old values, rehashing them
        for i in range(oldcap):
            if oldarr[i] is not None:
                self.put(oldarr[i].key, oldarr[i].value)
            
        return
        

    def get(self, key: str) -> object:
        """
        Gets value from array given key
        """
        i = self._hash_function(key)
        i = i % self.get_capacity()
        j = 1
        init = i
        count = self._capacity
        #after getting initial index, probe until key is found. 
        while self._buckets[i] is not None:
            if self._buckets[i].key == key:
                if self._buckets[i].is_tombstone is True:
                    return
                return self._buckets[i].value
            i = init + (j*j)
            i = i % self.get_capacity()
            j = j + 1
            count = count - 1
            if count == 0:
                return
        return
 

    def contains_key(self, key: str) -> bool:
        """
        Sees if key is in hashmap
        """
        i = self._hash_function(key)
        i = i % self.get_capacity()
        j = 1
        init = i
        count = self._capacity
        #after gettig initial index, probe until key is found.
        while self._buckets[i] is not None:
            if self._buckets[i].key == key:                
                return True
            i = init + (j*j)
            i = i % self.get_capacity()
            j = j + 1
            count = count - 1
            if count == 0:
                return False
        return False

    def remove(self, key: str) -> None:
        """
        'removes' key & value by designating its index as a tombstone
        """
        i = self._hash_function(key)
        i = i % self.get_capacity()
        j = 1
        init = i
        count = self._capacity
        #set initial index and probe until appropriate key is found
        while self._buckets[i] is not None:
            if self._buckets[i].key == key:
                #if key is already tombstone, no change
                if self._buckets[i].is_tombstone == True:
                    return
                self._buckets[i].is_tombstone = True
                self._size = self._size - 1
                return
            i = init + (j*j)
            i = i % self.get_capacity()
            j = j + 1
            count = count - 1
            if count == 0:
                return
             
        return

    def clear(self) -> None:
        """
        Clears hashmap
        """
        #set data to a new, empty dynamic array, set size to 0.
        self._buckets = DynamicArray()
        self._size = 0
        for _ in range(self._capacity):
            self._buckets.append(None)
        return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns array of keys and values
        """
        newarr = DynamicArray()
        for i in range(self._capacity):          
            if self._buckets[i] is not None:
                if self._buckets[i].is_tombstone == False:
                    v = self._buckets[i].value
                    k = self._buckets[i].key
                    t = (v,k)
                    newarr.append(t)
        return newarr


    def __iter__(self):
        """
        Set initial index for loop
        """       
        self.index = 0 
        return self
        

    def __next__(self):
        """
        Obtain value and advance iterator
        """
        if self.index >= self.get_capacity():
            raise StopIteration
        while self._buckets[self.index] is None:
            self.index = self.index + 1        
            if self.index >= self.get_capacity():
                raise StopIteration
        value = self._buckets[self.index]
        self.index = self.index + 1    
        return value
        
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

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(449, hash_function_2)
    keys = [i for i in range(0, 113)]
    for key in keys:
        m.put(str(key), key * 42)
    m.resize_table(10)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
