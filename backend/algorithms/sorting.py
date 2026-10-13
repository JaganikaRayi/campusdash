import time

def merge_sort_students(students_list, sort_key="reg_no", reverse=False):
    """
    Algorithm 6: Merge Sort for Student Records
    Time Complexity: O(n log n) in all cases (Best, Average, Worst)
    Space Complexity: O(n) auxiliary
    Stable sorting algorithm ideal for student ranking and registration order.
    """
    start_time = time.perf_counter()
    metrics = {"comparisons": 0, "merges": 0}

    def _merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            metrics["comparisons"] += 1
            left_val = left[i].get(sort_key, 0)
            right_val = right[j].get(sort_key, 0)

            # Support numeric or string comparison
            if not reverse:
                condition = left_val <= right_val
            else:
                condition = left_val >= right_val

            if condition:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        metrics["merges"] += 1
        return result

    def _merge_sort(items):
        if len(items) <= 1:
            return items
        mid = len(items) // 2
        left = _merge_sort(items[:mid])
        right = _merge_sort(items[mid:])
        return _merge(left, right)

    sorted_result = _merge_sort(list(students_list))
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    return {
        "algorithm": "Merge Sort",
        "sort_key": sort_key,
        "reverse": reverse,
        "total_elements": len(sorted_result),
        "comparisons": metrics["comparisons"],
        "merges": metrics["merges"],
        "time_ms": round(elapsed_ms, 5),
        "sorted_data": sorted_result,
        "complexity": {
            "best": "O(n log n)",
            "average": "O(n log n)",
            "worst": "O(n log n)",
            "space": "O(n)"
        },
        "explanation": f"Sorted {len(sorted_result)} student records using recursive divide-and-conquer Merge Sort with {metrics['comparisons']} comparisons."
    }
