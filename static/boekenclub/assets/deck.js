// Boekenclub-deck: schalen naar het scherm, pijltjes/spatie, vegen, tikken.
// #3 in de URL opent slide 3. Geen externe requests.
(function () {
  var stage = document.querySelector('.stage');
  var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  var i = 0;

  function fit() {
    var s = Math.min(window.innerWidth / 1080, window.innerHeight / 1350);
    stage.style.transform = 'scale(' + s + ')';
  }
  function go(n) {
    i = Math.max(0, Math.min(slides.length - 1, n));
    slides.forEach(function (el, k) { el.classList.toggle('active', k === i); });
    history.replaceState(null, '', '#' + (i + 1));
  }

  document.addEventListener('keydown', function (e) {
    if (['ArrowRight', ' ', 'PageDown', 'ArrowDown'].indexOf(e.key) >= 0) { e.preventDefault(); go(i + 1); }
    if (['ArrowLeft', 'PageUp', 'ArrowUp'].indexOf(e.key) >= 0) { e.preventDefault(); go(i - 1); }
    if (e.key === 'Home') go(0);
    if (e.key === 'End') go(slides.length - 1);
  });
  // Tikken of klikken: linkerderde terug, de rest verder (niet op een link).
  document.addEventListener('click', function (e) {
    if (e.target.closest('a')) return;
    go(e.clientX < window.innerWidth / 3 ? i - 1 : i + 1);
  });
  // Vegen op een telefoon.
  var x0 = null, y0 = null;
  document.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; }, { passive: true });
  document.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
    if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) { go(dx < 0 ? i + 1 : i - 1); e.preventDefault(); }
    x0 = null;
  });

  window.addEventListener('resize', fit);
  fit();
  go((parseInt(location.hash.slice(1), 10) || 1) - 1);
})();
