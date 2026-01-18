(function(){
  const btn = document.querySelector('[data-hamburger]');
  const menu = document.querySelector('[data-mobile-menu]');
  if(btn && menu){
    btn.addEventListener('click', () => {
      const isOpen = menu.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(isOpen));
    });
  }

  const path = (location.pathname || '').toLowerCase();
  const normalize = (href) => (href || '').toLowerCase().replace(/\/+$/, '');
  const isHomePath = () => (path === '' || path.endsWith('/') || path.endsWith('/index.html'));

  document.querySelectorAll('a[data-nav]').forEach(a => {
    const href = normalize(a.getAttribute('href'));
    const onHome = isHomePath();
    const isHomeLink = href === '' || href === '/' || href.endsWith('/index.html');
    const match = (isHomeLink && onHome) || (!isHomeLink && path.endsWith(href));
    if(match) a.classList.add('active');
  });
})();
