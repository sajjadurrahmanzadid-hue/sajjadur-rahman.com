/* ═══════════════════════════════════════════
   SAJJADUR RAHMAN — main.js
   ═══════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  /* ── ACTIVE NAV LINK ── */
  const page = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a, .mobile-nav a').forEach(a => {
    if (a.getAttribute('href') === page) a.classList.add('active');
  });

  /* ── HAMBURGER ── */
  const ham  = document.getElementById('hamburger');
  const mNav = document.getElementById('mobileNav');
  if (ham && mNav) {
    ham.addEventListener('click', () => {
      ham.classList.toggle('open');
      mNav.classList.toggle('open');
    });
    document.addEventListener('click', e => {
      if (!ham.contains(e.target) && !mNav.contains(e.target)) {
        ham.classList.remove('open');
        mNav.classList.remove('open');
      }
    });
  }

  /* ── LANGUAGE TOGGLE ── */
  const btnEN = document.getElementById('langEN');
  const btnBN = document.getElementById('langBN');
  const root  = document.documentElement;

  const setLang = lang => {
    if (lang === 'bn') {
      root.classList.add('lang-bn');
      btnBN && btnBN.classList.add('active');
      btnEN && btnEN.classList.remove('active');
      localStorage.setItem('sr_lang', 'bn');
    } else {
      root.classList.remove('lang-bn');
      btnEN && btnEN.classList.add('active');
      btnBN && btnBN.classList.remove('active');
      localStorage.setItem('sr_lang', 'en');
    }
  };

  // Restore preference
  const saved = localStorage.getItem('sr_lang') || 'en';
  setLang(saved);

  btnEN && btnEN.addEventListener('click', () => setLang('en'));
  btnBN && btnBN.addEventListener('click', () => setLang('bn'));

  /* ── SCROLL REVEAL ── */
  const reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && reveals.length) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('fade-up');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12 });
    reveals.forEach(el => io.observe(el));
  }

  /* ── COUNTER ANIMATION ── */
  const counters = document.querySelectorAll('.count-up');
  if (counters.length) {
    const countIO = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        const el  = e.target;
        const end = parseFloat(el.dataset.target);
        const dur = 1600;
        const step = 16;
        const inc  = end / (dur / step);
        let cur = 0;
        const tick = () => {
          cur = Math.min(cur + inc, end);
          el.textContent = Number.isInteger(end)
            ? Math.round(cur).toLocaleString()
            : cur.toFixed(1);
          if (cur < end) setTimeout(tick, step);
        };
        tick();
        countIO.unobserve(el);
      });
    }, { threshold: 0.5 });
    counters.forEach(el => countIO.observe(el));
  }

  /* ── CONTACT FORM ── */
  const form = document.getElementById('contactForm');
  if (form) {
    form.addEventListener('submit', async e => {
      e.preventDefault();
      const btn = form.querySelector('[type=submit]');
      const orig = btn.textContent;
      btn.textContent = '⏳ Sending…';
      btn.disabled = true;
      try {
        const res = await fetch(form.action, {
          method: 'POST',
          body: new FormData(form),
          headers: { 'Accept': 'application/json' }
        });
        if (res.ok) {
          btn.textContent = '✅ Sent!';
          form.reset();
          setTimeout(() => { btn.textContent = orig; btn.disabled = false; }, 3000);
        } else {
          throw new Error();
        }
      } catch {
        btn.textContent = '❌ Error — try WhatsApp';
        btn.disabled = false;
      }
    });
  }

  /* ── SMOOTH INTERNAL ANCHORS ── */
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  /* ── NAVBAR SHADOW ON SCROLL ── */
  const navbar = document.getElementById('navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.style.boxShadow = window.scrollY > 10
        ? '0 2px 12px rgba(30,28,24,0.10)'
        : 'none';
    }, { passive: true });
  }

});
