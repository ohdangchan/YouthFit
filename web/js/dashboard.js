/**
 * YouthFit AI - Diagnostic Dashboard & Checklist Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  const checkboxes = document.querySelectorAll('.doc-item');
  const progressText = document.getElementById('progress-text');
  const progressCircle = document.getElementById('progress-circle');
  const percentLabel = document.getElementById('percent-label');
  const heroProfileText = document.getElementById('hero-profile-text');

  // Load custom profile if set
  try {
    const profile = JSON.parse(localStorage.getItem('youthfit_profile') || '{}');
    if (profile.district && profile.age && heroProfileText) {
      const jobDesc = profile.jobStatus === 'jobseeker' ? '취준생' : profile.jobStatus === 'employed' ? '재직자' : '청년';
      const houseDesc = profile.household === 'single' ? '1인가구' : '다인가구';
      heroProfileText.textContent = `진단 완료: ${profile.age}세 ${jobDesc} (서울 ${profile.district} ${houseDesc})`;
    }
  } catch (e) {}

  function updateChecklistProgress() {
    const total = checkboxes.length;
    let checkedCount = 0;
    
    checkboxes.forEach(cb => {
      const statusPill = cb.closest('label')?.querySelector('.doc-status-pill');
      if (cb.checked) {
        checkedCount++;
        if (statusPill) {
          statusPill.className = "doc-status-pill px-2 py-0.5 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm";
          statusPill.textContent = "준비 완료";
        }
      } else {
        if (statusPill) {
          statusPill.className = "doc-status-pill px-2 py-0.5 rounded-full bg-surface-container-high text-on-surface-variant font-label-sm text-label-sm";
          statusPill.textContent = "미발급";
        }
      }
    });

    if (progressText) progressText.innerText = checkedCount;
    const percentage = Math.round((checkedCount / total) * 100);
    if (percentLabel) percentLabel.innerText = percentage + '%';
    if (progressCircle) progressCircle.setAttribute('stroke-dasharray', `${percentage}, 100`);
  }

  checkboxes.forEach(cb => {
    cb.addEventListener('change', updateChecklistProgress);
  });

  // Initial calculation
  updateChecklistProgress();

  // Export share & download handlers
  window.handleKakaoShare = function() {
    if (window.showToast) {
      window.showToast('카카오톡 알림톡으로 필수 서류 목록 및 정부24 링크가 전송되었습니다.', 'success');
    } else {
      alert('카카오톡 알림톡으로 필수 서류 목록 및 정부24 바로가기 링크가 전송되었습니다.');
    }
  };

  window.handlePdfDownload = function() {
    if (window.showToast) {
      window.showToast('맞춤 진단 결과가 포함된 2025 유스핏 종합 리포트 PDF 생성을 시작합니다.', 'info');
    } else {
      alert('맞춤 진단 결과 및 제출 체크리스트가 담긴 2025 유스핏 종합 리포트 PDF 생성을 시작합니다.');
    }
  };
});
