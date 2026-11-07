# Страницы по аудиту из чата «Сайт Бгиту» (публичная часть: пп. 1–32, 46–48).
# Выполняется в конце build_site.py (exec) и использует его данные и помощники.
# Реальные факты — с bgitu.ru (ноябрь 2026); где данных нет, блок помечен «демо».
import json
import site_extra as X

BG = 'https://bgitu.ru'
EOS = 'https://eos.bgitu.ru'
DEMO = '<span class="demo">демо-данные макета</span>'


def rows(items):
    """Список-ссылки в стиле ленты новостей: (метка, заголовок, ссылка[, подпись])."""
    out = '<ul class="news">'
    for it in items:
        lab, t, href = it[:3]; cap = it[3] if len(it) > 3 else ''
        ext = href.startswith('http')
        a = f'href="{href}" target="_blank" rel="noopener"' if ext else f'href="{href}"'
        out += f'<li><a {a} data-s="Ссылка" data-t="{t}"><time class="mono">{lab}</time><h3>{t}</h3><span class="mono dim">{cap or ("bgitu.ru ↗" if "bgitu.ru" in href else ("↗" if ext else "→"))}</span></a></li>'
    return out + '</ul>'


def cards(items):
    """Карточки: (метка, заголовок, текст, ссылка, подпись-ссылки)."""
    out = '<div class="cards">'
    for m, t, p, h, g in items:
        tag = 'a' if h else 'div'
        attr = (f' href="{h}"' + (' target="_blank" rel="noopener"' if h.startswith('http') else '')) if h else ''
        out += f'<{tag} class="card"{attr} data-s="Сервис" data-t="{t}"><span class="mono">{m}</span><h3>{t}</h3><p>{p}</p>{f"<span class=go>{g}</span>" if g else ""}</{tag}>'
    return out + '</div>'


def faq_block(items):
    return '<div class="faq">' + ''.join(f'<details data-s="Вопрос" data-t="{q}"><summary>{q}</summary><div><p>{a}</p></div></details>' for q, a in items) + '</div>'


def hero(cr, tag, h1, lead, extra=''):
    return page_hero([('index.html', 'Главная')] + cr, tag, h1, lead, extra)


def close(h2=None, b=None):
    return cta(h2, b) if h2 else '\n</main>'


def ext(href, text, kind='ghost', size='lg'):
    return btn(href, text, kind, '↗', size, True)


def save(name, cur, title, html, desc=None):
    write(name, E.page(cur, f'{title} — БГИТУ', html, TRAIL, desc))


WEEK = '<div class="meta-row"><span class="week" data-week></span></div>'

# ================================================================= СТУДЕНТУ (хаб)
html = hero([(None, 'Студенту')], 'Студенту', 'Всё для учёбы — <span class="hl">в одном месте</span>',
            'Расписание, ЭОС, стипендии, библиотека, справки и студенческая жизнь. Вход во все сервисы — через личный кабинет.', WEEK)
html += sec('services', '01', 'Сервисы', 'самое нужное', cards([
    ('каждый день', 'Расписание и звонки', 'Пары по корпусам, текущая неделя, выгрузка в календарь телефона.', 'schedule.html', 'Открыть →'),
    ('учёба', 'ЭОС и Moodle', 'Курсы, оценки, зачётка, учебные планы, задолженности.', 'eos.html', 'Карта сервисов →'),
    ('деньги', 'Стипендии и поддержка', 'Виды стипендий и калькулятор «как увеличить стипендию».', 'scholarships.html', 'Подробнее →'),
    ('книги', 'Библиотека', 'Каталог, литература по дисциплинам, ЭБС IPR SMART.', 'library.html', 'Подробнее →'),
    ('документы', 'Справки и заявления', 'Заказ справок и заявлений — в личном кабинете.', 'lk.html', 'Войти →'),
    ('отчёты', 'Титульный лист по ГОСТ', 'Генератор титульного листа для лабораторных, РГР и курсовых.', 'help.html#report', 'Собрать →'),
    ('жизнь', 'Клубы, спорт, профком', 'Объединённый совет обучающихся, «Тонус», спортклуб.', 'life.html', 'Подробнее →'),
    ('работа', 'Карьера', 'Стажировки, трудоустройство, целевые предложения.', 'career.html', 'Подробнее →'),
    ('жильё', 'Общежития и кампус', 'Четыре общежития, столовые, здравпункт, схема корпусов.', 'campus.html', 'Подробнее →')]), True)
html += sec('more', '02', 'Ещё для студентов', 'разделы на bgitu.ru', rows([
    ('график', 'Календарный учебный график 2026/27', BG + '/studentu/'), ('перевод', 'Перевод с платного обучения на бесплатное', 'transfer.html'),
    ('вкр', 'Перечень тем ВКР', BG + '/studentu/'), ('спт', 'Социально-психологическое тестирование (СПТ)', BG + '/studentu/'),
    ('семьи', 'Единое окно поддержки молодых семей', 'scholarships.html#support'), ('профком', 'Профком студентов', 'https://profkombgitu.ru/', 'profkombgitu.ru ↗'),
    ('овз', 'Лицам с ограниченными возможностями здоровья', BG + '/studentu/'), ('армия', 'Призывникам в Вооружённые Силы', BG + '/studentu/')]))
html += close('Не нашли нужное? <span class="hl">Спросите помощника</span>', btn('help.html#assistant', 'Помощник') + btn('contacts.html', 'Контакты', 'ghost', None))
save('student.html', 'student.html', 'Студенту', html)

# ================================================================= РАСПИСАНИЕ
BELLS = [(1, '8:20', '9:55', '8:50', '10:25'), (2, '10:05', '11:40', '10:35', '12:10'), (3, '11:50', '13:25', '12:20', '13:55'),
         (4, '14:00', '15:35', '14:30', '16:05'), (5, '15:45', '17:20', '16:15', '17:50'), (6, '17:30', '19:05', '18:00', '19:35')]
bells = ('<div class="tbl-wrap"><table class="tbl" id="bells"><thead><tr><th>Пара</th><th>Корпус №1 · пр-т Станке Димитрова, 3</th><th>Корпус №2 · пр-т Ленина, 26</th></tr></thead><tbody>'
         + ''.join(f'<tr data-a="{a}" data-b="{b}" data-c="{c}" data-d="{d}"><td>{n}</td><td>{a} – {b}</td><td>{c} – {d}</td></tr>' for n, a, b, c, d in BELLS) + '</tbody></table></div>')
sched_tool = f'''<div class="tool">
      <div class="filter-bar" style="margin-bottom:16px"><div class="chips" role="group" aria-label="Режим поиска" id="smode"><button type="button" data-k="g" aria-pressed="true">По группе</button><button type="button" data-k="t" aria-pressed="false">По преподавателю</button><button type="button" data-k="r" aria-pressed="false">По аудитории</button></div>{DEMO}</div>
      <div class="form"><label>Группа, преподаватель или аудитория<input id="sq" list="sopts" placeholder="например, ПИ-201"></label><datalist id="sopts"></datalist>
      <label>Корпус (для времени пар)<select id="scorp"><option value="1">№1 · Станке Димитрова, 3</option><option value="2" selected>№2 · Ленина, 26</option></select></label></div>
      <div class="tool__out" id="sout"><p class="dim">Введите группу — покажем пары на текущую неделю.</p></div>
      <div class="btn-row"><button class="btn btn--accent btn--sm" type="button" id="sics">Выгрузить неделю в календарь (.ics)</button></div>
    </div>'''
SCHED_JS = r"""<script>
/* Расписание: подсветка текущей пары, демо-поиск и выгрузка недели в .ics (Google / Apple / Outlook-календарь) */
(() => {
  const tm = (s) => { const [h, m] = s.split(':').map(Number); return h * 60 + m; };
  const now = new Date(), mins = now.getHours() * 60 + now.getMinutes();
  document.querySelectorAll('#bells tr[data-a]').forEach((tr) => {
    const in1 = mins >= tm(tr.dataset.a) && mins <= tm(tr.dataset.b), in2 = mins >= tm(tr.dataset.c) && mins <= tm(tr.dataset.d);
    if (in1 || in2) tr.classList.add('now');
  });
  // демо-данные: структура как в ЭОС (группа · день · пара · дисциплина · вид · аудитория · преподаватель)
  const D = {
    'ПИ-201': [[1,2,'Программная инженерия','лекция','480в','каф. ИТ'],[1,3,'Базы данных','практика','471','каф. ИТ'],[2,1,'Математика','лекция','333','каф. математики'],[3,2,'Иностранный язык','практика','294','каф. языков'],[4,2,'Алгоритмы и структуры данных','лаб.','480в','каф. ИТ'],[5,1,'Физическая культура','практика','спортзал','каф. физвоспитания']],
    'ИВТ-101': [[1,1,'Математика','лекция','333','каф. математики'],[2,2,'Информатика','лаб.','471','каф. ИТ'],[3,3,'История России','лекция','298','каф. ФИС'],[4,1,'Физика','лекция','106','каф. ОДиФ'],[5,2,'Инженерная графика','практика','493','каф. графики и геодезии']],
    'СТР-301': [[1,1,'Строительные конструкции','лекция','277','каф. СК'],[2,2,'Геодезия','практика','493','каф. графики и геодезии'],[3,1,'Технология строительного производства','лекция','376','каф. СП'],[4,3,'Автомобильные дороги','лекция','282а','каф. АД']],
    'ЭК-201': [[1,2,'Микроэкономика','лекция','364','каф. ЭиЭБ'],[2,3,'Бухгалтерский учёт','практика','364','каф. ЭиЭБ'],[3,2,'Статистика','лекция','333','каф. математики'],[4,1,'Менеджмент','практика','364','каф. ЭиЭБ']]
  };
  const DAYS = ['', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];
  const B = { 1: [['8:20','9:55'],['10:05','11:40'],['11:50','13:25'],['14:00','15:35'],['15:45','17:20'],['17:30','19:05']], 2: [['8:50','10:25'],['10:35','12:10'],['12:20','13:55'],['14:30','16:05'],['16:15','17:50'],['18:00','19:35']] };
  const q = document.getElementById('sq'); if (!q) return;
  const out = document.getElementById('sout'), corp = document.getElementById('scorp'), opts = document.getElementById('sopts');
  let mode = 'g';
  const all = () => Object.entries(D).flatMap(([g, rows]) => rows.map((r) => ({ g, day: r[0], n: r[1], s: r[2], k: r[3], room: r[4], t: r[5] })));
  const fill = () => { const v = mode === 'g' ? Object.keys(D) : [...new Set(all().map((x) => (mode === 't' ? x.t : x.room)))]; opts.innerHTML = v.map((x) => `<option value="${x}">`).join(''); };
  const pick = () => { const v = q.value.trim().toLowerCase(); if (!v) return []; return all().filter((x) => (mode === 'g' ? x.g : mode === 't' ? x.t : x.room).toLowerCase().includes(v)).sort((a, b) => a.day - b.day || a.n - b.n); };
  const render = () => {
    const r = pick(), bb = B[corp.value];
    if (!q.value.trim()) { out.innerHTML = '<p class="dim">Введите группу — покажем пары на текущую неделю.</p>'; return; }
    if (!r.length) { out.innerHTML = '<p class="dim">Ничего не нашлось. В демо есть группы ПИ-201, ИВТ-101, СТР-301, ЭК-201.</p>'; return; }
    out.innerHTML = `<p class="mono dim" style="margin-bottom:10px">${window.BGITU_WEEK || ''} неделя</p><div class="tbl-wrap"><table class="tbl"><thead><tr><th>День</th><th>Время</th><th>Дисциплина</th><th>Ауд.</th><th>${mode === 'g' ? 'Кафедра' : 'Группа'}</th></tr></thead><tbody>` +
      r.map((x) => `<tr><td>${DAYS[x.day].slice(0, 2)}</td><td>${bb[x.n - 1].join('–')}</td><td>${x.s} <span class="dim">· ${x.k}</span></td><td>${x.room}</td><td>${mode === 'g' ? x.t : x.g}</td></tr>`).join('') + '</tbody></table></div>';
  };
  document.querySelectorAll('#smode button').forEach((b) => b.addEventListener('click', () => { mode = b.dataset.k; document.querySelectorAll('#smode button').forEach((x) => x.setAttribute('aria-pressed', x === b)); q.value = ''; fill(); render(); }));
  q.addEventListener('input', render); corp.addEventListener('change', render); fill();
  document.getElementById('sics').addEventListener('click', () => {
    const r = pick(); if (!r.length) { out.innerHTML = '<p class="dim">Сначала выберите группу.</p>'; return; }
    const d = new Date(), mon = new Date(d.getFullYear(), d.getMonth(), d.getDate() - ((d.getDay() + 6) % 7)), bb = B[corp.value];
    const pad = (n) => String(n).padStart(2, '0'), stamp = (dt, t) => { const [h, m] = t.split(':').map(Number); const x = new Date(dt); x.setHours(h, m, 0, 0); return `${x.getFullYear()}${pad(x.getMonth() + 1)}${pad(x.getDate())}T${pad(h)}${pad(m)}00`; };
    let ics = 'BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//BGITU//Schedule demo//RU\r\n';
    r.forEach((x, i) => { const day = new Date(mon); day.setDate(mon.getDate() + x.day - 1);
      ics += `BEGIN:VEVENT\r\nUID:bgitu-${i}-${Date.now()}@demo\r\nDTSTART:${stamp(day, bb[x.n - 1][0])}\r\nDTEND:${stamp(day, bb[x.n - 1][1])}\r\nSUMMARY:${x.s} (${x.k})\r\nLOCATION:ауд. ${x.room}\r\nEND:VEVENT\r\n`; });
    ics += 'END:VCALENDAR\r\n';
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([ics], { type: 'text/calendar' })); a.download = 'bgitu-raspisanie.ics'; a.click(); URL.revokeObjectURL(a.href);
  });
})();
</script>
"""
html = hero([('student.html', 'Студенту'), (None, 'Расписание')], 'Расписание', 'Расписание <span class="hl">и звонки</span>',
            'Время пар в обоих корпусах, номер текущей недели и поиск по группе, преподавателю или аудитории.', WEEK)
html += sec('zvonki', '01', 'Расписание звонков', 'текущая пара подсвечена', bells, True)
html += sec('find', '02', 'Поиск и выгрузка в календарь', 'группа · преподаватель · аудитория', sched_tool)
html += sec('official', '03', 'Официальные расписания', 'bgitu.ru и ЭОС', rows([
    ('очное', 'Очное обучение', BG + '/studentu/raspisanie/ochnoe-obuchenie/'), ('заочное', 'Заочное обучение', BG + '/studentu/raspisanie/zaochnoe-obuchenie/'),
    ('о-з', 'Очно-заочное обучение', BG + '/studentu/raspisanie/ochno-zaochnoe/'), ('маг.', 'Магистратура, очная', BG + '/studentu/raspisanie/magistratura/'),
    ('маг.', 'Магистратура, заочная', BG + '/studentu/raspisanie/magistratura/zaochnoe/'), ('спо', 'Колледж (СПО)', BG + '/studentu/raspisanie/spo/'),
    ('гиа', 'Государственная итоговая аттестация', BG + '/studentu/raspisanie/gia/'), ('эос', 'Расписание в ЭОС: группа / преподаватель / аудитория', EOS + '/Rasp/Default.aspx', 'eos.bgitu.ru ↗'),
    ('вуц', 'Военный учебный центр', BG + '/universitet/voennyy-uchebnyy-tsentr/raspisanie-zanyatiy/')]), True)
html += close()
html = html.replace('\n</main>', '\n</main>' + SCHED_JS, 1)
save('schedule.html', 'schedule.html', 'Расписание', html)

# ================================================================= ЭОС
html = hero([('student.html', 'Студенту'), (None, 'ЭОС')], 'Электронная образовательная среда', 'ЭОС и <span class="hl">электронное обучение</span>',
            'Карта сервисов электронной информационно-образовательной среды БГИТУ. В новом сайте всё это открывается из единого личного кабинета.',
            '<div class="hero__cta">' + ext(EOS + '/Account/Login.aspx', 'Войти в ЭОС', 'accent') + ext('http://moodle.bgitu.ru/', 'СДО Moodle') + '</div>')
html += sec('map', '01', 'Карта сервисов', '12 разделов', cards([
    ('лк', 'Курсы', 'Изучаемые дисциплины и учебно-методические материалы.', 'lk.html', 'В кабинете →'),
    ('лк', 'Оценки', 'Электронные рейтинговые ведомости, текущие оценки и пересдачи.', 'lk.html', 'В кабинете →'),
    ('лк', 'Электронная зачётка', 'Результаты промежуточной аттестации по семестрам.', 'lk.html', 'В кабинете →'),
    ('открыто', 'Расписание', 'По группе, аудитории или преподавателю; текущая неделя.', 'schedule.html', 'Открыть →'),
    ('открыто', 'Графики учебного процесса', 'Контрольные точки, сессии, практики и каникулы.', EOS + '/', 'eos.bgitu.ru ↗'),
    ('открыто', 'Учебные планы', 'Рабочие планы на весь срок обучения.', 'program.html#plan', 'Пример плана →'),
    ('лк', 'Задолженности', 'Персональный список долгов, даты консультаций и пересдач.', 'lk.html', 'В кабинете →'),
    ('открыто', 'Сводные ведомости', 'Итоги сессии по группам.', EOS + '/', 'eos.bgitu.ru ↗'),
    ('лк', 'Моё портфолио', 'Достижения в учёбе, науке, спорте и общественной жизни.', 'scholarships.html#calc', 'Для ПГАС →'),
    ('лк', 'Почта', 'Сообщения деканата и преподавателей.', 'lk.html', 'В кабинете →'),
    ('открыто', 'Библиотека', 'Поиск литературы и список по дисциплинам.', 'library.html', 'Подробнее →'),
    ('сдо', 'Moodle', 'Дистанционные курсы по институтам и кафедрам.', 'http://moodle.bgitu.ru/', 'moodle.bgitu.ru ↗')]), True)
html += sec('access', '02', 'Доступ', 'вход и регистрация', faq_block([
    ('Как получить логин и пароль?', f'Логин обучающегося — его e-mail. Адрес должен быть внесён в личное дело в деканате. На странице <a href="{EOS}/Account/Register.aspx" target="_blank" rel="noopener">регистрации</a> введите e-mail и нажмите «Получить пароль».'),
    ('Забыл пароль', f'Новый пароль придёт на e-mail: <a href="{EOS}/Account/Register.aspx?fPass=1" target="_blank" rel="noopener">восстановление пароля</a>.'),
    ('Есть ли версия для слабовидящих?', 'Да: кнопка «Доступность» в шапке этого сайта меняет размер шрифта, интервалы, цвет и отключает изображения.'),
    ('Где мобильное приложение?', 'Этот сайт можно установить на телефон как приложение: в Safari — «Поделиться → На экран «Домой»», в Chrome — «Установить приложение».')]))
html += close()
save('eos.html', 'eos.html', 'ЭОС', html)

# ================================================================= СТИПЕНДИИ
SCH_JS = r"""<script>
/* Калькулятор «Как увеличить стипендию» — подсказки по видам стипендий; суммы — по приказам на bgitu.ru */
(() => {
  const f = document.getElementById('schf'); if (!f) return;
  const out = document.getElementById('schout');
  const run = () => {
    const v = (n) => f.elements[n].checked, g = f.elements.grades.value, tips = [], can = [];
    if (g === '5' || g === '45') can.push('Государственная академическая стипендия (ГАС) — сессия без троек и долгов');
    else tips.push('Закройте сессию без троек и задолженностей — это условие академической стипендии.');
    if (g === '5') can.push('Повышенный размер ГАС за отличную учёбу — уточните в деканате');
    const pgas = ['sci', 'sport', 'art', 'soc'].filter(v);
    if (pgas.length && g !== '3') can.push('Повышенная государственная академическая стипендия (ПГАС) — за ' + pgas.map((x) => ({ sci: 'науку', sport: 'спорт', art: 'творчество', soc: 'общественную работу' })[x]).join(', '));
    else tips.push('Для ПГАС нужны достижения в науке, спорте, творчестве или общественной работе — загружайте их в «Моё портфолио».');
    if (v('soc_need')) can.push('Государственная социальная стипендия (ГСС) — по справке из соцзащиты');
    if (v('family')) can.push('Единое окно поддержки молодых семей — материальная помощь');
    if (!v('sci')) tips.push('Публикация или участие в конференции — самый частый путь к ПГАС.');
    out.innerHTML = '<p class="mono dim">можно претендовать</p>' + (can.length ? '<ul class="deps">' + can.map((x) => `<li><div><h3>${x}</h3></div></li>`).join('') + '</ul>' : '<p class="dim">Пока ни на что — посмотрите подсказки ниже.</p>') +
      (tips.length ? '<p class="mono dim" style="margin-top:18px">что успеть до конца семестра</p><ul class="deps">' + tips.map((x) => `<li><div><p>${x}</p></div></li>`).join('') + '</ul>' : '');
  };
  f.addEventListener('change', run); run();
})();
</script>
"""
sch_tool = '''<div class="tool"><form class="form" id="schf" onsubmit="return false">
      <label class="wide">Итоги последней сессии<select name="grades"><option value="5">только «отлично»</option><option value="45" selected>«хорошо» и «отлично»</option><option value="3">есть тройки или долги</option></select></label>
      <label><span><input type="checkbox" name="sci" style="width:auto;min-height:0"> Научные публикации, конференции</span></label>
      <label><span><input type="checkbox" name="sport" style="width:auto;min-height:0"> Спортивные достижения</span></label>
      <label><span><input type="checkbox" name="art" style="width:auto;min-height:0"> Творческие конкурсы</span></label>
      <label><span><input type="checkbox" name="soc" style="width:auto;min-height:0"> Волонтёрство, общественная работа</span></label>
      <label><span><input type="checkbox" name="soc_need" style="width:auto;min-height:0"> Есть право на социальную поддержку</span></label>
      <label><span><input type="checkbox" name="family" style="width:auto;min-height:0"> Молодая семья</span></label>
    </form><div class="tool__out" id="schout"></div></div>'''
html = hero([('student.html', 'Студенту'), (None, 'Стипендии')], 'Стипендии и поддержка', 'Стипендии <span class="hl">и поддержка</span>',
            'Какие стипендии бывают, кто может их получать и как увеличить свою. Размеры выплат устанавливаются приказами университета.')
html += sec('types', '01', 'Виды стипендий', 'федеральные и именные', cards([
    ('гас', 'Академическая', 'Назначается по итогам сессии: без троек и академических задолженностей.', None, None),
    ('пгас', 'Повышенная академическая', 'За достижения в учёбе, науке, спорте, творчестве и общественной деятельности.', None, None),
    ('гсс', 'Социальная', 'Для студентов, имеющих право на государственную социальную помощь.', None, None),
    ('именные', 'Правительства и Президента РФ', 'Для студентов с выдающимися успехами, в том числе по приоритетным направлениям.', None, None)]), True)
html += sec('calc', '02', 'Как увеличить стипендию', 'калькулятор-подсказка', sch_tool)
html += sec('support', '03', 'Поддержка', 'помощь и льготы', rows([
    ('семьи', 'Единое окно поддержки молодых семей', BG + '/studentu/'), ('соцподдержка', 'Социальная поддержка', BG + '/studentu/'),
    ('профком', 'Материальная помощь через профком студентов', 'https://profkombgitu.ru/', 'profkombgitu.ru ↗'), ('сведения', 'Стипендии и меры поддержки — сведения об ОО', BG + '/sveden/grants/')]), True)
html += close()
html = html.replace('\n</main>', '\n</main>' + SCH_JS, 1)
save('scholarships.html', 'scholarships.html', 'Стипендии', html)

# ================================================================= БИБЛИОТЕКА
html = hero([('student.html', 'Студенту'), (None, 'Библиотека')], 'Библиотека', 'Библиотека <span class="hl">и ЭБС</span>',
            'Электронный каталог, литература по дисциплинам и электронно-библиотечная система IPR SMART — с единым входом через кабинет.',
            '<div class="hero__cta">' + ext(EOS + '/Library/Search.aspx', 'Поиск в каталоге', 'accent') + ext(EOS + '/Library/LibDiscipline.aspx', 'Литература по дисциплинам') + '</div>')
html += sec('res', '01', 'Ресурсы', 'каталог и ЭБС', cards([
    ('эос', 'Поиск по библиотеке', 'По названию, автору, специальности и дисциплине.', EOS + '/Library/Search.aspx', 'eos.bgitu.ru ↗'),
    ('эос', 'Дисциплины библиотеки', 'Списки литературы, привязанные к дисциплинам учебных планов.', EOS + '/Library/LibDiscipline.aspx', 'eos.bgitu.ru ↗'),
    ('эбс', 'IPR SMART', 'Электронные учебники и пособия; вход — через учётную запись ЭОС.', 'https://www.iprbookshop.ru/', 'iprbookshop.ru ↗')]), True)
html += sec('book', '02', 'Бронь читального места', 'корпус №2', f'''<div class="split-layout"><div class="sticky"><h3 class="big">Место <span class="hl">для работы</span></h3><p class="lead-2">Читальные места и комнаты для командной работы — в корпусе №2 (пр-т Ленина, 26).</p></div>
      <div class="tool"><p style="margin-bottom:14px">{DEMO}</p><form class="form" onsubmit="event.preventDefault(); this.nextElementSibling.hidden = false"><label>Дата<input type="date" required></label><label>Время<select><option>9:00–12:00</option><option>12:00–15:00</option><option>15:00–18:00</option></select></label>
      <label>Формат<select><option>Читальное место</option><option>Комната для команды (до 6 человек)</option></select></label><label>E-mail<input type="email" placeholder="you@bgitu.ru" required></label>
      <div class="wide"><button class="btn btn--accent btn--sm" type="submit">Забронировать</button></div></form><p class="note" hidden style="margin-top:14px">Демо: бронь не отправлена. В рабочей версии подтверждение придёт на почту.</p></div></div>''')
html += close()
save('library.html', 'library.html', 'Библиотека', html)

# ================================================================= СТУДЕНЧЕСКАЯ ЖИЗНЬ
html = hero([('student.html', 'Студенту'), (None, 'Студенческая жизнь')], 'Молодёжная политика', 'Студенческая <span class="hl">жизнь</span>',
            'Советы обучающихся, клубы, спорт, волонтёрство и профком — и единая афиша событий университета.')
html += sec('orgs', '01', 'Объединения', 'по структуре БГИТУ', cards([
    ('осо', 'Объединённый совет обучающихся', 'Студенческое самоуправление университета.', None, None),
    ('клуб', 'Студенческий клуб «Тонус»', 'Творческие коллективы и мероприятия.', None, None),
    ('спорт', 'Спортивный клуб БГИТУ', 'Секции и сборные; стадион на 400 мест и спортзал.', 'campus.html#life', 'Кампус →'),
    ('добро', 'Центр поддержки добровольческих инициатив', 'Волонтёрские проекты и «Обучение служением».', None, None),
    ('профком', 'Профком студентов', 'Защита прав студентов, материальная помощь.', 'https://profkombgitu.ru/', 'profkombgitu.ru ↗')]), True)
html += sec('afisha', '02', 'Афиша', 'ближайшие события — с bgitu.ru', '<ul class="news">\n' + news_rows(NEWS[:3] + ANN[:2]) + '\n    </ul>')
html += close('Хотите в команду? <span class="hl">Напишите нам</span>', ext('https://vk.com/bgitu_ru', 'ВКонтакте', 'accent') + ext('https://t.me/bgituofficial', 'Telegram'))
save('life.html', 'life.html', 'Студенческая жизнь', html)

# ================================================================= КАРЬЕРА
html = hero([('student.html', 'Студенту'), (None, 'Карьера')], 'Трудоустройство', 'Карьера <span class="hl">и практика</span>',
            'Центр содействия трудоустройству, стажировки у партнёров и целевое обучение с гарантией работы.')
html += sec('how', '01', 'С чего начать', '3 шага', '''<ol class="steps">
      <li data-reveal><span class="step-n">01</span><div><h4>Соберите резюме</h4><p>Добавьте практики, курсовые проекты и достижения из портфолио.</p></div></li>
      <li data-reveal><span class="step-n">02</span><div><h4>Выберите стажировку</h4><p>Партнёры университета приглашают студентов на практику и экскурсии на производство.</p></div></li>
      <li data-reveal><span class="step-n">03</span><div><h4>Обратитесь в центр</h4><p>Центр содействия трудоустройству поможет с резюме и подбором вакансий.</p></div></li></ol>''', True)
html += sec('links', '02', 'Ресурсы', 'вакансии и программы', rows([
    ('цст', 'Центр содействия трудоустройству', BG + '/studentu/'), ('вакансии', 'Работа в России — вакансии и целевое обучение', 'https://trudvsem.ru/', 'trudvsem.ru ↗'),
    ('целевое', 'Целевое обучение в БГИТУ', 'target.html'), ('практика', 'Экскурсии на производство и стажировки — в ленте новостей', 'news.html')]))
html += close()
save('career.html', 'career.html', 'Карьера', html)

# ================================================================= ДПО
html = hero([('student.html', 'Студенту'), (None, 'ДПО')], 'Дополнительное образование', 'Переподготовка <span class="hl">и повышение квалификации</span>',
            'Программы отдела дополнительного профессионального образования для специалистов и выпускников.',
            '<div class="meta-row"><span>Руководитель — <b>Ерохина Юлия Сергеевна</b></span><span>пр-т Станке Димитрова, 3, ауд. 241</span><a href="tel:+74832649562">+7 (4832) 64-95-62</a><a href="mailto:dpo@bgitu.ru">dpo@bgitu.ru</a></div>')
html += sec('progs', '01', 'Программы', 'набор открыт', rows([
    ('переподготовка', 'Ценообразование и сметное нормирование в строительстве', BG + '/obyavl/index.php?news=4591', 'объявление ↗')]), True)
html += sec('enrol', '02', 'Заявка', 'обратный звонок', f'''<div class="tool"><p style="margin-bottom:14px">{DEMO}</p><form class="form" onsubmit="event.preventDefault(); this.nextElementSibling.hidden = false"><label>Имя<input required></label><label>Телефон<input type="tel" required></label>
      <label class="wide">Программа<select><option>Ценообразование и сметное нормирование в строительстве</option><option>Другая — уточню по телефону</option></select></label><div class="wide"><button class="btn btn--accent btn--sm">Отправить</button></div></form>
      <p class="note" hidden style="margin-top:14px">Демо: заявка не отправлена. Позвоните в отдел ДПО: +7 (4832) 64-95-62.</p></div>''')
html += close()
save('dpo.html', 'dpo.html', 'ДПО', html)

# ================================================================= ПОМОЩЬ: FAQ, ГОСТ, ЧАТ
deps_all = [(u['short'], d[0]) for k, u in UNITS.items() for d in u['deps']]
REPORT_JS = r"""<script>
/* Генератор титульного листа по ГОСТ: предпросмотр, печать в PDF и файл .doc для Word */
(() => {
  const f = document.getElementById('rf'); if (!f) return;
  const P = document.getElementById('paper'), v = (n) => (f.elements[n].value || '').trim();
  const draw = () => {
    P.innerHTML = `<div>Министерство науки и высшего образования Российской Федерации<br>ФГБОУ ВО «Брянский государственный инженерно-технологический университет»</div>
      <div style="margin-top:4%">${v('inst')}<br>${v('dep')}</div>
      <div class="t">${v('kind')}${v('num') ? ' № ' + v('num') : ''}</div><div>по дисциплине «${v('disc') || '…'}»</div>${v('topic') ? `<div style="margin-top:2%">на тему: «${v('topic')}»</div>` : ''}
      <div class="who">Выполнил: студент гр. ${v('group') || '…'}<br>${v('student') || '…'}<br><br>Проверил: ${v('teacher') || '…'}</div>
      <div class="city">Брянск ${new Date().getFullYear()}</div>`;
  };
  f.addEventListener('input', draw); draw();
  document.getElementById('rprint').addEventListener('click', () => { const w = open('', '_blank'); w.document.write(`<html><head><title>Титульный лист</title><style>@page{size:A4;margin:20mm 15mm 20mm 30mm}body{font:14pt/1.5 'Times New Roman',serif;text-align:center}.t{margin-top:30%;font-weight:700;text-transform:uppercase}.who{margin-top:25%;margin-left:52%;text-align:left}.city{margin-top:15%}</style></head><body>${P.innerHTML}</body></html>`); w.document.close(); w.focus(); w.print(); });
  document.getElementById('rdoc').addEventListener('click', () => {
    const html = `<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word"><head><meta charset="utf-8"><style>@page{size:21cm 29.7cm;margin:2cm 1.5cm 2cm 3cm}body{font-family:'Times New Roman';font-size:14pt;text-align:center}.t{margin-top:200pt;font-weight:bold;text-transform:uppercase}.who{margin-top:150pt;margin-left:250pt;text-align:left}.city{margin-top:80pt}</style></head><body>${P.innerHTML}</body></html>`;
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob(['﻿', html], { type: 'application/msword' })); a.download = 'titulnyi-list.doc'; a.click(); URL.revokeObjectURL(a.href);
  });
})();
/* Помощник: отвечает по базе этого сайта и даёт ссылку на источник (демо без ИИ-сервера) */
(() => {
  const form = document.getElementById('chatf'); if (!form) return;
  const log = document.getElementById('chatlog'), inp = form.querySelector('input');
  const KB = [
    [['поступ', 'документ', 'приём', 'абитур'], 'Подать документы можно в приёмной комиссии (пр-т Станке Димитрова, 3, ауд. 216) или онлайн через «Госуслуги».', 'admission.html'],
    [['расписан', 'пара', 'звонк', 'недел'], 'Время пар обоих корпусов и номер текущей недели — на странице расписания.', 'schedule.html'],
    [['стипенд', 'пгас', 'деньг'], 'Виды стипендий и калькулятор «как увеличить стипендию».', 'scholarships.html'],
    [['общежит', 'заселен', 'жиль'], 'В университете 4 общежития; порядок заселения — в приёмной комиссии.', 'campus.html'],
    [['эос', 'парол', 'логин', 'moodle'], 'Логин в ЭОС — ваш e-mail из личного дела; пароль можно получить на странице регистрации ЭОС.', 'eos.html'],
    [['справк', 'заявлен'], 'Справки и заявления заказываются в личном кабинете.', 'lk.html'],
    [['титул', 'гост', 'отчёт', 'отчет', 'лаборатор', 'курсов'], 'Титульный лист по ГОСТ собирается прямо на этой странице, ниже.', 'help.html#report'],
    [['перевод', 'бюджет', 'восстанов'], 'Порядок перевода и восстановления, в том числе с платного на бюджет.', 'transfer.html'],
    [['библиот', 'книг', 'эбс'], 'Каталог, литература по дисциплинам и ЭБС IPR SMART.', 'library.html'],
    [['телефон', 'контакт', 'адрес', 'почт'], 'Телефоны и адреса всех подразделений — на странице контактов.', 'contacts.html'],
    [['армия', 'вуц', 'военн'], 'Военная подготовка — в военном учебном центре.', 'inst-vuc.html']];
  const say = (t, me) => { const d = document.createElement('div'); d.className = 'chat__msg' + (me ? ' me' : ''); d.innerHTML = t; log.append(d); log.scrollTop = log.scrollHeight; };
  say('Здравствуйте! Я отвечаю по материалам этого сайта. Спросите, например: «как получить пароль от ЭОС?»');
  form.addEventListener('submit', (e) => {
    e.preventDefault(); const q = inp.value.trim(); if (!q) return; say(q.replace(/</g, '&lt;'), true); inp.value = '';
    const ql = q.toLowerCase(), hit = KB.find(([keys]) => keys.some((k) => ql.includes(k)));
    setTimeout(() => say(hit ? `${hit[1]} <a href="${hit[2]}">Подробнее →</a>` : 'Не нашёл ответа на сайте. Передайте вопрос в приёмную комиссию: <a href="tel:+74832649912">+7 (4832) 64-99-12</a> или на <a href="mailto:mail@bgitu.ru">mail@bgitu.ru</a>.'), 350);
  });
})();
</script>
"""
inst_opts = ''.join(f'<option>{u["name"]}</option>' for k, u in UNITS.items() if k in ('les', 'stroy', 'econ', 'fop'))
dep_opts = ''.join(f'<option>{d}</option>' for s, d in deps_all if d.startswith('Кафедра'))
report = f'''<div class="split-layout"><div class="tool"><form class="form" id="rf" onsubmit="return false">
      <label class="wide">Институт<select name="inst">{inst_opts}</select></label><label class="wide">Кафедра<select name="dep">{dep_opts}</select></label>
      <label>Вид работы<select name="kind"><option>Отчёт по лабораторной работе</option><option>Расчётно-графическая работа</option><option>Курсовая работа</option><option>Курсовой проект</option><option>Отчёт по практике</option></select></label>
      <label>Номер<input name="num" placeholder="1"></label><label class="wide">Дисциплина<input name="disc" placeholder="Программная инженерия"></label><label class="wide">Тема<input name="topic" placeholder="необязательно"></label>
      <label>Группа<input name="group" placeholder="ПИ-201"></label><label>Студент<input name="student" placeholder="Фамилия И. О."></label><label class="wide">Преподаватель<input name="teacher" placeholder="должность, Фамилия И. О."></label></form>
      <div class="btn-row"><button class="btn btn--accent btn--sm" type="button" id="rprint">Печать / PDF</button><button class="btn btn--ghost btn--sm" type="button" id="rdoc">Скачать .doc</button></div></div>
      <div><div class="paper" id="paper" aria-label="Предпросмотр титульного листа"></div><p class="dim" style="margin-top:12px;font-size:.875rem">Поля по ГОСТ: левое 30 мм, правое 15 мм, верхнее и нижнее 20 мм; Times New Roman 14 пт. Сверьте с требованиями своей кафедры.</p></div></div>'''
chat = '<div class="chat" id="chat"><div class="chat__log" id="chatlog" aria-live="polite"></div><form id="chatf"><input placeholder="Ваш вопрос" aria-label="Вопрос помощнику"><button class="btn btn--accent btn--sm">Спросить</button></form></div>'
html = hero([('student.html', 'Студенту'), (None, 'Помощь')], 'Помощь', 'Ответы, инструкции <span class="hl">и инструменты</span>',
            'Частые вопросы, генератор титульного листа по ГОСТ и помощник, который отвечает по материалам сайта.')
html += sec('faq', '01', 'Частые вопросы', 'студентам и абитуриентам', faq_block([
    ('Как получить справку об обучении?', 'Закажите её в личном кабинете — когда справка будет готова, придёт уведомление.'),
    ('Как перевестись с платного обучения на бюджет?', 'Порядок и сроки — на странице <a href="transfer.html">«Перевод и восстановление»</a>.'),
    ('Как закрыть академическую задолженность?', 'Список долгов и даты пересдач — в личном кабинете, раздел «Задолженности».'),
    ('Как зарегистрироваться в ЭБС IPR SMART?', 'Вход — через учётную запись ЭОС, подробности на странице <a href="library.html">«Библиотека»</a>.'),
    ('Где расписание звонков?', 'На странице <a href="schedule.html">«Расписание»</a> — для обоих корпусов, с подсветкой текущей пары.')]), True)
html += sec('report', '02', 'Титульный лист по ГОСТ', 'лабораторные · РГР · курсовые', report)
html += sec('assistant', '03', 'Помощник', 'отвечает по материалам сайта', f'<p style="margin-bottom:16px">{DEMO}</p>' + chat, True)
html += close()
html = html.replace('\n</main>', '\n</main>' + REPORT_JS, 1)
save('help.html', 'help.html', 'Помощь', html)

# ================================================================= НАУКА
html = hero([(None, 'Наука')], 'Наука и инновации', 'Наука, <span class="hl">которая работает на отрасль</span>',
            'Научные центры, гранты, конференции и подготовка кадров высшей квалификации.',
            '<div class="meta-row"><span>Проректор по научной и инновационной деятельности — <b>Тихомиров П. В.</b></span></div>')
html += sec('centers', '01', 'Подразделения', 'по структуре БГИТУ', cards([
    ('унои', 'Управление научно-образовательных инноваций', 'Организация научной работы и инновационных проектов.', None, None),
    ('цкп', 'ЦКП научным оборудованием', 'Центр коллективного пользования для исследований.', None, None),
    ('инжиниринг', 'Инжиниринговый центр', 'Проекты для промышленных партнёров.', None, None),
    ('цифра', 'Центр цифровых компетенций', 'IT-проекты и цифровые навыки.', None, None),
    ('кадры', 'Аспирантура', '14 научных специальностей, очная форма.', 'aspirantura.html', 'Подробнее →')]), True)
html += sec('grants', '02', 'Гранты и проекты', 'с главной bgitu.ru', rows([
    ('рнф', 'Грант РНФ № 23-28-00180', BG + '/'), ('рффи', 'Грант РФФИ № 18-41-320003', BG + '/'), ('рффи', 'Грант РФФИ № 18-08-00567', BG + '/'), ('рффи', 'Грант РФФИ № 16-38-00041', BG + '/')]))
html += sec('events', '03', 'Конференции и проекты', 'октябрь 2026', '<ul class="news">\n' + news_rows([n for n in NEWS if 'конференц' in n[1].lower() or 'проект' in n[1].lower()]) + '\n    </ul>', True)
html += close('Хотите в науку? <span class="hl">Начните с аспирантуры</span>', btn('aspirantura.html', 'Аспирантура') + btn('contacts.html', 'Контакты', 'ghost', None))
save('science.html', 'science.html', 'Наука', html)

# ================================================================= АСПИРАНТУРА
asp_list = '<ul class="dirs">' + ''.join(f'<li data-s="Направление" data-t="{c} {t}"><span class="mono">{c}</span><b>{t}</b><span class="mono dim">аспирантура</span><span class="mono dim">очная</span></li>' for c, t in ASP) + '</ul>'
html = hero([('science.html', 'Наука'), (None, 'Аспирантура')], 'Кадры высшей квалификации', 'Аспирантура <span class="hl">БГИТУ</span>',
            'Научные специальности, правила приёма и расписание занятий. Отдел подготовки кадров высшей квалификации — корпус №1, ауд. 210.')
html += sec('list', '01', 'Научные специальности', f'{len(ASP)} специальностей · очная форма', asp_list, True)
html += sec('links', '02', 'Документы и расписание', 'bgitu.ru', rows([
    ('расписание', 'Расписание занятий аспирантов', BG + '/nauka/otdel-podgotovki-kadrov-vysshey-kvalifikatsii-i-molodezhnoy-nauki/raspisanie-zanyatiy-aspirantura/'),
    ('приём', 'Поступление в аспирантуру', 'admission.html#levels')]))
html += close()
save('aspirantura.html', 'aspirantura.html', 'Аспирантура', html)

# ================================================================= КАТАЛОГ НАПРАВЛЕНИЙ + КАЛЬКУЛЯТОР ЕГЭ
bak = [p for p in PROGS if p[4] in ('бакалавриат', 'специалитет')]
EGE_JS = """<script>
/* Калькулятор «Хватит ли баллов ЕГЭ» (демо): сумма трёх предметов + индивидуальные достижения и подходящие направления */
(() => {
  const f = document.getElementById('egef'); if (!f) return;
  const PR = %s;
  const SETS = { tech: [['rus'], ['mat'], ['fiz', 'inf']], it: [['rus'], ['mat'], ['inf', 'fiz']], econ: [['rus'], ['mat'], ['obs', 'inf']], gmu: [['rus'], ['obs', 'mat'], ['ist', 'inf']], bio: [['rus'], ['mat', 'bio'], ['bio', 'him']] };
  const kind = (c) => c.startsWith('09') ? 'it' : c.startsWith('38.03.04') ? 'gmu' : c.startsWith('38') ? 'econ' : c.startsWith('35.03.07') || c.startsWith('35.03.05') ? 'bio' : 'tech';
  const out = document.getElementById('egeout');
  const run = () => {
    const s = {}; ['rus', 'mat', 'fiz', 'inf', 'obs', 'ist', 'him', 'bio'].forEach((k) => { s[k] = Math.min(100, Math.max(0, +f.elements[k].value || 0)); });
    const id = Math.min(10, Math.max(0, +f.elements.id.value || 0));
    const res = PR.map(([c, t]) => { const set = SETS[kind(c)]; let sum = 0, ok = true;
      set.forEach((alt) => { const best = Math.max(...alt.map((k) => s[k])); if (!best) ok = false; sum += best; });
      return { c, t, ok, sum: sum + id }; }).filter((x) => x.ok).sort((a, b) => b.sum - a.sum);
    out.innerHTML = res.length ? `<p class="mono dim">ваша сумма с ИД</p><div class="tool__big">${res[0].sum}</div><p class="mono dim" style="margin:16px 0 8px">направления, на которые подходят ваши предметы</p><ul class="dirs">` +
      res.map((x) => `<li><span class="mono">${x.c}</span><b>${x.t}</b><span class="mono dim">${x.sum} баллов</span><span class="mono dim"></span></li>`).join('') + '</ul>'
      : '<p class="dim">Введите баллы хотя бы по русскому, математике и одному профильному предмету.</p>';
  };
  f.addEventListener('input', run); run();
})();
</script>
""" % json.dumps([[p[0], p[1] + (' — ' + p[2].split(' · ')[0] if p[2] and p[0] == '35.03.02' else '')] for p in bak], ensure_ascii=False)
ege = f'''<div class="split-layout"><div class="tool"><p style="margin-bottom:14px">{DEMO}</p><form class="form" id="egef" onsubmit="return false">
      <label>Русский язык<input name="rus" type="number" min="0" max="100" value="70"></label><label>Математика (профиль)<input name="mat" type="number" min="0" max="100" value="65"></label>
      <label>Физика<input name="fiz" type="number" min="0" max="100"></label><label>Информатика<input name="inf" type="number" min="0" max="100" value="72"></label>
      <label>Обществознание<input name="obs" type="number" min="0" max="100"></label><label>История<input name="ist" type="number" min="0" max="100"></label>
      <label>Химия<input name="him" type="number" min="0" max="100"></label><label>Биология<input name="bio" type="number" min="0" max="100"></label>
      <label class="wide">Индивидуальные достижения (до 10 баллов)<input name="id" type="number" min="0" max="10" value="0"></label></form>
      <p class="dim" style="margin-top:14px;font-size:.875rem">Наборы предметов в демо условные. Точный перечень вступительных испытаний и проходные баллы — в разделе «Вступительные испытания» на bgitu.ru.</p></div>
      <div class="tool"><div id="egeout"></div></div></div>'''
html = hero([('admission.html', 'Поступающим'), (None, 'Направления')], 'Каталог программ', 'Направления подготовки <span class="hl">2026/27</span>',
            f'{len(PROGS)} программ трёх институтов: колледж, бакалавриат, специалитет и магистратура. Фильтры по институту и уровню, поиск по названию, профилю и коду.')
html += sec('dirs', '01', 'Каталог', f'набор 2026/27 · {len(PROGS)} программ', dirs.replace('id="dirlist"', 'id="dirlist2"').replace('data-filter="#dirlist"', 'data-filter="#dirlist2"'), True)
html += sec('ege', '02', 'Хватит ли баллов ЕГЭ', 'калькулятор', ege)
html += sec('card', '03', 'Карточка направления', 'пример', cards([('09.03.04', 'Программная инженерия', 'Как устроена карточка: учебный план по семестрам, кафедра, вступительные испытания, вопросы.', 'program.html', 'Открыть пример →')]), True)
html += close('Нужна помощь с выбором? <span class="hl">Позвоните</span>', btn(tel(PRIEM), PRIEM, 'accent', None) + btn('admission.html', 'Приёмная комиссия', 'ghost', None))
html = html.replace('\n</main>', '\n</main>' + EGE_JS, 1)
save('programs.html', 'programs.html', 'Направления подготовки', html)

# ================================================================= КАРТОЧКА НАПРАВЛЕНИЯ (пример 09.03.04)
PLAN = [('1 семестр', [('Математика', 'экз'), ('Информатика', 'экз'), ('Иностранный язык', 'зач'), ('История России', 'зач')]),
        ('2 семестр', [('Программирование', 'экз'), ('Дискретная математика', 'экз'), ('Физика', 'зач'), ('Физическая культура', 'зач')]),
        ('3 семестр', [('Алгоритмы и структуры данных', 'экз'), ('Базы данных', 'экз'), ('Операционные системы', 'зач')]),
        ('4 семестр', [('Объектно-ориентированное программирование', 'экз'), ('Компьютерные сети', 'зач'), ('Курсовая работа', 'КР')]),
        ('5 семестр', [('Проектирование ПО', 'экз'), ('Веб-разработка', 'зач'), ('Учебная практика', 'зач')]),
        ('6–8 семестры', [('Тестирование ПО', 'экз'), ('Управление проектами', 'зач'), ('Производственная практика', 'зач'), ('ВКР', 'ГИА')])]
plan = f'<p style="margin-bottom:14px">{DEMO}</p><div class="plan">' + ''.join(f'<div><b>{s}</b><ul>' + ''.join(f'<li><span>{d}</span><span>{c}</span></li>' for d, c in ds) + '</ul></div>' for s, ds in PLAN) + '</div>'
econ = UNITS['econ']
html = hero([('admission.html', 'Поступающим'), ('programs.html', 'Направления'), (None, '09.03.04')], 'Бакалавриат · Инженерно-экономический институт', 'Программная <span class="hl">инженерия</span>',
            'Разработка, тестирование и сопровождение программного обеспечения — от алгоритмов до управления проектами.',
            f'<div class="meta-row"><span>Код — <b>09.03.04</b></span><span>Выпускающая кафедра — <b>информационных технологий</b></span><a href="inst-econ.html">ИЭИ →</a></div>')
html += sec('plan', '01', 'Учебный план', 'по семестрам', plan, True)
html += sec('dept', '02', 'Кафедра', 'информационных технологий', contact_dl([('Заведующий', 'Казаков Олег Дмитриевич'), ('Адрес', 'пр-т Ленина, 26, ауд. 480в · учебный корпус №2'), ('Телефон', a_tel('+7 (4832) 64-59-89')), ('Почта', a_mail('kaf-it@bgitu.ru'))]))
html += sec('faq', '03', 'Вопросы', 'о направлении', faq_block([
    ('Какие вступительные испытания?', f'Перечень и минимальные баллы публикуются в разделе «Вступительные испытания» на <a href="{BG}/abitur/" target="_blank" rel="noopener">bgitu.ru</a>. Прикинуть сумму можно в <a href="programs.html#ege">калькуляторе</a>.'),
    ('Есть ли практика?', 'Да: учебная и производственная практика входят в учебный план.'),
    ('Можно ли продолжить обучение?', 'Да, в магистратуре по направлению 09.04.02 «Информационные системы и технологии».')]), True)
html += close('Поступайте на <span class="hl">программную инженерию</span>', btn('admission.html', 'Как поступить') + btn('programs.html#ege', 'Калькулятор ЕГЭ', 'ghost'))
save('program.html', 'program.html', 'Программная инженерия', html)

# ================================================================= ЦЕЛЕВОЕ, ШКОЛЬНИКАМ, ПЕРЕВОД, ПЛАТНОЕ, ИНОСТРАННЫМ
html = hero([('admission.html', 'Поступающим'), (None, 'Целевое обучение')], 'Целевое обучение', 'Учёба с гарантией <span class="hl">работы</span>',
            'Целевое обучение — договор с будущим работодателем: место в отдельной квоте, поддержка во время учёбы и трудоустройство после выпуска.')
html += sec('how', '01', 'Как это работает', '3 шага', '''<ol class="steps">
      <li data-reveal><span class="step-n">01</span><div><h4>Найдите предложение</h4><p>Предложения заказчиков целевого обучения публикуются на платформе «Работа в России».</p></div></li>
      <li data-reveal><span class="step-n">02</span><div><h4>Подайте заявку</h4><p>Заявка на целевое обучение подаётся на платформе одновременно с поступлением.</p></div></li>
      <li data-reveal><span class="step-n">03</span><div><h4>Поступите по квоте</h4><p>Конкурс по целевой квоте идёт отдельно от общего.</p></div></li></ol>''', True)
html += sec('links', '02', 'Ссылки', 'подробнее', rows([('бгиту', 'Приём на целевое обучение', BG + '/abitur/tselevoy-priem/'), ('платформа', 'Работа в России — предложения целевого обучения', 'https://trudvsem.ru/', 'trudvsem.ru ↗')]))
html += close()
save('target.html', 'target.html', 'Целевое обучение', html)

html = hero([('admission.html', 'Поступающим'), (None, 'Школьникам')], 'Довузовская подготовка', 'Школьникам: <span class="hl">инженерный старт</span>',
            'Центр технического образования, олимпиады, Малая инженерная академия и курсы подготовки к ЕГЭ.')
html += sec('progs', '01', 'Программы', 'для 9–11 классов', cards([
    ('цто', 'Центр технического образования школьников', 'Занятия для одиннадцатиклассников в Советском и Фокинском районах Брянска, в Унече и Клинцах.', BG + '/schoolboys/tsentr-tekhnicheskogo-obrazovaniya-shkolnikov/', 'bgitu.ru ↗'),
    ('олимпиада', 'Инженерная олимпиада школьников Центра России', 'Олимпиада для будущих инженеров.', BG + '/schoolboys/inzhenernaya-olimpiada-shkolnikov-tsentra-rossii/', 'bgitu.ru ↗'),
    ('миа', 'Малая инженерная академия', 'Олимпиады по математике, информатике и физике вместе с центрами технического образования.', BG + '/schoolboys/malaya-inzhenernaya-akademiya-mia/', 'bgitu.ru ↗'),
    ('it', 'Код будущего', 'Курсы программирования для школьников.', BG + '/schoolboys/kod-budushchego/', 'bgitu.ru ↗'),
    ('егэ', 'Курсы подготовки к ЕГЭ', 'Отбор одиннадцатиклассников на подготовительные курсы.', BG + '/schoolboys/kursy-podgotovki-k-ege/', 'bgitu.ru ↗')]), True)
html += sec('enrol', '02', 'Записаться', 'онлайн-заявка', f'''<div class="tool"><p style="margin-bottom:14px">{DEMO}</p><form class="form" onsubmit="event.preventDefault(); this.nextElementSibling.hidden = false"><label>Имя школьника<input required></label><label>Класс<select><option>9</option><option>10</option><option selected>11</option></select></label>
      <label>Программа<select><option>Центр технического образования</option><option>Малая инженерная академия</option><option>Код будущего</option><option>Курсы подготовки к ЕГЭ</option></select></label><label>Телефон родителя<input type="tel" required></label>
      <div class="wide"><button class="btn btn--accent btn--sm">Отправить заявку</button></div></form><p class="note" hidden style="margin-top:14px">Демо: заявка не отправлена. Узнать о записи — в приёмной комиссии: +7 (4832) 64-99-12.</p></div>''')
html += close()
save('school.html', 'school.html', 'Школьникам', html)

html = hero([('admission.html', 'Поступающим'), (None, 'Перевод и восстановление')], 'Перевод и восстановление', 'Перевод <span class="hl">и восстановление</span>',
            'Перевод с платного обучения на бесплатное, из другого вуза или между направлениями, а также восстановление после отчисления.')
html += sec('steps', '01', 'Порядок', '4 шага', '''<ol class="steps">
      <li data-reveal><span class="step-n">01</span><div><h4>Проверьте вакантные места</h4><p>Таблица вакантных мест для перевода публикуется в сведениях об образовательной организации.</p></div></li>
      <li data-reveal><span class="step-n">02</span><div><h4>Подготовьте документы</h4><p>Заявление, справка о периоде обучения (для перевода из другого вуза), документ об образовании.</p></div></li>
      <li data-reveal><span class="step-n">03</span><div><h4>Подайте заявление</h4><p>В деканат своего института или онлайн — в личном кабинете, со статусом рассмотрения.</p></div></li>
      <li data-reveal><span class="step-n">04</span><div><h4>Дождитесь решения</h4><p>Решение принимает аттестационная комиссия; результат — в кабинете и по почте.</p></div></li></ol>''', True)
html += sec('links', '02', 'Документы', 'bgitu.ru', rows([('места', 'Вакантные места для приёма (перевода)', BG + '/sveden/vacant/'), ('бюджет', 'Перевод с платного обучения на бесплатное', BG + '/studentu/'),
                                                       ('рф', 'Перевод и зачисление граждан РФ, Украины, ЛНР, ДНР', BG + '/studentu/')]))
html += close()
save('transfer.html', 'transfer.html', 'Перевод и восстановление', html)

html = hero([('admission.html', 'Поступающим'), (None, 'Платное обучение')], 'Платное обучение', 'Платное обучение <span class="hl">и оплата</span>',
            'Стоимость по направлениям, договоры, образовательный кредит и реквизиты для оплаты.')
html += sec('links', '01', 'Документы', 'раздел «Абитуриенту» на bgitu.ru', rows([('стоимость', 'Платное обучение: стоимость и договоры', BG + '/abitur/'), ('кредит', 'Образовательный кредит в СПО', BG + '/abitur/'),
                                                                                ('реквизиты', 'Банковские реквизиты для оплаты за обучение', BG + '/abitur/'), ('сведения', 'Платные образовательные услуги — сведения об ОО', BG + '/sveden/paid_edu/')]), True)
html += close('Вопросы об оплате? <span class="hl">Позвоните</span>', btn(tel(PRIEM), PRIEM, 'accent', None))
save('paid.html', 'paid.html', 'Платное обучение', html)

html = hero([('admission.html', 'Поступающим'), (None, 'Иностранным гражданам')], 'Study in Russia', 'Иностранным <span class="hl">гражданам</span>',
            'Приём, визы, адаптация и общежитие для иностранных студентов. Information for international students.')
html += sec('links', '01', 'Разделы', 'bgitu.ru', rows([('info', 'Information for international students', BG + '/studentu/'), ('приём', 'Поступление иностранных граждан', 'admission.html'),
                                                      ('инт.', 'Международное сотрудничество — сведения об ОО', BG + '/sveden/inter/'), ('новость', 'Встреча иностранных студентов БГИТУ из стран Африки с Луисом Гоуендом', BG + '/news/index.php?news=4929')]), True)
html += close('Questions? <span class="hl">Write to us</span>', btn('mailto:mail@bgitu.ru', 'mail@bgitu.ru', 'accent', None))
save('international.html', 'international.html', 'Иностранным гражданам', html)

# ================================================================= СОТРУДНИКАМ, СВЕДЕНИЯ, ДОКУМЕНТЫ, ПРЕСС-ЦЕНТР, БОТСАД
html = hero([('university.html', 'Университет'), (None, 'Сотрудникам')], 'Сотрудникам и преподавателям', 'Сотрудникам <span class="hl">и преподавателям</span>',
            'Ведомости и учебная нагрузка в ЭОС, кадровый состав, телефонный справочник и профсоюз.')
html += sec('links', '01', 'Сервисы', 'для работы', rows([
    ('эос', 'Электронные рейтинговые ведомости и нагрузка', EOS + '/Account/Login.aspx', 'eos.bgitu.ru ↗'), ('сдо', 'Курсы в СДО Moodle', 'http://moodle.bgitu.ru/', 'moodle.bgitu.ru ↗'),
    ('кадры', 'Кадровый состав', BG + '/universitet/kadrovyy-sostav/?section=23'), ('справочник', 'Телефонный справочник', BG + '/universitet/kontakty/telefonnyy-spravochnik/'),
    ('бланки', 'Документы и бланки', 'docs.html'), ('кафедры', 'Кафедры и заведующие', 'contacts.html#directory')]), True)
html += close()
save('staff.html', 'staff.html', 'Сотрудникам', html)

SVEDEN = [('common', 'Основные сведения'), ('struct', 'Структура и органы управления'), ('document', 'Документы'), ('education', 'Образование'), ('eduStandarts', 'Образовательные стандарты и требования'),
          ('managers', 'Руководство'), ('employees', 'Педагогический состав'), ('objects', 'Материально-техническое обеспечение и оснащённость'), ('grants', 'Стипендии и меры поддержки обучающихся'),
          ('paid_edu', 'Платные образовательные услуги'), ('budget', 'Финансово-хозяйственная деятельность'), ('vacant', 'Вакантные места для приёма (перевода)'), ('inter', 'Международное сотрудничество'),
          ('catering', 'Организация питания в образовательной организации')]
html = hero([('university.html', 'Университет'), (None, 'Сведения об ОО')], 'Сведения об образовательной организации', 'Сведения <span class="hl">об образовательной организации</span>',
            'Обязательный раздел по приказу Рособрнадзора № 1493. Дата создания университета — 3 июля 1930 года, учредитель — Министерство науки и высшего образования РФ.')
html += sec('list', '01', 'Подразделы', f'{len(SVEDEN)} разделов', rows([(f'{i + 1:02d}', t, f'{BG}/sveden/{s}/') for i, (s, t) in enumerate(SVEDEN)]), True)
html += close()
save('sveden.html', 'sveden.html', 'Сведения об образовательной организации', html)

html = hero([('university.html', 'Университет'), (None, 'Документы')], 'Документы и бланки', 'Документы <span class="hl">и бланки</span>',
            'Устав, лицензия, аккредитация, локальные акты и шаблоны заявлений.')
html += sec('docs', '01', 'Документы университета', 'bgitu.ru', rows([('устав', 'Устав, лицензия, свидетельство об аккредитации', BG + '/sveden/document/'), ('акты', 'Локальные нормативные акты', BG + '/sveden/document/'),
                                                                       ('приём', 'Правила приёма и нормативная документация', BG + '/abitur/'), ('стандарты', 'Образовательные стандарты', BG + '/sveden/eduStandarts/')]), True)
html += sec('forms', '02', 'Заявления', 'онлайн — в личном кабинете', rows([('справка', 'Справка об обучении', 'lk.html'), ('справка', 'Справка о стипендии', 'lk.html'), ('военкомат', 'Справка для военкомата', 'lk.html'),
                                                                             ('отпуск', 'Заявление на академический отпуск', 'lk.html'), ('перевод', 'Заявление на перевод', 'transfer.html')]))
html += close()
save('docs.html', 'docs.html', 'Документы', html)

html = hero([('university.html', 'Университет'), (None, 'Пресс-центр')], 'Пресс-центр', 'Пресс-центр <span class="hl">БГИТУ</span>',
            'Отдел по информационной политике и связям с общественностью — учебный корпус №1, каб. 213. Официальные соцсети и логотип для скачивания.')
html += sec('soc', '01', 'Официальные соцсети', '5 площадок', rows([(n.lower()[:6], n, u, u.split('/')[2] + ' ↗') for n, u in X.SOCIAL]), True)
html += sec('brand', '02', 'Логотип', 'для партнёров и СМИ', cards([('png', 'Знак БГИТУ', 'Квадратный знак 512×512 для публикаций и презентаций.', 'icon-512.png', 'Скачать →')]))
html += close()
save('press.html', 'press.html', 'Пресс-центр', html)

html = hero([('university.html', 'Университет'), (None, 'Ботанический сад')], 'Природно-производственные объекты', 'Ботанический сад <span class="hl">и лесхоз</span>',
            'Ботанический сад им. Б. В. Гроздова на ул. Горького, 31 и Учебно-опытный лесхоз — учебные и научные базы лесного профиля университета.')
html += sec('obj', '01', 'Объекты', 'учебные базы', cards([
    ('ул. Горького, 31', 'Ботанический сад им. Б. В. Гроздова', 'Коллекции растений, практики студентов, экскурсии.', 'https://yandex.ru/maps/?text=Брянск%2C%20улица%20Горького%2C%2031', 'На карте ↗'),
    ('практика', 'Учебно-опытный лесхоз', 'Полевые практики и научные исследования по лесному хозяйству.', None, None)]), True)
html += close('Хотите на экскурсию? <span class="hl">Позвоните</span>', btn('tel:+74832746008', 'Приёмная ректора', 'accent', None))
save('garden.html', 'garden.html', 'Ботанический сад и лесхоз', html)

# ================================================================= ЛИЧНЫЙ КАБИНЕТ (вход)
html = hero([(None, 'Личный кабинет')], 'Единый вход', 'Личный <span class="hl">кабинет</span>',
            'Один вход во все сервисы: сайт, ЭОС, расписание, зачётка и Moodle. Внутри — оценки, долги, пропуски, стипендия и справки.')
html += sec('login', '01', 'Вход', 'демо-режим', f'''<div class="split-layout"><div class="tool"><p style="margin-bottom:14px">{DEMO}</p><form class="form" onsubmit="event.preventDefault(); this.nextElementSibling.hidden = false">
      <label class="wide">E-mail<input type="email" autocomplete="username" placeholder="you@bgitu.ru" required></label><label class="wide">Пароль<input type="password" autocomplete="current-password" required></label>
      <div class="wide"><button class="btn btn--accent btn--sm">Войти</button></div></form><p class="note" hidden style="margin-top:14px">Демо: вход не выполняется. Единый кабинет в разработке — пока используйте вход в ЭОС.</p>
      <div class="btn-row">{ext(EOS + "/Account/Login.aspx", "Вход в ЭОС", "ghost", "sm")}{ext(EOS + "/Account/Register.aspx", "Получить пароль", "ghost", "sm")}{ext(EOS + "/Account/Register.aspx?fPass=1", "Забыли пароль?", "ghost", "sm")}</div></div>
      <div><h3 class="big">Что будет <span class="hl">внутри</span></h3><ul class="deps" style="margin-top:24px">''' + ''.join(f'<li><div><h3>{a}</h3><p class="who">{b}</p></div></li>' for a, b in [
    ('Оценки и зачётка', 'Баллы БРС, рейтинговые ведомости, электронная зачётная книжка'), ('Долги и пропуски', 'Задолженности с датами пересдач, посещаемость'),
    ('Стипендия', 'Начисления, приказы и калькулятор ПГАС'), ('Расписание', 'Персональное, с заменами и выгрузкой в календарь'), ('Справки и заявления', 'Заказ онлайн со статусом готовности')]) + '</ul></div></div>', True)
html += close()
save('lk.html', 'lk.html', 'Личный кабинет', html)

# ================================================================= КАРТА САЙТА, ПОЛИТИКА ПДн, 404
smap = '<div class="sitemap">' + ''.join(f'<div><h3>{g}</h3>' + ''.join(f'<a href="{h}">{n}</a>' for h, n, k in items) + '</div>' for g, items in X.PAGES) + '</div>'
html = hero([(None, 'Карта сайта')], 'Навигация', 'Карта <span class="hl">сайта</span>', 'Все страницы сайта. Быстрый поиск — Ctrl + K (⌘ + K на Mac).')
html += sec('all', '01', 'Все разделы', f'{sum(len(i) for _, i in X.PAGES)} страниц', smap, True)
html += close()
save('sitemap.html', 'sitemap.html', 'Карта сайта', html)

html = hero([(None, 'Политика ПДн')], 'Персональные данные', 'Политика обработки <span class="hl">персональных данных</span>',
            'Как этот сайт обращается с данными посетителей — по Федеральному закону № 152-ФЗ «О персональных данных».')
html += sec('text', '01', 'Положения', 'макет сайта', '''<div class="prose">
      <p class="lead-p">Оператор — ФГБОУ ВО «Брянский государственный инженерно-технологический университет», 241037, г. Брянск, пр-т Станке Димитрова, 3, mail@bgitu.ru.</p>
      <h2>Какие данные сохраняются</h2><p>Макет сайта не отправляет данные на сервер. В браузере посетителя сохраняются только настройки: выбранная тема оформления, параметры версии для слабовидящих и отметка о прочтении уведомления о cookies.</p>
      <h2>Формы</h2><p>Формы на страницах работают в демо-режиме и никуда не передают введённое. В рабочей версии сайта данные форм обрабатываются только для ответа на обращение, с согласия посетителя.</p>
      <h2>Как удалить данные</h2><p>Очистите данные сайта в настройках браузера — все сохранённые настройки удалятся.</p></div>''', True)
html += close()
save('privacy.html', 'privacy.html', 'Политика обработки персональных данных', html)

html = hero([(None, 'Страница не найдена')], 'Ошибка 404', 'Такой страницы <span class="hl">нет</span>', 'Возможно, она переехала. Воспользуйтесь поиском (Ctrl + K) или быстрыми ссылками.',
            '<div class="hero__cta">' + btn('index.html', 'На главную') + btn('sitemap.html', 'Карта сайта', 'ghost', None) + btn('admission.html', 'Поступающим', 'ghost', None) + '</div>')
html += '\n</main>'
save('404.html', '404.html', 'Страница не найдена', html)
# ================================================================= PWA: иконки, манифест, офлайн-кэш
from PIL import Image, ImageDraw
def icon(size, path, pad=0.0):
    im = Image.new('RGB', (size, size), '#0d0d0d'); d = ImageDraw.Draw(im)
    m = size * (0.16 + pad); d.rounded_rectangle([m, m, size - m, size - m], radius=(size - 2 * m) * 0.29, fill='#ff5a2e')
    u = (size - 2 * m) / 24; X0, Y0 = m, m; w = max(2, round(u * 2.4))
    pt = lambda x, y: (X0 + x * u, Y0 + y * u)
    d.line([pt(16, 6), pt(8, 6), pt(8, 18), pt(13, 18)], fill='#0d0d0d', width=w, joint='curve')
    d.arc([pt(9.5, 11)[0], pt(9.5, 11)[1], pt(16.5, 18)[0], pt(16.5, 18)[1]], start=-90, end=90, fill='#0d0d0d', width=w)
    d.line([pt(13, 11), pt(8, 11)], fill='#0d0d0d', width=w)
    im.save(os.path.join(OUT, path))
icon(180, 'icon-180.png'); icon(192, 'icon-192.png'); icon(512, 'icon-512.png'); icon(512, 'icon-maskable-512.png', pad=0.06)
json.dump({'name': 'БГИТУ — Брянский государственный инженерно-технологический университет', 'short_name': 'БГИТУ', 'lang': 'ru',
           'start_url': 'index.html', 'scope': './', 'display': 'standalone', 'background_color': '#0d0d0d', 'theme_color': '#0d0d0d',
           'icons': [{'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
                     {'src': 'icon-maskable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'}],
           'shortcuts': [{'name': 'Расписание', 'url': 'schedule.html'}, {'name': 'Личный кабинет', 'url': 'lk.html'}, {'name': 'Поступающим', 'url': 'admission.html'}]},
          open(os.path.join(OUT, 'manifest.webmanifest'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
pages = sorted(f for f in os.listdir(OUT) if f.endswith('.html'))
open(os.path.join(OUT, 'sw.js'), 'w', encoding='utf-8').write("""// Офлайн-кэш: страницы открываются без сети; при сети — свежая версия (network first)
const C = 'bgitu-%s', PAGES = %s;
self.addEventListener('install', (e) => e.waitUntil(caches.open(C).then((c) => c.addAll(PAGES)).then(() => self.skipWaiting())));
self.addEventListener('activate', (e) => e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== C).map((k) => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener('fetch', (e) => { if (e.request.method !== 'GET' || new URL(e.request.url).origin !== location.origin) return;
  e.respondWith(fetch(e.request).then((r) => { const cp = r.clone(); caches.open(C).then((c) => c.put(e.request, cp)); return r; }).catch(() => caches.match(e.request).then((r) => r || caches.match('404.html')))); });
""" % (__import__('time').strftime('%Y%m%d%H%M'), json.dumps(pages + ['manifest.webmanifest', 'icon-192.png', 'icon-512.png'])))
print('extra pages done', len(pages))
