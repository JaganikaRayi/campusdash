import time

def greedy_timetable_schedule(subjects, faculties, rooms, periods_per_day=6, days=None):
    """
    Algorithm 4: Greedy Algorithm for Timetable Generation
    Makes the locally optimal choice at each step (earliest available period & room).
    Time Complexity: O(S * D * P) where S=subjects, D=days, P=periods
    Note: Greedy may get stuck or produce clashes when resources are heavily constrained!
    """
    if days is None:
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    start_time = time.perf_counter()
    timetable = []
    clashes = []
    faculty_busy = {} # (day, period, faculty_id) -> subject
    room_busy = {}    # (day, period, room) -> subject

    operations = 0
    assigned_count = 0

    # Required weekly periods per subject
    # e.g., {'CS301': 6, 'CS302': 6, 'CS303': 6, 'BS301': 6, 'ES301': 6, 'CS301_LAB': 6}
    subject_queue = []
    for sub in subjects:
        needed = sub.get('periods_needed', 5)
        for _ in range(needed):
            subject_queue.append(sub)

    for item in subject_queue:
        assigned = False
        sub_code = item['subject_code']
        fac_id = item['faculty_id']
        pref_room = item.get('room_no', rooms[0] if rooms else 'LH-301')

        # Greedy: scan earliest available day and period
        for day in days:
            if assigned:
                break
            for period in range(1, periods_per_day + 1):
                operations += 1
                key_fac = (day, period, fac_id)
                key_room = (day, period, pref_room)

                # Check if faculty or room is busy
                if key_fac not in faculty_busy and key_room not in room_busy:
                    # Greedily assign!
                    faculty_busy[key_fac] = sub_code
                    room_busy[key_room] = sub_code
                    timetable.append({
                        "day": day,
                        "period": period,
                        "subject_code": sub_code,
                        "subject_name": item.get('subject_name', sub_code),
                        "faculty_id": fac_id,
                        "faculty_name": item.get('faculty_name', fac_id),
                        "room_no": pref_room,
                        "strategy": "Greedy Earliest Slot"
                    })
                    assigned = True
                    assigned_count += 1
                    break

        if not assigned:
            clashes.append({
                "subject_code": sub_code,
                "reason": f"No clash-free slot found for {sub_code} under greedy choice."
            })

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    return {
        "algorithm": "Greedy Timetable Scheduler",
        "success": len(clashes) == 0,
        "assigned_periods": assigned_count,
        "total_requested": len(subject_queue),
        "clashes_count": len(clashes),
        "clashes": clashes,
        "timetable_entries": timetable,
        "operations": operations,
        "time_ms": round(elapsed_ms, 5),
        "complexity": {
            "time": "O(N * D * P)",
            "space": "O(D * P * (F + R))"
        },
        "explanation": "Greedy approach placed classes into the first available time slot. If faculty/rooms are tight, greedy choices may lead to unresolvable slots (clashes)."
    }
