/* University Laboratory Checkout System - Enhanced UX */
(function () {
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Auto-focus first text input in filter forms
  const filterForms = document.querySelectorAll('form[method="get"]');
  filterForms.forEach(form => {
    const input = form.querySelector('input[type="text"], input:not([type]), select, textarea');
    if (input) { input.focus({ preventScroll: true }); }
  });

  // Smooth anchor scroll
  if (!prefersReducedMotion) {
    document.querySelectorAll('a[href^="#"]').forEach(a => {
      a.addEventListener('click', e => {
        const id = a.getAttribute('href').slice(1);
        const el = document.getElementById(id);
        if (el) { e.preventDefault(); el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
      });
    });
  }

  // Enhanced table interactions
  document.querySelectorAll('table.table tbody tr').forEach(tr => {
    // Skip if row is empty state
    if (tr.querySelector('td[colspan]')) return;
    
    tr.style.cursor = 'pointer';
    
    // Find primary link in row
    const primaryLink = tr.querySelector('td:first-child a');
    
    if (primaryLink) {
      tr.addEventListener('click', (e) => {
        // Don't navigate if clicking on a button or link directly
        if (e.target.tagName === 'A' || e.target.tagName === 'BUTTON' || e.target.closest('a') || e.target.closest('button')) {
          return;
        }
        primaryLink.click();
      });
    }
  });

  // Add loading state to forms
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn && !form.classList.contains('no-loading')) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span>Processing...</span>';
      }
    });
  });

  // Animate stats on load
  if (!prefersReducedMotion) {
    const stats = document.querySelectorAll('.stat .num');
    stats.forEach((stat, index) => {
      stat.style.opacity = '0';
      stat.style.transform = 'translateY(10px)';
      setTimeout(() => {
        stat.style.transition = 'all 0.4s ease';
        stat.style.opacity = '1';
        stat.style.transform = 'translateY(0)';
      }, index * 100);
    });
  }

  // Add ripple effect to buttons
  if (!prefersReducedMotion) {
    document.querySelectorAll('.btn, .action').forEach(button => {
      button.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
          position: absolute;
          width: ${size}px;
          height: ${size}px;
          border-radius: 50%;
          background: rgba(255, 255, 255, 0.3);
          left: ${x}px;
          top: ${y}px;
          pointer-events: none;
          transform: scale(0);
          animation: ripple 0.6s ease-out;
        `;
        
        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        button.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
      });
    });
    
    // Add ripple animation
    const style = document.createElement('style');
    style.textContent = `
      @keyframes ripple {
        to {
          transform: scale(4);
          opacity: 0;
        }
      }
    `;
    document.head.appendChild(style);
  }
})();
