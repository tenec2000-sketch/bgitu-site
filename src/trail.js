/* Фон «След»: одна линия ведёт через всю страницу. Идёт по полям, у каждой секции
   цепляется за линию заголовка (.sec-head) и пробегает по ней, подсвечивая раздел.
   Вариант задаётся константой VARIANT: 'sled' — пучок светящихся нитей, 'tush' — мазок кистью. */
(() => {
  'use strict';
  const VARIANT = '__VARIANT__';
  const cv = document.querySelector('.trail');
  if (!cv) return;
  const ctx = cv.getContext('2d');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const SHOT = document.documentElement.classList.contains('shot');
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  let W = 0, H = 0, DPR = 1;
  const resize = () => { DPR = Math.min(devicePixelRatio || 1, 1.5); W = innerWidth; H = innerHeight; cv.width = W * DPR; cv.height = H * DPR; };
  addEventListener('resize', resize); resize();

  // цвета — из токенов, как у «шёлка»
  let ACC = '255,90,46', AUX = '255,154,60', INK = '242,242,242';
  const hex = (v) => { v = v.trim().replace('#', ''); if (v.length === 3) v = v.replace(/./g, '$&$&'); const n = parseInt(v, 16); return `${n >> 16 & 255},${n >> 8 & 255},${n & 255}`; };
  const palette = () => { const cs = getComputedStyle(document.documentElement);
    try { ACC = hex(cs.getPropertyValue('--brand-accent')); AUX = hex(cs.getPropertyValue('--brand-aux')); INK = hex(cs.getPropertyValue('--brand-ink')); } catch (e) {} };
  palette();
  addEventListener('bgitu:palette', palette); // переключатель палитры дёргает сразу, без ожидания
  const acc = (a) => `rgba(${ACC},${a})`, aux = (a) => `rgba(${AUX},${a})`, ink = (a) => `rgba(${INK},${a})`;

  // шум с фиксированным сидом: рисунок одинаковый при каждом открытии
  const SEED = 20261105, PERM = new Uint8Array(512);
  const rnd = ((a) => () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; })(SEED);
  for (let i = 0; i < 256; i++) PERM[i] = i;
  for (let i = 255; i > 0; i--) { const j = rnd() * (i + 1) | 0; [PERM[i], PERM[j]] = [PERM[j], PERM[i]]; }
  for (let i = 0; i < 256; i++) PERM[i + 256] = PERM[i];
  const fade = (t) => t * t * (3 - 2 * t);
  const noise = (x, y) => { const X = Math.floor(x) & 255, Y = Math.floor(y) & 255, fx = x - Math.floor(x), fy = y - Math.floor(y);
    const a = PERM[PERM[X] + Y] / 255, b = PERM[PERM[X + 1] + Y] / 255, c = PERM[PERM[X] + Y + 1] / 255, d = PERM[PERM[X + 1] + Y + 1] / 255, u = fade(fx), v = fade(fy);
    return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v; };
  const hash = (i, k) => { const x = Math.sin(i * 12.9898 + k * 78.233 + 3.17) * 43758.5453; return x - Math.floor(x); };
  const STR = [];
  for (let j = 0, M = 16; j < M; j++) STR.push({ f: j / (M - 1) - 0.5, a: 0.2 + rnd() * 0.6, al: 0.14 + rnd() * 0.4, lw: 0.7 + rnd() * 0.8, fray: rnd() < 0.28, k: rnd() * 100 });

  // ---------- путь в координатах документа: свободная лента сверху вниз, за контентом
  let P = [], HEADS = [], SY = 0, gw = 40, wmax = 30, WORD = null;
  // несколько лент: толщина, сдвиг головы (доля экрана), свой рисунок пути, смещение по x
  const LINES = /3$/.test(VARIANT)
    ? [{ sc: 1, lag: 0, seed: 0, dx: 0 }, { sc: 0.55, lag: -0.13, seed: 1, dx: 80 }, { sc: 0.38, lag: 0.09, seed: 2, dx: -110 }]
    : [{ sc: 1, lag: 0, seed: 0, dx: 0 }];
  let CUR = LINES[0];

  function build(T = 0) {
    SY = scrollY; P = [];
    const cont = document.querySelector('.container').getBoundingClientRect();
    gw = Math.max(cont.left, 8);
    wmax = clamp(W * 0.022, 8, 34);
    const push = (x, y) => P.push({ x, y, key: y });
    const catmull = (c, n) => { for (let i = 0; i < c.length - 1; i++) { const p0 = c[i - 1] || c[i], p1 = c[i], p2 = c[i + 1], p3 = c[i + 2] || p2;
      for (let s = 1; s <= n; s++) { const t = s / n, t2 = t * t, t3 = t2 * t;
        const f = (a, b, c2, d) => 0.5 * (2 * b + (-a + c2) * t + (2 * a - 5 * b + 4 * c2 - d) * t2 + (-a + 3 * b - 3 * c2 + d) * t3);
        push(f(p0[0], p1[0], p2[0], p3[0]), f(p0[1], p1[1], p2[1], p3[1])); } } };

    // первый экран: широкий — по просвету между текстом и карточкой и под ней; узкий — справа
    const heroEl = document.querySelector('.hero, .page-hero') || document.querySelector('main');
    const hero = heroEl.getBoundingClientRect(), flow = document.querySelector('.flow');
    const fr = flow ? flow.getBoundingClientRect() : null, ht = hero.top + SY, hb = hero.bottom + SY;
    const wide = fr && fr.top - hero.top < hero.height * 0.4;
    const ctrl = wide
      ? [[fr.left + fr.width * 0.35, -80], [fr.left - 34, ht + hero.height * 0.3], [fr.left + fr.width * 0.25, fr.bottom + SY + 46], [fr.right - 10, fr.bottom + SY + 70]]
      : [[W * 0.97, -80], [W * 0.78, ht + hero.height * 0.25], [W * 0.7, ht + hero.height * 0.6]];
    ctrl.forEach((q, n) => { if (n) q[0] += CUR.dx * (n === ctrl.length - 1 ? 1.4 : 0.6); });
    P.push({ x: ctrl[0][0], y: -80, key: -80 });
    catmull(ctrl, 60);

    // дальше — свободное петляние по всей ширине до призыва
    const cta = document.querySelector('.cta'), c = cta ? cta.getBoundingClientRect() : null;
    const fw = document.querySelector('.footer__word');
    const yEnd = c ? c.top + SY + 60 : fw ? fw.getBoundingClientRect().top + SY - 300 : document.documentElement.scrollHeight;
    const last = P[P.length - 1], fx = (y) => clamp(W * 0.5 + (noise(y * 0.0009, 1.3 + CUR.seed * 11.7) - 0.5) * 2 * W * 0.44 + (noise(y * 0.003, 5.2 + CUR.seed * 7.1) - 0.5) * 36, 20, W - 20);
    for (let y = last.y + 4; y < yEnd; y += 4) { const u = fade(clamp((y - last.y) / 420, 0, 1)); push(last.x + (fx(y) - last.x) * u, y); }
    // финал: линии вливаются в надпись «БГИТУ» в подвале — каждая в свою часть слова
    const word = document.querySelector('.footer__word'), wr = word ? word.getBoundingClientRect() : null, e = P[P.length - 1];
    WORD = null;
    if (wr) {
      const wy = wr.top + SY + wr.height * 0.55, wx = wr.left + wr.width * [0.5, 0.2, 0.8][CUR.seed];
      const mid = c ? [W / 2 + CUR.dx * 0.4, c.bottom + SY - 80] : [(e.x + wx) / 2, (e.y + wy) / 2];
      catmull([[e.x, e.y], mid, [wx + (mid[0] - wx) * 0.2, wy - wr.height * 0.9], [wx, wy]], 60);
      WORD = { el: word, top: wr.top + SY, cy: wy };
    } else if (c) { const b = c.bottom + SY; catmull([[e.x, e.y], [e.x + (W / 2 - e.x) * 0.5, b - 200], [W / 2 + CUR.dx * 0.4, b - 64 - CUR.seed * 18]], 50); }

    // движение в покое: путь медленно колышется волной и дрейфует по шуму — линия живёт и без прокрутки
    const AMP = clamp(W * 0.011, 6, 16);
    for (const q of P) {
      const env = clamp((q.y + 80) / 260, 0, 1);   // у верхнего края старт стоит на месте
      q.x = clamp(q.x + env * (Math.sin(T * 0.55 + q.y * 0.0045 + CUR.seed * 2.1) * AMP
                             + (noise(q.y * 0.002 + T * 0.04, 7 + CUR.seed * 3) - 0.5) * AMP * 1.4), 20, W - 20);
    }
    // длина дуги и нормали
    let s = 0;
    for (let i = 0; i < P.length; i++) { if (i) s += Math.hypot(P[i].x - P[i - 1].x, P[i].y - P[i - 1].y); P[i].s = s; P[i].wf = 1;
      const a = P[Math.max(0, i - 1)], b = P[Math.min(P.length - 1, i + 1)], dx = b.x - a.x, dy = b.y - a.y, l = Math.hypot(dx, dy) || 1;
      P[i].nx = -dy / l; P[i].ny = dx / l; }
    // заголовки разделов: точка загорается, когда след проходит их уровень
    HEADS = [...document.querySelectorAll('.sec-head')].map((el) => ({ el, y: el.getBoundingClientRect().bottom + SY }));
  }

  // ---------- голова следа
  function headIndex() {
    // у конца страницы голова догоняет конец пути — иначе линии не доходят до подвала
    const maxS = document.documentElement.scrollHeight - H, prog = maxS > 0 ? SMS / maxS : 1;
    const kh = SHOT ? Infinity : SMS + H * (0.62 + CUR.lag) + clamp((prog - 0.8) / 0.2, 0, 1) * H * 0.55;   // голова мазка дорастает за сглаженной прокруткой   // в режиме съёмки макета — весь путь
    let i = 0; while (i < P.length - 1 && P[i + 1].key <= kh) i++;
    const a = P[i], b = P[i + 1];
    let head = { x: a.x, y: a.y, s: a.s };
    if (b && b.key > a.key) { const u = clamp((kh - a.key) / (b.key - a.key), 0, 1); head = { x: a.x + (b.x - a.x) * u, y: a.y + (b.y - a.y) * u, s: a.s + (b.s - a.s) * u }; }
    if (!CUR.seed) HEADS.forEach((h) => h.el.classList.toggle('is-lit', head.y >= h.y));
    if (!CUR.seed && WORD) WORD.el.style.setProperty('--fill', clamp((head.y - (WORD.top - 40)) / (WORD.cy - WORD.top + 40), 0, 1).toFixed(3));   // окраска «БГИТУ»
    return { i, kh, head, done: i >= P.length - 1 };
  }
  const onScreen = (p) => p.y - SY > -120 && p.y - SY < H + 120;
  function headDot(h, t) { const k = 0.5 + 0.5 * CUR.sc;
    const x = h.x, y = h.y - SY;
    ctx.fillStyle = acc(0.18); ctx.beginPath(); ctx.arc(x, y, 14 * k, 0, 7); ctx.fill();
    ctx.fillStyle = acc(1); ctx.beginPath(); ctx.arc(x, y, 3.6 * k, 0, 7); ctx.fill();
    ctx.strokeStyle = acc(0.4); ctx.lineWidth = 1; ctx.beginPath(); ctx.arc(x, y, (11 + Math.sin(t * 3) * 3) * k, 0, 7); ctx.stroke();
  }
  // путь из точек [i0..i1] с функцией смещения по нормали; рвётся, где смещение не нужно (skip)
  function strand(i1, head, off, skip) {
    ctx.beginPath(); let on = false;
    for (let i = 0; i <= i1 + 1 && i < P.length; i++) {
      let p = P[i]; if (i === i1 + 1) p = { ...P[i1], x: head.x, y: head.y, s: head.s };
      if (!onScreen(p) || (skip && skip(p))) { on = false; continue; }
      const o = off(p), x = p.x + P[Math.min(i, i1)].nx * o, y = p.y - SY + P[Math.min(i, i1)].ny * o;
      on ? ctx.lineTo(x, y) : ctx.moveTo(x, y); on = true;
    }
  }
  const qpt = (a, c, e, u) => { const v = 1 - u; return [v * v * a[0] + 2 * v * u * c[0] + u * u * e[0], v * v * a[1] + 2 * v * u * c[1] + u * u * e[1]]; };

  // ---------- вариант 1: «След» — пучок светящихся нитей
  function drawSled(t) {
    const { i: hi, head, kh, done } = headIndex();
    const tp = (p) => clamp((head.s - p.s) / 320, 0, 1);
    const w = (p) => wmax * CUR.sc * (0.45 + 0.55 * noise(p.s * 0.0016, 9.1 + CUR.seed * 5)) * p.wf * tp(p);
    // будущий путь — едва заметный пунктир
    if (!CUR.seed) { ctx.setLineDash([2, 9]); } else ctx.setLineDash([0, 1e6]); ctx.strokeStyle = ink(0.1); ctx.lineWidth = 1; ctx.beginPath(); let on = false;
    for (let i = hi; i < P.length; i++) { const p = P[i]; if (!onScreen(p)) { on = false; continue; } on ? ctx.lineTo(p.x, p.y - SY) : ctx.moveTo(p.x, p.y - SY); on = true; }
    ctx.stroke(); ctx.setLineDash([]);
    ctx.globalCompositeOperation = 'lighter';
    // нити
    STR.forEach((S, j) => {
      strand(hi, head, (p) => { const ww = w(p), k = p.wf * tp(p);
        let o = (S.f + S.a * (noise(p.s * 0.004, S.k + CUR.seed * 31) - 0.5)) * 2 * ww + Math.sin(p.s * 0.026 - t * 1.6 + j * 0.4) * 1.5 * k;
        if (S.fray) { const n = noise(p.s * 0.003, S.k + 40); if (n > 0.62) o += (n - 0.62) * Math.min(220, W * 0.12) * Math.sign(S.f || 0.1) * k; }
        return o; }, (p) => p.wf < 0.02);
      ctx.strokeStyle = (CUR.seed === 2 ? j % 2 : j % 5) === 0 ? aux(S.al) : acc(S.al * 0.8); ctx.lineWidth = S.lw; ctx.stroke();
    });
    // хребет
    ctx.globalCompositeOperation = 'source-over';
    if (done) { const p = P[P.length - 1], y = p.y - SY;
      for (let r = 0; r < 3; r++) { const rr = ((t * 22 + r * 30) % 90); ctx.strokeStyle = acc(0.5 * (1 - rr / 90)); ctx.lineWidth = 1; ctx.beginPath(); ctx.arc(p.x, y, rr, 0, 7); ctx.stroke(); } }
    headDot(head, t);
  }

  // ---------- вариант 2: «Тушь» — мазок кистью
  let TT = 0;            // время для «дыхания» мазка
  const TUSH_W = 1.25;   // ширина мазка относительно исходной
  // мазок со свечением: широкий мягкий ореол → ближний ореол → сам мазок с чуть размытыми краями
  const GS = 0.25, gcv = document.createElement('canvas'), gctx = gcv.getContext('2d');
  let glowUsed = false;
  const glowBegin = () => { const w = Math.ceil(W * GS), h = Math.ceil(H * GS);
    if (gcv.width !== w || gcv.height !== h) { gcv.width = w; gcv.height = h; }
    gctx.setTransform(1, 0, 0, 1, 0, 0); gctx.clearRect(0, 0, w, h); gctx.setTransform(GS, 0, 0, GS, 0, 0); glowUsed = false; };
  const glowEnd = () => { if (!glowUsed) return;
    ctx.save(); ctx.globalCompositeOperation = 'destination-over'; ctx.imageSmoothingQuality = 'high'; ctx.drawImage(gcv, 0, 0, W, H); ctx.restore(); };
  function glowFill(path, col) {
    const dark = document.documentElement.dataset.theme !== 'paper';
    // ореол: размытие на маленьком холсте (14px и 5px в полном размере) — в ~16 раз дешевле
    gctx.filter = `blur(${14 * GS}px)`; gctx.fillStyle = col(dark ? 0.24 : 0.12); gctx.fill(path);
    gctx.filter = `blur(${5 * GS}px)`; gctx.fillStyle = col(dark ? 0.28 : 0.16); gctx.fill(path);
    gctx.filter = 'none'; glowUsed = true;
    const a = CUR.seed === 1 ? 0.92 : 0.86;
    ctx.fillStyle = col(a); ctx.fill(path);
    ctx.lineWidth = 1.1; ctx.strokeStyle = col(a * 0.35); ctx.stroke(path);   // мягкий край
  }
  function drawTush(t) {
    TT = t;
    const { i: hi, head, kh, done } = headIndex();
    const tp = (p) => clamp((head.s - p.s) / 90, 0, 1);
    const bw = (p) => ((1.2 + Math.min(8, W * 0.006) * Math.pow(noise(p.s * 0.004 - TT * 0.06, 21 + CUR.seed * 9), 1.5)) * p.wf * tp(p) + 0.5) * (0.4 + 0.6 * CUR.sc) * TUSH_W;
    if (!CUR.seed) { ctx.setLineDash([2, 9]); } else ctx.setLineDash([0, 1e6]); ctx.strokeStyle = ink(0.1); ctx.lineWidth = 1; ctx.beginPath(); let on = false;
    for (let i = hi; i < P.length; i++) { const p = P[i]; if (!onScreen(p)) { on = false; continue; } on ? ctx.lineTo(p.x, p.y - SY) : ctx.moveTo(p.x, p.y - SY); on = true; }
    ctx.stroke(); ctx.setLineDash([]);
    // основной мазок: заливка между двумя краями, по видимым кускам
    let L = [], Rr = [];
    const flush = () => { if (L.length > 1) { const path = new Path2D(); L.forEach((q, i) => i ? path.lineTo(q[0], q[1]) : path.moveTo(q[0], q[1]));
      for (let i = Rr.length - 1; i >= 0; i--) path.lineTo(Rr[i][0], Rr[i][1]); path.closePath(); glowFill(path, CUR.seed === 1 ? acc : ink); } L = []; Rr = []; };
    for (let i = 0; i <= hi + 1 && i < P.length; i++) {
      let p = P[i]; const n = P[Math.min(i, hi)]; if (i === hi + 1) p = { ...P[hi], x: head.x, y: head.y, s: head.s, wf: P[hi].wf };
      if (!onScreen(p)) { flush(); continue; }
      const w = bw(p); L.push([p.x - n.nx * w, p.y - SY - n.ny * w]); Rr.push([p.x + n.nx * w, p.y - SY + n.ny * w]);
    }
    flush();
    // сухая кисть
    for (let j = 0; j < Math.round(8 * CUR.sc); j++) {
      strand(hi, head, (p) => (j / 7 - 0.5) * 2 * (bw(p) * 1.9 + 2 * p.wf), (p) => p.wf < 0.05 || noise(p.s * 0.012 - TT * 0.18, j * 5.3 + 2) < 0.5);
      ctx.strokeStyle = CUR.seed === 1 ? acc(0.35) : ink(0.32); ctx.lineWidth = 0.7; ctx.stroke();
    }
    // брызги: привязаны к высоте на странице (не к длине линии — она меняется, когда линия колышется)
    // и ставятся плавно между точками пути, поэтому едут вместе с мазком без перескоков
    const STEP = 22;
    for (let k = 1, yy = Math.ceil(P[0].y / STEP) * STEP; k < P.length; yy += STEP) {
      while (k < P.length && P[k].y < yy) k++;
      if (k >= P.length) break;
      const a = P[k - 1], b = P[k]; if (b.y <= a.y) continue;
      const u = (yy - a.y) / (b.y - a.y), sv = a.s + (b.s - a.s) * u;
      if (sv > head.s) break;
      const i = Math.round(yy / STEP);
      if (hash(i + CUR.seed * 101, 1) < 0.83 + 0.08 * CUR.seed) continue;
      const wf = a.wf + (b.wf - a.wf) * u; if (wf < 0.3) continue;
      const x = a.x + (b.x - a.x) * u, y = yy - SY; if (y < -60 || y > H + 60) continue;
      let nx = a.nx + (b.nx - a.nx) * u, ny = a.ny + (b.ny - a.ny) * u; const nl = Math.hypot(nx, ny) || 1; nx /= nl; ny /= nl;
      const o = (hash(i, 2) - 0.5) * 110 * TUSH_W * wf;
      ctx.fillStyle = ink(0.7); ctx.beginPath(); ctx.arc(x + nx * o, y + ny * o, (0.6 + hash(i, 3) * 2.2) * TUSH_W, 0, 7); ctx.fill();
      if (hash(i, 6) > 0.6) { ctx.beginPath(); ctx.arc(x + nx * o + (hash(i, 7) - 0.5) * 12, y + ny * o + (hash(i, 8) - 0.5) * 12, 0.55, 0, 7); ctx.fill(); }
    }
    if (done) { const p = P[P.length - 1]; ctx.save(); ctx.shadowColor = acc(0.9); ctx.shadowBlur = 18; ctx.fillStyle = acc(1); ctx.beginPath(); ctx.arc(p.x, p.y - SY, (4 + Math.sin(t * 2) * 0.8) * TUSH_W, 0, 7); ctx.fill(); ctx.restore(); }
    else { ctx.save(); ctx.shadowColor = (CUR.seed === 1 ? acc : ink)(0.9); ctx.shadowBlur = 14; ctx.fillStyle = (CUR.seed === 1 ? acc : ink)(0.95); ctx.beginPath(); ctx.arc(head.x, head.y - SY, 2.6 * TUSH_W, 0, 7); ctx.fill(); ctx.restore(); }
  }

  const draw = VARIANT.startsWith('tush') ? drawTush : drawSled;

  // ---------- частицы: редкая «пыль» за мазками (только «Тушь ×3»)
  const DUST = VARIANT === 'tush3';
  let PARTS = [];
  const seedParts = () => {
    const n = clamp(Math.round(W * H / 24000), 24, 80);
    PARTS = Array.from({ length: n }, () => { const z = 0.25 + Math.random() * 0.75, c = Math.random();
      return { x: Math.random() * W, y: Math.random() * H, z, r: 0.5 + z * 1.3, a: 0.1 + 0.32 * z,
        vx: (Math.random() - 0.5) * 0.06, vy: -(0.04 + Math.random() * 0.16) * z, ph: Math.random() * 6.28,
        col: c < 0.1 ? 'acc' : c < 0.22 ? 'aux' : 'ink', glow: Math.random() < 0.12 }; });
  };
  function drawDust(t) {
    if (!PARTS.length) seedParts();
    const span = H + 40;
    for (const p of PARTS) {
      const tt = reduce ? 0 : t;   // 60 = прежняя скорость «на кадр» при 60 кадрах в секунду
      const px = p.x + p.vx * 60 * tt + Math.sin(tt * 0.3 + p.ph) * 3.2, py = p.y + p.vy * 60 * tt;
      const x = ((px % (W + 20)) + W + 20) % (W + 20) - 10;
      const y = (((py - SMS * 0.25 * p.z) % span) + span) % span - 20;   // глубина: дальние медленнее при скролле
      const a = p.a * (0.65 + 0.35 * Math.sin(t * 0.7 + p.ph));
      const col = p.col === 'acc' ? acc : p.col === 'aux' ? aux : ink;
      if (p.glow) { ctx.fillStyle = col(a * 0.18); ctx.beginPath(); ctx.arc(x, y, p.r * 4, 0, 7); ctx.fill(); }
      ctx.fillStyle = col(a); ctx.beginPath(); ctx.arc(x, y, p.r, 0, 7); ctx.fill();
    }
  }
  addEventListener('resize', () => { PARTS = []; });

  // сглаженная прокрутка: колесо листает скачками, а частицы и голова мазка догоняют плавно (инерция ~0.2 с)
  let SMS = scrollY, lastNow = performance.now();
  const smoothScroll = (now) => {
    const dt = Math.min(0.1, (now - lastNow) / 1000); lastNow = now;
    const d = scrollY - SMS;
    SMS = reduce || Math.abs(d) < 0.05 ? scrollY : SMS + d * (1 - Math.exp(-dt * 9));
  };
  const t0 = performance.now(); let frame = 0;
  const loop = () => {
    if (!document.hidden) {
      ctx.setTransform(DPR, 0, 0, DPR, 0, 0); ctx.clearRect(0, 0, W, H);
      ctx.lineJoin = 'round'; ctx.lineCap = 'round';
      const now = performance.now(); smoothScroll(now);
      const t = reduce ? 0 : (now - t0) / 1000;
      if (DUST) drawDust(t);
      glowBegin();
      for (const L of LINES) { CUR = L; build(t); draw(t); }
      glowEnd();
      if (++frame % 120 === 0) palette();
    }
    requestAnimationFrame(loop);
  };
  requestAnimationFrame(loop);
})();
