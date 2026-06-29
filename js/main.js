(function () {
  'use strict';

  // Hero background video
  const hero = document.getElementById('hero');
  const heroVideo = document.querySelector('.hero__video');

  if (hero && heroVideo) {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const disableHeroVideo = () => {
      hero.classList.add('hero--no-video');
      heroVideo.pause();
    };

    if (prefersReducedMotion) {
      disableHeroVideo();
    } else {
      heroVideo.addEventListener('error', disableHeroVideo, { once: true });

      const playHeroVideo = () => {
        const playPromise = heroVideo.play();
        if (playPromise && typeof playPromise.catch === 'function') {
          playPromise.catch(disableHeroVideo);
        }
      };

      if (heroVideo.readyState >= 2) {
        playHeroVideo();
      } else {
        heroVideo.addEventListener('loadeddata', playHeroVideo, { once: true });
      }
    }
  }

  // Mobile nav toggle
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');
  const nav = document.getElementById('nav');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
    });

    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => navLinks.classList.remove('open'));
    });
  }

  // Nav scroll effect
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      nav.classList.add('nav--scrolled');
    } else {
      nav.classList.remove('nav--scrolled');
    }
  });

  // Manual sidebar navigation
  const manualLinks = document.querySelectorAll('.manual-nav__link');
  const manualSections = document.querySelectorAll('.manual-section');

  manualLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const sectionId = link.dataset.section;

      manualLinks.forEach(l => l.classList.remove('active'));
      link.classList.add('active');

      manualSections.forEach(section => {
        section.classList.toggle('active', section.id === sectionId);
      });
    });
  });

  // Form submissions (demo)
  function showToast(message) {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    document.body.appendChild(toast);

    requestAnimationFrame(() => toast.classList.add('show'));

    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 400);
    }, 3500);
  }

  const academyForm = document.getElementById('academyForm');
  if (academyForm) {
    academyForm.addEventListener('submit', (e) => {
      e.preventDefault();
      showToast('✓ Заявка отправлена. Ожидайте ответа от SWAT Academy.');
      academyForm.reset();
    });
  }

  const complaintForm = document.getElementById('complaintForm');
  if (complaintForm) {
    complaintForm.addEventListener('submit', (e) => {
      e.preventDefault();
      showToast('✓ Жалоба зарегистрирована. Internal Affairs свяжется с вами.');
      complaintForm.reset();
    });
  }

  // Personnel accordion
  document.querySelectorAll('.card--accordion .card__toggle').forEach(toggle => {
    toggle.addEventListener('click', () => {
      const card = toggle.closest('.card--accordion');
      const details = card.querySelector('.card__details');
      const isOpen = card.classList.toggle('is-open');

      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      details.hidden = !isOpen;
    });
  });

  // Fade-in on scroll
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }
      });
    },
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
  );

  document.querySelectorAll('.card, .order, .step, .data-table, .org-block, .exam-block').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(el);
  });
})();
