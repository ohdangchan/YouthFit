/**
 * YouthFit AI - Global Application Utilities
 */

// Smooth scroll for in-page anchors
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href').substring(1);
      if (!targetId) return;
      const targetEl = document.getElementById(targetId);
      if (targetEl) {
        e.preventDefault();
        targetEl.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
});

/**
 * Toast Notification Utility
 */
function showToast(message, type = 'info') {
  let toastContainer = document.getElementById('youthfit-toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'youthfit-toast-container';
    toastContainer.style.cssText = `
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 8px;
      pointer-events: none;
    `;
    document.body.appendChild(toastContainer);
  }

  const toast = document.createElement('div');
  const bg = type === 'success' ? '#006c4a' : type === 'error' ? '#ba1a1a' : '#004ac6';
  toast.style.cssText = `
    background: ${bg};
    color: #ffffff;
    padding: 12px 20px;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 500;
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    opacity: 0;
    transform: translateY(10px);
    transition: all 0.25s ease-out;
    pointer-events: auto;
    display: flex;
    align-items: center;
    gap: 8px;
  `;
  toast.innerHTML = `
    <span class="material-symbols-outlined text-[18px]">
      ${type === 'success' ? 'check_circle' : type === 'error' ? 'error' : 'info'}
    </span>
    <span>${message}</span>
  `;

  toastContainer.appendChild(toast);
  requestAnimationFrame(() => {
    toast.style.opacity = '1';
    toast.style.transform = 'translateY(0)';
  });

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 250);
  }, 3200);
}

/**
 * Toggle Hot Policies Section (Expand / Collapse)
 */
function toggleHotPolicies() {
  const cards = document.getElementById('hot-policies-grid');
  const banner = document.getElementById('expanded-status-banner');
  const icon = document.getElementById('policy-toggle-icon');
  const txt = document.getElementById('policy-toggle-text');
  if (!cards) return;

  const isHidden = cards.classList.contains('hidden');
  if (isHidden) {
    cards.classList.remove('hidden');
    if (banner) banner.classList.remove('hidden');
    if (icon) icon.textContent = 'expand_less';
    if (txt) txt.textContent = '주요 정책 목록 접기';
  } else {
    cards.classList.add('hidden');
    if (banner) banner.classList.add('hidden');
    if (icon) icon.textContent = 'expand_more';
    if (txt) txt.textContent = '주요 정책 목록 펼치기';
  }
}

window.showToast = showToast;
window.toggleHotPolicies = toggleHotPolicies;

