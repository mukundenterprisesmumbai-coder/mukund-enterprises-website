// Interactive tools: product finder quiz, bulk price estimator, logo-on-umbrella preview.
// Product names, links, photos and "From" prices are read from products.html, so they never go out of date.
(function () {
  const WA = '919137878456';
  const waLink = text => 'https://wa.me/' + WA + '?text=' + encodeURIComponent(text);
  const tr = (n, p) => { try { track(n, p); } catch (_) {} };
  const inr = n => '₹' + Math.round(n).toLocaleString('en-IN');
  const root = document.querySelector('script[src$="tools.js"]').getAttribute('src').replace(/tools\.js$/, '');

  let catalogue;
  function loadProducts() {
    if (!catalogue) catalogue = fetch(root + 'products.html').then(r => r.text()).then(html => {
      const doc = new DOMParser().parseFromString(html, 'text/html');
      return [...doc.querySelectorAll('.product')].map(p => {
        const a = p.querySelector('h3 a'), img = p.querySelector('img'), price = p.querySelector('.price');
        const m = price && price.textContent.match(/₹\s?([\d,]+)/);
        return { name: a.textContent.trim(), url: root + a.getAttribute('href'), img: root + img.getAttribute('src'), cat: p.dataset.cat, price: m ? +m[1].replace(/,/g, '') : 0 };
      }).filter(p => p.price);
    });
    return catalogue;
  }

  // ---------- product finder quiz ----------
  const quiz = document.getElementById('finder');
  if (quiz) {
    const steps = [...quiz.querySelectorAll('.q-step')], out = quiz.querySelector('.q-result'), ans = {};
    const show = i => { steps.forEach((s, j) => s.hidden = j !== i); out.hidden = i < steps.length; quiz.querySelector('.q-progress b').style.width = (Math.min(i, steps.length) / steps.length * 100) + '%'; };
    const USE = { logo: ['Promotional', 'Folding'], rain: ['Folding', 'Rain'], shade: ['Outdoor', 'Accessories'], events: ['Tents', 'Promotional'] };
    const BUDGET = { low: [0, 400], mid: [400, 1000], high: [1000, 1e9] };
    quiz.addEventListener('click', async e => {
      const b = e.target.closest('button[data-k]');
      if (b) {
        ans[b.dataset.k] = b.dataset.v; ans[b.dataset.k + 'Label'] = b.textContent.trim();
        const i = steps.indexOf(b.closest('.q-step')) + 1;
        if (i < steps.length) return show(i);
        show(i);
        const all = await loadProducts();
        const [lo, hi] = BUDGET[ans.budget];
        let list = all.filter(p => USE[ans.use].includes(p.cat));
        const inBudget = list.filter(p => p.price >= lo && p.price < hi);
        const mid = (lo + Math.min(hi, lo * 3 || 400)) / 2;
        list = (inBudget.length ? inBudget : list).sort((a, b) => (USE[ans.use].indexOf(a.cat) - USE[ans.use].indexOf(b.cat)) || Math.abs(a.price - mid) - Math.abs(b.price - mid)).slice(0, 3);
        const note = ans.use === 'logo' && ans.qty === 'small' ? '<p class="note">Logo printing starts at 300 pieces. For smaller quantities, ask us about plain stock.</p>' : '';
        const text = `Hi, I used the product finder on your website.\nFor: ${ans.useLabel}\nQuantity: ${ans.qtyLabel}\nBudget: ${ans.budgetLabel}\nSuggested: ${list.map(p => p.name).join(', ')}`;
        out.querySelector('.q-cards').innerHTML = list.map(p => `<a class="q-card" href="${p.url}"><img src="${p.img}" alt="" loading="lazy" width="120" height="120"><span><b>${p.name}</b><small>From ${inr(p.price)}</small></span></a>`).join('') + note;
        out.querySelector('.q-wa').href = waLink(text);
        tr('finder_complete', { label: ans.use + '/' + ans.qty + '/' + ans.budget });
      }
      if (e.target.closest('.q-restart')) show(0);
    });
    out.querySelector('.q-wa').target = '_blank';
    out.querySelector('.q-wa').addEventListener('click', () => tr('whatsapp_click', { label: 'product finder' }));
    show(0);
  }

  // ---------- bulk price estimator ----------
  const est = document.getElementById('estimator');
  if (est) {
    const sel = est.querySelector('select'), qty = est.querySelector('input'), res = est.querySelector('.e-result');
    loadProducts().then(list => {
      sel.innerHTML = list.map((p, i) => `<option value="${i}">${p.name} (from ${inr(p.price)})</option>`).join('');
      const pre = new URLSearchParams(location.search).get('product');
      const hit = pre && list.findIndex(p => p.name.toLowerCase() === pre.toLowerCase());
      if (hit >= 0) sel.value = hit;
      const update = () => {
        const p = list[sel.value], q = Math.max(1, parseInt(qty.value, 10) || 1);
        res.querySelector('.e-total').textContent = inr(p.price * q);
        res.querySelector('.e-line').textContent = `${q.toLocaleString('en-IN')} × ${inr(p.price)} list price, GST included, delivery extra`;
        res.querySelector('.e-wa').href = waLink(`Hi, I need a quote.\nProduct: ${p.name}\nQuantity: ${q}\nEstimate on website: ${inr(p.price * q)}\n${new URL(p.url, location.href).href}`);
        const f = document.getElementById('enquiry');
        res.querySelector('.e-form').hidden = !f;
        est.dataset.product = p.name; est.dataset.qty = q;
      };
      sel.addEventListener('change', update); qty.addEventListener('input', update); update();
      res.querySelector('.e-wa').addEventListener('click', () => tr('whatsapp_click', { label: 'estimator' }));
      res.querySelector('.e-form').addEventListener('click', () => {
        const f = document.getElementById('enquiry');
        f.product.value = est.dataset.product; f.qty.value = est.dataset.qty + ' pieces'; f.topic.value = 'Bulk or B2B order';
        f.scrollIntoView({ behavior: 'smooth' }); f.name.focus({ preventScroll: true });
      });
    });
  }

  // ---------- logo on umbrella preview ----------
  const cv = document.getElementById('umb');
  if (cv) {
    const ctx = cv.getContext('2d'), form = document.getElementById('umb-controls');
    let logo = null;
    const N = 8;
    function draw() {
      const W = cv.width, c = W / 2, R = W * 0.46, A = form.colA.value, B = form.colB.value, n = +form.panels.value;
      ctx.clearRect(0, 0, W, W);
      const ang = i => (-90 - 180 / N + i * 360 / N) * Math.PI / 180;
      const pt = (a, r) => [c + Math.cos(a) * r, c + Math.sin(a) * r];
      // shadow
      ctx.save(); ctx.fillStyle = 'rgba(0,0,0,.18)'; ctx.filter = 'blur(14px)'; ctx.beginPath(); ctx.arc(c + 10, c + 16, R * .98, 0, 7); ctx.fill(); ctx.restore();
      for (let i = 0; i < N; i++) {
        const a0 = ang(i), a1 = ang(i + 1), am = (a0 + a1) / 2;
        ctx.beginPath(); ctx.moveTo(c, c); ctx.lineTo(...pt(a0, R));
        ctx.quadraticCurveTo(...pt(am, R * 0.955), ...pt(a1, R)); ctx.closePath();
        ctx.fillStyle = i % 2 ? B : A; ctx.fill();
        // soft light across each panel
        const g = ctx.createLinearGradient(...pt(a0, R * .7), ...pt(a1, R * .7));
        g.addColorStop(0, 'rgba(255,255,255,.10)'); g.addColorStop(.5, 'rgba(255,255,255,0)'); g.addColorStop(1, 'rgba(0,0,0,.10)');
        ctx.fillStyle = g; ctx.fill();
        ctx.strokeStyle = 'rgba(0,0,0,.18)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(c, c); ctx.lineTo(...pt(a0, R)); ctx.stroke();
      }
      const rg = ctx.createRadialGradient(c - R * .2, c - R * .25, R * .1, c, c, R);
      rg.addColorStop(0, 'rgba(255,255,255,.18)'); rg.addColorStop(1, 'rgba(0,0,0,.12)');
      ctx.fillStyle = rg; ctx.beginPath(); ctx.arc(c, c, R, 0, 7); ctx.fill();
      // printed panels: 1 = top, 2 = top + bottom, 4 = every other panel, 8 = all
      const step = n === 1 ? N : N / n;
      for (let i = 0; i < N; i += step) {
        const am = (ang(i) + ang(i + 1)) / 2, [x, y] = pt(am, R * .6);
        ctx.save(); ctx.translate(x, y); ctx.rotate(am + Math.PI / 2);
        const bw = R * .38, bh = R * .26;
        if (logo) {
          const s = Math.min(bw / logo.width, bh / logo.height);
          ctx.drawImage(logo, -logo.width * s / 2, -logo.height * s / 2, logo.width * s, logo.height * s);
        } else {
          ctx.fillStyle = form.colA.value === form.colB.value || i % 2 === 0 ? '#fff' : '#1B2A4A';
          ctx.font = `700 ${Math.round(R * .085)}px Poppins, Arial, sans-serif`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
          ctx.fillText('YOUR', 0, -R * .05); ctx.fillText('LOGO', 0, R * .05);
        }
        ctx.restore();
      }
      ctx.fillStyle = '#333'; ctx.beginPath(); ctx.arc(c, c, R * .035, 0, 7); ctx.fill();
      ctx.fillStyle = '#888'; ctx.beginPath(); ctx.arc(c - R * .01, c - R * .01, R * .015, 0, 7); ctx.fill();
    }
    form.addEventListener('input', draw);
    form.logo.addEventListener('change', () => {
      const f = form.logo.files[0]; if (!f) return;
      const r = new FileReader();
      r.onload = () => { const im = new Image(); im.onload = () => { logo = im; draw(); tr('logo_preview', { label: 'uploaded' }); }; im.src = r.result; };
      r.readAsDataURL(f);
    });
    form.querySelectorAll('[data-pair]').forEach(b => b.addEventListener('click', () => { const [a, bb] = b.dataset.pair.split(','); form.colA.value = a; form.colB.value = bb; draw(); }));
    document.getElementById('umb-download').addEventListener('click', () => {
      const a = document.createElement('a'); a.download = 'my-logo-umbrella.png'; a.href = cv.toDataURL('image/png'); a.click();
      tr('logo_preview', { label: 'downloaded' });
    });
    document.getElementById('umb-wa').addEventListener('click', e => {
      e.currentTarget.href = waLink(`Hi, I tried the logo preview on your website. I'd like a quote for logo umbrellas.\nCanopy colours: ${form.colA.value} / ${form.colB.value}\nLogo on ${form.panels.value} panel(s)\nQuantity: __\n(I'll send my logo and the preview image here.)`);
      tr('whatsapp_click', { label: 'logo preview' });
    });
    document.fonts && document.fonts.ready.then(draw); draw();
  }
})();
