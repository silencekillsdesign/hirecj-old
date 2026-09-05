// Gallery lightbox for project pages — vanilla <dialog>, click-through with arrows.
(function () {
  var links = Array.prototype.slice.call(document.querySelectorAll('.pp-gallery figure a'));
  if (!links.length) return;

  var dlg = document.createElement('dialog');
  dlg.className = 'pp-lightbox';
  dlg.innerHTML =
    '<button class="lb-close" aria-label="Close">&times;</button>' +
    '<button class="lb-prev" aria-label="Previous image">&#8592;</button>' +
    '<figure><img alt="" /><figcaption></figcaption></figure>' +
    '<button class="lb-next" aria-label="Next image">&#8594;</button>';
  document.body.appendChild(dlg);

  var img = dlg.querySelector('img');
  var cap = dlg.querySelector('figcaption');
  var i = 0;

  function show(n) {
    i = (n + links.length) % links.length;
    img.src = links[i].href;
    var c = links[i].closest('figure').querySelector('figcaption');
    cap.textContent = (c ? c.textContent : '') + '  ·  ' + (i + 1) + ' / ' + links.length;
  }

  links.forEach(function (a, n) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      show(n);
      dlg.showModal();
    });
  });

  dlg.querySelector('.lb-close').addEventListener('click', function () { dlg.close(); });
  dlg.querySelector('.lb-prev').addEventListener('click', function () { show(i - 1); });
  dlg.querySelector('.lb-next').addEventListener('click', function () { show(i + 1); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
  document.addEventListener('keydown', function (e) {
    if (!dlg.open) return;
    if (e.key === 'ArrowLeft') show(i - 1);
    if (e.key === 'ArrowRight') show(i + 1);
  });
})();
