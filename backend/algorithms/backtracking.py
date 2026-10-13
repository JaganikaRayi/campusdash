import time

def backtracking_timetable_schedule(subjects, faculties, rooms, periods_per_day=6, days=None):
    """
    Algorithm 5: Backtracking Constraint Satisfaction Timetable Generator
    Tries valid slots recursively; if a conflict or dead-end is reached,
    it unwinds (backtracks) and tries alternative slots until a clash-free schedule is found.
    Time Complexity: O(M^N) in worst case (exponential branch & bound), highly efficient with pruning.
    Space Complexity: O(N) recursion stack.
    """
    if days is None:
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    start_time = time.perf_counter()
    metrics = {"recursive_calls": 0, "backtracks": 0}

    # Generate flat list of requirements
    requirements = []
    for sub in subjects:
        needed = sub.get('periods_needed', 5)
        for _ in range(needed):
            requirements.append(sub)

    # Generate all possible (day, period) slots
    all_slots = []
    for d in days:
        for p in range(1, periods_per_day + 1):
            all_slots.append((d, p))

    # Assigned state: slot_index -> {subject, room}
    timetable = {}
    faculty_slots = {} # faculty_id -> set of (day, period)
    room_slots = {}    # room_no -> set of (day, period)

    def is_safe(sub, slot, room):
        fac_id = sub['faculty_id']
        if slot in faculty_slots.get(fac_id, set()):
            return False
        if slot in room_slots.get(room, set()):
            return False
        return True

    def solve(req_index):
        metrics["recursive_calls"] += 1

        if req_index == len(requirements):
            return True # Successfully scheduled all required classes!

        current_sub = requirements[req_index]
        fac_id = current_sub['faculty_id']
        pref_room = current_sub.get('room_no', rooms[0] if rooms else 'LH-301')

        # Try slot choices
        for slot in all_slots:
            if slot in timetable:
                continue # Slot already occupied for this section

            for room in ([pref_room] + [r for r in rooms if r != pref_room]):
                if is_safe(current_sub, slot, room):
                    # Make assignment
                    timetable[slot] = {
                        "day": slot[0],
                        "period": slot[1],
                        "subject_code": current_sub['subject_code'],
                        "subject_name": current_sub.get('subject_name', current_sub['subject_code']),
                        "faculty_id": fac_id,
                        "faculty_name": current_sub.get('faculty_name', fac_id),
                        "room_no": room,
                        "strategy": "Backtracking Constraint Search"
                    }
                    if fac_id not in faculty_slots:
                        faculty_slots[fac_id] = set()
                    faculty_slots[fac_id].add(slot)

                    if room not in room_slots:
                        room_slots[room] = set()
                    room_slots[room].add(slot)

                    # Recurse
                    if solve(req_index + 1):
                        return True

                    # Backtrack! Undo assignment
                    del timetable[slot]
                    faculty_slots[fac_id].remove(slot)
                    room_slots[room].remove(slot)
                    metrics["backtracks"] += 1

        return False # No valid assignment at this branch

    success = solve(0)
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    timetable_list = sorted(list(timetable.values()), key=lambda x: (days.index(x['day']), x['period']))

    return {
        "algorithm": "Backtracking Constraint Satisfaction Timetable Generator",
        "success": success,
        "total_required": len(requirements),
        "scheduled_count": len(timetable_list),
        "recursive_calls": metrics["recursive_calls"],
        "backtracks": metrics["backtracks"],
        "time_ms": round(elapsed_ms, 5),
        "timetable_entries": timetable_list,
        "complexity": {
            "worst_time": "O(S^N) with constraint pruning",
            "space": "O(N) recursion stack"
        },
        "explanation": f"Constraint solver completed {metrics['recursive_calls']} state evaluations and {metrics['backtracks']} backtracks to produce an 100% clash-free timetable."
    }
