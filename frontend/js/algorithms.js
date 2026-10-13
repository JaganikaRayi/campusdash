// CampusDash - Advanced Data Structures and Algorithms Interactive Controller

document.addEventListener('DOMContentLoaded', () => {
  // Run default search benchmark on page load
  runSearchBenchmark('25221A0515');
});

// ==========================================
// 1 & 2. SEARCHING: Hash Table vs Binary Search vs Linear Search
// ==========================================
async function runSearchBenchmark(customTarget = null) {
  const target = customTarget || document.getElementById('search-reg-input').value.trim() || '25221A0515';
  const container = document.getElementById('search-benchmark-results');
  if (!container) return;

  container.innerHTML = `<div class="text-center py-4 text-info"><i class="fas fa-spinner fa-spin fa-2x mb-2"></i><p>Executing Hash Table, Binary Search, and Linear Search across dataset...</p></div>`;

  try {
    const res = await API.post('/algorithms/search', { target_reg_no: target });
    if (!res.success) return;

    const hash = res.hash_table;
    const bin = res.binary_search;
    const lin = res.linear_search;

    container.innerHTML = `
      <div class="row g-3 mb-4">
        <!-- Hash Table -->
        <div class="col-md-4">
          <div class="glass-panel p-3 h-100 border-primary">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <span class="badge bg-primary">Algorithm 1</span>
              <span class="badge bg-success bg-opacity-25 text-success">${hash.complexity.average}</span>
            </div>
            <h5 class="fw-bold text-white mb-1">${hash.algorithm}</h5>
            <div class="display-6 fw-bold text-info my-2">${hash.operations} <span class="fs-6 text-muted">op</span></div>
            <p class="small text-muted mb-2">Time: <strong class="text-white">${hash.time_ms} ms</strong></p>
            <p class="small text-light">${hash.explanation}</p>
          </div>
        </div>

        <!-- Binary Search -->
        <div class="col-md-4">
          <div class="glass-panel p-3 h-100 border-info">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <span class="badge bg-info text-dark">Algorithm 2</span>
              <span class="badge bg-info bg-opacity-25 text-info">${bin.complexity.average}</span>
            </div>
            <h5 class="fw-bold text-white mb-1">${bin.algorithm}</h5>
            <div class="display-6 fw-bold text-warning my-2">${bin.operations} <span class="fs-6 text-muted">steps</span></div>
            <p class="small text-muted mb-2">Time: <strong class="text-white">${bin.time_ms} ms</strong></p>
            <p class="small text-light">${bin.explanation}</p>
          </div>
        </div>

        <!-- Linear Search -->
        <div class="col-md-4">
          <div class="glass-panel p-3 h-100 border-secondary">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <span class="badge bg-secondary">Baseline</span>
              <span class="badge bg-danger bg-opacity-25 text-danger">${lin.complexity.worst}</span>
            </div>
            <h5 class="fw-bold text-white mb-1">${lin.algorithm}</h5>
            <div class="display-6 fw-bold text-danger my-2">${lin.operations} <span class="fs-6 text-muted">comparisons</span></div>
            <p class="small text-muted mb-2">Time: <strong class="text-white">${lin.time_ms} ms</strong></p>
            <p class="small text-light">${lin.explanation}</p>
          </div>
        </div>
      </div>

      <!-- Result Card -->
      <div class="p-3 rounded border border-secondary border-opacity-50" style="background: rgba(15, 23, 42, 0.8);">
        <h6 class="fw-bold text-white mb-2"><i class="fas fa-id-badge text-primary me-2"></i> Found Student Record:</h6>
        ${hash.result ? `
          <div class="row g-2 small">
            <div class="col-md-3"><span class="text-muted">Reg No:</span> <strong class="text-info">${hash.result.reg_no}</strong></div>
            <div class="col-md-3"><span class="text-muted">Name:</span> <strong class="text-white">${hash.result.name}</strong></div>
            <div class="col-md-3"><span class="text-muted">Branch / Sec:</span> <strong class="text-white">${hash.result.branch} - ${hash.result.section}</strong></div>
            <div class="col-md-3"><span class="text-muted">Attendance:</span> <strong class="text-success">${hash.result.attendance_pct}%</strong></div>
          </div>
        ` : `<div class="text-danger small">No student found matching '${target}'.</div>`}
      </div>

      <!-- Binary Search Step Trace -->
      ${bin.trace && bin.trace.length > 0 ? `
        <div class="mt-3">
          <h6 class="fw-bold text-white mb-2 small"><i class="fas fa-stream text-warning me-2"></i> Binary Search Divide-and-Conquer Trace:</h6>
          <div class="table-responsive">
            <table class="table table-sm table-campus mb-0">
              <thead>
                <tr>
                  <th>Step</th>
                  <th>Low Index</th>
                  <th>Mid Index</th>
                  <th>High Index</th>
                  <th>Checked Reg No</th>
                </tr>
              </thead>
              <tbody>
                ${bin.trace.map(t => `
                  <tr>
                    <td><span class="badge bg-secondary">#${t.step}</span></td>
                    <td class="text-muted">${t.low}</td>
                    <td class="fw-bold text-warning">${t.mid}</td>
                    <td class="text-muted">${t.high}</td>
                    <td class="text-info fw-mono">${t.checked_reg_no}</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      ` : ''}
    `;

  } catch (e) {
    console.error(e);
  }
}

// ==========================================
// 6. SORTING: Merge Sort
// ==========================================
async function runMergeSortBenchmark(key = 'attendance_pct', reverse = true) {
  const container = document.getElementById('sort-benchmark-results');
  if (!container) return;

  container.innerHTML = `<div class="text-center py-4 text-info"><i class="fas fa-spinner fa-spin fa-2x mb-2"></i><p>Executing Merge Sort O(n log n)...</p></div>`;

  try {
    const res = await API.post('/algorithms/sort', { sort_key: key, reverse: reverse });
    if (!res.success) return;

    container.innerHTML = `
      <div class="d-flex flex-wrap justify-content-between align-items-center mb-3">
        <div>
          <h5 class="fw-bold text-white mb-1">Merge Sort Execution Summary</h5>
          <span class="text-muted small">${res.explanation}</span>
        </div>
        <div class="d-flex gap-2">
          <span class="metric-pill"><span class="text-muted">Time:</span> <strong class="text-success">${res.time_ms} ms</strong></span>
          <span class="metric-pill"><span class="text-muted">Comparisons:</span> <strong class="text-warning">${res.comparisons}</strong></span>
          <span class="metric-pill"><span class="text-muted">Merges:</span> <strong class="text-info">${res.merges}</strong></span>
          <span class="metric-pill"><span class="text-muted">Complexity:</span> <strong class="text-primary">${res.complexity.average}</strong></span>
        </div>
      </div>

      <div class="table-responsive" style="max-height: 380px; overflow-y: auto;">
        <table class="table table-campus table-sm">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Reg No</th>
              <th>Name</th>
              <th>Branch & Sec</th>
              <th>${key === 'attendance_pct' ? 'Attendance %' : 'Reg No'}</th>
            </tr>
          </thead>
          <tbody>
            ${res.sorted_data.slice(0, 25).map((s, idx) => `
              <tr>
                <td><span class="badge ${idx < 3 ? 'bg-warning text-dark' : 'bg-secondary'}">#${idx + 1}</span></td>
                <td class="fw-bold text-info font-monospace">${s.reg_no}</td>
                <td class="text-white">${s.name}</td>
                <td class="text-muted">${s.branch} - ${s.section}</td>
                <td class="fw-bold ${s.attendance_pct >= 75 ? 'text-success' : 'text-danger'}">${s.attendance_pct}%</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    `;
  } catch (e) {
    console.error(e);
  }
}

// ==========================================
// 3. GRAPH ALGORITHMS: BFS & Dijkstra
// ==========================================
async function runGraphAlgorithm(type = 'dijkstra') {
  const start = document.getElementById('graph-start-node').value;
  const target = document.getElementById('graph-target-node').value;
  const container = document.getElementById('graph-results-box');
  if (!container) return;

  container.innerHTML = `<div class="text-center py-4 text-info"><i class="fas fa-spinner fa-spin fa-2x mb-2"></i><p>Executing Graph ${type.toUpperCase()} Algorithm...</p></div>`;

  try {
    const res = await API.post('/algorithms/graph', {
      algorithm: type,
      start_node: start,
      target_node: target
    });

    if (!res.success) return;

    if (type === 'dijkstra') {
      container.innerHTML = `
        <div class="alert alert-success bg-opacity-25 border-success mb-3">
          <div class="d-flex justify-content-between align-items-center">
            <strong class="text-white"><i class="fas fa-route text-success me-2"></i> Shortest Navigation Route Found</strong>
            <span class="badge bg-success">${res.shortest_distance_meters} meters</span>
          </div>
          <p class="small text-light mb-0 mt-1">${res.explanation}</p>
        </div>

        <div class="mb-3">
          <h6 class="fw-bold text-white small mb-2"><i class="fas fa-map-marker-alt text-danger me-2"></i> Step-by-Step Walking Navigation:</h6>
          <div class="d-flex flex-column gap-2">
            ${res.path_details.map(p => `
              <div class="p-2 rounded border border-secondary border-opacity-25 d-flex justify-content-between align-items-center" style="background: rgba(255,255,255,0.02);">
                <div class="d-flex align-items-center gap-2">
                  <span class="badge bg-primary">Step ${p.step}</span>
                  <span class="text-white fw-semibold">${p.location_name}</span>
                </div>
                <div class="text-end small">
                  ${p.leg_distance_meters > 0 ? `<span class="text-warning me-2">+${p.leg_distance_meters} m</span>` : ''}
                  <span class="text-info">Total: ${p.total_distance_meters} m</span>
                </div>
              </div>
            `).join('')}
          </div>
        </div>

        <div class="metric-pill w-100 justify-content-between">
          <span class="text-muted">Algorithm Complexity:</span> <strong class="text-info">${res.complexity.time}</strong>
          <span class="text-muted">Execution Time:</span> <strong class="text-success">${res.time_ms} ms</strong>
        </div>
      `;
    } else {
      // BFS Traversal
      container.innerHTML = `
        <div class="alert alert-info bg-opacity-25 border-info mb-3">
          <strong class="text-white"><i class="fas fa-sitemap text-info me-2"></i> Breadth-First Search (BFS) Level Exploration</strong>
          <p class="small text-light mb-0 mt-1">${res.explanation}</p>
        </div>

        <div class="mb-3">
          <h6 class="fw-bold text-white small mb-2">Explored Campus Layers (Breadth Order):</h6>
          ${Object.keys(res.levels).map(lvl => `
            <div class="p-2 mb-2 rounded border border-secondary border-opacity-25" style="background: rgba(255,255,255,0.03);">
              <span class="badge bg-secondary mb-1">Layer ${lvl} (Hop Distance: ${lvl})</span>
              <div class="text-white small">${res.levels[lvl].join('  ➡️  ')}</div>
            </div>
          `).join('')}
        </div>

        <div class="metric-pill w-100 justify-content-between">
          <span class="text-muted">Algorithm Complexity:</span> <strong class="text-info">${res.complexity.time}</strong>
          <span class="text-muted">Execution Time:</span> <strong class="text-success">${res.time_ms} ms</strong>
        </div>
      `;
    }
  } catch (e) {
    console.error(e);
  }
}

// ==========================================
// 4 & 5. TIMETABLE: Greedy vs Backtracking
// ==========================================
async function compareTimetableAlgorithms() {
  const container = document.getElementById('timetable-compare-results');
  if (!container) return;

  container.innerHTML = `<div class="text-center py-4 text-info"><i class="fas fa-spinner fa-spin fa-2x mb-2"></i><p>Running side-by-side comparison of Greedy vs Backtracking Timetable Algorithms...</p></div>`;

  try {
    const [greedyRes, backtrackRes] = await Promise.all([
      API.post('/algorithms/timetable', { algorithm: 'greedy' }),
      API.post('/algorithms/timetable', { algorithm: 'backtracking' })
    ]);

    container.innerHTML = `
      <div class="row g-3">
        <!-- Greedy Result -->
        <div class="col-md-6">
          <div class="glass-panel p-3 h-100 border-warning">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <span class="badge bg-warning text-dark">Algorithm 4: Greedy</span>
              <span class="badge ${greedyRes.clashes_count > 0 ? 'bg-danger' : 'bg-success'}">${greedyRes.clashes_count} Clashes</span>
            </div>
            <h6 class="fw-bold text-white mb-1">${greedyRes.algorithm}</h6>
            <p class="small text-muted mb-2">Assigned: <strong class="text-white">${greedyRes.assigned_periods} / ${greedyRes.total_requested}</strong> slots</p>
            <p class="small text-light">${greedyRes.explanation}</p>
            <div class="metric-pill w-100 justify-content-between mt-2">
              <span class="text-muted">Operations:</span> <strong class="text-warning">${greedyRes.operations}</strong>
              <span class="text-muted">Time:</span> <strong class="text-white">${greedyRes.time_ms} ms</strong>
            </div>
          </div>
        </div>

        <!-- Backtracking Result -->
        <div class="col-md-6">
          <div class="glass-panel p-3 h-100 border-success">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <span class="badge bg-success">Algorithm 5: Backtracking</span>
              <span class="badge bg-success">0 Clashes (Clash-Free)</span>
            </div>
            <h6 class="fw-bold text-white mb-1">${backtrackRes.algorithm}</h6>
            <p class="small text-muted mb-2">Assigned: <strong class="text-white">${backtrackRes.scheduled_count} / ${backtrackRes.total_required}</strong> slots</p>
            <p class="small text-light">${backtrackRes.explanation}</p>
            <div class="metric-pill w-100 justify-content-between mt-2">
              <span class="text-muted">Backtracks:</span> <strong class="text-warning">${backtrackRes.backtracks}</strong>
              <span class="text-muted">Time:</span> <strong class="text-white">${backtrackRes.time_ms} ms</strong>
            </div>
          </div>
        </div>
      </div>
    `;
  } catch (e) {
    console.error(e);
  }
}

// ==========================================
// 7 & 8. QUEUES: FIFO vs Priority Queue
// ==========================================
async function runQueueComparison() {
  const container = document.getElementById('queue-compare-results');
  if (!container) return;

  container.innerHTML = `<div class="text-center py-4 text-info"><i class="fas fa-spinner fa-spin fa-2x mb-2"></i><p>Executing Queue Comparison...</p></div>`;

  try {
    const res = await API.post('/algorithms/queues', {});
    if (!res.success) return;

    container.innerHTML = `
      <div class="row g-3">
        <!-- FIFO Queue -->
        <div class="col-md-6">
          <div class="glass-panel p-3 h-100">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <span class="badge bg-secondary">Algorithm 7: FIFO Queue</span>
              <span class="badge bg-secondary">Arrival Order</span>
            </div>
            <h6 class="fw-bold text-white mb-2">First-In-First-Out Order (Arrival Time)</h6>
            <div class="d-flex flex-column gap-2">
              ${res.fifo_order.map((item, idx) => `
                <div class="p-2 rounded border border-secondary border-opacity-25 d-flex justify-content-between align-items-center small" style="background: rgba(255,255,255,0.02);">
                  <div>
                    <span class="badge bg-dark border me-1">#${idx + 1}</span>
                    <strong class="text-white">${item.student_name || item.student_reg_no}</strong>
                    <div class="text-muted" style="font-size:0.75rem;">${item.reason}</div>
                  </div>
                  <span class="badge ${item.priority === 3 ? 'bg-danger' : (item.priority === 2 ? 'bg-warning text-dark' : 'bg-secondary')}">Prio ${item.priority}</span>
                </div>
              `).join('')}
            </div>
          </div>
        </div>

        <!-- Priority Queue Heap -->
        <div class="col-md-6">
          <div class="glass-panel p-3 h-100 border-primary">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <span class="badge bg-primary">Algorithm 8: Priority Queue</span>
              <span class="badge bg-success">Max-Heap</span>
            </div>
            <h6 class="fw-bold text-white mb-2">Binary Heap Priority Order (Urgency First)</h6>
            <div class="d-flex flex-column gap-2">
              ${res.priority_queue_order.map((entry, idx) => {
                const item = entry.item;
                return `
                  <div class="p-2 rounded border border-primary border-opacity-25 d-flex justify-content-between align-items-center small" style="background: rgba(79, 70, 229, 0.05);">
                    <div>
                      <span class="badge bg-primary me-1">#${idx + 1}</span>
                      <strong class="text-white">${item.student_name || item.student_reg_no}</strong>
                      <div class="text-muted" style="font-size:0.75rem;">${item.reason}</div>
                    </div>
                    <span class="badge ${entry.priority === 3 ? 'badge-urgent' : (entry.priority === 2 ? 'bg-warning text-dark' : 'bg-secondary')}">
                      ${entry.priority === 3 ? 'URGENT (Medical)' : (entry.priority === 2 ? 'HIGH (Sports)' : 'NORMAL')}
                    </span>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        </div>
      </div>
    `;
  } catch (e) {
    console.error(e);
  }
}

// ==========================================
// 9. DYNAMIC PROGRAMMING: Study Task Knapsack
// ==========================================
async function runKnapsackPlanner() {
  const hours = parseInt(document.getElementById('knapsack-hours-input').value) || 8;
  const container = document.getElementById('knapsack-results-box');
  if (!container) return;

  container.innerHTML = `<div class="text-center py-4 text-info"><i class="fas fa-spinner fa-spin fa-2x mb-2"></i><p>Computing Dynamic Programming Matrix...</p></div>`;

  try {
    const res = await API.post('/algorithms/knapsack', { available_hours: hours });
    if (!res.success) return;

    container.innerHTML = `
      <div class="alert alert-success bg-opacity-25 border-success mb-3">
        <div class="d-flex justify-content-between align-items-center">
          <strong class="text-white"><i class="fas fa-brain text-success me-2"></i> ${res.algorithm}</strong>
          <span class="badge bg-success fs-6">Max Exam Score: ${res.max_score} pts</span>
        </div>
        <p class="small text-light mb-0 mt-1">${res.explanation}</p>
      </div>

      <div class="row g-3 mb-3">
        <div class="col-md-6">
          <h6 class="fw-bold text-white small mb-2"><i class="fas fa-check-square text-success me-2"></i> Selected Optimal Study Modules:</h6>
          <div class="d-flex flex-column gap-2">
            ${res.selected_tasks.map(t => `
              <div class="p-2 rounded border border-success border-opacity-50 d-flex justify-content-between align-items-center small" style="background: rgba(16, 185, 129, 0.08);">
                <div>
                  <span class="badge bg-dark text-info me-1">${t.subject}</span>
                  <strong class="text-white">${t.task_name}</strong>
                </div>
                <div class="text-end">
                  <span class="badge bg-secondary me-1">${t.hours} hrs</span>
                  <span class="badge bg-success">+${t.exam_weight} pts</span>
                </div>
              </div>
            `).join('')}
          </div>
          <div class="mt-2 text-muted small">
            Total Study Hours Used: <strong class="text-white">${res.total_hours_used} / ${res.available_hours} hrs</strong>
          </div>
        </div>

        <div class="col-md-6">
          <h6 class="fw-bold text-white small mb-2"><i class="fas fa-table text-primary me-2"></i> DP State Matrix Snapshot [Item x Hours]:</h6>
          <div class="table-responsive" style="max-height: 240px; overflow-y: auto;">
            <table class="table table-sm table-campus mb-0" style="font-size: 0.75rem;">
              <thead>
                <tr>
                  <th>Task</th>
                  ${res.dp_matrix.headers.map(h => `<th>${h}</th>`).join('')}
                </tr>
              </thead>
              <tbody>
                ${res.dp_matrix.rows.map(r => `
                  <tr>
                    <td class="text-nowrap text-white fw-semibold">${r.task_label}</td>
                    ${r.values.map((v, i) => `<td class="${v === res.max_score && i === res.available_hours ? 'bg-success text-white fw-bold' : 'text-muted'}">${v}</td>`).join('')}
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="metric-pill w-100 justify-content-between">
        <span class="text-muted">Complexity:</span> <strong class="text-info">${res.complexity.time}</strong>
        <span class="text-muted">Storage:</span> <strong class="text-light">${res.complexity.space}</strong>
        <span class="text-muted">Compute Time:</span> <strong class="text-success">${res.time_ms} ms</strong>
      </div>
    `;
  } catch (e) {
    console.error(e);
  }
}
