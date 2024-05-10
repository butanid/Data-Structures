# Name: Deep Butani
# OSU Email: butanid@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3/14/24
# Description: HashMap (Portfolio Assignment) - Part 1


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
        Method used to update the key/value pair in the hash map
        """
        # Checks if load factor of table is greater than or equal to 1
        if self.table_load() >= 1:
            # Double capacity
            self.resize_table(self._capacity * 2)

        # Calculating index
        index = self._hash_function(key) % self._capacity
        # Initializing variable for bucket
        hash_bucket = self._buckets[index]

        # Iterating through each key/value pair
        for pair in hash_bucket:
            # Checks if given key is found
            if pair.key == key:
                # Replaces value with new value
                pair.value = value
                return

        # Inserting key/value pair if given key does not exist
        hash_bucket.insert(key, value)
        # Incrementing table size
        self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Method used to change the capacity of the underlying hash table
        """
        # Checks if new capacity is less than 1
        if new_capacity < 1:
            return

        # Checks if new capacity is a prime number
        if not self._is_prime(new_capacity):
            # Change new capacity to next highest prime number
            new_capacity = self._next_prime(new_capacity)

        # Initializing variable for new resized hash table
        resized_table = HashMap(new_capacity, self._hash_function)

        # Checks if new capacity is 2
        if new_capacity == 2:
            # Set resized hash table capacity to 2
            resized_table._capacity = 2

        # Iterating through each element from original table
        for index in range(self._capacity):
            # Checks if length greater than 0
            if self._buckets[index].length() > 0:
                # Iterating through each key/value pair
                for pair in self._buckets[index]:
                    # Putting key/value pairs into new resized table
                    resized_table.put(pair.key, pair.value)

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
        # Initializing variable to track empty bucket count
        bucket_count = 0

        # Iterating through each element of table
        for index in range(self._capacity):
            # Checks if length is 0
            if self._buckets[index].length() == 0:
                # Increment bucket count
                bucket_count += 1

        return bucket_count

    def get(self, key: str):
        """
        Method used to return the value associated with the given key, otherwise None
        """
        # Calculating index
        index = self._hash_function(key) % self._capacity

        # Iterating through each key/value pair
        for pair in self._buckets[index]:
            # Checks if given key is found
            if pair.key == key:
                # Return the pairs value
                return pair.value

        return None

    def contains_key(self, key: str) -> bool:
        """
        Method used to return True if the given key is in the hashmap, otherwise False
        """
        # Calculating index
        index = self._hash_function(key) % self._capacity

        # Iterating through each key/value pair
        for pair in self._buckets[index]:
            # Checks if given key is found
            if pair.key == key:
                return True

        return False

    def remove(self, key: str) -> None:
        """
        Method used to remove the given key and its associated value from the hash map
        """
        # Calculating index
        index = self._hash_function(key) % self._capacity

        # Iterating through each key/value pair
        for pair in self._buckets[index]:
            # Checks if given key is found
            if pair.key == key:
                # Removing key
                self._buckets[index].remove(key)
                # Decrement table size
                self._size -= 1
                return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Method used to return a dynamic array where each index contains a key/value tuple pair
        stored in the hash map
        """
        # Initializing new DynamicArray to store key/value pairs
        key_value_array = DynamicArray()

        # Iterating through each element of table
        for index in range(self._capacity):
            # Checks if length is greater than 0
            if self._buckets[index].length() != 0:
                # Iterating through each key/value pair
                for pair in self._buckets[index]:
                    # Appending key/value pairs into new array
                    key_value_array.append((pair.key, pair.value))

        return key_value_array

    def clear(self) -> None:
        """
        Method used to clear the contents of the hash map
        """
        # Initializing hash map bucket to empty DynamicArray
        self._buckets = DynamicArray()

        # Iterating through each element of table
        for index in range(self._capacity):
            # Appending empty linked list to buckets
            self._buckets.append(LinkedList())
        # Updating table size to 0
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Method used to receive a DynamicArray and return a tuple containing the mode and its highest frequency
    """
    # Initializing variable for HashMap instance
    map = HashMap()

    # Iterating through each element of given array
    for value in range(da.length()):
        # Checks if value matches given key using get method
        if map.get(da[value]):
            # Update value using put method and increment map
            map.put(da[value], map.get(da[value]) + 1)
        else:
            # Add value to the map using put method
            map.put(da[value], 1)

    # Initializing variable to track the highest frequency count
    mode_frequency = 0
    # Initializing new DynamicArray to store mode values
    mode_array = DynamicArray()
    # Initializing variable to store key/value pairs into an array using helper method
    tuple_array = map.get_keys_and_values()

    # Iterating through each element of array
    for value in range(tuple_array.length()):
        # Checks if frequency count is less than value in array starting at first index
        if mode_frequency < tuple_array[value][1]:
            # Increment frequency count
            mode_frequency = tuple_array[value][1]

    # Iterating through each element of array
    for value in range(tuple_array.length()):
        # Initializing variable for index pointer starting at first index
        index_pointer = tuple_array[value][1]
        # Checks if value matches highest frequency value
        if index_pointer == mode_frequency:
            # Append values to mode array
            mode_array.append(tuple_array[value][0])

    return mode_array, mode_frequency


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
