/* Keep links visible if JavaScript is unavailable. */
(function () {
  var nav = document.querySelector('.site-nav');
  if (!nav) return;
  var toggle = nav.querySelector('.mobile-menu-toggle');
  function closeMenu() {
    nav.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
  }
  nav.classList.add('mobile-nav-ready');
  toggle.addEventListener('click', function () {
    var open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
  });
  nav.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
      closeMenu();
      toggle.focus();
    }
  });
  nav.querySelector('ul').addEventListener('click', function (event) {
    if (event.target.closest('a')) closeMenu();
  });
})();
