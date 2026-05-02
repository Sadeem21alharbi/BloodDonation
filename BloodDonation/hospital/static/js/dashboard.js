
  // Blood type picker
  document.querySelectorAll('.blood-type-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.blood-type-btn').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
    });
  });

  // Urgency picker
  document.querySelectorAll('.urgency-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.urgency-btn').forEach(b => b.classList.remove('sel-high','sel-medium','sel-low'));
      const label = btn.querySelector('.urg-label').textContent.trim().toLowerCase();
      btn.classList.add('sel-' + label);
    });
  });

  // Filter chips
  document.querySelectorAll('.filter-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      chip.closest('.filter-bar').querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
    });
  });
