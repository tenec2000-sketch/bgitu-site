"""Сквозные функции сайта по аудиту из чата «Сайт Бгиту»: меню по сценариям, панель для слабовидящих,
PWA (установка на телефон), индикатор учебной недели, баннер cookies/ПДн, вход в ЛК, индекс всех страниц для ⌘K."""
import re
import site_engine as E

# ---------- меню по сценариям (аудит: «сократить верхнее меню до понятных сценариев»)
E.NAV = [('university.html', 'Университет', 'о вузе история руководство структура институты кампус'),
         ('admission.html', 'Поступающим', 'абитуриенту приёмная комиссия направления калькулятор егэ'),
         ('student.html', 'Студенту', 'расписание стипендия эос библиотека общежитие справки'),
         ('science.html', 'Наука', 'исследования гранты аспирантура конференции'),
         ('news.html', 'Новости', 'события объявления'),
         ('contacts.html', 'Контакты', 'адрес телефон почта справочник')]
# какой пункт меню подсвечивать на внутренних страницах
SECTION = {'institutes.html': 'university.html', 'campus.html': 'university.html', 'garden.html': 'university.html', 'sveden.html': 'university.html',
           'docs.html': 'university.html', 'press.html': 'university.html', 'staff.html': 'university.html',
           'programs.html': 'admission.html', 'program.html': 'admission.html', 'target.html': 'admission.html', 'school.html': 'admission.html',
           'transfer.html': 'admission.html', 'paid.html': 'admission.html', 'international.html': 'admission.html',
           'schedule.html': 'student.html', 'eos.html': 'student.html', 'scholarships.html': 'student.html', 'library.html': 'student.html',
           'life.html': 'student.html', 'career.html': 'student.html', 'help.html': 'student.html', 'dpo.html': 'student.html',
           'aspirantura.html': 'science.html', 'article.html': 'news.html'}

# все страницы сайта: файл, название, ключевые слова для поиска ⌘K и карта сайта
PAGES = [
    ('Университет', [('index.html', 'Главная', 'главная бгиту'), ('university.html', 'Об университете', 'история ректор руководство учёный совет'),
                     ('institutes.html', 'Институты и подразделения', 'институты факультет колледж вуц'), ('campus.html', 'Кампус', 'корпуса общежития столовая стадион'),
                     ('garden.html', 'Ботанический сад и лесхоз', 'ботсад гроздова лесхоз'), ('sveden.html', 'Сведения об образовательной организации', 'сведения 1493 структура документы'),
                     ('docs.html', 'Документы и бланки', 'устав лицензия аккредитация заявления'), ('press.html', 'Пресс-центр', 'соцсети вк телеграм rutube логотип'),
                     ('staff.html', 'Сотрудникам и преподавателям', 'сотрудник преподаватель ведомости нагрузка кадры')]),
    ('Поступающим', [('admission.html', 'Приёмная комиссия', 'абитуриент поступление документы шаги'), ('programs.html', 'Направления подготовки и калькулятор ЕГЭ', 'каталог программ баллы егэ калькулятор'),
                     ('program.html', 'Карточка направления (пример)', 'учебный план программная инженерия'), ('target.html', 'Целевое обучение', 'целевое квота работа в россии'),
                     ('school.html', 'Школьникам', 'цто олимпиада малая инженерная академия код будущего курсы егэ'), ('transfer.html', 'Перевод и восстановление', 'перевод восстановление бюджет вакантные места'),
                     ('paid.html', 'Платное обучение', 'стоимость оплата договор кредит'), ('international.html', 'Иностранным гражданам', 'study in russia international')]),
    ('Студенту', [('student.html', 'Студенту', 'хаб сервисы студента'), ('schedule.html', 'Расписание и звонки', 'расписание пары звонки неделя ics'),
                  ('eos.html', 'ЭОС и электронное обучение', 'эос moodle сдо курсы оценки'), ('scholarships.html', 'Стипендии и поддержка', 'стипендия пгас гас социальная калькулятор'),
                  ('library.html', 'Библиотека', 'эбс ipr smart каталог читальный зал'), ('life.html', 'Студенческая жизнь', 'тонус спортклуб профком волонтёры'),
                  ('career.html', 'Карьера и трудоустройство', 'вакансии стажировки трудоустройство'), ('dpo.html', 'Дополнительное образование', 'дпо переподготовка повышение квалификации'),
                  ('help.html', 'Помощь: FAQ, отчёт по ГОСТ, чат', 'инструкции faq титульный лист гост чат'), ('lk.html', 'Личный кабинет', 'лк вход эос')]),
    ('Наука и контакты', [('science.html', 'Наука и инновации', 'наука гранты рнф конференции'), ('aspirantura.html', 'Аспирантура', 'аспирантура научные специальности'),
                          ('news.html', 'Новости и объявления', 'новости объявления'), ('contacts.html', 'Контакты', 'телефоны адреса почта'),
                          ('sitemap.html', 'Карта сайта', 'карта сайта все страницы'), ('privacy.html', 'Политика обработки персональных данных', 'пдн 152-фз cookies')]),
]

SOCIAL = [('ВКонтакте', 'https://vk.com/bgitu_ru'), ('Telegram', 'https://t.me/bgituofficial'), ('MAX', 'https://max.ru/id3234017534_gos'),
          ('Одноклассники', 'https://ok.ru/bgituoffic'), ('Rutube', 'https://rutube.ru/channel/25386572/')]

A11Y_BTN = ('<button class="theme-btn a11y-btn" type="button" popovertarget="a11y-pop" aria-label="Версия для слабовидящих">'
            '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg><span>Доступность</span></button>')


def _grp(label, key, opts):
    b = ''.join(f'<button type="button" data-a11y="{key}" data-v="{v}" aria-pressed="false">{t}</button>' for v, t in opts)
    return f'<div class="a11y-row"><p class="mono dim">{label}</p><div class="chips" role="group" aria-label="{label}">{b}</div></div>'


A11Y_POP = ('<div class="theme-pop a11y-pop" id="a11y-pop" popover aria-label="Версия для слабовидящих"><p class="mono dim">версия для слабовидящих</p>'
            + _grp('Размер шрифта', 'fs', [('0', 'А'), ('1', 'А+'), ('2', 'А++')])
            + _grp('Интервалы', 'sp', [('0', 'Обычные'), ('1', 'Увеличенные')])
            + _grp('Цвет', 'cl', [('0', 'Обычный'), ('gray', 'Ч/б'), ('hc', 'Контраст')])
            + _grp('Изображения и анимация', 'im', [('0', 'Показывать'), ('1', 'Скрыть')])
            + '<button type="button" class="btn btn--ghost btn--sm a11y-reset" data-a11y-reset>Сбросить настройки</button>'
            + '<p class="theme-pop__note">По ГОСТ Р 52872-2019 и ПП РФ № 102</p></div>')

PWA_HEAD = ('<link rel="manifest" href="manifest.webmanifest">\n<link rel="apple-touch-icon" href="icon-180.png">\n'
            '<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="mobile-web-app-capable" content="yes">\n'
            '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n<meta name="apple-mobile-web-app-title" content="БГИТУ">\n')

CSS = r"""
/* ================= Панель для слабовидящих ================= */
.a11y-pop { width: 330px; }
.a11y-row { padding: 6px 6px 10px; }
.a11y-row .mono { margin-bottom: 8px; }
.a11y-row .chips button { min-height: 38px; }
.a11y-reset { width: calc(100% - 12px); margin: 6px; }
html.a11y-fs1 { font-size: 118%; }
html.a11y-fs2 { font-size: 136%; }
html.a11y-sp body { letter-spacing: 0.04em; word-spacing: 0.16em; }
html.a11y-sp :is(p, li, dd) { line-height: 1.9 !important; }
html.a11y-gray { filter: grayscale(1); }
html.a11y-hc { --brand-base: #000 !important; --brand-ink: #fff !important; --brand-accent: #ffe14d !important; --brand-on-accent: #000 !important; --brand-aux: #ffe14d !important; }
html.a11y-im .trail, html.a11y-im img, html.a11y-im .ia, html.a11y-im :is(.tile, .card, .feature)::before, html.a11y-im .tile::after { display: none !important; }
html.a11y-im *, html.a11y-im *::before, html.a11y-im *::after { animation: none !important; transition: none !important; }
@media (max-width: 640px) { .a11y-btn span { display: none; } .a11y-btn { width: 44px; justify-content: center; padding: 0; } }
@media (max-width: 420px) { .a11y-btn { display: none; } }

/* ================= Индикатор учебной недели ================= */
.week { display: inline-flex; align-items: center; gap: 0.6em; }
.week i { width: 7px; height: 7px; border-radius: 50%; background: var(--accent); box-shadow: 0 0 10px var(--accent-glow); }

/* ================= Cookies / ПДн ================= */
.cookie { position: fixed; left: 50%; bottom: 16px; translate: -50% 0; z-index: 60; display: flex; flex-wrap: wrap; align-items: center; gap: 12px 18px; width: min(680px, calc(100% - 24px));
  padding: 14px 16px 14px 20px; border: 1px solid var(--line-strong); border-radius: var(--radius-m); background: var(--bg-glass); backdrop-filter: blur(16px); font-size: 0.875rem; color: var(--text-muted); }
.cookie p { flex: 1 1 280px; }
.cookie a { color: var(--text); border-bottom: 1px solid var(--line-strong); }
.cookie[hidden] { display: none; }

/* ================= Формы, таблицы, сервисы ================= */
.form { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 14px 16px; }
.form label { display: grid; gap: 6px; font-size: 0.875rem; color: var(--text-muted); }
.form .wide { grid-column: 1 / -1; }
:is(.form, .tool) :is(input, select, textarea) { width: 100%; min-height: 46px; padding: 10px 14px; border: 1px solid var(--line-strong); border-radius: var(--radius-s); color: var(--text); background: var(--bg-raised); font: inherit; }
:is(.form, .tool) textarea { min-height: 96px; resize: vertical; }
:is(.form, .tool) :is(input, select, textarea):focus-visible { outline: 2px solid var(--focus); outline-offset: 1px; }
.tool { padding: clamp(20px, 3vw, 32px); border: 1px solid var(--line); border-radius: var(--radius-l); background: var(--bg-panel); }
.tool__out { margin-top: 20px; padding-top: 20px; border-top: 1px solid var(--line); }
.tool__big { font: 800 clamp(2.25rem, 1.4rem + 2.6vw, 3.75rem)/1 var(--font-display); letter-spacing: -0.04em; color: var(--accent); }
.btn-row { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 18px; }
.tbl { width: 100%; border-collapse: collapse; font-variant-numeric: tabular-nums; }
.tbl th, .tbl td { padding: 14px 12px; border-bottom: 1px solid var(--line); text-align: left; }
.tbl th { font: 500 var(--fs-mono)/1.4 var(--font-mono); letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-faint); }
.tbl td:first-child { font: 600 1.125rem/1 var(--font-display); color: var(--accent); }
.tbl tr.now td { background: var(--accent-soft); }
.tbl-wrap { overflow-x: auto; }
.demo { display: inline-flex; gap: 0.5em; align-items: center; padding: 0.3em 0.8em; border: 1px dashed var(--line-strong); border-radius: var(--radius-pill); color: var(--text-faint); font: 500 0.6875rem/1.4 var(--font-mono); letter-spacing: 0.08em; text-transform: uppercase; }
.plan { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; }
.plan > div { padding: 18px; border: 1px solid var(--line); border-radius: var(--radius-m); background: var(--bg-panel); }
.plan b { display: block; margin-bottom: 10px; font: 600 1rem/1.2 var(--font-display); }
.plan li { display: flex; justify-content: space-between; gap: 10px; padding: 6px 0; border-top: 1px solid var(--line); font-size: 0.875rem; color: var(--text-muted); }
.plan li span:last-child { font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-faint); white-space: nowrap; }
.paper { width: 100%; max-width: 560px; aspect-ratio: 210 / 297; margin-inline: auto; padding: 8% 7% 6% 11%; display: flex; flex-direction: column; text-align: center;
  color: #111; background: #fff; border-radius: 6px; box-shadow: 0 20px 60px rgb(0 0 0 / 0.25); font: 400 clamp(9px, 1.25vw, 14px)/1.45 "Times New Roman", Times, serif; text-shadow: none !important; }
.paper * { text-shadow: none !important; }
.paper .t { margin-top: 32%; font-weight: 700; font-size: 1.25em; text-transform: uppercase; }
.paper .who { margin-top: auto; margin-left: 52%; text-align: left; }
.paper .city { margin-top: 12%; }
.chat { display: flex; flex-direction: column; height: 460px; border: 1px solid var(--line); border-radius: var(--radius-l); background: var(--bg-panel); overflow: hidden; }
.chat__log { flex: 1; overflow-y: auto; padding: 18px; display: flex; flex-direction: column; gap: 10px; }
.chat__msg { max-width: 85%; padding: 10px 14px; border-radius: 14px; background: var(--bg-raised); line-height: 1.45; font-size: 0.9375rem; }
.chat__msg.me { align-self: flex-end; background: var(--accent); color: var(--accent-ink); }
.chat__msg a { border-bottom: 1px solid currentColor; }
.chat form { display: flex; gap: 8px; padding: 12px; border-top: 1px solid var(--line); }
.chat input { flex: 1; min-height: 46px; padding: 0 14px; border: 1px solid var(--line-strong); border-radius: var(--radius-pill); color: var(--text); background: var(--bg-raised); font: inherit; }
.sitemap { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 32px; }
.sitemap h3 { margin-bottom: 12px; font: 600 1.125rem/1.2 var(--font-display); }
.sitemap a { display: block; padding: 8px 0; border-bottom: 1px solid var(--line); color: var(--text-muted); }
.sitemap a:hover { color: var(--accent); }
.footer__cols .soc { display: flex; flex-wrap: wrap; gap: 4px 14px; margin-top: 10px; }
.footer__cols .soc a { padding: 2px 0; }
"""

JS = r"""<script>
/* Индикатор учебной недели: считается от опорного понедельника, неделя на bgitu.ru 19.10.2026 — «вторая» */
(() => {
  const anchor = Date.UTC(2026, 9, 19), d = new Date(), today = Date.UTC(d.getFullYear(), d.getMonth(), d.getDate());
  const wd = (d.getDay() + 6) % 7, monday = today - wd * 864e5, weeks = Math.round((monday - anchor) / (7 * 864e5));
  const kind = ((weeks % 2) + 2) % 2 === 0 ? 'вторая' : 'первая';
  const date = d.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' }), day = d.toLocaleDateString('ru-RU', { weekday: 'long' });
  window.BGITU_WEEK = kind;
  document.querySelectorAll('[data-week]').forEach((el) => { el.innerHTML = `<i aria-hidden="true"></i>${date}, ${day} · ${kind} неделя`; });
})();

/* Версия для слабовидящих: настройки хранятся в браузере */
(() => {
  const root = document.documentElement;
  let st = {}; try { st = JSON.parse(localStorage.getItem('bgitu-a11y') || '{}'); } catch (e) {}
  const apply = () => {
    root.classList.toggle('a11y-fs1', st.fs === '1'); root.classList.toggle('a11y-fs2', st.fs === '2');
    root.classList.toggle('a11y-sp', st.sp === '1'); root.classList.toggle('a11y-gray', st.cl === 'gray');
    root.classList.toggle('a11y-hc', st.cl === 'hc'); root.classList.toggle('a11y-im', st.im === '1');
    document.querySelectorAll('[data-a11y]').forEach((b) => b.setAttribute('aria-pressed', (st[b.dataset.a11y] || '0') === b.dataset.v));
    try { localStorage.setItem('bgitu-a11y', JSON.stringify(st)); } catch (e) {}
    dispatchEvent(new Event('bgitu:palette'));
  };
  document.addEventListener('click', (e) => {
    const b = e.target.closest('[data-a11y]'); if (b) { st[b.dataset.a11y] = b.dataset.v; apply(); }
    if (e.target.closest('[data-a11y-reset]')) { st = {}; apply(); }
  });
  apply();
})();

/* Cookies / ПДн: только технические, без трекеров в макете */
(() => {
  const bar = document.querySelector('.cookie'); if (!bar || document.documentElement.classList.contains('shot')) return;
  let ok = false; try { ok = localStorage.getItem('bgitu-cookie') === '1'; } catch (e) {}
  if (!ok) bar.hidden = false;
  bar.querySelector('button').addEventListener('click', () => { bar.hidden = true; try { localStorage.setItem('bgitu-cookie', '1'); } catch (e) {} });
})();

/* PWA: сайт ставится на экран телефона как приложение и открывается офлайн */
if ('serviceWorker' in navigator && /^https?:/.test(location.protocol)) addEventListener('load', () => navigator.serviceWorker.register('sw.js').catch(() => {}));
</script>
"""

COOKIE = ('<div class="cookie" role="region" aria-label="Уведомление о cookies" hidden><p>Сайт сохраняет в браузере только выбранную тему и настройки доступности. '
          'Подробнее — в <a href="privacy.html">политике обработки персональных данных</a>.</p><button class="btn btn--accent btn--sm" type="button">Понятно</button></div>')


def _index():
    links = ''.join(f'<a href="{h}" data-s="Страница" data-t="{n}" data-k="{k}">{n}</a>' for _, items in PAGES for h, n, k in items)
    return f'<nav hidden aria-hidden="true">{links}</nav>'


_orig_page = E.page


def page(cur, title, main_html, trail_js, desc=None):
    nav_cur = SECTION.get(cur, cur)
    html = _orig_page(nav_cur, title, main_html, trail_js, desc)
    # вход в ЛК — страница входа вместо заглушки
    html = html.replace('href="#" data-soon data-s="Раздел" data-t="Личный кабинет"', 'href="lk.html" data-s="Раздел" data-t="Личный кабинет"')
    html = html.replace('<a class="btn btn--accent btn--lg" href="#" data-soon>Личный кабинет</a>', '<a class="btn btn--accent btn--lg" href="lk.html">Личный кабинет</a>')
    html = html.replace('<a href="#" data-soon>Личный кабинет</a>', '<a href="lk.html">Личный кабинет</a>')
    # шапка: кнопка доступности рядом с темой; поповер — рядом с поповером темы
    html = html.replace('<button class="theme-btn" type="button" popovertarget="theme-pop"', A11Y_BTN + '\n      <button class="theme-btn" type="button" popovertarget="theme-pop"', 1)
    html = html.replace('<div class="secbar"', A11Y_POP + '\n<div class="secbar"', 1)
    # на телефоне кнопка в шапке скрыта — версия для слабовидящих доступна из мобильного меню
    html = html.replace('  <div class="menu-theme"', '  <button class="btn btn--ghost btn--lg" type="button" popovertarget="a11y-pop" style="margin-top:12px">Версия для слабовидящих</button>\n  <div class="menu-theme"', 1)
    # футер: карта разделов, соцсети, политика ПДн
    cols = ''.join(f'<a href="{h}">{n}</a>' for h, n in [('index.html', 'Главная'), ('university.html', 'Университет'), ('institutes.html', 'Институты'),
                                                      ('admission.html', 'Поступающим'), ('student.html', 'Студенту'), ('schedule.html', 'Расписание'),
                                                      ('science.html', 'Наука'), ('news.html', 'Новости'), ('sveden.html', 'Сведения об ОО'),
                                                      ('sitemap.html', 'Карта сайта'), ('lk.html', 'Личный кабинет')])
    html = re.sub(r'<div><h2 class="mono">Разделы</h2>.*?</div>', f'<div><h2 class="mono">Разделы</h2>{cols}</div>', html, count=1, flags=re.S)
    # это и есть основной сайт: вместо «Официальный сайт bgitu.ru» — сервисы и соцсети, без подписи «макет»
    soc = '<div class="soc">' + ''.join(f'<a href="{u}" target="_blank" rel="noopener">{n} ↗</a>' for n, u in SOCIAL) + '</div>'
    services = ''.join(f'<a href="{h}" data-s="Сервис" data-t="{n}">{n}</a>' for h, n in [('lk.html', 'Личный кабинет'), ('eos.html', 'ЭОС и Moodle'), ('schedule.html', 'Расписание'),
                                                                                         ('programs.html', 'Направления подготовки'), ('library.html', 'Библиотека')])
    html = re.sub(r'<div><h2 class="mono">Официальный сайт</h2>.*?</div>', lambda m: f'<div><h2 class="mono">Сервисы и соцсети</h2>{services}{soc}</div>', html, count=1, flags=re.S)
    html = re.sub(r'(<div class="footer__bottom mono"><span>© <span id="year">\d+</span> БГИТУ</span>)<span>.*?</span>',
                  lambda m: m.group(1).replace('БГИТУ</span>', 'ФГБОУ ВО «Брянский государственный инженерно-технологический университет»</span>') +
                  '<span><a href="privacy.html">Политика ПДн</a> · <a href="sveden.html">Сведения об ОО</a> · <a href="sitemap.html">Карта сайта</a></span>', html, count=1, flags=re.S)
    html = html.replace('<p class="mono dim">режим работы 8:30–18:00</p>', '<p class="mono dim">режим работы 8:30–18:00</p><p class="mono dim week" data-week></p>', 1)
    # PWA, стили, скрипты, индекс страниц для поиска, баннер cookies
    html = html.replace('</head>', PWA_HEAD + '</head>', 1)
    i = html.index('</style>'); html = html[:i] + CSS + html[i:]
    k = html.rindex('</body>')   # последний: в скриптах страниц бывают строки с '</body>'
    html = html[:k] + _index() + '\n' + COOKIE + '\n' + JS + html[k:]
    return html


E.page = page
