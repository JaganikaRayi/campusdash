// Authentication Page Controller

let currentRole = 'student';

function selectRole(role) {
  currentRole = role;
  document.querySelectorAll('.role-tab-btn').forEach(btn => {
    btn.classList.remove('active');
  });
  const activeBtn = document.getElementById(`tab-${role}`);
  if (activeBtn) activeBtn.classList.add('active');

  const userInput = document.getElementById('login-username');
  const passInput = document.getElementById('login-password');
  const userLabel = document.getElementById('username-label');
  const passLabel = document.getElementById('password-label');

  if (role === 'student') {
    userLabel.innerText = 'Registration Number';
    userInput.placeholder = 'e.g. 25221A0501';
    passLabel.innerText = 'Student Name or Password';
    passInput.placeholder = 'e.g. Aarav Reddy (or student123)';
  } else if (role === 'faculty') {
    userLabel.innerText = 'Faculty ID / Email';
    userInput.placeholder = 'e.g. FAC01';
    passLabel.innerText = 'Faculty Password';
    passInput.placeholder = 'e.g. faculty123';
  } else {
    userLabel.innerText = 'Administrator Username';
    userInput.placeholder = 'e.g. admin';
    passLabel.innerText = 'Admin Password';
    passInput.placeholder = 'e.g. admin123';
  }
}

function fillDemoCreds(role) {
  selectRole(role);
  const userInput = document.getElementById('login-username');
  const passInput = document.getElementById('login-password');

  if (role === 'student') {
    userInput.value = '25221A0501';
    passInput.value = 'Aarav Reddy';
  } else if (role === 'faculty') {
    userInput.value = 'FAC01';
    passInput.value = 'faculty123';
  } else if (role === 'admin') {
    userInput.value = 'admin';
    passInput.value = 'admin123';
  }
}

async function handleLogin(e) {
  e.preventDefault();
  const username = document.getElementById('login-username').value.trim();
  const password = document.getElementById('login-password').value.trim();
  const errorBox = document.getElementById('login-error');
  const submitBtn = document.getElementById('login-btn');

  if (!username) {
    showToast('Please enter your registration number or username.', 'warning');
    return;
  }

  submitBtn.disabled = true;
  submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> Logging in...';
  if (errorBox) errorBox.classList.add('d-none');

  try {
    const res = await API.post('/login', {
      username: username,
      password: password,
      role: currentRole
    });

    if (res.success) {
      Auth.setUser(res.user);
      showToast(res.message, 'success');
      setTimeout(() => {
        window.location.href = 'dashboard.html';
      }, 500);
    } else {
      if (errorBox) {
        errorBox.innerText = res.message || 'Login failed';
        errorBox.classList.remove('d-none');
      }
      showToast(res.message || 'Invalid credentials', 'danger');
    }
  } catch (err) {
    if (errorBox) {
      errorBox.innerText = 'Could not connect to the server.';
      errorBox.classList.remove('d-none');
    }
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = '<i class="fas fa-sign-in-alt me-2"></i> Sign In to Portal';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('login-form');
  if (form) {
    form.addEventListener('submit', handleLogin);
  }
  // If already logged in, redirect to dashboard
  const user = Auth.getUser();
  if (user && window.location.pathname.endsWith('index.html')) {
    // allow user to stay or auto-redirect
  }
});
