import time

def hash_table_search(students_dict, target_reg_no):
    """
    Algorithm 1: Hash Table Lookup
    Time Complexity:
      Average: O(1)
      Worst: O(n)
    Space Complexity: O(1) auxiliary
    """
    start_time = time.perf_counter()
    operations = 1
    found = target_reg_no in students_dict
    result = students_dict.get(target_reg_no) if found else None
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    return {
        "algorithm": "Hash Table (Dictionary Index)",
        "found": found,
        "result": result,
        "operations": operations,
        "time_ms": round(elapsed_ms, 5),
        "complexity": {
            "best": "O(1)",
            "average": "O(1)",
            "worst": "O(n)"
        },
        "explanation": f"Hash table computed hash('{target_reg_no}') and reached bucket index in 1 atomic key-lookup step."
    }

def linear_search(students_list, target_reg_no):
    """
    Linear Search Comparison
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    start_time = time.perf_counter()
    operations = 0
    found = False
    result = None
    steps = []

    for idx, student in enumerate(students_list):
        operations += 1
        current_reg = student.get('reg_no')
        if idx < 5 or current_reg == target_reg_no: # record snapshot of steps
            steps.append(f"Step {operations}: Checked index {idx} -> {current_reg}")
        if current_reg == target_reg_no:
            found = True
            result = student
            break

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    return {
        "algorithm": "Linear Search",
        "found": found,
        "result": result,
        "operations": operations,
        "time_ms": round(elapsed_ms, 5),
        "steps_sample": steps,
        "complexity": {
            "best": "O(1)",
            "average": "O(n/2)",
            "worst": "O(n)"
        },
        "explanation": f"Scanned sequentially through {operations} student record(s) until match was found or list ended."
    }

def binary_search(sorted_students, target_reg_no):
    """
    Algorithm 2: Binary Search
    Precondition: List must be sorted by reg_no.
    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    start_time = time.perf_counter()
    low = 0
    high = len(sorted_students) - 1
    operations = 0
    found = False
    result = None
    trace = []

    while low <= high:
        operations += 1
        mid = (low + high) // 2
        mid_val = sorted_students[mid].get('reg_no')
        trace.append({
            "step": operations,
            "low": low,
            "mid": mid,
            "high": high,
            "checked_reg_no": mid_val
        })

        if mid_val == target_reg_no:
            found = True
            result = sorted_students[mid]
            break
        elif mid_val < target_reg_no:
            low = mid + 1
        else:
            high = mid - 1

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    return {
        "algorithm": "Binary Search",
        "found": found,
        "result": result,
        "operations": operations,
        "time_ms": round(elapsed_ms, 5),
        "trace": trace,
        "complexity": {
            "best": "O(1)",
            "average": "O(log n)",
            "worst": "O(log n)"
        },
        "explanation": f"Divided search interval in half each iteration; located target within {operations} comparison step(s)."
    }
