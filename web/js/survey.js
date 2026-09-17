/**
 * YouthFit AI - 1-Minute Survey & Real-Time Benefit Calculator
 */

document.addEventListener('DOMContentLoaded', () => {
  const state = {
    age: 24,
    district: '관악구',
    jobStatus: 'jobseeker',
    household: 'single',
    income: 'income60'
  };

  const ageInput = document.getElementById('age-input');
  const districtBtns = document.querySelectorAll('#district-selector button');
  const jobStatusCards = document.querySelectorAll('#job-status-group > div');
  const householdBtns = document.querySelectorAll('#household-group button');
  const incomeBtns = document.querySelectorAll('#income-group button');
  const startBtn = document.getElementById('start-diagnosis-btn');

  const estimateAmountEl = document.getElementById('estimate-amount');
  const estimateSubtextEl = document.getElementById('estimate-subtext');
  const barYouthAllowance = document.getElementById('bar-youth-allowance');
  const textYouthAllowance = document.getElementById('text-youth-allowance');
  const barRentSupport = document.getElementById('bar-rent-support');
  const textRentSupport = document.getElementById('text-rent-support');

  // Load from localStorage if present
  try {
    const saved = localStorage.getItem('youthfit_profile');
    if (saved) {
      Object.assign(state, JSON.parse(saved));
    }
  } catch (e) {}

  // 1. Age Input Handler
  if (ageInput) {
    ageInput.value = state.age;
    ageInput.addEventListener('input', (e) => {
      let val = parseInt(e.target.value, 10);
      if (isNaN(val)) val = 24;
      state.age = val;
      recalculateEstimate();
    });
  }

  // 2. District Selector
  districtBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      districtBtns.forEach(b => {
        b.className = "py-2.5 px-3 rounded-lg font-label-md text-label-md text-center transition-all bg-surface-container-low text-on-surface-variant hover:bg-surface-container-high";
        const icon = b.querySelector('.material-symbols-outlined');
        if (icon) icon.remove();
      });

      btn.className = "py-2.5 px-3 rounded-lg font-label-md text-label-md text-center transition-all bg-primary-container text-on-primary shadow-sm font-semibold flex items-center justify-center gap-1";
      btn.innerHTML = `<span class="material-symbols-outlined text-xs">check</span> ${btn.textContent.trim().replace('check', '').trim()}`;
      state.district = btn.textContent.trim().replace('check', '').trim();
      recalculateEstimate();
    });
  });

  // 3. Job Status Selector
  jobStatusCards.forEach(card => {
    card.addEventListener('click', () => {
      jobStatusCards.forEach(c => {
        c.className = "p-4 rounded-xl bg-surface-container-lowest hover:bg-surface-container-low text-on-surface cursor-pointer transition-colors shadow-sm flex items-start justify-between border border-hairline-border";
        const title = c.querySelector('p.font-headline-sm');
        if (title) title.className = "font-headline-sm text-headline-sm text-on-surface font-semibold";
        const circle = c.querySelector('span.rounded-full:last-child');
        if (circle) {
          circle.className = "w-5 h-5 rounded-full bg-surface-container-high";
          circle.innerHTML = "";
        }
      });

      card.className = "p-4 rounded-xl bg-surface-container-high text-on-surface cursor-pointer shadow-sm flex items-start justify-between border border-primary";
      const title = card.querySelector('p.font-headline-sm');
      if (title) title.className = "font-headline-sm text-headline-sm text-primary font-bold";
      const circle = card.querySelector('span.rounded-full:last-child');
      if (circle) {
        circle.className = "w-5 h-5 rounded-full bg-primary text-on-primary flex items-center justify-center";
        circle.innerHTML = '<span class="material-symbols-outlined text-xs">check</span>';
      }

      state.jobStatus = card.getAttribute('data-status') || 'jobseeker';
      recalculateEstimate();
    });
  });

  // 4. Household Buttons
  householdBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      householdBtns.forEach(b => {
        b.className = "p-3.5 rounded-lg bg-surface-container-low hover:bg-surface-container-high text-left flex flex-col justify-between gap-2 transition-colors";
        const title = b.querySelector('p.font-label-lg');
        if (title) title.className = "font-label-lg text-label-lg text-on-surface font-semibold";
      });

      btn.className = "p-3.5 rounded-lg bg-surface-container-high text-left flex flex-col justify-between gap-2 shadow-sm border border-primary";
      const title = btn.querySelector('p.font-label-lg');
      if (title) title.className = "font-label-lg text-label-lg text-primary font-bold";

      state.household = btn.getAttribute('data-household') || 'single';
      recalculateEstimate();
    });
  });

  // 5. Income Buttons
  incomeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      incomeBtns.forEach(b => {
        b.className = "p-3 rounded-lg bg-surface-container-low hover:bg-surface-container-high text-left transition-colors";
        const title = b.querySelector('p.font-label-md');
        if (title) title.className = "font-label-md text-label-md text-on-surface font-semibold";
      });

      btn.className = "p-3 rounded-lg bg-surface-container-high text-left shadow-sm border border-primary";
      const title = btn.querySelector('p.font-label-md');
      if (title) title.className = "font-label-md text-label-md text-primary font-bold";

      state.income = btn.getAttribute('data-income') || 'income60';
      recalculateEstimate();
    });
  });

  // Calculation Engine
  function recalculateEstimate() {
    let amount = 0;
    let allowanceMatch = 90;
    let rentMatch = 75;
    let subtext = "선택하신 조건에 부합하는 정책을 집계 중입니다.";

    if (state.jobStatus === 'jobseeker') {
      amount += 3000000; // 서울시 청년수당 (50만원 x 6회)
      allowanceMatch = 96;
      subtext = "서울시 청년수당(월 50만원×6회)";
    } else if (state.jobStatus === 'employed') {
      amount += 3600000; // 희망두배 / 도약계좌
      allowanceMatch = 45;
      subtext = "희망두배 청년통장 자산형성 매칭(연 최대 360만원)";
    } else {
      amount += 1200000;
      allowanceMatch = 70;
      subtext = "청년 취업역량 바우처 및 자격증 응시료 지원";
    }

    if (state.household === 'single' && (state.income === 'income60' || state.income === 'income120')) {
      amount += 2400000; // 월세 특별지원 (월 20만원 x 12회)
      rentMatch = 92;
      subtext += " + 청년 월세 지원 대상 후보";
    } else {
      rentMatch = 40;
    }

    // 교통비 기본 매칭
    if (state.age >= 19 && state.age <= 24) {
      amount += 100000;
    }

    if (estimateAmountEl) {
      estimateAmountEl.textContent = amount.toLocaleString('ko-KR');
    }
    if (estimateSubtextEl) {
      estimateSubtextEl.textContent = subtext;
    }
    if (barYouthAllowance) {
      barYouthAllowance.style.width = `${allowanceMatch}%`;
    }
    if (textYouthAllowance) {
      textYouthAllowance.textContent = `${allowanceMatch}% ${allowanceMatch > 80 ? '매우 높음' : '적합'}`;
    }
    if (barRentSupport) {
      barRentSupport.style.width = `${rentMatch}%`;
    }
    if (textRentSupport) {
      textRentSupport.textContent = `${rentMatch}% ${rentMatch > 80 ? '통과 예상' : '검토 필요'}`;
    }
  }

  // Trigger initial calculation
  recalculateEstimate();

  // Start Diagnosis Action -> Navigate to loading.html
  if (startBtn) {
    startBtn.addEventListener('click', () => {
      try {
        localStorage.setItem('youthfit_profile', JSON.stringify(state));
      } catch (e) {}
      window.location.href = 'loading.html';
    });
  }
});
