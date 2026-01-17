(function(){
  const btn = document.querySelector('[data-hamburger]');
  const menu = document.querySelector('[data-mobile-menu]');
  if(btn && menu){
    btn.addEventListener('click', () => {
      const isOpen = menu.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(isOpen));
    });
  }

  // Set active link based on pathname
  const path = (location.pathname || '').toLowerCase();
  const markActive = (selector) => {
    document.querySelectorAll(selector).forEach(a => {
      const href = (a.getAttribute('href') || '').toLowerCase();
      if(!href) return;
      const isHome = (href === 'index.html' || href === '/' || href === './' || href === './index.html');
      const onHome = (path.endsWith('/') || path.endsWith('/index.html') || path === '' || path.endsWith('index.html'));
      const match =
        (isHome && onHome) ||
        (!isHome && path.endsWith(href));
      if(match) a.classList.add('active');
    });
  };
  markActive('.nav-links a');
  markActive('.mobile-menu a');
})();
