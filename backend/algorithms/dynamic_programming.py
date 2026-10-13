import time

DEFAULT_STUDY_TASKS = [
    {"id": 1, "task_name": "ADS: AVL Trees & Binary Heaps", "subject": "CS301", "hours": 3, "exam_weight": 25},
    {"id": 2, "task_name": "Python: Decorators & Iterators", "subject": "CS302", "hours": 2, "exam_weight": 18},
    {"id": 3, "task_name": "Java: Collections & Streams", "subject": "CS303", "hours": 4, "exam_weight": 30},
    {"id": 4, "task_name": "Discrete Math: Recurrence Relations", "subject": "BS301", "hours": 3, "exam_weight": 22},
    {"id": 5, "task_name": "Engineering Science: Thermodynamics", "subject": "ES301", "hours": 2, "exam_weight": 15},
    {"id": 6, "task_name": "ADS: Dynamic Programming & Knapsack", "subject": "CS301", "hours": 3, "exam_weight": 28},
    {"id": 7, "task_name": "Java: Exception Handling & Multithreading", "subject": "CS303", "hours": 2, "exam_weight": 16}
]

def optimize_study_plan_knapsack(tasks=None, total_available_hours=8):
    """
    Algorithm 9: Dynamic Programming (0/1 Knapsack Formulation)
    Problem: A student has limited study hours (W) before exams.
             Given a set of study modules each requiring (hours_i) and yielding (exam_weight_i),
             select the combination of topics that maximizes the total score without exceeding W.
    Time Complexity: O(N * W) where N=tasks count, W=available hours
    Space Complexity: O(N * W)
    """
    if tasks is None:
        tasks = DEFAULT_STUDY_TASKS

    start_time = time.perf_counter()
    n = len(tasks)
    w_cap = int(total_available_hours)

    # dp[i][w] = max value achievable considering first i tasks with w hours
    dp = [[0 for _ in range(w_cap + 1)] for _ in range(n + 1)]

    # Fill DP Table (Bottom-Up)
    for i in range(1, n + 1):
        item = tasks[i - 1]
        item_hours = int(item['hours'])
        item_weight = int(item['exam_weight'])

        for w in range(w_cap + 1):
            if item_hours <= w:
                dp[i][w] = max(
                    dp[i - 1][w],                         # Exclude item
                    dp[i - 1][w - item_hours] + item_weight # Include item
                )
            else:
                dp[i][w] = dp[i - 1][w]

    max_score = dp[n][w_cap]

    # Reconstruct selected tasks
    selected_tasks = []
    rem_w = w_cap
    for i in range(n, 0, -1):
        if dp[i][rem_w] != dp[i - 1][rem_w]:
            chosen = tasks[i - 1]
            selected_tasks.append(chosen)
            rem_w -= int(chosen['hours'])

    selected_tasks.reverse()
    total_hours_used = sum(t['hours'] for t in selected_tasks)
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    # Create compact table summary for visual rendering
    matrix_headers = [f"{h}h" for h in range(w_cap + 1)]
    matrix_rows = []
    for i in range(n + 1):
        label = "Base (0)" if i == 0 else tasks[i - 1]['task_name'][:18] + "..."
        matrix_rows.append({
            "task_label": label,
            "values": dp[i]
        })

    return {
        "algorithm": "Dynamic Programming (0/1 Knapsack Study Planner)",
        "available_hours": w_cap,
        "total_tasks_considered": n,
        "max_score": max_score,
        "total_hours_used": total_hours_used,
        "selected_tasks": selected_tasks,
        "dp_matrix": {
            "headers": matrix_headers,
            "rows": matrix_rows
        },
        "time_ms": round(elapsed_ms, 5),
        "complexity": {
            "time": f"O(N × W) = O({n} × {w_cap}) = {n * w_cap} operations",
            "space": f"O(N × W) = {n + 1} × {w_cap + 1} states"
        },
        "explanation": f"Optimal study plan selected {len(selected_tasks)} topics yielding maximum score of {max_score} in {total_hours_used}/{w_cap} available hours."
    }
