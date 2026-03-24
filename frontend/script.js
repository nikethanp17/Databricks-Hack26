/* ═══════════════════════════════════════
   script.js — Kirana Supply Optimizer
   Shared utilities + page logic
═══════════════════════════════════════ */

const API_BASE = 'http://127.0.0.1:8000';

/* ── Auth Helpers ───────────────────── */
const Auth = {
  isLoggedIn: () => localStorage.getItem('isLoggedIn') === 'true',
  login:      () => localStorage.setItem('isLoggedIn', 'true'),
  logout:     () => { localStorage.removeItem('isLoggedIn'); window.location.href = 'login.html'; },
  guard:      () => { if (!Auth.isLoggedIn()) window.location.href = 'login.html'; }
};

/* ── DOM Helpers ────────────────────── */
const $  = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

function showAlert(el, msg) {
  if (!el) return;
  el.textContent = msg;
  el.classList.add('show');
}

function hideAlert(el) {
  if (!el) return;
  el.textContent = '';
  el.classList.remove('show');
}

function setFieldError(inputEl, msgEl, msg) {
  inputEl?.classList.add('error-input');
  if (msgEl) { msgEl.textContent = msg; msgEl.classList.add('show'); }
}

function clearFieldError(inputEl, msgEl) {
  inputEl?.classList.remove('error-input');
  msgEl?.classList.remove('show');
}

/* ── Validation ─────────────────────── */
function validateDashboardForm(data) {
  const errors = {};
  if (!data.product)    errors.product   = 'Please select a product.';
  if (!data.day_type)   errors.day_type  = 'Please select a day type.';
  if (!data.time_slot)  errors.time_slot = 'Please select a time slot.';
  if (data.inventory === '' || data.inventory === null)
    errors.inventory = 'Please enter current inventory.';
  else if (isNaN(Number(data.inventory)) || Number(data.inventory) < 0)
    errors.inventory = 'Inventory must be a non-negative number.';
  return errors;
}

/* ═══════════════════════════════════════
   PAGE: Login
═══════════════════════════════════════ */
function initLogin() {
  if (Auth.isLoggedIn()) { window.location.href = 'landing.html'; return; }

  const form   = $('#loginForm');
  const errBox = $('#alertError');
  if (!form) return;

  form.addEventListener('submit', e => {
    e.preventDefault();
    const username = $('#username').value.trim();
    const password = $('#password').value.trim();
    hideAlert(errBox);

    if (username === 'admin' && password === '1234') {
      Auth.login();
      window.location.href = 'landing.html';
    } else {
      showAlert(errBox, 'Invalid credentials. Try admin / 1234');
      form.style.animation = 'shake 0.45s';
      setTimeout(() => { form.style.animation = ''; }, 450);
    }
  });

  // Clear error on input
  $$('input', form).forEach(inp =>
    inp.addEventListener('input', () => hideAlert(errBox))
  );
}

/* ═══════════════════════════════════════
   PAGE: Landing
═══════════════════════════════════════ */
function initLanding() {
  Auth.guard();

  // Typewriter
  const target = $('#typewriterText');
  const text   = 'AI-driven demand prediction & smart restocking';
  let i = 0;
  function type() {
    if (i < text.length) {
      target.textContent += text[i++];
      setTimeout(type, 42);
    }
  }
  setTimeout(type, 1200);

  // Enter dashboard
  const btn = $('#enterDashboard');
  btn?.addEventListener('click', () => {
    document.body.style.animation = 'fadeOut 0.55s ease-out forwards';
    setTimeout(() => window.location.href = 'dashboard.html', 550);
  });
}

/* ═══════════════════════════════════════
   PAGE: Dashboard
═══════════════════════════════════════ */
function initDashboard() {
  Auth.guard();

  const form        = $('#predictionForm');
  const spinner     = $('#spinner');
  const resultSec   = $('#resultSection');
  const serverAlert = $('#serverAlert');
  if (!form) return;

  // Logout
  $('#logoutBtn')?.addEventListener('click', Auth.logout);

  form.addEventListener('submit', async e => {
    e.preventDefault();
    hideAlert(serverAlert);

    // Collect raw values
    const raw = {
      product:   $('#product').value,
      day_type:  $('#day_type').value,
      time_slot: $('#time_slot').value,
      inventory: $('#inventory').value
    };

    // Clear previous field errors
    ['product','day_type','time_slot','inventory'].forEach(f => {
      clearFieldError($(`#${f}`), $(`#${f}Err`));
    });

    // Validate
    const errors = validateDashboardForm(raw);
    if (Object.keys(errors).length) {
      Object.entries(errors).forEach(([f, msg]) =>
        setFieldError($(`#${f}`), $(`#${f}Err`), msg)
      );
      return;
    }

    const payload = { ...raw, inventory: Number(raw.inventory) };

    // Show spinner, hide results
    resultSec.classList.remove('show');
    spinner.classList.add('show');
    $('#submitBtn').disabled = true;

    try {
      const res = await fetch(`${API_BASE}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `Server responded with ${res.status}`);
      }

      const data = await res.json();

      $('#demandVal').textContent  = `${data.predicted_demand.toFixed(1)} units`;
      $('#restockVal').textContent = `${data.restock} units`;
      $('#explanationText').textContent = data.explanation;

      spinner.classList.remove('show');
      resultSec.classList.add('show');

    } catch (err) {
      spinner.classList.remove('show');
      showAlert(serverAlert,
        err.message.includes('fetch')
          ? '⚠️ Cannot connect to server. Make sure the FastAPI backend is running on port 8000.'
          : `⚠️ ${err.message}`
      );
    } finally {
      $('#submitBtn').disabled = false;
    }
  });

  // Live clear field errors
  ['product','day_type','time_slot','inventory'].forEach(f => {
    $(`#${f}`)?.addEventListener('change', () => clearFieldError($(`#${f}`), $(`#${f}Err`)));
    $(`#${f}`)?.addEventListener('input',  () => clearFieldError($(`#${f}`), $(`#${f}Err`)));
  });
}

/* ── Auto-init based on page ─────────── */
document.addEventListener('DOMContentLoaded', () => {
  const page = document.body.dataset.page;
  if (page === 'login')     initLogin();
  if (page === 'landing')   initLanding();
  if (page === 'dashboard') initDashboard();
});
