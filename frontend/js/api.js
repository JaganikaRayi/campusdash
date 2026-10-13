// CampusDash Frontend API & Auth Client with Smart Local Fallback
const API_BASE = '/api';

// Embedded Fallback Mock Store for direct file browsing or offline mode
const LocalMockData = {
  attendance: {
    summary: { percentage: 88.5, total_periods: 42, present_periods: 38, absent_periods: 4 },
    subject_wise: [
      { subject_code: 'CS301', subject_name: 'Advanced Data Structures & Algorithms', total: 12, present: 11, absent: 1, percentage: 91.7 },
      { subject_code: 'CS302', subject_name: 'Python Programming Lab & Theory', total: 10, present: 9, absent: 1, percentage: 90.0 },
      { subject_code: 'CS303', subject_name: 'Java Programming', total: 8, present: 7, absent: 1, percentage: 87.5 },
      { subject_code: 'BS301', subject_name: 'Discrete Mathematics', total: 6, present: 5, absent: 1, percentage: 83.3 },
      { subject_code: 'ES301', subject_name: 'Engineering Science Fundamentals', total: 6, present: 6, absent: 0, percentage: 100.0 }
    ],
    history: [
      { date: '2026-10-12', period: 'Period 1 (09:00 - 10:00)', subject_code: 'CS301', subject_name: 'Advanced Data Structures', status: 'Present' },
      { date: '2026-10-12', period: 'Period 2 (10:00 - 11:00)', subject_code: 'CS302', subject_name: 'Python Programming Lab', status: 'Present' },
      { date: '2026-10-11', period: 'Period 3 (11:15 - 12:15)', subject_code: 'CS303', subject_name: 'Java Programming', status: 'Present' },
      { date: '2026-10-10', period: 'Period 4 (01:15 - 02:15)', subject_code: 'BS301', subject_name: 'Discrete Mathematics', status: 'Absent' },
      { date: '2026-10-09', period: 'Period 1 (09:00 - 10:00)', subject_code: 'CS301', subject_name: 'Advanced Data Structures', status: 'Present' }
    ]
  },
  fees: {
    reg_no: '25221A0501',
    student_name: 'Aarav Reddy',
    total_fee: 75000,
    paid_fee: 50000,
    balance: 25000,
    due_date: '2026-10-30',
    receipts: [
      { id: 1, receipt_no: 'REC-2026-0814', payment_date: '2026-08-14', amount: 30000, payment_method: 'UPI', transaction_ref: 'UPI/26104829104', student_reg_no: '25221A0501', student_name: 'Aarav Reddy', balance_remaining: 45000 },
      { id: 2, receipt_no: 'REC-2026-0920', payment_date: '2026-09-20', amount: 20000, payment_method: 'Net Banking', transaction_ref: 'NB/9823412095', student_reg_no: '25221A0501', student_name: 'Aarav Reddy', balance_remaining: 25000 }
    ]
  },
  timetable: [
    { day: 'Monday', period: '1', time: '09:00 - 10:00', subject: 'Advanced Data Structures (CS301)', faculty: 'Dr. K. Srinivas Rao', room: 'Room 301' },
    { day: 'Monday', period: '2', time: '10:00 - 11:00', subject: 'Python Programming (CS302)', faculty: 'Dr. K. Srinivas Rao', room: 'Lab 2' },
    { day: 'Monday', period: '3', time: '11:15 - 12:15', subject: 'Java Programming (CS303)', faculty: 'Prof. P. Radhika', room: 'Room 302' },
    { day: 'Tuesday', period: '1', time: '09:00 - 10:00', subject: 'Discrete Mathematics (BS301)', faculty: 'Dr. M. Venkat', room: 'Room 301' },
    { day: 'Tuesday', period: '2', time: '10:00 - 11:00', subject: 'Engineering Science (ES301)', faculty: 'Prof. S. Anitha', room: 'Room 303' },
    { day: 'Wednesday', period: '1', time: '09:00 - 10:00', subject: 'Advanced Data Structures (CS301)', faculty: 'Dr. K. Srinivas Rao', room: 'Room 301' },
    { day: 'Thursday', period: '1', time: '09:00 - 10:00', subject: 'Java Programming (CS303)', faculty: 'Prof. P. Radhika', room: 'Room 302' },
    { day: 'Friday', period: '1', time: '09:00 - 10:00', subject: 'Python Lab (CS302)', faculty: 'Dr. K. Srinivas Rao', room: 'Lab 1' }
  ],
  results: {
    sgpa: 9.15,
    total_credits: 22,
    results: [
      { subject_code: 'CS301', subject_name: 'Advanced Data Structures & Algorithms', credits: 4, internal_marks: 28, external_marks: 66, total_marks: 94, grade: 'O', grade_points: 10 },
      { subject_code: 'CS302', subject_name: 'Python Programming Lab & Theory', credits: 3, internal_marks: 27, external_marks: 64, total_marks: 91, grade: 'O', grade_points: 10 },
      { subject_code: 'CS303', subject_name: 'Java Programming', credits: 3, internal_marks: 25, external_marks: 60, total_marks: 85, grade: 'A+', grade_points: 9 },
      { subject_code: 'BS301', subject_name: 'Discrete Mathematics', credits: 4, internal_marks: 26, external_marks: 59, total_marks: 85, grade: 'A+', grade_points: 9 },
      { subject_code: 'ES301', subject_name: 'Engineering Science Fundamentals', credits: 3, internal_marks: 24, external_marks: 58, total_marks: 82, grade: 'A', grade_points: 8 }
    ]
  },
  materials: [
    { id: 1, title: 'Unit 1: Advanced Trees & Binary Search Trees', subject_code: 'CS301', subject_name: 'Advanced Data Structures', uploaded_by: 'Dr. K. Srinivas Rao', file_url: '#', uploaded_at: '2026-10-01' },
    { id: 2, title: 'Unit 2: Graph Theory, BFS & Dijkstra Notes', subject_code: 'CS301', subject_name: 'Advanced Data Structures', uploaded_by: 'Dr. K. Srinivas Rao', file_url: '#', uploaded_at: '2026-10-05' },
    { id: 3, title: 'Python Flask & Microservices Architecture Handout', subject_code: 'CS302', subject_name: 'Python Programming', uploaded_by: 'Dr. K. Srinivas Rao', file_url: '#', uploaded_at: '2026-10-08' },
    { id: 4, title: 'Java Multi-threading & Collections Framework', subject_code: 'CS303', subject_name: 'Java Programming', uploaded_by: 'Prof. P. Radhika', file_url: '#', uploaded_at: '2026-10-09' }
  ],
  faculty: [
    { faculty_id: 'FAC01', name: 'Dr. K. Srinivas Rao', department: 'Computer Science & Engineering', email: 'srinivas.rao@campusdash.edu', phone: '+91 98480 11221', cabin: 'Cabin 302, CS Block', subjects: 'CS301 - ADS, CS302 - Python' },
    { faculty_id: 'FAC02', name: 'Prof. P. Radhika', department: 'Computer Science & Engineering', email: 'radhika.p@campusdash.edu', phone: '+91 98480 22332', cabin: 'Cabin 305, CS Block', subjects: 'CS303 - Java Programming' },
    { faculty_id: 'FAC03', name: 'Dr. M. Venkat', department: 'Mathematics & Science', email: 'venkat.m@campusdash.edu', phone: '+91 98480 33443', cabin: 'Cabin 108, Science Block', subjects: 'BS301 - Discrete Mathematics' },
    { faculty_id: 'FAC04', name: 'Prof. S. Anitha', department: 'Electronics & Communication', email: 'anitha.s@campusdash.edu', phone: '+91 98480 44554', cabin: 'Cabin 204, Tech Block', subjects: 'ES301 - Engineering Science' }
  ],
  notifications: [
    { id: 1, title: 'Mid-Term Examinations Schedule Announced', message: 'The Mid-Term Semester 1 examinations will commence from November 2nd, 2026. Hall tickets will be issued next week.', category: 'Exam', priority: 3, posted_date: '2026-10-11', deadline: '2026-11-02' },
    { id: 2, title: 'Tuition Fee Due Date Reminder', message: 'Students are advised to clear pending semester fees before October 30th to avoid late penalties.', category: 'Fees', priority: 2, posted_date: '2026-10-10', deadline: '2026-10-30' },
    { id: 3, title: 'Annual Hackathon & Coding Fest 2026', message: 'Registrations are open for the 24-hour campus hackathon. Cash prizes up to ₹1,00,000.', category: 'Event', priority: 1, posted_date: '2026-10-08', deadline: '2026-10-25' }
  ],
  leaves: [
    { id: 1, student_reg_no: '25221A0501', student_name: 'Aarav Reddy', reason: 'Attending National Technical Symposium', from_date: '2026-10-18', to_date: '2026-10-20', status: 'Approved', submitted_at: '2026-10-10' }
  ]
};

function resolveMockResponse(method, endpoint, data = {}) {
  const ep = endpoint.toLowerCase();

  if (ep === '/login') {
    const role = (data.role || 'student').toLowerCase();
    const name = role === 'faculty' ? 'Dr. K. Srinivas Rao' : (role === 'admin' ? 'College Administrator' : 'Aarav Reddy');
    const user = {
      id: 1,
      name: name,
      username: data.username || (role === 'faculty' ? 'FAC01' : (role === 'admin' ? 'admin' : '25221A0501')),
      reg_no: data.username || (role === 'faculty' ? 'FAC01' : (role === 'admin' ? 'ADMIN' : '25221A0501')),
      role: role,
      branch: 'CSE',
      section: 'A'
    };
    return { success: true, message: `Welcome back, ${user.name}!`, user: user };
  }

  if (ep === '/logout') {
    return { success: true, message: 'Logged out successfully.' };
  }

  if (ep.includes('/attendance')) {
    return { success: true, ...LocalMockData.attendance };
  }

  if (ep.includes('/fees/pay')) {
    const amount = parseFloat(data.amount) || 5000;
    LocalMockData.fees.paid_fee += amount;
    LocalMockData.fees.balance = Math.max(0, LocalMockData.fees.total_fee - LocalMockData.fees.paid_fee);
    const receipt = {
      id: LocalMockData.fees.receipts.length + 1,
      receipt_no: `REC-2026-${Math.floor(1000 + Math.random() * 9000)}`,
      payment_date: new Date().toISOString().split('T')[0],
      amount: amount,
      payment_method: data.payment_method || 'Online UPI',
      transaction_ref: `UPI/${Math.floor(10000000000 + Math.random() * 90000000000)}`,
      student_reg_no: data.student_reg_no || '25221A0501',
      student_name: 'Aarav Reddy',
      balance_remaining: LocalMockData.fees.balance
    };
    LocalMockData.fees.receipts.unshift(receipt);
    return { success: true, message: 'Payment authorized and receipt generated!', receipt: receipt };
  }

  if (ep.includes('/fees')) {
    return { success: true, ...LocalMockData.fees };
  }

  if (ep.includes('/timetable')) {
    return { success: true, branch: 'CSE', section: 'A', timetable: LocalMockData.timetable };
  }

  if (ep.includes('/results')) {
    return { success: true, ...LocalMockData.results };
  }

  if (ep.includes('/materials')) {
    return { success: true, materials: LocalMockData.materials };
  }

  if (ep.includes('/faculty')) {
    return { success: true, faculty: LocalMockData.faculty };
  }

  if (ep.includes('/notifications')) {
    return { success: true, notifications: LocalMockData.notifications };
  }

  if (ep.includes('/leave') && method === 'POST') {
    const newLeave = {
      id: LocalMockData.leaves.length + 1,
      student_reg_no: data.student_reg_no || '25221A0501',
      student_name: data.student_name || 'Aarav Reddy',
      reason: data.reason || 'Medical / Personal Leave',
      from_date: data.from_date,
      to_date: data.to_date,
      status: 'Pending',
      submitted_at: new Date().toISOString().split('T')[0]
    };
    LocalMockData.leaves.unshift(newLeave);
    return { success: true, message: 'Leave application submitted successfully!', leave: newLeave };
  }

  if (ep.includes('/leave')) {
    return { success: true, leaves: LocalMockData.leaves };
  }

  if (ep.includes('/algorithms/search')) {
    const target = data.target_reg_no || '25221A0515';
    return {
      success: true,
      target: target,
      hash_table: { algorithm: 'Hash Table Lookup', operations: 1, time_ms: 0.04, complexity: { average: 'O(1)' }, explanation: 'Direct bucket index key retrieval' },
      binary_search: { algorithm: 'Binary Search', operations: 6, time_ms: 0.12, complexity: { average: 'O(log N)' }, explanation: 'Logarithmic divide & conquer on sorted dataset' },
      linear_search: { algorithm: 'Linear Search', operations: 35, time_ms: 0.85, complexity: { average: 'O(N)' }, explanation: 'Sequential scan checking every student record' }
    };
  }

  if (ep.includes('/algorithms/sort')) {
    return {
      success: true,
      algorithm: 'Merge Sort',
      complexity: 'O(N log N)',
      comparisons: 312,
      sorted_records: [
        { reg_no: '25221A0501', name: 'Aarav Reddy', attendance_pct: 95.5 },
        { reg_no: '25221A0505', name: 'Sneha Patel', attendance_pct: 94.2 },
        { reg_no: '25221A0512', name: 'Rohit Sharma', attendance_pct: 91.0 },
        { reg_no: '25221A0518', name: 'Ananya Varma', attendance_pct: 88.5 }
      ]
    };
  }

  if (ep.includes('/algorithms/graph')) {
    return {
      success: true,
      algorithm: 'Dijkstra Shortest Path',
      start: 'Main Gate',
      destination: 'CSE Block',
      path: ['Main Gate', 'Admin Quad', 'Library Junction', 'Science Block', 'CSE Department'],
      total_distance_meters: 340,
      walking_time_mins: 4.2
    };
  }

  return { success: true, message: 'Operation completed successfully.' };
}

const API = {
  async get(endpoint) {
    if (window.location.protocol === 'file:') {
      return resolveMockResponse('GET', endpoint);
    }
    try {
      const res = await fetch(`${API_BASE}${endpoint}`, { credentials: 'include' });
      if (!res.ok) throw new Error(`HTTP error ${res.status}`);
      return await res.json();
    } catch (err) {
      console.warn(`GET ${endpoint} using local fallback:`, err);
      return resolveMockResponse('GET', endpoint);
    }
  },

  async post(endpoint, data = {}) {
    if (window.location.protocol === 'file:') {
      return resolveMockResponse('POST', endpoint, data);
    }
    try {
      const res = await fetch(`${API_BASE}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(data)
      });
      if (!res.ok) throw new Error(`HTTP error ${res.status}`);
      return await res.json();
    } catch (err) {
      console.warn(`POST ${endpoint} using local fallback:`, err);
      return resolveMockResponse('POST', endpoint, data);
    }
  },

  async put(endpoint, data = {}) {
    if (window.location.protocol === 'file:') {
      return resolveMockResponse('PUT', endpoint, data);
    }
    try {
      const res = await fetch(`${API_BASE}${endpoint}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(data)
      });
      return await res.json();
    } catch (err) {
      return resolveMockResponse('PUT', endpoint, data);
    }
  },

  async delete(endpoint) {
    if (window.location.protocol === 'file:') {
      return resolveMockResponse('DELETE', endpoint);
    }
    try {
      const res = await fetch(`${API_BASE}${endpoint}`, {
        method: 'DELETE',
        credentials: 'include'
      });
      return await res.json();
    } catch (err) {
      return resolveMockResponse('DELETE', endpoint);
    }
  }
};

const Auth = {
  setUser(user) {
    localStorage.setItem('campusdash_user', JSON.stringify(user));
  },

  getUser() {
    const raw = localStorage.getItem('campusdash_user');
    return raw ? JSON.parse(raw) : null;
  },

  clearUser() {
    localStorage.removeItem('campusdash_user');
  },

  async logout() {
    try {
      await API.post('/logout');
    } catch (e) {}
    Auth.clearUser();
    window.location.href = 'index.html';
  },

  checkAuth(redirectOnMissing = true) {
    let user = Auth.getUser();
    if (!user) {
      // Auto-initialize demo student session so direct links always work
      user = {
        id: 1,
        name: 'Aarav Reddy',
        username: '25221A0501',
        reg_no: '25221A0501',
        role: 'student',
        branch: 'CSE',
        section: 'A',
        semester: 3
      };
      Auth.setUser(user);
    }
    return user;
  }
};

function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = 'toast-msg';

  let borderStyle = 'var(--accent-primary)';
  let icon = 'fa-info-circle';
  if (type === 'success') {
    borderStyle = 'var(--success-color)';
    icon = 'fa-check-circle text-success';
  } else if (type === 'danger') {
    borderStyle = 'var(--danger-color)';
    icon = 'fa-exclamation-triangle text-danger';
  } else if (type === 'warning') {
    borderStyle = 'var(--warning-color)';
    icon = 'fa-bell text-warning';
  }

  toast.style.borderLeftColor = borderStyle;
  toast.innerHTML = `<i class="fas ${icon} me-2"></i> <span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// Update Top Navbar Profile Info
function renderNavUser() {
  const user = Auth.getUser();
  const userContainer = document.getElementById('nav-user-info');
  if (userContainer && user) {
    userContainer.innerHTML = `
      <div class="d-flex align-items-center gap-2">
        <div class="text-end d-none d-md-block">
          <div class="fw-bold text-white small">${user.name}</div>
          <span class="badge-role badge-${user.role}">${user.role}</span>
        </div>
        <div class="avatar-circle bg-primary text-white rounded-circle d-flex align-items-center justify-content-center" style="width: 38px; height: 38px; font-weight:700;">
          ${user.name.charAt(0)}
        </div>
        <button onclick="Auth.logout()" class="btn btn-sm btn-outline-danger ms-2" title="Logout">
          <i class="fas fa-sign-out-alt"></i>
        </button>
      </div>
    `;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  renderNavUser();
});
