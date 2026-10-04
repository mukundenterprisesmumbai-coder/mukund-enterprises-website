// ---- EDIT THESE ----
const SITE = {
  phone: '+91 91378 78456',   // shown on the site
  whatsapp: '919137878456',      // digits only
};
// --------------------

document.querySelectorAll('[data-phone]').forEach(e => { e.textContent = SITE.phone; if (e.tagName === 'A') e.href = 'tel:' + SITE.phone.replace(/\s/g, ''); });
document.querySelectorAll('[data-wa]').forEach(e => {
  const msg = e.dataset.wa ? '?text=' + encodeURIComponent(e.dataset.wa) : '';
  e.href = 'https://wa.me/' + SITE.whatsapp + msg;
  e.target = '_blank'; e.rel = 'noopener';
});

// mobile menu
const burger = document.querySelector('.burger');
if (burger) burger.addEventListener('click', () => document.querySelector('nav ul').classList.toggle('open'));

// product filters
const fbtns = document.querySelectorAll('.filters button');
fbtns.forEach(b => b.addEventListener('click', () => {
  fbtns.forEach(x => x.classList.remove('on')); b.classList.add('on');
  document.querySelectorAll('.product').forEach(p => {
    p.style.display = (b.dataset.f === 'all' || p.dataset.cat === b.dataset.f) ? '' : 'none';
  });
}));

// contact form -> saved by Netlify Forms (emailed to the business); WhatsApp offered as an optional follow-up
const form = document.getElementById('enquiry');
if (form) {
  const p = new URLSearchParams(location.search);
  if (p.get('product')) form.message.value = 'Hi, I would like a quote for: ' + p.get('product');
  if (p.get('topic')) form.topic.value = p.get('topic');
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const f = new FormData(form);
    const btn = form.querySelector('button[type="submit"]');
    const ok = form.querySelector('.ok'), err = form.querySelector('.err');
    ok.style.display = err.style.display = 'none';
    btn.disabled = true; btn.firstChild.textContent = 'Sending…';
    // WhatsApp stays available as an optional, faster channel (visitor chooses to use it)
    const text = `New enquiry\nName: ${f.get('name')}\nPhone: ${f.get('phone')}\nEmail: ${f.get('email')}\nTopic: ${f.get('topic')}\nQuantity: ${f.get('qty') || '-'}\n\n${f.get('message')}`;
    form.querySelectorAll('.wa-link').forEach(a => a.href = 'https://wa.me/' + SITE.whatsapp + '?text=' + encodeURIComponent(text));
    try {
      // saved by Netlify Forms and emailed to the business
      const r = await fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(f).toString() });
      if (!r.ok) throw new Error(r.status);
      ok.style.display = 'block';
      form.reset();
      // enquiry is saved; now take the visitor straight to WhatsApp with their details filled in
      setTimeout(() => { location.href = form.querySelector('.wa-link').href; }, 2000);
    } catch (_) {
      err.style.display = 'block';
    }
    btn.disabled = false; btn.firstChild.textContent = 'Send message';
  });
}
// home page hero: photos fade into each other (1 second fade, a new photo every 2 seconds)
const slides = document.querySelectorAll('.hero-slides .slide');
const ready = new Set([0]);
// load the later photos after the page is ready, and only show a photo once it has fully loaded
window.addEventListener('load', () => slides.forEach((s, i) => {
  if (!s.dataset.bg) return;
  const img = new Image();
  img.onload = () => { s.style.backgroundImage = "url('" + s.dataset.bg + "')"; ready.add(i); };
  img.src = s.dataset.bg;
}));
if (slides.length > 1 && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  let cur = 0;
  setInterval(() => {
    const next = (cur + 1) % slides.length;
    if (!ready.has(next)) return;
    slides[cur].classList.remove('on');
    cur = next;
    slides[cur].classList.add('on');
  }, 2000);
}

// home page: featured products carousel - loops forward forever (1 2 3 4 5 1 2 3 ...)
const car = document.querySelector('.carousel');
if (car) {
  const track = car.querySelector('.track');
  const originals = [...track.children];
  // a hidden second copy of the cards lets the row keep moving forward without rewinding
  originals.forEach(c => {
    const copy = c.cloneNode(true);
    copy.setAttribute('aria-hidden', 'true');
    copy.querySelectorAll('a').forEach(l => l.tabIndex = -1);
    track.appendChild(copy);
  });
  const setWidth = () => track.children[originals.length].offsetLeft - track.children[0].offsetLeft;
  const step = () => originals[0].getBoundingClientRect().width + 22;
  const jump = x => car.scrollTo({ left: x, behavior: 'instant' });
  const go = dir => {
    const w = setWidth();
    if (dir > 0 && car.scrollLeft >= w - 2) jump(car.scrollLeft - w);   // silently back to the same card in the first copy
    if (dir < 0 && car.scrollLeft <= 2) jump(car.scrollLeft + w);
    car.scrollBy({ left: dir * step(), behavior: 'smooth' });
  };
  // keep manual swiping endless too
  let t; car.addEventListener('scroll', () => { clearTimeout(t); t = setTimeout(() => { const w = setWidth(); if (car.scrollLeft >= w) jump(car.scrollLeft - w); }, 150); }, { passive: true });
  document.querySelector('.carousel-nav .next')?.addEventListener('click', () => go(1));
  document.querySelector('.carousel-nav .prev')?.addEventListener('click', () => go(-1));
  let paused = false;
  ['mouseenter', 'touchstart', 'focusin'].forEach(e => car.addEventListener(e, () => paused = true, { passive: true }));
  car.addEventListener('mouseleave', () => paused = false);
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) setInterval(() => { if (!paused) go(1); }, 3500);
}
