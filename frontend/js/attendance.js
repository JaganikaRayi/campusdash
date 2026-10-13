// Attendance Page Controller

let attendanceChartInstance = null;

document.addEventListener('DOMContentLoaded', async () => {
  const user = Auth.checkAuth(true);
  if (!user) return;

  const regNo = user.role === 'student' ? (user.reg_no || '25221A0501') : '25221A0501';
  await loadAttendanceData(regNo);

  // Setup faculty marking actions if role is faculty or admin
  if (user.role === 'faculty' || user.role === 'admin') {
    const facultyBtn = document.getElementById('faculty-mark-btn');
    if (facultyBtn) facultyBtn.classList.remove('d-none');
    loadStudentsForFacultyMarking();
  }
});

async function loadAttendanceData(regNo) {
  try {
    const res = await API.get(`/attendance/${regNo}`);
    if (!res.success) return;

    // Render Summary
    const sum = res.summary;
    document.getElementById('att-summary-pct').innerText = `${sum.percentage}%`;
    document.getElementById('att-summary-total').innerText = sum.total_periods;
    document.getElementById('att-summary-present').innerText = sum.present_periods;
    document.getElementById('att-summary-absent').innerText = sum.absent_periods;

    // Status warning
    const alertBox = document.getElementById('att-warning-alert');
    if (alertBox) {
      if (sum.percentage < 75) {
        alertBox.classList.remove('d-none');
        alertBox.innerHTML = `<i class="fas fa-exclamation-triangle me-2"></i> Attendance is below 75% requirement! Immediate attention required to ensure examination eligibility.`;
      } else {
        alertBox.classList.add('d-none');
      }
    }

    // Render Subject-Wise Cards
    renderSubjectCards(res.subject_wise);

    // Render Logs Table
    renderHistoryTable(res.history);

    // Render Chart.js
    renderAttendanceChart(sum.present_periods, sum.absent_periods);

  } catch (err) {
    console.error('Failed to load attendance:', err);
  }
}

function renderSubjectCards(subjects) {
  const container = document.getElementById('subject-cards-container');
  if (!container) return;

  container.innerHTML = subjects.map(s => {
    const isGood = s.percentage >= 75;
    return `
      <div class="col-md-6 col-lg-4 mb-3">
        <div class="glass-panel p-3 h-100">
          <div class="d-flex justify-content-between align-items-start mb-2">
            <div>
              <span class="badge bg-secondary mb-1">${s.subject_code}</span>
              <h6 class="fw-bold text-white mb-0">${s.subject_name}</h6>
            </div>
            <span class="fs-5 fw-bold ${isGood ? 'text-success' : 'text-danger'}">${s.percentage}%</span>
          </div>
          <div class="progress my-2" style="height: 6px;">
            <div class="progress-bar ${isGood ? 'bg-success' : 'bg-danger'}" style="width: ${s.percentage}%;"></div>
          </div>
          <div class="d-flex justify-content-between text-muted small mt-2">
            <span>Present: <strong class="text-white">${s.present}</strong> / ${s.total}</span>
            <span>Absent: <strong class="text-danger">${s.absent}</strong></span>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

function renderHistoryTable(history) {
  const tbody = document.getElementById('attendance-history-body');
  if (!tbody) return;

  if (history.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" class="text-center text-muted py-3">No attendance records found.</td></tr>`;
    return;
  }

  tbody.innerHTML = history.map(h => `
    <tr>
      <td class="text-white"><i class="far fa-calendar-alt text-primary me-2"></i> ${h.date}</td>
      <td><span class="badge bg-dark border border-secondary text-info">Period ${h.period}</span></td>
      <td class="fw-semibold text-white">${h.subject_name} (${h.subject_code})</td>
      <td class="text-muted small">${h.faculty_name || 'Faculty'}</td>
      <td>
        <span class="badge ${h.status === 'Present' ? 'badge-present' : 'badge-absent'}">
          <i class="fas ${h.status === 'Present' ? 'fa-check' : 'fa-times'} me-1"></i> ${h.status}
        </span>
      </td>
    </tr>
  `).join('');
}

function renderAttendanceChart(present, absent) {
  const canvas = document.getElementById('attendanceDoughnutChart');
  if (!canvas) return;

  if (attendanceChartInstance) {
    attendanceChartInstance.destroy();
  }

  attendanceChartInstance = new Chart(canvas, {
    type: 'doughnut',
    data: {
      labels: ['Present Periods', 'Absent Periods'],
      datasets: [{
        data: [present || 1, absent || 0],
        backgroundColor: ['#10B981', '#EF4444'],
        borderWidth: 0,
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom',
          labels: { color: '#94A3B8', font: { family: 'Plus Jakarta Sans', size: 12 } }
        }
      },
      cutout: '70%'
    }
  });
}

async function loadStudentsForFacultyMarking() {
  const container = document.getElementById('faculty-student-marking-list');
  if (!container) return;

  try {
    const res = await API.get('/students?section=A');
    if (res.success) {
      container.innerHTML = res.students.slice(0, 15).map(s => `
        <div class="d-flex justify-content-between align-items-center py-2 border-bottom border-secondary border-opacity-25">
          <div>
            <div class="text-white fw-bold small">${s.name}</div>
            <div class="text-muted small">${s.reg_no}</div>
          </div>
          <div class="btn-group btn-group-sm" role="group">
            <input type="radio" class="btn-check" name="status-${s.reg_no}" id="p-${s.reg_no}" value="Present" checked>
            <label class="btn btn-outline-success" for="p-${s.reg_no}">P</label>

            <input type="radio" class="btn-check" name="status-${s.reg_no}" id="a-${s.reg_no}" value="Absent">
            <label class="btn btn-outline-danger" for="a-${s.reg_no}">A</label>
          </div>
        </div>
      `).join('');
    }
  } catch (e) {}
}

async function submitFacultyBatchAttendance(e) {
  e.preventDefault();
  const date = document.getElementById('mark-date').value;
  const period = document.getElementById('mark-period').value;
  const subject = document.getElementById('mark-subject').value;

  const list = [];
  document.querySelectorAll('#faculty-student-marking-list input[type="radio"]:checked').forEach(radio => {
    const reg = radio.name.replace('status-', '');
    list.push({ reg_no: reg, status: radio.value });
  });

  try {
    const res = await API.post('/attendance/batch', {
      subject_code: subject,
      date: date,
      period: parseInt(period),
      attendance_list: list
    });

    if (res.success) {
      showToast(res.message, 'success');
      const modalEl = document.getElementById('markAttendanceModal');
      const modal = bootstrap.Modal.getInstance(modalEl);
      if (modal) modal.hide();
      const user = Auth.getUser();
      loadAttendanceData(user.reg_no || '25221A0501');
    }
  } catch (e) {}
}
