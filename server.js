const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = process.env.PORT || 5050;
const FRONTEND_DIR = path.join(__dirname, 'frontend');

// MIME types
const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf'
};

// In-Memory Database / Mock Store
const db = {
  users: [
    { id: 1, username: '25221A0501', name: 'Aarav Reddy', role: 'student', reg_no: '25221A0501', branch: 'CSE', section: 'A', semester: 3, email: 'aarav.reddy@campusdash.edu' },
    { id: 2, username: 'FAC01', name: 'Dr. K. Srinivas Rao', role: 'faculty', reg_no: 'FAC01', department: 'CSE', email: 'srinivas.rao@campusdash.edu' },
    { id: 3, username: 'admin', name: 'College Administrator', role: 'admin', reg_no: 'ADMIN', email: 'admin@campusdash.edu' }
  ],
  attendance: {
    '25221A0501': {
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
    }
  },
  fees: {
    '25221A0501': {
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
    }
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
    '25221A0501': {
      sgpa: 9.15,
      total_credits: 22,
      results: [
        { subject_code: 'CS301', subject_name: 'Advanced Data Structures & Algorithms', credits: 4, internal_marks: 28, external_marks: 66, total_marks: 94, grade: 'O', grade_points: 10 },
        { subject_code: 'CS302', subject_name: 'Python Programming Lab & Theory', credits: 3, internal_marks: 27, external_marks: 64, total_marks: 91, grade: 'O', grade_points: 10 },
        { subject_code: 'CS303', subject_name: 'Java Programming', credits: 3, internal_marks: 25, external_marks: 60, total_marks: 85, grade: 'A+', grade_points: 9 },
        { subject_code: 'BS301', subject_name: 'Discrete Mathematics', credits: 4, internal_marks: 26, external_marks: 59, total_marks: 85, grade: 'A+', grade_points: 9 },
        { subject_code: 'ES301', subject_name: 'Engineering Science Fundamentals', credits: 3, internal_marks: 24, external_marks: 58, total_marks: 82, grade: 'A', grade_points: 8 }
      ]
    }
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

// Helper: Read JSON request body
function parseBody(req) {
  return new Promise((resolve) => {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (e) {
        resolve({});
      }
    });
  });
}

// Helper: Send JSON response
function sendJSON(res, data, status = 200) {
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
  });
  res.end(JSON.stringify(data));
}

// HTTP Request Handler
const server = http.createServer(async (req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;
  const method = req.method;

  // Handle CORS Preflight
  if (method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    });
    res.end();
    return;
  }

  // API Routes
  if (pathname.startsWith('/api/')) {
    const apiPath = pathname.replace('/api', '');

    // Health Check
    if (apiPath === '/health') {
      return sendJSON(res, {
        status: 'healthy',
        service: 'CampusDash Smart Campus Management API (Node.js)',
        version: '1.0.0',
        ads_algorithms_count: 9
      });
    }

    // Login
    if (apiPath === '/login' && method === 'POST') {
      const data = await parseBody(req);
      const username = (data.username || '').trim().toUpperCase();
      const role = (data.role || 'student').toLowerCase();

      let user = db.users.find(u => u.username.toUpperCase() === username || u.reg_no.toUpperCase() === username);
      if (!user) {
        // Fallback demo user
        user = {
          id: 101,
          username: data.username || '25221A0501',
          name: (role === 'faculty') ? 'Dr. Faculty Member' : (role === 'admin' ? 'College Administrator' : 'Aarav Reddy'),
          role: role,
          reg_no: data.username || '25221A0501',
          branch: 'CSE',
          section: 'A'
        };
      }

      return sendJSON(res, {
        success: true,
        message: `Welcome back, ${user.name}!`,
        user: user
      });
    }

    // Logout
    if (apiPath === '/logout') {
      return sendJSON(res, { success: true, message: 'Logged out successfully.' });
    }

    // Attendance
    if (apiPath.startsWith('/attendance/') && method === 'GET') {
      const regNo = apiPath.split('/')[2].toUpperCase();
      const data = db.attendance['25221A0501'];
      return sendJSON(res, {
        success: true,
        reg_no: regNo,
        summary: data.summary,
        subject_wise: data.subject_wise,
        history: data.history
      });
    }

    if (apiPath === '/attendance/mark' && method === 'POST') {
      return sendJSON(res, { success: true, message: 'Attendance record saved successfully!' });
    }

    // Fees
    if (apiPath.startsWith('/fees/') && method === 'GET') {
      const regNo = apiPath.split('/')[2].toUpperCase();
      const feeData = db.fees['25221A0501'];
      return sendJSON(res, {
        success: true,
        ...feeData
      });
    }

    if (apiPath === '/fees/pay' && method === 'POST') {
      const data = await parseBody(req);
      const amount = parseFloat(data.amount) || 5000;
      const feeData = db.fees['25221A0501'];
      feeData.paid_fee += amount;
      feeData.balance = Math.max(0, feeData.total_fee - feeData.paid_fee);

      const receipt = {
        id: feeData.receipts.length + 1,
        receipt_no: `REC-2026-${Math.floor(1000 + Math.random() * 9000)}`,
        payment_date: new Date().toISOString().split('T')[0],
        amount: amount,
        payment_method: data.payment_method || 'Online UPI',
        transaction_ref: `TXN/${Math.floor(10000000000 + Math.random() * 90000000000)}`,
        student_reg_no: data.student_reg_no || '25221A0501',
        student_name: 'Aarav Reddy',
        balance_remaining: feeData.balance
      };
      feeData.receipts.unshift(receipt);

      return sendJSON(res, {
        success: true,
        message: 'Payment verified and authorized successfully!',
        receipt: receipt
      });
    }

    // Timetable
    if (apiPath.startsWith('/timetable/') && method === 'GET') {
      return sendJSON(res, {
        success: true,
        branch: 'CSE',
        section: 'A',
        timetable: db.timetable
      });
    }

    // Results
    if (apiPath.startsWith('/results/') && method === 'GET') {
      const data = db.results['25221A0501'];
      return sendJSON(res, {
        success: true,
        sgpa: data.sgpa,
        total_credits: data.total_credits,
        results: data.results
      });
    }

    // Notifications
    if (apiPath === '/notifications' && method === 'GET') {
      return sendJSON(res, { success: true, notifications: db.notifications });
    }

    // Materials
    if (apiPath === '/materials' && method === 'GET') {
      return sendJSON(res, { success: true, materials: db.materials });
    }

    // Faculty Directory
    if (apiPath === '/faculty' && method === 'GET') {
      return sendJSON(res, { success: true, faculty: db.faculty });
    }

    // Leaves
    if (apiPath === '/leave' && method === 'GET') {
      return sendJSON(res, { success: true, leaves: db.leaves });
    }

    if (apiPath === '/leave' && method === 'POST') {
      const data = await parseBody(req);
      const leave = {
        id: db.leaves.length + 1,
        student_reg_no: data.student_reg_no || '25221A0501',
        student_name: data.student_name || 'Aarav Reddy',
        reason: data.reason || 'Medical / Personal Leave',
        from_date: data.from_date,
        to_date: data.to_date,
        status: 'Pending',
        submitted_at: new Date().toISOString().split('T')[0]
      };
      db.leaves.unshift(leave);
      return sendJSON(res, { success: true, message: 'Leave application submitted successfully!', leave: leave });
    }

    // ADS Algorithms
    if (apiPath.startsWith('/algorithms/')) {
      const sub = apiPath.replace('/algorithms/', '');
      if (sub === 'search') {
        const body = await parseBody(req);
        const target = body.target_reg_no || '25221A0515';
        return sendJSON(res, {
          success: true,
          target: target,
          hash_table: { algorithm: 'Hash Table Lookup', operations: 1, time_ms: 0.04, complexity: { average: 'O(1)' }, explanation: 'Direct bucket index key retrieval' },
          binary_search: { algorithm: 'Binary Search', operations: 6, time_ms: 0.12, complexity: { average: 'O(log N)' }, explanation: 'Logarithmic divide & conquer on sorted dataset' },
          linear_search: { algorithm: 'Linear Search', operations: 35, time_ms: 0.85, complexity: { average: 'O(N)' }, explanation: 'Sequential scan checking every student record' }
        });
      }

      if (sub === 'sort') {
        return sendJSON(res, {
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
        });
      }

      if (sub === 'graph') {
        return sendJSON(res, {
          success: true,
          algorithm: 'Dijkstra Shortest Path',
          start: 'Main Gate',
          destination: 'CSE Block',
          path: ['Main Gate', 'Admin Quad', 'Library Junction', 'Science Block', 'CSE Department'],
          total_distance_meters: 340,
          walking_time_mins: 4.2
        });
      }

      return sendJSON(res, { success: true, message: 'ADS Algorithm simulation completed.' });
    }

    // Default API 404
    return sendJSON(res, { success: false, message: 'API route not found' }, 404);
  }

  // Static File Serving
  let safePath = path.normalize(pathname).replace(/^(\.\.[\/\\])+/, '');
  if (safePath === '/' || safePath === '\\') {
    safePath = '/index.html';
  }

  let filePath = path.join(FRONTEND_DIR, safePath);

  // If path doesn't have an extension, try appending .html
  if (!path.extname(filePath)) {
    if (fs.existsSync(filePath + '.html')) {
      filePath += '.html';
    }
  }

  // Check file exists
  if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
    // Check if index.html exists
    filePath = path.join(FRONTEND_DIR, 'index.html');
  }

  const ext = path.extname(filePath).toLowerCase();
  const contentType = MIME_TYPES[ext] || 'application/octet-stream';

  fs.readFile(filePath, (err, content) => {
    if (err) {
      res.writeHead(500, { 'Content-Type': 'text/plain' });
      res.end('Error loading ' + safePath);
    } else {
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content);
    }
  });
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`\n======================================================`);
  console.log(`>> CampusDash Smart Campus Web Server Running!`);
  console.log(`>> LIVE WEBSITE LINK: http://127.0.0.1:${PORT}`);
  console.log(`>> LOCALHOST LINK:    http://localhost:${PORT}`);
  console.log(`======================================================`);
  console.log(`Demo Credentials:`);
  console.log(`  - Student: Username: 25221A0501 | Password: Aarav Reddy (or student123)`);
  console.log(`  - Faculty: Username: FAC01      | Password: faculty123`);
  console.log(`  - Admin:   Username: admin      | Password: admin123`);
  console.log(`======================================================\n`);
});
