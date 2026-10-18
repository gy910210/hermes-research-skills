'use strict';
(() => {
  document.documentElement.classList.add('js-enabled');
  const toc = document.getElementById('toc');
  const toggle = document.getElementById('toc-toggle');
  const progress = document.getElementById('reading-progress');
  const headings = [...document.querySelectorAll('article h1,article h2,article h3,article h4,article h5,article h6')];
  const links = [...toc.querySelectorAll('a')];
  toggle.addEventListener('click', () => {
    const open = toc.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
    if (open) links[0]?.focus();
  });
  links.forEach(link => link.addEventListener('click', () => {
    toc.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
  }));
  document.querySelector('[data-print]').addEventListener('click', () => window.print());
  let pending = false;
  function update() {
    const height = document.documentElement.scrollHeight - window.innerHeight;
    progress.value = height > 0 ? Math.min(100, Math.max(0, window.scrollY / height * 100)) : 100;
    let current = headings[0]?.id;
    for (const heading of headings) {
      if (heading.getBoundingClientRect().top <= 150) current = heading.id;
    }
    for (const link of links) {
      if (decodeURIComponent(link.hash.slice(1)) === current) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    }
    pending = false;
  }
  function schedule() {
    if (!pending) { pending = true; window.requestAnimationFrame(update); }
  }
  window.addEventListener('scroll', schedule, {passive: true});
  window.addEventListener('resize', schedule);
  update();
})();
