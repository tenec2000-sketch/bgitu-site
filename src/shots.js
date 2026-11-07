// Снимки макетов: каждая страница целиком в трёх темах. node shots.js <base url> <папка>
const path = require('path');
const puppeteer = require(path.join(process.env.APPDATA, 'npm/node_modules/puppeteer-core'));
const [base, out] = process.argv.slice(2);
const PAGES = [['index', 'Главная'], ['university', 'Университет'], ['institutes', 'Институты'], ['inst-les', 'Страница института'],
  ['admission', 'Поступление'], ['campus', 'Кампус'], ['news', 'Новости'], ['article', 'Статья'], ['contacts', 'Контакты']];
const THEMES = ['paper', 'surik', 'latun'];
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

(async () => {
  const browser = await puppeteer.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: true });
  const page = await browser.newPage();
  for (const theme of THEMES) {
    for (const [file] of PAGES) {
      for (const [w, h, suffix] of [[1440, 900, ''], ...(file === 'index' ? [[390, 844, '-mobile']] : [])]) {
        await page.setViewport({ width: w, height: h, deviceScaleFactor: 1 });
        await page.goto(`${base}/${file}.html?theme=${theme}&shot`, { waitUntil: 'load' });
        await wait(600);
        const full = await page.evaluate(() => document.documentElement.scrollHeight);
        await page.setViewport({ width: w, height: Math.min(full, 16000), deviceScaleFactor: 1 });
        await wait(2200); // счётчики, перебор букв, перерисовка фона под новую высоту
        const name = path.join(out, theme, `${file}${suffix}.jpg`);
        await page.screenshot({ path: name, type: 'jpeg', quality: 84 });
        console.log('ok', theme, file + suffix, full);
      }
    }
  }
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
