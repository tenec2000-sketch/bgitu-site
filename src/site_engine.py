"""Движок сайта БГИТУ: берёт макет команды (стили, шапка, поиск, футер, скрипты) и собирает страницы.
Общие правки: темы (Бумага по умолчанию, Сурик/Латунь — тёмные), фон «Тушь ×3» с пылью, плавное
появление текста, липкая плашка раздела, навигация по страницам."""
import re

SRC = None  # исходный макет


def load(path):
    global SRC
    SRC = open(path, encoding='utf-8').read()


def cut(s, a, b, inclusive_b=False):
    i = s.index(a)
    j = s.index(b, i)
    return s[i:j + (len(b) if inclusive_b else 0)]


# ---------------------------------------------------------------- навигация
NAV = [('university.html', 'Университет', 'о вузе история руководство структура документы'),
       ('institutes.html', 'Институты', 'факультеты кафедры подразделения колледж'),
       ('admission.html', 'Поступление', 'абитуриенту приёмная комиссия направления документы'),
       ('campus.html', 'Кампус', 'корпуса общежития стадион столовая ботанический сад'),
       ('news.html', 'Новости', 'события объявления'),
       ('contacts.html', 'Контакты', 'адрес телефон почта связаться')]


def nav_ul(cur):
    li = ''.join(f'<li><a href="{h}"{" aria-current=" + chr(34) + "page" + chr(34) if h == cur else ""} data-s="Раздел" data-k="{k}">{n}</a></li>'
                 for h, n, k in NAV)
    return f'<ul>{li}</ul>'


THEMES = [('paper', 'Бумага', 'светлая · киноварь', '#b8322a', '#f2eee6'),
          ('surik', 'Сурик', 'тёмная · красно-оранжевый', '#ff5a2e', '#0d0d0d'),
          ('latun', 'Латунь', 'тёмная · золото', '#d6b072', '#0d0d0d')]


def theme_opts():
    return ''.join(f'<button type="button" role="radio" aria-checked="false" data-theme-set="{k}">'
                   f'<i style="--a:{a};--b:{b}" aria-hidden="true"></i><span><b>{n}</b><small>{d}</small></span></button>'
                   for k, n, d, a, b in THEMES)


THEME_BTN = ('<button class="theme-btn" type="button" popovertarget="theme-pop" aria-label="Оформление сайта">'
             '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8" fill="none" stroke="currentColor" stroke-width="2"/>'
             '<path d="M12 4a8 8 0 0 1 0 16z" fill="currentColor"/></svg><span>Тема</span></button>')

THEME_POP = (f'<div class="theme-pop" id="theme-pop" popover aria-label="Оформление сайта">'
             f'<p class="mono dim">оформление</p><div role="radiogroup" aria-label="Тема">{theme_opts()}</div>'
             f'<p class="theme-pop__note">Выбор сохранится в этом браузере</p></div>')

SECBAR = '<div class="secbar" aria-hidden="true" hidden><div class="container secbar__slot"></div></div>'

HEAD_JS = """<script>
/* тема до первой отрисовки: ?theme= (для макетов) → сохранённый выбор → «Бумага» по умолчанию */
(() => { const r = document.documentElement, q = new URLSearchParams(location.search);
  let t = q.get('theme'); try { t = t || localStorage.getItem('bgitu-theme'); } catch (e) {}
  if (['paper', 'surik', 'latun'].includes(t)) r.dataset.theme = t;
  if (q.has('shot')) r.classList.add('shot'); })();
</script>
"""

# ---------------------------------------------------------------- стили
CSS = r"""
/* ================= ТЕМЫ: меняются только брендовые токены ================= */
html[data-theme="paper"] { --brand-base: #f2eee6; --brand-ink: #171614; --brand-accent: #b8322a; --brand-on-accent: #ffffff; --brand-aux: #8c6b3f; --aurora-blend: multiply; color-scheme: light; }
html[data-theme="surik"] { --brand-base: #0d0d0d; --brand-ink: #f2f2f2; --brand-accent: #ff5a2e; --brand-on-accent: #0d0d0d; --brand-aux: #ff9a3c; color-scheme: dark; }
html[data-theme="latun"] { --brand-base: #0d0d0d; --brand-ink: #f2f2f2; --brand-accent: #d6b072; --brand-on-accent: #0d0d0d; --brand-aux: #f0d49a; color-scheme: dark; }
html[data-theme="paper"] .glass { box-shadow: 0 24px 60px rgb(0 0 0 / 0.08); }
html[data-theme="paper"] .search { box-shadow: 0 30px 80px rgb(0 0 0 / 0.12), 0 0 0 6px var(--accent-soft); }
html.theme-anim, html.theme-anim * { transition: background-color 0.45s, color 0.45s, border-color 0.45s, fill 0.45s !important; }

/* ================= Фон «Тушь ×3»: единый, под контентом ================= */
/* насколько заметны линии фона: 1 — как было, меньше — спокойнее */
:root { --trail-op: 0.5; }
html[data-theme="paper"] { --trail-op: 0.42; }
.trail { position: fixed; inset: 0; z-index: 0; width: 100%; height: 100%; max-width: none; pointer-events: none; opacity: var(--trail-op); }
main, .footer { position: relative; z-index: 1; }
.section--raised { background: transparent; border-block: 0; }
.cta { border-top: 0; }
.cta__shade { display: none; }
.hero__shade { background: linear-gradient(90deg, color-mix(in oklab, var(--bg) 70%, transparent) 0%, transparent 55%); }
main :is(h1, h2, h3, h4, p, dt, dd, time, li, .statement, .inst__note, .inst__idx, .mono) { text-shadow: 0 0 4px var(--bg), 0 0 14px var(--bg); }
main :is(.btn, .btn *, .inst__row:hover *, .inst.is-open .inst__row *, .flow__n, .chips button[aria-pressed="true"]), main :is(.tile, .card, .person, .feature) * { text-shadow: none; }

/* ================= Шапка: кнопка темы и окно выбора ================= */
kbd { white-space: nowrap; }
.theme-btn { display: inline-flex; align-items: center; gap: 0.6em; min-height: 44px; padding: 0 0.95em; border: 1px solid var(--line); border-radius: var(--radius-pill);
  color: var(--text-muted); font-size: 0.875rem; font-weight: 500; transition: color var(--dur-fast), border-color var(--dur-fast), background var(--dur-fast); }
.theme-btn:hover { color: var(--text); border-color: var(--line-strong); background: var(--line); }
.theme-btn svg { width: 16px; height: 16px; flex: none; }
.theme-pop { position: fixed; inset: calc(12px + var(--head-h) + 8px) max(12px, calc((100vw - var(--container)) / 2)) auto auto; margin: 0; width: 290px; padding: 14px;
  color: var(--text); background: var(--bg-raised); border: 1px solid var(--line-strong); border-radius: var(--radius-m); box-shadow: 0 30px 80px rgb(0 0 0 / 0.25); }
.theme-pop:popover-open { animation: pop 0.22s var(--ease); }
.theme-pop > .mono { padding: 2px 6px 10px; }
.theme-pop [role="radiogroup"], .menu-theme { display: grid; gap: 4px; }
.theme-pop button, .menu-theme button { display: grid; grid-template-columns: 30px 1fr 16px; gap: 12px; align-items: center; width: 100%; min-height: 52px; padding: 6px 10px; border-radius: var(--radius-s); transition: background var(--dur-fast); }
.theme-pop button:hover, .menu-theme button:hover { background: var(--line); }
.theme-pop button::after, .menu-theme button::after { content: ""; width: 8px; height: 8px; border-radius: 50%; justify-self: center; }
.theme-pop button[aria-checked="true"]::after, .menu-theme button[aria-checked="true"]::after { background: var(--accent); box-shadow: 0 0 10px var(--accent-glow); }
.theme-pop i, .menu-theme i { width: 30px; height: 30px; border-radius: 50%; background: conic-gradient(var(--a) 0 50%, var(--b) 0); box-shadow: inset 0 0 0 1px var(--line-strong); }
.theme-pop b, .menu-theme b { display: block; font-weight: 600; line-height: 1.2; }
.theme-pop small, .menu-theme small { display: block; color: var(--text-muted); font-size: 0.8125rem; line-height: 1.3; }
.theme-pop__note { padding: 10px 6px 2px; color: var(--text-faint); font-size: 0.8125rem; }
.menu-theme { margin-top: 28px; padding-top: 20px; border-top: 1px solid var(--line); }
.menu-theme > .mono { margin-bottom: 6px; color: var(--text-faint); }
.menu .menu-theme button { padding: 6px 4px; border-bottom: 0; font: inherit; }
@media (max-width: 1180px) { .nav, .head-actions .btn { display: none; } .burger { display: block; } .head-actions { margin-left: auto; } }
@media (max-width: 640px) { .theme-btn span { display: none; } .theme-btn { width: 44px; justify-content: center; padding: 0; } }

/* ================= Заголовки разделов + липкая плашка ================= */
html { scroll-padding-top: calc(var(--head-h) + 96px); }
.sec-head { align-items: baseline; }
.sec-head h2 { white-space: nowrap; color: var(--text); }
.sec-head > :last-child { text-align: right; }
.sec-head h2::before { content: ""; display: inline-block; flex: none; width: 7px; height: 7px; margin-right: 0.9em; vertical-align: 0.1em; border-radius: 50%;
  background: var(--accent); box-shadow: 0 0 12px var(--accent-glow); }
/* плашка = точная копия заголовка раздела: встаёт на его место пиксель в пиксель, следующий заголовок выталкивает её вверх */
.secbar { position: fixed; inset: 0 0 auto; z-index: 45; pointer-events: none; padding-top: calc(12px + var(--head-h) + 22px); background: var(--bg); will-change: transform; }
.secbar[hidden] { display: none; }
.secbar .sec-head { margin-bottom: 0; }
/* переход по якорю к разделу ставит его заголовок ровно на место плашки: 12 + шапка + 22 − отступ html − верхний padding секции */
main section.section[id] { scroll-margin-top: calc(34px - 96px - clamp(72px, 11vw, 150px)); }
.js .sec-head[data-reveal] { transform: none; }   /* без сдвига: плашка должна совпадать с заголовком даже при быстрой прокрутке */

/* ================= Текущая страница в шапке — акцентом палитры ================= */
.nav a[aria-current="page"] { color: var(--accent); background: var(--accent-soft); }
.nav a[aria-current="page"]:hover { color: var(--accent); background: color-mix(in oklab, var(--brand-accent) 22%, transparent); }
.menu a[aria-current="page"] { color: var(--accent); }
.menu a[aria-current="page"]::before { content: ""; display: inline-block; width: 8px; height: 8px; margin-right: 0.6em; vertical-align: 0.15em; border-radius: 50%; background: var(--accent); box-shadow: 0 0 10px var(--accent-glow); }

/* ================= Плавное появление текста ================= */
.js .split .w { display: inline-block; opacity: 0; transform: translateY(0.45em); transition: opacity 0.9s var(--ease), transform 0.9s var(--ease);
  transition-delay: calc(var(--d, 0) * 90ms + var(--w) * 40ms); }
.js .split.is-in .w { opacity: 1; transform: none; }
.js [data-reveal].split { opacity: 1; transform: none; }
@media (prefers-reduced-motion: reduce) { .js .split .w { opacity: 1; transform: none; } }

/* ================= «Путь абитуриента»: шаги — ссылки ================= */
.flow__steps li { display: block; padding: 0; }
.flow__steps li > a { display: grid; grid-template-columns: 2.5rem 1fr; gap: 14px; align-items: center; padding: 16px 0; border-radius: var(--radius-s); }
.flow__steps:hover li, .flow__steps:focus-within li { animation: none; opacity: 0.5; }
.flow__steps:hover .flow__n, .flow__steps:focus-within .flow__n { animation: none; background: transparent; }
.flow__steps li:hover, .flow__steps li:focus-within { opacity: 1 !important; }
.flow__steps li:hover .flow__n, .flow__steps li:focus-within .flow__n { background: var(--accent) !important; color: var(--accent-ink); border-color: var(--accent); box-shadow: 0 0 22px var(--accent-glow); }
.flow__steps li > a::after { content: "→"; grid-column: 2; justify-self: end; margin-top: -2.4em; color: var(--accent); opacity: 0; transform: translateX(-6px); transition: opacity var(--dur), transform var(--dur) var(--ease); }
.flow__steps li:hover > a::after, .flow__steps li > a:focus-visible::after { opacity: 1; transform: none; }
.steps li:target { animation: rowflash 2.4s var(--ease); }
.steps li:target .step-n { animation: numflash 2.4s var(--ease); }
@keyframes rowflash { 0%, 35% { background: var(--accent-soft); } 100% { background: transparent; } }
@keyframes numflash { 0%, 30% { text-shadow: 0 0 28px var(--accent-glow); transform: translateX(6px); } }

/* ================= Новости (строки) ================= */
.news { border-top: 1px solid var(--line); }
.news a { display: grid; grid-template-columns: 9rem minmax(0, 1fr) auto; gap: 24px; align-items: baseline; padding: 26px 0; border-bottom: 1px solid var(--line); transition: color var(--dur-fast); }
.news time { color: var(--accent); }
.news h3 { font: 600 clamp(1.0625rem, 0.9rem + 0.6vw, 1.5rem)/1.25 var(--font-display); letter-spacing: -0.01em; text-wrap: balance; transition: transform var(--dur) var(--ease); }
.news .dim { white-space: nowrap; }
.news a:hover h3 { color: var(--accent); transform: translateX(8px); }
.sec-head a.dim:hover, .more a:hover { color: var(--accent); }
.more { display: flex; justify-content: flex-end; margin-top: clamp(28px, 4vw, 48px); }
.more a { display: inline-flex; align-items: center; gap: 0.6em; min-height: 44px; color: var(--accent); }
.more a span { transition: transform var(--dur) var(--ease); }
.more a:hover span { transform: translateX(4px); }

/* ================= Внутренние страницы ================= */
.page-hero { position: relative; padding: calc(var(--head-h) + clamp(88px, 12vw, 150px)) 0 clamp(56px, 8vw, 96px); }
.crumbs { display: flex; flex-wrap: wrap; gap: 0.6em; margin-bottom: 28px; color: var(--text-faint); }
.crumbs a { color: var(--text-muted); } .crumbs a:hover { color: var(--accent); }
.page-hero h1 { max-width: 16em; margin: 24px 0 24px; font: 800 clamp(2.25rem, 0.9rem + 4.2vw, 5rem)/1.04 var(--font-display); letter-spacing: -0.03em; text-wrap: balance; }
.page-hero h1.long { max-width: 22em; font-size: clamp(2rem, 1rem + 2.8vw, 3.75rem); }
.page-hero__lead { max-width: 58ch; color: var(--text-muted); font-size: var(--fs-lead); line-height: 1.55; }
.page-hero .hero__cta { margin-top: 32px; }
.meta-row { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 32px; }
.meta-row > * { display: inline-flex; align-items: center; gap: 0.6em; min-height: 40px; padding: 0 1.1em; border: 1px solid var(--line-strong); border-radius: var(--radius-pill); color: var(--text-muted); background: var(--bg-glass); backdrop-filter: blur(10px); }
.meta-row a:hover { color: var(--accent); border-color: var(--accent); }
.meta-row b { color: var(--text); font-weight: 600; }
@media (max-width: 640px) { .meta-row > * { min-height: 0; padding: 9px 1.1em; border-radius: 22px; line-height: 1.35; } }
.lead-2 { max-width: 46ch; color: var(--text-muted); font-size: var(--fs-lead); line-height: 1.55; }
.split-layout { display: grid; grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr); gap: clamp(32px, 6vw, 96px); align-items: start; }
.split-layout > .sticky { position: sticky; top: calc(var(--head-h) + 110px); }
.split-layout h3.big { font: 800 clamp(1.75rem, 1rem + 2.2vw, 3rem)/1.08 var(--font-display); letter-spacing: -0.025em; text-wrap: balance; overflow-wrap: anywhere; hyphens: auto; }
.adm__intro { top: calc(var(--head-h) + 110px); }
.split-layout h3.big + p { margin-top: 24px; }

/* карточки */
.cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; }
.card { position: relative; isolation: isolate; overflow: hidden; display: flex; flex-direction: column; gap: 10px; min-height: 200px; padding: 24px;
  border: 1px solid var(--line); border-radius: var(--radius-m); background: var(--bg-panel); transition: border-color var(--dur), transform var(--dur) var(--ease); }
.card::before { content: ""; position: absolute; inset: 0; z-index: -1; background: radial-gradient(80% 90% at 100% 0%, var(--accent-soft), transparent 70%); opacity: 0; transition: opacity var(--dur); }
.card .mono { color: var(--accent); }
.card h3 { font: 600 clamp(1.125rem, 1rem + 0.5vw, 1.375rem)/1.22 var(--font-display); letter-spacing: -0.01em; text-wrap: balance; }
.card p { color: var(--text-muted); font-size: 0.9375rem; line-height: 1.45; }
.card .go { margin-top: auto; padding-top: 12px; color: var(--accent); font-weight: 600; font-size: 0.9375rem; }
a.card:hover { border-color: var(--line-strong); transform: translateY(-3px); }
a.card:hover::before { opacity: 1; }
.card--num .num { font: 800 clamp(2.25rem, 1.4rem + 2.4vw, 3.5rem)/1 var(--font-display); letter-spacing: -0.04em; }

/* люди */
.people { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 16px; }
.person { display: grid; grid-template-columns: 64px 1fr; gap: 16px; align-items: center; padding: 20px; border: 1px solid var(--line); border-radius: var(--radius-m); background: var(--bg-panel); }
.person--lead { grid-column: 1 / -1; grid-template-columns: 96px 1fr; padding: 28px; }
.ava { display: grid; place-items: center; width: 64px; aspect-ratio: 1; border-radius: 50%; border: 1px solid var(--line-strong); color: var(--accent); font: 600 1.125rem/1 var(--font-display);
  background: radial-gradient(70% 70% at 30% 20%, var(--accent-soft), transparent 70%), var(--bg-raised); }
.person--lead .ava { width: 96px; font-size: 1.75rem; }
.person b { display: block; font-weight: 600; line-height: 1.3; }
.person--lead b { font: 600 clamp(1.25rem, 1rem + 1vw, 1.875rem)/1.2 var(--font-display); letter-spacing: -0.01em; }
.person small { display: block; margin-top: 4px; color: var(--text-muted); font-size: 0.875rem; line-height: 1.4; }

/* вертикальная хронология */
.vtl li { position: relative; display: grid; grid-template-columns: 7.5rem 1fr; gap: 24px; padding: 0 0 36px 28px; border-left: 1px solid var(--line-strong); }
.vtl li:last-child { padding-bottom: 0; }
.vtl li::before { content: ""; position: absolute; left: -4px; top: 0.55em; width: 7px; height: 7px; border-radius: 50%; background: var(--accent); box-shadow: 0 0 14px var(--accent-glow); }
.vtl time { font: 700 1.5rem/1.1 var(--font-display); }
.vtl b { display: block; font-weight: 600; line-height: 1.35; }
.vtl p { margin-top: 4px; color: var(--text-muted); font-size: 0.9375rem; line-height: 1.5; }

/* направления */
.chips { display: flex; flex-wrap: wrap; gap: 8px; }
.chips button { min-height: 40px; padding: 0 1.1em; border: 1px solid var(--line-strong); border-radius: var(--radius-pill); color: var(--text-muted); font: 500 var(--fs-mono)/1 var(--font-mono); letter-spacing: 0.08em; text-transform: uppercase; transition: color var(--dur-fast), background var(--dur-fast), border-color var(--dur-fast); }
.chips button:hover { color: var(--text); border-color: var(--text-muted); }
.chips button[aria-pressed="true"] { background: var(--accent); border-color: var(--accent); color: var(--accent-ink); }
.filter-bar { display: flex; flex-wrap: wrap; gap: 12px 24px; align-items: center; justify-content: space-between; margin-bottom: 24px; }
.filter-bar input { min-width: min(320px, 100%); min-height: 44px; padding: 0 1.1em; border: 1px solid var(--line-strong); border-radius: var(--radius-pill); color: var(--text); background: var(--bg-glass); font: inherit; }
.filter-bar input::placeholder { color: var(--text-faint); }
.dirs { border-top: 1px solid var(--line); }
.dirs li { display: grid; grid-template-columns: 7rem minmax(0, 1fr) 11rem 9rem; gap: 20px; align-items: baseline; padding: 18px 0; border-bottom: 1px solid var(--line); transition: color var(--dur-fast); }
.dirs li > .mono:first-child { color: var(--accent); }
.dirs b { font-weight: 600; line-height: 1.35; }
.dirs b small { display: block; margin-top: 4px; color: var(--text-muted); font-weight: 400; font-size: 0.875rem; line-height: 1.4; }
.filter-bar .chips + .chips { padding-left: 12px; border-left: 1px solid var(--line); }
@media (max-width: 640px) { .filter-bar .chips + .chips { padding-left: 0; border-left: 0; } }
.dirs .dim { text-align: right; }
.dirs li[hidden] { display: none; }
.dirs__empty { padding: 24px 0; color: var(--text-muted); }

/* кафедры */
.deps { border-top: 1px solid var(--line); }
.deps li { display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); gap: 16px 40px; padding: 26px 0; border-bottom: 1px solid var(--line); }
.deps h3 { font: 600 clamp(1.0625rem, 0.95rem + 0.5vw, 1.375rem)/1.25 var(--font-display); letter-spacing: -0.01em; text-wrap: balance; }
.deps .who { margin-top: 6px; color: var(--text-muted); }
.deps .c { display: flex; flex-direction: column; gap: 4px; color: var(--text-muted); font-size: 0.9375rem; }
.deps .c a { width: fit-content; color: var(--text); border-bottom: 1px solid var(--line-strong); }
.deps .c a:hover { color: var(--accent); border-color: var(--accent); }

/* вопросы */
.faq { border-top: 1px solid var(--line); }
.faq details { border-bottom: 1px solid var(--line); }
.faq summary { display: grid; grid-template-columns: minmax(0, 1fr) 2.5rem; gap: 20px; align-items: center; min-height: 44px; padding: 24px 0; cursor: pointer; list-style: none;
  font: 600 clamp(1.0625rem, 0.95rem + 0.5vw, 1.375rem)/1.3 var(--font-display); letter-spacing: -0.01em; }
.faq summary::-webkit-details-marker { display: none; }
.faq summary::after { content: "+"; display: grid; place-items: center; width: 2.5rem; height: 2.5rem; border: 1px solid var(--line-strong); border-radius: 50%; font: 400 1.25rem/1 var(--font-text); transition: transform var(--dur) var(--ease), color var(--dur), border-color var(--dur); }
.faq details[open] summary::after { transform: rotate(45deg); color: var(--accent); border-color: var(--accent); }
.faq summary:hover { color: var(--accent); }
.faq details > div { max-width: 66ch; padding: 0 3.5rem 26px 0; color: var(--text-muted); }
.faq details > div a { color: var(--text); border-bottom: 1px solid var(--line-strong); }

/* карта-заглушка */
.map { position: relative; isolation: isolate; overflow: hidden; min-height: 380px; border: 1px solid var(--line); border-radius: var(--radius-m); background: var(--bg-panel); }
.map::before { content: ""; position: absolute; inset: 0; z-index: -1; opacity: 0.8;
  background: linear-gradient(var(--line) 1px, transparent 1px) 0 0 / 40px 40px, linear-gradient(90deg, var(--line) 1px, transparent 1px) 0 0 / 40px 40px; }
.map svg.roads { position: absolute; inset: 0; width: 100%; height: 100%; color: var(--line-strong); }
.pin { position: absolute; display: flex; align-items: center; gap: 10px; translate: -7px -7px; }
.pin i { width: 14px; height: 14px; border-radius: 50%; background: var(--accent); box-shadow: 0 0 0 6px var(--accent-soft), 0 0 24px var(--accent-glow); }
.pin span { padding: 6px 12px; border: 1px solid var(--line-strong); border-radius: var(--radius-pill); background: var(--bg-glass); backdrop-filter: blur(10px); font-size: 0.875rem; white-space: nowrap; }
.map__links { position: absolute; left: 20px; bottom: 20px; display: flex; flex-wrap: wrap; gap: 8px; }

/* статья */
.prose { max-width: 68ch; }
.prose > * + * { margin-top: 1.1em; }
.prose p { font-size: 1.0625rem; line-height: 1.7; }
.prose .lead-p { font-size: var(--fs-lead); line-height: 1.55; color: var(--text); }
.prose h2 { margin-top: 1.8em; font: 600 clamp(1.25rem, 1rem + 1vw, 1.75rem)/1.25 var(--font-display); letter-spacing: -0.01em; }
.prose blockquote { margin: 1.6em 0; padding: 4px 0 4px 24px; border-left: 3px solid var(--accent); font: 600 clamp(1.125rem, 1rem + 0.6vw, 1.5rem)/1.35 var(--font-display); }
.figure { display: grid; place-items: center; aspect-ratio: 16 / 9; margin: 1.8em 0; border: 1px dashed var(--line-strong); border-radius: var(--radius-m); color: var(--text-faint); background: var(--bg-panel); }
.note { padding: 14px 18px; border: 1px solid var(--line-strong); border-radius: var(--radius-s); color: var(--text-muted); font-size: 0.9375rem; }
.share { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 40px; padding-top: 24px; border-top: 1px solid var(--line); }

/* главная новость */
.feature { position: relative; isolation: isolate; overflow: hidden; display: grid; gap: 18px; align-content: end; min-height: 360px; padding: clamp(24px, 4vw, 48px);
  border: 1px solid var(--line); border-radius: var(--radius-l); background: var(--bg-panel); transition: border-color var(--dur); }
.feature::before { content: ""; position: absolute; inset: 0; z-index: -1; background: radial-gradient(70% 90% at 90% 0%, var(--accent-soft), transparent 70%), radial-gradient(60% 80% at 0% 100%, var(--aux-soft), transparent 70%); }
.feature .mono { color: var(--accent); }
.feature h2 { max-width: 20em; font: 800 clamp(1.75rem, 1rem + 2.6vw, 3.25rem)/1.08 var(--font-display); letter-spacing: -0.025em; text-wrap: balance; }
.feature p { max-width: 56ch; color: var(--text-muted); }
.feature:hover { border-color: var(--line-strong); }
.inst__go::before { width: 10px; height: 10px; margin: -5px 0 0 -7px; background: none; border: solid currentColor; border-width: 2px 2px 0 0; transform: rotate(45deg); }
.inst__go::after { display: none; }

@media (max-width: 1100px) { .split-layout { grid-template-columns: 1fr; } .split-layout > .sticky { position: static; } }
@media (max-width: 1000px) { .dirs li { grid-template-columns: 6rem minmax(0, 1fr); } .dirs .dim { grid-column: 2; text-align: left; } .deps li { grid-template-columns: 1fr; } }
@media (max-width: 640px) {
  .news a { grid-template-columns: 1fr; gap: 8px; }
  .vtl li { grid-template-columns: 1fr; gap: 6px; }
  .person--lead { grid-template-columns: 64px 1fr; padding: 20px; } .person--lead .ava { width: 64px; font-size: 1.125rem; }
  .dirs li { grid-template-columns: 1fr; gap: 6px; } .dirs .dim { grid-column: 1; }
  .faq details > div { padding-right: 0; }
  .map { min-height: 300px; }
}

/* ================= «БГИТУ» в подвале: линии вливаются и окрашивают надпись ================= */
.footer__word { position: relative; }
.footer__word::after { content: attr(data-text); position: absolute; inset: 0; pointer-events: none; color: transparent;
  background: linear-gradient(90deg, var(--text) 0%, var(--accent) 50%, var(--text) 100%); -webkit-background-clip: text; background-clip: text;
  opacity: calc(var(--fill, 0) * 0.85); clip-path: inset(0 calc((1 - var(--fill, 0)) * 50%)); }

/* ================= Режим съёмки макетов (?shot) ================= */
html.shot { scroll-behavior: auto; }
html.shot .hero { min-height: 900px; }
html.shot .site-head { position: absolute; }
html.shot .secbar, html.shot .theme-pop, html.shot .scroll-cue { display: none; }
html.shot [data-reveal], html.shot .split .w { opacity: 1 !important; transform: none !important; transition: none !important; }
html.shot .fact::after { transform: none !important; }
html.shot .adm__intro, html.shot .split-layout > .sticky { position: static; }
"""

# ---------------------------------------------------------------- скрипты
REVEAL_JS = r"""<script>
/* Плавное появление текста: блоки — снизу вверх по очереди, крупные заголовки — по словам.
   Запускается до основного скрипта макета, тот подхватывает [data-reveal] своим IntersectionObserver. */
(() => {
  if (document.documentElement.classList.contains('shot')) document.querySelectorAll('[data-scramble]').forEach((el) => el.removeAttribute('data-scramble'));
  const AUTO = '.hero .tag, .hero__title, .hero__lead, .hero__cta, .hero__meta, .flow, .page-hero .crumbs, .page-hero .tag, .page-hero h1, .page-hero__lead, .page-hero .hero__cta, .page-hero .meta-row, .timeline li, .cta > .container > *, main .card, main .person, .vtl li, .dirs li, .deps li, .faq details, .people, .cards, .chips, .filter-bar, .feature, .prose > *, .map, .more, .lead-2, .split-layout h3.big, .footer__cols > div';
  document.querySelectorAll(AUTO).forEach((el) => {
    if (el.hasAttribute('data-reveal') || el.parentElement.closest('[data-reveal]:not(.split)')) return;
    el.setAttribute('data-reveal', '');
    if (!el.style.getPropertyValue('--d')) el.style.setProperty('--d', Math.min([...el.parentElement.children].indexOf(el), 6));
  });
  // по словам: текстовые узлы режем на слова, вложенные элементы (акцентное слово) — целиком
  document.querySelectorAll('.hero__title, .page-hero h1, .statement, .cta h2, .split-layout h3.big, .feature h2').forEach((el) => {
    let n = 0;
    [...el.childNodes].forEach((node) => {
      if (node.nodeType === 3) {
        const frag = document.createDocumentFragment();
        node.textContent.split(/(\s+)/).forEach((part) => {
          if (!part) return;
          if (/^\s+$/.test(part)) return frag.append(part);
          const w = document.createElement('span'); w.className = 'w'; w.style.setProperty('--w', n++); w.textContent = part; frag.append(w);
        });
        node.replaceWith(frag);
      } else if (node.nodeType === 1) { node.classList.add('w'); node.style.setProperty('--w', n++); }
    });
    el.classList.add('split'); el.setAttribute('data-reveal', '');
  });
})();
</script>
"""

SECBAR_JS = r"""<script>
/* Липкая плашка раздела. Плашка — клон настоящего заголовка, поэтому совпадает с ним пиксель в пиксель:
   заголовок доезжает до места плашки → подмена без анимации и затуханий. Следующий заголовок, подъезжая
   снизу, выталкивает плашку вверх и сам встаёт на её место. Между разделами плашка не пропадает. */
(() => {
  const bar = document.querySelector('.secbar'), slot = bar && bar.querySelector('.secbar__slot');
  const heads = [...document.querySelectorAll('main .sec-head')];
  if (!bar || !heads.length || document.documentElement.classList.contains('shot')) return;
  let cur = -1, clone = null, raf = 0;
  const place = (k) => {
    if (k === cur) return;
    cur = k; clone = heads[k].cloneNode(true);
    clone.removeAttribute('data-reveal'); clone.style.cssText = '';
    clone.querySelectorAll('[id]').forEach((e) => e.removeAttribute('id'));
    slot.replaceChildren(clone);
  };
  const update = () => {
    raf = 0;
    const pin = parseFloat(getComputedStyle(bar).paddingTop);
    const tops = heads.map((h) => h.getBoundingClientRect().top);
    let k = -1; tops.forEach((t, i) => { if (t <= pin + 1) k = i; });
    heads.forEach((h, i) => { h.style.visibility = i === k && tops[i] < pin - 0.5 ? 'hidden' : ''; });
    if (k < 0) { bar.hidden = true; cur = -1; return; }
    place(k); bar.hidden = false;
    const hgt = clone.offsetHeight;
    const pusher = k + 1 < heads.length ? tops[k + 1] : heads[k].closest('section').getBoundingClientRect().bottom;
    const off = Math.min(0, pusher - (pin + hgt));
    bar.style.transform = off ? `translateY(${off}px)` : '';
    if (off <= -(pin + hgt)) bar.hidden = true;
  };
  const req = () => { if (!raf) raf = requestAnimationFrame(update); };
  addEventListener('scroll', req, { passive: true });
  addEventListener('resize', () => { cur = -1; req(); });
  update();
})();

/* Тема: «Бумага» по умолчанию, «Сурик» и «Латунь» — тёмные. Выбор хранится в браузере. */
(() => {
  const root = document.documentElement, pop = document.getElementById('theme-pop');
  const sync = () => document.querySelectorAll('[data-theme-set]').forEach((b) => b.setAttribute('aria-checked', b.dataset.themeSet === (root.dataset.theme || 'paper')));
  document.addEventListener('click', (e) => {
    const b = e.target.closest('[data-theme-set]'); if (!b) return;
    root.classList.add('theme-anim'); setTimeout(() => root.classList.remove('theme-anim'), 500);
    root.dataset.theme = b.dataset.themeSet;
    try { localStorage.setItem('bgitu-theme', b.dataset.themeSet); } catch (err) {}
    sync(); dispatchEvent(new Event('bgitu:palette'));
    if (pop && pop.matches(':popover-open')) setTimeout(() => pop.hidePopover(), 180);
  });
  // стрелки внутри группы тем
  document.addEventListener('keydown', (e) => {
    const b = e.target.closest && e.target.closest('[data-theme-set]'); if (!b || !/Arrow(Up|Down)/.test(e.key)) return;
    const all = [...b.parentElement.querySelectorAll('[data-theme-set]')], i = all.indexOf(b);
    all[(i + (e.key === 'ArrowDown' ? 1 : all.length - 1)) % all.length].focus(); e.preventDefault();
  });
  sync();
})();

/* Фильтры направлений и новостей: группы чипов (data-g: k — институт/тип, l — уровень) + поиск по строке */
document.querySelectorAll('[data-filter]').forEach((box) => {
  const list = document.querySelector(box.dataset.filter), q = box.querySelector('input'), empty = list.parentElement.querySelector('.dirs__empty');
  const state = {};
  box.querySelectorAll('.chips').forEach((g) => { state[g.dataset.g || 'k'] = 'all'; });
  const apply = () => {
    const words = (q ? q.value : '').toLowerCase().replace(/ё/g, 'е').split(/\s+/).filter(Boolean);
    let shown = 0;
    list.querySelectorAll(':scope > li').forEach((li) => {
      const hay = li.textContent.toLowerCase().replace(/ё/g, 'е');
      const ok = Object.entries(state).every(([g, v]) => v === 'all' || li.dataset[g] === v) && words.every((w) => hay.includes(w));
      li.hidden = !ok; if (ok) { shown++; li.classList.add('is-in'); }
    });
    if (empty) empty.hidden = shown > 0;
  };
  box.querySelectorAll('.chips').forEach((g) => g.querySelectorAll('button').forEach((b) => b.addEventListener('click', () => {
    state[g.dataset.g || 'k'] = b.dataset.k; g.querySelectorAll('button').forEach((x) => x.setAttribute('aria-pressed', x === b)); apply();
  })));
  q && q.addEventListener('input', apply);
});
</script>
"""


# ---------------------------------------------------------------- сборка страницы
def parts():
    s = SRC
    # правки, общие для всех страниц
    s = s.replace('  <canvas class="aurora" data-aurora aria-hidden="true"></canvas>\n', '')
    s = s.replace('  <canvas class="aurora" data-aurora data-seed="2.7" aria-hidden="true"></canvas>\n', '')
    s = s.replace("  $$('[data-aurora]').forEach(aurora);\n", '')
    s = s.replace("join('');\n      if (p < 1) requestAnimationFrame(tick);\n    })(t0);\n  };\n  const io",
                  "join('');\n      if (p < 1) requestAnimationFrame(tick); else el.style.minWidth = '';\n    })(t0);\n  };\n  const io")
    # перебор букв — один раз: заголовок и слово наблюдаются одновременно, второй запуск запомнил бы уже перемешанные буквы
    s = s.replace("  const scramble = (el) => {\n    if (reduce) return;",
                  "  const scramble = (el) => {\n    if (reduce || el.dataset.scrambled) return;\n    el.dataset.scrambled = '1';")
    s = s.replace("    if (reduce) return (el.textContent = to);\n    const t0 = performance.now();",
                  "    if (reduce || 'plain' in el.dataset) return (el.textContent = to);\n    const t0 = performance.now();")
    s = s.replace("addEventListener('resize', () => innerWidth > 1000 && !menu.hidden && setMenu(false));",
                  "addEventListener('resize', () => innerWidth > 1180 && !menu.hidden && setMenu(false));")
    s = s.replace('<html lang="ru">', '<html lang="ru" data-theme="paper">', 1)
    head = s[:s.index('</style>')] + CSS + '</style>\n' + HEAD_JS + s[s.index('</style>') + len('</style>\n'):s.index('<body')]
    header = cut(s, '<a class="skip"', '<main id="main">')
    main = cut(s, '<main id="main">', '</main>', True)
    footer = cut(s, '<!-- ============ ФУТЕР', '<script>')
    script = s[s.rindex('<script>'):s.rindex('</body>')]
    return head, header, main, footer, script


def page(cur, title, main_html, trail_js, desc=None):
    head, header, _, footer, script = parts()
    head = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', head, count=1, flags=re.S)
    if desc:
        head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', head, count=1)
    # шапка: ссылки на страницы, кнопка темы, бургер-меню с выбором темы
    header = re.sub(r'<nav class="nav" aria-label="Основное">\s*<ul>.*?</ul>', '<nav class="nav" aria-label="Основное">\n      ' + nav_ul(cur), header, count=1, flags=re.S)
    header = header.replace('<a class="brand" href="#top"', '<a class="brand" href="index.html"')
    header = header.replace('<button class="search-btn"', THEME_BTN + '\n      <button class="search-btn"', 1)
    menu_links = ''.join(f'  <a href="{h}"{" aria-current=" + chr(34) + "page" + chr(34) if h == cur else ""}>{n}</a>\n' for h, n, k in NAV)
    header = re.sub(r'(<div class="menu" id="menu" hidden>\n).*?(  <a class="btn)', r'\1' + menu_links.replace('\\', '\\\\') + r'\2', header, count=1, flags=re.S)
    header = header.replace('</div>\n\n', f'  <div class="menu-theme" role="radiogroup" aria-label="Тема"><p class="mono">оформление</p>{theme_opts()}</div>\n</div>\n\n', 1) \
        if False else re.sub(r'(<a class="btn btn--accent btn--lg" href="#" data-soon>Личный кабинет</a>\n)</div>',
                             r'\1  <div class="menu-theme" role="radiogroup" aria-label="Тема"><p class="mono">оформление</p>' + theme_opts() + '</div>\n</div>', header, count=1)
    header = header + '\n' if not header.endswith('\n') else header
    extras = '<canvas class="trail" aria-hidden="true"></canvas>\n' + SECBAR + '\n' + THEME_POP + '\n'
    header = header.replace('<a class="skip" href="#main">К содержимому</a>\n', '<a class="skip" href="#main">К содержимому</a>\n' + extras, 1)
    # футер: разделы → страницы
    sections = ''.join(f'<a href="{h}">{n}</a>' for h, n, k in NAV)
    footer = footer.replace('<p class="footer__word" aria-hidden="true">БГИТУ</p>', '<p class="footer__word" aria-hidden="true" data-text="БГИТУ">БГИТУ</p>')
    footer = re.sub(r'<div><h2 class="mono">Разделы</h2>.*?</div>', f'<div><h2 class="mono">Разделы</h2><a href="index.html">Главная</a>{sections}<a href="#" data-soon>Личный кабинет</a></div>', footer, count=1, flags=re.S)
    return (head + '<body id="top">\n' + header + main_html + '\n\n' + footer + REVEAL_JS + script + '</body>\n'
            .replace('</body>', '<script>\n' + trail_js + '\n</script>\n' + SECBAR_JS + '</body>') + '</html>\n')


# ---------------------------------------------------------------- строительные блоки разметки
def sec(sid, num, title, caption, inner, raised=False, more=None):
    cls = 'section section--raised' if raised else 'section'
    cap = caption if caption.startswith('<') else f'<span class="mono dim">{caption}</span>'
    m = f'\n    <p class="more"><a class="mono" href="{more[0]}">{more[1]} <span aria-hidden="true">→</span></a></p>' if more else ''
    return f'''
<section class="{cls}" id="{sid}" aria-labelledby="{sid}-h">
  <div class="container">
    <header class="sec-head" data-reveal><h2 class="mono" id="{sid}-h">{num} — {title}</h2>{cap}</header>
    {inner}{m}
  </div>
</section>
'''


def page_hero(crumbs, tag, h1, lead, extra=''):
    cr = '<span aria-hidden="true">/</span>'.join(f'<a href="{h}">{n}</a>' if h else f'<span aria-current="page">{n}</span>' for h, n in crumbs)
    return f'''<main id="main">
<section class="page-hero" aria-labelledby="ph">
  <div class="container">
    <nav class="crumbs mono" aria-label="Вы здесь">{cr}</nav>
    <p class="tag mono"><i></i>{tag}</p>
    <h1 id="ph"{" class=" + chr(34) + "long" + chr(34) if len(re.sub("<.*?>", "", h1)) > 42 else ""}>{h1}</h1>
    <p class="page-hero__lead">{lead}</p>{extra}
  </div>
</section>
'''


def cta(h2, btns, small='БГИТУ · Брянск · с 1930 года'):
    return f'''
<section class="cta" aria-labelledby="cta-h">
  <div class="container">
    <p class="mono dim">{small}</p>
    <h2 id="cta-h">{h2}</h2>
    <div class="hero__cta">{btns}</div>
  </div>
</section>
</main>'''


def btn(href, text, kind='accent', arrow='→', size='lg', ext=False):
    t = ' target="_blank" rel="noopener"' if ext else ''
    a = f' <span aria-hidden="true">{arrow}</span>' if arrow else ''
    return f'<a class="btn btn--{kind} btn--{size}" href="{href}"{t}>{text}{a}</a>'


def initials(fio):
    p = fio.split()
    return (p[1][0] + p[2][0]) if len(p) >= 3 else p[0][0]


def tel(t):
    return 'tel:+' + re.sub(r'\D', '', t)
