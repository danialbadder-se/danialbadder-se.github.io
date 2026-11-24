'use strict';

const menu = document.getElementById('mobile-nav');
const toggle = document.querySelector('.nav-toggle');

function setMenu(open) {
  menu.hidden = !open;
  toggle.setAttribute('aria-expanded', String(open));
  toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
}

toggle.addEventListener('click', () => setMenu(menu.hidden));
menu.addEventListener('click', event => {
  if (event.target.closest('a')) setMenu(false);
});
window.matchMedia('(min-width: 791px)').addEventListener('change', event => {
  if (event.matches) setMenu(false);
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && !menu.hidden) {
    setMenu(false);
    toggle.focus();
  }
});

for (const container of document.querySelectorAll('[data-switch]')) {
  const buttons = [...container.querySelectorAll('[data-choice]')];
  const panels = [...container.querySelectorAll('[data-panel]')];
  for (const button of buttons) {
    button.addEventListener('click', () => {
      for (const control of buttons) control.setAttribute('aria-pressed', String(control === button));
      for (const panel of panels) panel.hidden = panel.dataset.panel !== button.dataset.choice;
    });
  }
}

const filters = [...document.querySelectorAll('[data-filter]')];
const cards = [...document.querySelectorAll('[data-project-category]')];
for (const filter of filters) {
  filter.addEventListener('click', () => {
    for (const option of filters) option.setAttribute('aria-pressed', String(option === filter));
    let visible = 0;
    for (const card of cards) {
      card.hidden = filter.dataset.filter !== 'all' && filter.dataset.filter !== card.dataset.projectCategory;
      if (!card.hidden) visible++;
    }
    const more = document.querySelector('.more-projects');
    more.hidden = !more.querySelector('details:not([hidden])');
    document.getElementById('filter-count').textContent = visible + (visible === 1 ? ' project' : ' projects');
  });
}

const dialog = document.getElementById('image-dialog');
let opener = null;
for (const trigger of document.querySelectorAll('[data-lightbox]')) {
  trigger.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || typeof dialog.showModal !== 'function') return;
    event.preventDefault();
    opener = trigger;
    const caption = trigger.dataset.lightbox;
    const image = dialog.querySelector('img');
    image.alt = caption;
    image.src = trigger.href;
    dialog.querySelector('h2').textContent = caption;
    dialog.querySelector('.full-image').href = trigger.href;
    document.body.classList.add('modal-open');
    dialog.showModal();
  });
}
dialog.querySelector('[data-close]').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => {
  if (event.target !== dialog) return;
  const box = dialog.getBoundingClientRect();
  if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close();
});
dialog.addEventListener('close', () => {
  document.body.classList.remove('modal-open');
  opener?.focus({ preventScroll: true });
});

document.querySelector('[data-copy]').addEventListener('click', async () => {
  const mail = document.querySelector('.contact-mail');
  const status = document.querySelector('.copy-status');
  try {
    await navigator.clipboard.writeText(mail.textContent.trim());
    status.textContent = 'Email address copied.';
  } catch {
    const range = document.createRange();
    range.selectNodeContents(mail);
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    status.textContent = 'Email selected. Use your device’s copy command.';
  }
});

const pageData = document.getElementById('page-data');
const dataset = pageData ? JSON.parse(pageData.textContent) : null;
const write = (id, text) => { document.getElementById(id).textContent = text; };

const internshipRow = document.getElementById('internship-row');
internshipRow?.addEventListener('change', () => {
  const row = dataset.rows.find(item => item.row === Number(internshipRow.value));
  if (!row) return;
  write('internship-cell', 'I' + row.row);
  write('internship-formula', row.formulas.I);
  write('internship-level-one', row.K + ' kV');
  write('internship-level-two', row.L + ' kV');
  write('internship-rating', row.N);
  write('internship-description', row.I);
  write('internship-length', row.J + ' characters');
});

const equipmentSelect = document.getElementById('equipment-select');
equipmentSelect?.addEventListener('change', () => {
  const entry = dataset.checklist.find(([id]) => id === Number(equipmentSelect.value));
  if (!entry) return;
  const items = entry[2].split('\n').map(line => {
    const item = document.createElement('li');
    item.textContent = line.replace(/^\d+\)\s*/, '').trim();
    return item;
  });
  document.getElementById('equipment-fields').replaceChildren(...items);
});

const daySelect = document.getElementById('day-select');
daySelect?.addEventListener('change', () => {
  const row = dataset.daily.find(record => record.day === Number(daySelect.value));
  if (!row) return;
  write('day-visits', row.visits);
  write('day-wait', row.wait.toFixed(2) + ' min');
  write('day-score', row.satisfaction.toFixed(2));
});

const screenSelect = document.getElementById('news-screen');
const screens = {
  text: ['news-text.html', 'templates/detect.html · Text', 'Original VeriCleri text entry screen'],
  url: ['news-url.html', 'templates/detect.html · URL', 'Original VeriCleri URL entry screen'],
  wa: ['news-wa.html', 'templates/detect.html · WhatsApp', 'Original VeriCleri forwarded message screen'],
  extension: ['news-extension.html', 'browser_extension/popup.html', 'Original TruthDetect Chrome extension']
};
screenSelect?.addEventListener('change', () => {
  const [file, source, title] = screens[screenSelect.value];
  const frame = document.getElementById('news-frame');
  frame.src = '/exhibits/' + file;
  frame.title = title + ', read-only exhibit';
  write('screen-file', source);
});

const exampleSelect = document.getElementById('example-select');
exampleSelect?.addEventListener('change', () => {
  const record = dataset.examples[Number(exampleSelect.value)];
  write('example-text', record.text);
  write('example-label', record.label[0] + record.label.slice(1).toLowerCase());
  write('example-score', (record.fake * 100).toFixed(2) + '%');
});

const metricSelect = document.getElementById('metric-select');
const explanations = {
  macro_auroc: 'Higher is better. AUROC measures how well scores rank positive examples above negative ones.',
  macro_average_precision: 'Higher is better. Macro average precision gives equal weight to every scored observation.',
  micro_f1: 'Higher is better. Micro F1 combines precision and recall across known labels at a threshold of 0.5.',
  brier: 'Lower is better. Brier score measures squared probability error. Bars are scaled to the largest displayed score.',
  pooled_ece_10_bins: 'Lower is better. This calibration measure compares confidence with observed frequencies in ten bins. Bars are scaled to the largest displayed score.'
};
metricSelect?.addEventListener('change', () => {
  const key = metricSelect.value;
  const models = dataset.models.filter(model => ['image','text','concat','full'].includes(model.key));
  const max = ['brier','pooled_ece_10_bins'].includes(key) ? Math.max(...models.map(model => model[key])) : 1;
  const bars = document.querySelectorAll('#model-bars .model-bar');
  models.forEach((model,index) => {
    bars[index].querySelector('i').style.width = (100 * model[key] / max) + '%';
    bars[index].querySelector('strong').textContent = model[key].toFixed(5);
  });
  write('metric-note', explanations[key]);
});

const missingSelect = document.getElementById('missing-select');
missingSelect?.addEventListener('change', () => {
  const record = dataset.missing.find(row => row.missing === Number(missingSelect.value));
  write('mask-auc', record.macro_auroc.toFixed(5));
  write('mask-f1', record.micro_f1.toFixed(5));
  write('mask-brier', record.brier.toFixed(5));
});
