/**
 * YouthFit AI - Authentication and Guest Quick Start Logic
 */

function switchAuthTab(tab) {
  const paneLogin = document.getElementById('pane-login');
  const paneSignup = document.getElementById('pane-signup');
  const paneGuest = document.getElementById('pane-guest');
  
  const tabLogin = document.getElementById('tab-login');
  const tabSignup = document.getElementById('tab-signup');
  const tabGuest = document.getElementById('tab-guest');

  // Reset all tabs
  [paneLogin, paneSignup, paneGuest].forEach(p => p && p.classList.add('hidden'));
  [tabLogin, tabSignup, tabGuest].forEach(t => {
    if (t) {
      t.classList.remove('bg-surface-container-lowest', 'text-primary', 'shadow-sm');
      t.classList.add('text-on-surface-variant');
    }
  });

  if (tab === 'login') {
    if (paneLogin) paneLogin.classList.remove('hidden');
    if (tabLogin) {
      tabLogin.classList.add('bg-surface-container-lowest', 'text-primary', 'shadow-sm');
      tabLogin.classList.remove('text-on-surface-variant');
    }
  } else if (tab === 'signup') {
    if (paneSignup) paneSignup.classList.remove('hidden');
    if (tabSignup) {
      tabSignup.classList.add('bg-surface-container-lowest', 'text-primary', 'shadow-sm');
      tabSignup.classList.remove('text-on-surface-variant');
    }
  } else if (tab === 'guest') {
    if (paneGuest) paneGuest.classList.remove('hidden');
    if (tabGuest) {
      tabGuest.classList.add('bg-surface-container-lowest', 'text-primary', 'shadow-sm');
      tabGuest.classList.remove('text-on-surface-variant');
    }
  }
}

function togglePasswordVisibility(inputId, btn) {
  const input = document.getElementById(inputId);
  if (!input) return;
  const icon = btn.querySelector('.material-symbols-outlined');
  if (input.type === 'password') {
    input.type = 'text';
    if (icon) icon.textContent = 'visibility_off';
  } else {
    input.type = 'password';
    if (icon) icon.textContent = 'visibility';
  }
}

function toggleAllAgreements(masterCheck) {
  const checkboxes = document.querySelectorAll('.agree-sub');
  checkboxes.forEach(chk => {
    chk.checked = masterCheck.checked;
  });
}

function handleLoginSubmit(event) {
  event.preventDefault();
  const email = document.getElementById('login-email')?.value || '사용자';
  if (window.showToast) {
    window.showToast(`${email} 계정으로 로그인되었습니다. 대시보드로 이동합니다.`, 'success');
  } else {
    alert(`${email} 계정으로 인증되었습니다. 수혜 정책 보관함으로 이동합니다.`);
  }
  setTimeout(() => {
    window.location.href = 'dashboard.html';
  }, 800);
}

function handleSignupSubmit(event) {
  event.preventDefault();
  const name = document.getElementById('signup-name')?.value || '회원';
  if (window.showToast) {
    window.showToast(`${name}님 환영합니다! 1분 맞춤 진단으로 이동합니다.`, 'success');
  } else {
    alert(`${name}님 환영합니다! 신규 청년정책 진단 결과 페이지로 연결됩니다.`);
  }
  setTimeout(() => {
    window.location.href = 'diagnosis.html';
  }, 800);
}

function guestQuickStart() {
  window.location.href = 'diagnosis.html';
}

window.switchAuthTab = switchAuthTab;
window.togglePasswordVisibility = togglePasswordVisibility;
window.toggleAllAgreements = toggleAllAgreements;
window.handleLoginSubmit = handleLoginSubmit;
window.handleSignupSubmit = handleSignupSubmit;
window.guestQuickStart = guestQuickStart;
