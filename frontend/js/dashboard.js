// Dashboard Dynamic Logic

document.addEventListener('DOMContentLoaded', async () => {
  const user = Auth.checkAuth(true);
  if (!user) return;

  renderDashboardHeader(user);

  if (user.role === 'student') {
    await loadStudentDashboard(user);
  } else if (user.role === 'faculty') {
    await loadFacultyDashboard(user);
  } else {
    await loadAdminDashboard(user);
  }

  loadRecentNotifications();
});

function renderDashboardHeader(user) {
  const header = document.getElementById('dashboard-greeting');
  if (header) {
    const timeOfDay = new Date().getHours() < 12 ? 'Good Morning' : (new Date().getHours() < 17 ? 'Good Afternoon' : 'Good Evening');
    header.innerHTML = `
      <div class="d-flex flex-wrap justify-content-between align-items-center gap-3">
        <div>
          <h2 class="fw-bold text-white mb-1">${timeOfDay}, ${user.name} 👋</h2>
          <p class="text-muted mb-0">
            <span class="badge-role badge-${user.role} me-2">${user.role.toUpperCase()}</span>
            ${user.reg_no ? `<span class="text-light">ID: <strong>${user.reg_no}</strong></span>` : ''}
            ${user.profile && user.profile.branch ? ` • ${user.profile.branch} (Section ${user.profile.section})` : ''}
          </p>
        </div>
        <div class="d-flex gap-2">
          <a href="algorithms.html" class="btn btn-campus btn-sm">
            <i class="fas fa-microchip me-1"></i> ADS Visualizer
          </a>
        </div>
      </div>
    `;
  }
}

async function loadStudentDashboard(user) {
  const regNo = user.reg_no || '25221A0501';

  try {
    // 1. Fetch Attendance
    const attRes = await API.get(`/attendance/${regNo}`);
    if (attRes.success && attRes.summary) {
      const pct = attRes.summary.percentage;
      document.getElementById('stat-attendance').innerText = `${pct}%`;
      const attProgress = document.getElementById('stat-att-progress');
      if (attProgress) {
        attProgress.style.width = `${pct}%`;
        attProgress.className = `progress-bar ${pct >= 75 ? 'bg-success' : 'bg-danger'}`;
      }
      document.getElementById('att-subtext').innerText = `${attRes.summary.present_periods} of ${attRes.summary.total_periods} periods attended`;
    }

    // 2. Fetch Fees
    const feeRes = await API.get(`/fees/${regNo}`);
    if (feeRes.success && feeRes.fee_summary) {
      const f = feeRes.fee_summary;
      document.getElementById('stat-fee-total').innerText = `₹${f.total_amount.toLocaleString()}`;
      document.getElementById('stat-fee-paid').innerText = `₹${f.paid_amount.toLocaleString()}`;
      document.getElementById('stat-fee-bal').innerText = `₹${f.balance_amount.toLocaleString()}`;
      
      const balBadge = document.getElementById('fee-bal-badge');
      if (balBadge) {
        balBadge.innerText = f.balance_amount === 0 ? 'Fully Paid' : 'Payment Due';
        balBadge.className = `badge ${f.balance_amount === 0 ? 'bg-success' : 'bg-warning text-dark'}`;
      }
    }

    // 3. Fetch Results / SGPA
    const resData = await API.get(`/results/${regNo}`);
    if (resData.success) {
      document.getElementById('stat-sgpa').innerText = resData.sgpa || '9.0';
      document.getElementById('sgpa-subtext').innerText = `${resData.total_credits} credits earned`;
    }

    // 4. Fetch Today's Timetable
    const ttRes = await API.get(`/timetable/${regNo}`);
    renderTodayTimetable(ttRes.timetable || []);

  } catch (e) {
    console.error('Error loading student dashboard:', e);
  }
}

async function loadFacultyDashboard(user) {
  const facId = user.reg_no || 'FAC01';
  document.getElementById('student-stat-grid').classList.add('d-none');
  const facGrid = document.getElementById('faculty-stat-grid');
  if (facGrid) facGrid.classList.remove('d-none');

  try {
    const ttRes = await API.get(`/timetable/faculty/${facId}`);
    renderTodayTimetable(ttRes.timetable || []);
  } catch (e) {
    console.error(e);
  }
}

async function loadAdminDashboard(user) {
  document.getElementById('student-stat-grid').classList.add('d-none');
  const adminGrid = document.getElementById('admin-stat-grid');
  if (adminGrid) adminGrid.classList.remove('d-none');

  try {
    const studentsRes = await API.get('/students');
    const feeRep = await API.get('/reports/fees');

    if (studentsRes.success) {
      document.getElementById('admin-total-students').innerText = studentsRes.count;
    }
    if (feeRep.success && feeRep.stats) {
      document.getElementById('admin-fee-collected').innerText = `₹${(feeRep.stats.total_collected || 0).toLocaleString()}`;
      document.getElementById('admin-fee-pending').innerText = `₹${(feeRep.stats.total_outstanding || 0).toLocaleString()}`;
    }
  } catch (e) {
    console.error(e);
  }
}

function renderTodayTimetable(timetable) {
  const container = document.getElementById('today-timetable-container');
  if (!container) return;

  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const todayName = days[new Date().getDay()] || 'Monday';
  const displayDay = todayName === 'Sunday' ? 'Monday' : todayName;

  const todaySlots = timetable.filter(t => t.day_of_week === displayDay);

  if (todaySlots.length === 0) {
    container.innerHTML = `
      <div class="text-center text-muted py-4">
        <i class="fas fa-coffee fs-3 mb-2"></i>
        <p>No classes scheduled for ${displayDay}. Enjoy your break!</p>
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h6 class="fw-bold text-white mb-0"><i class="far fa-calendar-alt text-primary me-2"></i> Today's Schedule (${displayDay})</h6>
      <a href="timetable.html" class="small text-decoration-none text-primary">Full Week <i class="fas fa-chevron-right ms-1"></i></a>
    </div>
    <div class="table-responsive">
      <table class="table table-campus table-sm">
        <thead>
          <tr>
            <th>Period</th>
            <th>Subject</th>
            <th>Time</th>
            <th>Room</th>
            <th>Faculty</th>
          </tr>
        </thead>
        <tbody>
          ${todaySlots.map(s => `
            <tr>
              <td><span class="badge bg-secondary">P${s.period}</span></td>
              <td class="fw-semibold text-white">${s.subject_name || s.subject_code}</td>
              <td class="text-muted small">${s.start_time || '09:00'} - ${s.end_time || '09:50'}</td>
              <td><span class="badge bg-dark border border-secondary text-info">${s.room_no}</span></td>
              <td class="text-muted small">${s.faculty_name || s.faculty_id}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>
  `;
}

async function loadRecentNotifications() {
  const container = document.getElementById('recent-notifications-list');
  if (!container) return;

  try {
    const res = await API.get('/notifications');
    if (res.success && res.notifications) {
      const topNotifs = res.notifications.slice(0, 4);
      container.innerHTML = topNotifs.map(n => `
        <div class="p-3 mb-2 rounded border border-secondary border-opacity-25" style="background: rgba(255,255,255,0.02);">
          <div class="d-flex justify-content-between align-items-start mb-1">
            <h6 class="fw-bold text-white mb-0 small">${n.title}</h6>
            <span class="badge ${n.priority === 3 ? 'badge-urgent' : 'badge-student'}">${n.priority === 3 ? 'URGENT' : n.category}</span>
          </div>
          <p class="text-muted small mb-1">${n.message}</p>
          <div class="d-flex justify-content-between text-dim small">
            <span><i class="far fa-calendar me-1"></i> ${n.posted_date}</span>
            ${n.deadline ? `<span class="text-warning"><i class="far fa-clock me-1"></i> Due: ${n.deadline}</span>` : ''}
          </div>
        </div>
      `).join('');
    }
  } catch (e) {}
}
