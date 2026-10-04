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

// contact form -> opens WhatsApp with the message pre-filled
const form = document.getElementById('enquiry');
if (form) {
  const p = new URLSearchParams(location.search);
  if (p.get('product')) form.message.value = 'Hi, I would like a quote for: ' + p.get('product');
  if (p.get('topic')) form.topic.value = p.get('topic');
  form.addEventListener('submit', e => {
    e.preventDefault();
    const f = new FormData(form);
    // 1) send to Netlify Forms -> arrives in your email
    fetch('/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams(f).toString(),
      keepalive: true,
    }).catch(() => {});
    // 2) also open WhatsApp with the details filled in
    const text = `New enquiry\nName: ${f.get('name')}\nPhone: ${f.get('phone')}\nEmail: ${f.get('email')}\nTopic: ${f.get('topic')}\nQuantity: ${f.get('qty') || '-'}\n\n${f.get('message')}`;
    window.open('https://wa.me/' + SITE.whatsapp + '?text=' + encodeURIComponent(text), '_blank');
    document.querySelector('.ok').style.display = 'block';
    form.reset();
  });
}
// home page hero: rotate the background photos every 6 seconds
const slides = document.querySelectorAll('.hero-slides .slide');
if (slides.length > 1 && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  let cur = 0;
  setInterval(() => {
    slides[cur].classList.remove('on');
    cur = (cur + 1) % slides.length;
    slides[cur].classList.add('on');
  }, 6000);
}
