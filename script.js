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

// Google review pop-up (bottom-left). Add real reviews to REVIEWS; the pop-up stays hidden while the list is empty.
const REVIEWS = [
  // { name: 'Customer name', stars: 5, text: 'Review text' }   // optional place: 'Dombivli' links the card to the Dombivli listing
  { name: 'S.T. Joisher', stars: 5, text: 'I have been using this brand for the past 8 years, and it is by far one of the best I’ve come across. The quality and durability of their products are outstanding, and they have consistently exceeded my expectations. I would highly recommend this brand to anyone looking for a reliable and long-lasting umbrella, it truly stands out as one of the best in the market.' },
  { name: 'Deepika Pawar', stars: 5, text: 'When it comes to promotional umbrellas gazebos and canopies Mukund enterprises is my go to place. I am very much inspired by the ethics and integrity of the way they do business.' },
  { name: 'Hrithik Panchal', stars: 5, text: 'Best Quality Umbrellas for Retail and Wholesale both. Thanks Mr Mukund for your response 😛' },
  { name: 'Bikash Jha', stars: 5, text: 'Your umbrella is of very good quality and the rate is also better than others. And your communication with the customer is also satisfactory ! Very good' },
  { name: 'Mohit Rochlani', stars: 5, text: 'They have a good variety of umbrellas, with great quality and excellent service. The staff is helpful and the overall experience was very good.' },
  { name: 'Zeal Tanna', stars: 5, text: 'Great Quality, lovely designs' },
  { name: 'NIKHILESH MANE', stars: 5, text: 'Brilliant product & service' },
  { name: 'Kunal Patil', stars: 5, text: 'Har Har Mahadev 🙏 Our First Exibation Stall at Shiv Mandir ,Sagaon...... Very Good Quality' },
  { name: 'sruthi sree', stars: 5, text: 'Nice quality,had good experience with mukund enterprises and I am very happy with this products.' },
  { name: 'Gaurav Aggarwal', stars: 5, place: 'Dombivli', text: 'Great work and good services' },
  { name: 'Manoj jha', stars: 5, text: 'Very good umbrella brand and faithful work' },
  { name: 'venkata giri', stars: 5, text: 'I love this products very much.I very appreciate this website for selling good things.' },
  { name: 'Saurabh Singh', stars: 4, text: 'Amazing product and services 👍.' },
  { name: 'Sreelatha M', stars: 5, text: 'Good quality 👌 👌 👌' },
  { name: 'Deepak Patidar', stars: 4, text: 'Nice product' },
];
const REVIEW_LINKS = {
  Kalbadevi: 'https://maps.google.com/?cid=11543601895112526243',
  Dombivli: 'https://maps.google.com/?cid=12498948281697536009'
};
(function reviewPopup() {
  const list = window.REVIEWS_PREVIEW || REVIEWS;
  if (!list.length || !document.querySelector('.hero')) return;
  try { if (sessionStorage.getItem('reviewsClosed')) return; } catch (e) {}
  const box = document.createElement('aside');
  box.className = 'review-pop';
  box.setAttribute('aria-live', 'polite');
  document.body.appendChild(box);
  const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const G = '<svg viewBox="0 0 48 48" width="22" height="22" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 13 4 4 13 4 24s9 20 20 20 20-9 20-20c0-1.3-.1-2.6-.4-3.5z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-7.9l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.6-.4-3.5z"/></svg>';
  let i = 0, timer, stopped = false;
  const show = () => {
    const r = list[i % list.length]; i++;
    // long reviews: keep whole sentences up to ~230 characters, otherwise cut at a word
    let text = r.text;
    if (text.length > 230) {
      const cut = text.slice(0, 230), end = Math.max(cut.lastIndexOf('. '), cut.lastIndexOf('! '));
      text = end > 80 ? cut.slice(0, end + 1) + ' …' : cut.slice(0, cut.lastIndexOf(' ')) + '…';
    }
    box.innerHTML = `<button class="rp-close" aria-label="Close reviews">×</button>
      <a class="rp-body" href="${REVIEW_LINKS[r.place] || REVIEW_LINKS.Kalbadevi}" target="_blank" rel="noopener">
        <div class="rp-top">${G}<span class="rp-stars">${'★'.repeat(r.stars)}${'☆'.repeat(5 - r.stars)}</span></div>
        <p class="rp-text">“${esc(text)}”</p>
        <p class="rp-name">${esc(r.name)} <span>· Google review</span></p></a>`;
    box.querySelector('.rp-close').onclick = () => { stopped = true; clearTimeout(timer); box.classList.remove('show'); try { sessionStorage.setItem('reviewsClosed', '1'); } catch (e) {} };
    box.classList.add('show');
    timer = setTimeout(() => { box.classList.remove('show'); if (!stopped) timer = setTimeout(show, 3000); }, 7000);
  };
  box.addEventListener('mouseenter', () => clearTimeout(timer));
  box.addEventListener('mouseleave', () => { if (!stopped) timer = setTimeout(() => { box.classList.remove('show'); timer = setTimeout(show, 3000); }, 3000); });
  setTimeout(show, 4000);
})();
