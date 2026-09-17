/**
 * YouthFit AI - Neural Match Engine Simulation & Pipeline Progress
 */

document.addEventListener('DOMContentLoaded', () => {
  let progress = 85;
  const progressText = document.getElementById('progress-percentage');
  const progressCircle = document.getElementById('progress-circle');
  const step3Status = document.getElementById('step3-status');
  const step4Card = document.getElementById('step4-card');
  const step4Status = document.getElementById('step4-status');
  const userConditionEl = document.getElementById('user-condition-title');
  const circumference = 314.159;

  // Retrieve customized profile if present
  try {
    const profile = JSON.parse(localStorage.getItem('youthfit_profile') || '{}');
    if (profile.district && profile.age && userConditionEl) {
      userConditionEl.textContent = `${profile.district} ${profile.age}세 청년`;
    }
  } catch (e) {}

  const interval = setInterval(() => {
    if (progress < 100) {
      progress += 1;
      if (progressText) progressText.textContent = `${progress}%`;
      if (progressCircle) {
        const offset = circumference - (progress / 100) * circumference;
        progressCircle.style.strokeDashoffset = offset;
      }

      // Step 4 packaging trigger around 95%
      if (progress >= 95 && step4Card && step4Status) {
        step4Card.className = "group flex items-start gap-4 p-3.5 rounded-lg bg-surface-container-low transition-all";
        step4Status.className = "font-label-md text-label-md px-2 py-0.5 rounded-full bg-secondary-container text-on-secondary-container font-semibold";
        step4Status.textContent = "패키징 완료";
      }
    } else {
      clearInterval(interval);
      if (progressText) progressText.textContent = "100%";
      if (step3Status) {
        step3Status.textContent = "판별 완료";
      }

      // Automatically transition to dashboard after 800ms
      setTimeout(() => {
        window.location.href = 'dashboard.html';
      }, 900);
    }
  }, 220);
});
