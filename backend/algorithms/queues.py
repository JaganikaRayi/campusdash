from collections import deque
import heapq
import time

class FIFOQueue:
    """
    Algorithm 7: First-In-First-Out (FIFO) Queue
    Used for processing leave applications and student requests in chronological arrival order.
    Time Complexity:
      Enqueue: O(1)
      Dequeue: O(1)
      Peek: O(1)
    Space Complexity: O(n)
    """
    def __init__(self):
        self._queue = deque()

    def enqueue(self, item):
        self._queue.append(item)

    def dequeue(self):
        if not self._queue:
            return None
        return self._queue.popleft()

    def peek(self):
        if not self._queue:
            return None
        return self._queue[0]

    def size(self):
        return len(self._queue)

    def to_list(self):
        return list(self._queue)

class PriorityQueueHeap:
    """
    Algorithm 8: Priority Queue using Binary Heap
    Used for prioritizing urgent leave requests (Medical > Academic > Personal)
    and critical broadcast notifications.
    Time Complexity:
      Push (Insert): O(log n)
      Pop (Extract Max Priority): O(log n)
      Peek: O(1)
    Space Complexity: O(n)
    """
    def __init__(self):
        # We store tuples: (-priority, entry_counter, item) to simulate Max-Heap with heapq
        self._heap = []
        self._counter = 0

    def push(self, item, priority):
        # Invert priority so that higher numerical priority comes first
        heapq.heappush(self._heap, (-priority, self._counter, item))
        self._counter += 1

    def pop(self):
        if not self._heap:
            return None
        neg_prio, _, item = heapq.heappop(self._heap)
        return {"priority": -neg_prio, "item": item}

    def peek(self):
        if not self._heap:
            return None
        neg_prio, _, item = self._heap[0]
        return {"priority": -neg_prio, "item": item}

    def size(self):
        return len(self._heap)

    def to_sorted_list(self):
        # Return items in priority order without emptying the heap
        copy_heap = list(self._heap)
        result = []
        while copy_heap:
            neg_prio, _, item = heapq.heappop(copy_heap)
            result.append({"priority": -neg_prio, "item": item})
        return result

def compare_queue_order(items_with_priority):
    """
    Simulates FIFO vs Priority Queue order for demo comparison.
    items_with_priority: list of dicts with 'id', 'title', 'priority', 'arrival_time'
    """
    start_time = time.perf_counter()

    # FIFO Order
    fifo = FIFOQueue()
    for item in items_with_priority:
        fifo.enqueue(item)
    fifo_order = fifo.to_list()

    # Priority Queue Order
    pq = PriorityQueueHeap()
    for item in items_with_priority:
        pq.push(item, item.get('priority', 1))
    pq_order = pq.to_sorted_list()

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    return {
        "algorithm": "Queue (FIFO) vs Priority Queue (Binary Heap)",
        "input_count": len(items_with_priority),
        "fifo_order": fifo_order,
        "priority_queue_order": pq_order,
        "time_ms": round(elapsed_ms, 5),
        "complexity": {
            "fifo": {"enqueue": "O(1)", "dequeue": "O(1)"},
            "priority_queue": {"insert": "O(log n)", "extract_max": "O(log n)", "peek": "O(1)"}
        },
        "explanation": "FIFO processes tasks purely by arrival timestamp; Priority Queue reorganizes processing so emergency/critical tasks are served first."
    }
