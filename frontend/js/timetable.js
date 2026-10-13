// Timetable Page Controller

const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const PERIOD_TIMES = [
  { period: 1, time: '09:00 - 09:50' },
  { period: 2, time: '09:50 - 10:40' },
  { period: 3, time: '10:50 - 11:40' },
  { period: 4, time: '11:40 - 12:30' },
  { period: 5, time: '01:30 - 02:20' },
  { period: 6, time: '02:20 - 03:10' }
];

document.addEventListener('DOMContentLoaded', async () => {
  const user = Auth.checkAuth(true);
  if (!user) return;

  const target = user.role === 'faculty' ? (user.reg_no || 'FAC01') : 'A';
  if (user.role === 'faculty') {
    await loadFacultyTimetable(target);
  } else {
    await loadSectionTimetable('A');
  }
});

async function loadSectionTimetable(section = 'A') {
  try {
    const res = await API.get(`/timetable/${section}`);
    if (res.success) {
      renderTimetableGrid(res.timetable);
    }
  } catch (e) {
    console.error(e);
  }
}

async function loadFacultyTimetable(facId) {
  try {
    const res = await API.get(`/timetable/faculty/${facId}`);
    if (res.success) {
      renderTimetableGrid(res.timetable);
    }
  } catch (e) {
    console.error(e);
  }
}

function renderTimetableGrid(entries) {
  const tbody = document.getElementById('timetable-grid-body');
  if (!tbody) return;

  // Build 2D lookup: matrix[day][period]
  const matrix = {};
  DAYS.forEach(d => { matrix[d] = {}; });

  entries.forEach(item => {
    if (matrix[item.day_of_week]) {
      matrix[item.day_of_week][item.period] = item;
    }
  });

  tbody.innerHTML = DAYS.map(day => `
    <tr>
      <td class="fw-bold text-white bg-dark bg-opacity-50 text-center" style="width: 120px;">
        ${day}
      </td>
      ${[1, 2, 3, 4, 5, 6].map(p => {
        const slot = matrix[day][p];
        if (!slot) {
          return `<td class="text-center text-muted small p-2"><span class="badge bg-secondary bg-opacity-25 text-muted">Free</span></td>`;
        }
        return `
          <td class="p-2">
            <div class="p-2 rounded border border-secondary border-opacity-50" style="background: rgba(30, 41, 59, 0.7);">
              <div class="fw-bold text-info small mb-1">${slot.subject_code}</div>
              <div class="text-white small fw-semibold text-truncate">${slot.subject_name || slot.subject_code}</div>
              <div class="d-flex justify-content-between align-items-center mt-2 pt-1 border-top border-secondary border-opacity-25">
                <span class="badge bg-primary bg-opacity-50 text-white" style="font-size: 0.7rem;">${slot.room_no}</span>
                <span class="text-muted" style="font-size: 0.72rem;">${slot.faculty_name || slot.faculty_id || ''}</span>
              </div>
            </div>
          </td>
        `;
      }).join('')}
    </tr>
  `).join('');
}

async function runTimetableADSGenerator(algorithm) {
  const resultContainer = document.getElementById('generator-result-box');
  if (resultContainer) {
    resultContainer.classList.remove('d-none');
    resultContainer.innerHTML = `<div class="text-center text-info py-4"><i class="fas fa-spinner fa-spin fa-2x mb-2"></i><p>Executing ADS ${algorithm.toUpperCase()} constraint satisfaction scheduler...</p></div>`;
  }

  try {
    const res = await API.post('/timetable/generate', { algorithm: algorithm });
    if (res.success && resultContainer) {
      const data = res.data;
      resultContainer.innerHTML = `
        <div class="alert alert-success bg-opacity-25 border-success mb-3">
          <div class="d-flex justify-content-between align-items-center">
            <strong class="text-white"><i class="fas fa-check-circle text-success me-2"></i> ${data.algorithm}</strong>
            <span class="badge bg-success">${data.time_ms} ms</span>
          </div>
          <p class="small text-light mb-0 mt-1">${data.explanation}</p>
        </div>
        <div class="row g-2 mb-3">
          <div class="col-4">
            <div class="metric-pill w-100 justify-content-between">
              <span class="text-muted">Assigned:</span> <strong class="text-white">${data.scheduled_count || data.assigned_periods}</strong>
            </div>
          </div>
          <div class="col-4">
            <div class="metric-pill w-100 justify-content-between">
              <span class="text-muted">Complexity:</span> <strong class="text-info">${data.complexity ? (data.complexity.time || data.complexity.worst_time) : 'O(N)'}</strong>
            </div>
          </div>
          <div class="col-4">
            <div class="metric-pill w-100 justify-content-between">
              <span class="text-muted">Backtracks:</span> <strong class="text-warning">${data.backtracks || 0}</strong>
            </div>
          </div>
        </div>
      `;

      // Update grid with newly generated timetable
      if (data.timetable_entries) {
        renderTimetableGrid(data.timetable_entries);
        showToast('Timetable updated with clash-free ADS schedule!', 'success');
      }
    }
  } catch (e) {
    if (resultContainer) {
      resultContainer.innerHTML = `<div class="alert alert-danger">Error running timetable generator.</div>`;
    }
  }
}
