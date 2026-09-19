/* Native details keeps navigation usable without JavaScript. */
(() => {
  const menus = [...document.querySelectorAll('.docs-nav')];
  menus.forEach(menu => {
    const trigger = menu.querySelector('summary');
    const sync = () => trigger.setAttribute('aria-expanded', String(menu.open));
    menu.addEventListener('toggle', () => {
      sync();
      if (menu.open) menus.forEach(other => { if (other !== menu) other.open = false; });
    });
    menu.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menu.open) {
        menu.open = false;
        sync();
        trigger.focus();
        event.preventDefault();
      }
    });
    sync();
  });
  const closeOutside = event => {
    menus.forEach(menu => { if (!menu.contains(event.target)) menu.open = false; });
  };
  document.addEventListener('pointerdown', closeOutside);
  // Close on the next focused element, not blur: some browsers report a null
  // relatedTarget when a link is clicked, before its click can navigate.
  document.addEventListener('focusin', closeOutside);
  function revealAnchor() {
    if (!location.hash) return;
    const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (target && target.matches('details')) target.open = true;
  }
  addEventListener('hashchange', revealAnchor);
  revealAnchor();
})();
