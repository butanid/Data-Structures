# Name: Deep Butani
# OSU Email: butanid@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3/14/24
# Description: HashMap (Portfolio Assignment) - Part 2

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
        Method used to update the key/value pair in the hash map
        """
        # Checks if load factor of table is greater than or equal to 1
        if self.table_load() >= 0.5:
            # Double capacity
            self.resize_table(self._capacity * 2)

        # Calculating index
        index = self._hash_function(key) % self._capacity
        # Initializing variable to track probe count
        probe = 0

        # Checks if index value and its key equals to given key
        if self._buckets[index] and self._buckets[index].key == key:
            # Replacing index key with given key
            self._buckets[index].key = key
            # Replacing index value with given value
            self._buckets[index].value = value
            return
        # Checks if index value is none or if tombstone
        elif self._buckets[index] is None or self._buckets[index].is_tombstone:
            # Inserting key/value pair
            self._buckets[index] = HashEntry(key, value)
            # Incrementing table size
            self._size += 1
            return

        # Probing method
        else:
            # Initializing variable for index value
            index_value = index

            # Condition to check if index and not a tombstone
            while self._buckets[index] and not self._buckets[index].is_tombstone:
                # Incrementing probe count
                probe += 1
                # Calculating probed index
                index = (index_value + probe ** 2) % self._capacity

                # Checks if probed index and its key equals to given key
                if self._buckets[index] and self._buckets[index].key == key:
                    # Checks if probed index is a tombstone
                    if self._buckets[index].is_tombstone:
                        return
                    # Checks if probed index is not a tombstone
                    elif not self._buckets[index].is_tombstone:
                        # Decrementing table size
                        self._size -= 1
                        break

            # Inserting key/value pair
            self._buckets[index] = HashEntry(key, value)
            # Incrementing table size
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Method used to change the capacity of the underlying hash table
        """
        # Checks if new_capacity is less than table size
        if new_capacity < self._size:
            return

        # Checks if new_capacity is a prime number
        if self._is_prime(new_capacity):
            pass
        else:
            # Update new_capacity to next highest prime number
            new_capacity = self._next_prime(new_capacity)

        # Initializing variable for new resized hash table
        resized_table = HashMap(new_capacity, self._hash_function)

        # Iterating through each element of original table
        for index in range(self._capacity):
            # Checks if index and not a tombstone
            if self._buckets[index] and not self._buckets[index].is_tombstone:
                # Put key/value pairs into new resized table
                resized_table.put(self._buckets[index].key, self._buckets[index].value)
                # Incrementing table size
                self._size += 1

        # Updating underlying storage to new resized table storage
        self._buckets = resized_table._buckets
        self._capacity = resized_table._capacity
        self._size = resized_table._size

    def table_load(self) -> float:
        """
        Method used to return the current hash table load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Method used to return the number of empty buckets in the hash table
        """
        return self._capacity - self._size

    def get(self, key: str) -> object:
        """
        Method used to return the value associated with the given key, otherwise None
        """
        # Calculating Index
        index = self._hash_function(key) % self._capacity
        # Initializing variable to track probe count
        probe = 0

        # Condition to check if probe count less than capacity
        while probe < self._capacity:
            # Probed Index computation
            get_index = (index + probe ** 2) % self._capacity

            # Checks if probed index
            if self._buckets[get_index]:
                # Checks if probed index's key equals to given key and not a tombstone
                if self._buckets[get_index].key == key and not self._buckets[get_index].is_tombstone:
                    # Return value of probed index
                    return self._buckets[get_index].value

            # Incrementing probe count
            probe += 1

        return None

    def contains_key(self, key: str) -> bool:
        """
        Method used to return True if the given key is in the hashmap, otherwise False
        """
        if self.get(key):
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Method used to remove the given key and its associated value from the hash map
        """
        # Calculating Index
        index = self._hash_function(key) % self._capacity
        # Initializing variable to track probe count
        probe = 0

        # Condition to check if probe count less than capacity
        while probe < self._capacity:
            # Probed Index computation
            remove_index = (index + probe ** 2) % self._capacity

            # Checks if probed index
            if self._buckets[remove_index]:
                # Checks if probed index's key equals to given key and not a tombstone
                if self._buckets[remove_index].key == key and not self._buckets[remove_index].is_tombstone:
                    # Updating probed index to a tombstone
                    self._buckets[remove_index].is_tombstone = True
                    # Decrementing table size
                    self._size -= 1
                    return

            # Increment probe count
            probe += 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Method used to return a dynamic array where each index contains a key/value tuple pair
        stored in the hash map
        """
        # Initializing new DynamicArray to store key/value pairs
        key_value_array = DynamicArray()

        # Iterating through each element of bucket
        for index in range(self._buckets.length()):
            # Initializing variable for key/value pair
            pair = self._buckets[index]

            # Checks if key/value pair and not a tombstone
            if pair and not pair.is_tombstone:
                # Appending key/value pair into new array
                key_value_array.append((pair.key, pair.value))

        return key_value_array

    def clear(self) -> None:
        """
        Method used to clear the contents of the hash map
        """
        # Initializing hash map bucket to empty DynamicArray
        self._buckets = DynamicArray()

        # Iterating through each element of original table
        for index in range(self._capacity):
            # Appending None to each bucket
            self._buckets.append(None)

        # Updating table size to 0
        self._size = 0

    def __iter__(self):
        """
        Method used to enable hash map to iterate across itself
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Method used to return the next item in the hash map based on the location of iterator
        """
        # Module 3 - Exploration: Encapsulation and Iterators
        if self._index >= self._buckets.length():
            raise StopIteration

        value = self._buckets.get_at_index(self._index)

        self._index = self._index + 1

        # Condition to check if value is none or is a tombstone
        while value is None or value.is_tombstone:
            # Module 3 - Exploration: Encapsulation and Iterators
            if self._index >= self._buckets.length():
                raise StopIteration

            value = self._buckets.get_at_index(self._index)

            self._index = self._index + 1

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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
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
