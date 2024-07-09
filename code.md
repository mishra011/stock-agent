**

Here's a step-by-step explanation of the binary search algorithm and its implementation in Python:

1. **Initialization:** Set two pointers, `low` and `high`, to the start and end indices of the array, respectively.
2. **Calculation:** Calculate the midpoint index using the formula `(low + high) // 2`. This ensures that the search interval is always halved.
3. **Comparison:** Compare the value at the midpoint index with the target value. If they match, return the midpoint index as the result.
4. **Update:** Update the `low` and `high` pointers based on whether the target value is less than or greater than the midpoint value. This will narrow down the search interval for the next iteration.
5. **Repeat:** Repeat steps 2-4 until the search interval is empty (i.e., `low > high`) or the target value is found.

I hope this explanation helps you understand the binary search algorithm and its implementation in Python!