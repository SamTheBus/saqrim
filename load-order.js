'use strict';
(() => {
  const $ = id => document.getElementById(id);
  const key = 'saqrim-load-order-220-2026-09-17';
  const notes = {
    17: 'The recorded Part 2 description says it belongs below ESM/master files. Its recorded position is preserved here; this page does not silently reorder it.',
    115: 'Alternative Lite port, 962.9 KB. Full menu title is clipped. Do not substitute the earlier full-size animation package just because the names resemble each other.',
    136: 'Inn-Tegrated NPCs patch: variant identified by Sam. The current recorded description is sparse; this is not a second copy of the main Echoes of Oblivion pack.',
    170: 'Identified as Cities of the North AIO from the filename and companion patch description. The visible title is COTN AIO.ESP; the exact web listing is not matched.',
    172: 'The recorded port description warns against Lux / Lux Orbis. Lux remains at recorded position #219. This page preserves that warning without changing the order.',
    215: 'Great Cities / minor cities compatibility role is described in the recording, but the full published title is clipped. Match the patch carefully; no web-listing verification is claimed.'
  };
  let data = [], rows = [], added = new Set(), canSave = true;
  try {
    const stored = JSON.parse(localStorage.getItem(key) || '[]');
    if (Array.isArray(stored)) added = new Set(stored.filter(v => Number.isInteger(v) && v >= 1 && v <= 220));
    localStorage.setItem(key, JSON.stringify([...added]));
  } catch (_) { canSave = false; }
  function say(text) { $('feedback').textContent = text; $('feedback').hidden = false; }
  function save() {
    try { localStorage.setItem(key, JSON.stringify([...added])); }
    catch (_) { canSave = false; $('storage-status').textContent = 'Browser storage is unavailable. Checkmarks work for this visit only.'; }
  }
  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }
  function filter() {
    const query = $('search').value.trim().toLowerCase();
    const number = /^#?0*([1-9]\d{0,2})$/.exec(query);
    const terms = query.split(/\s+/).filter(Boolean);
    let shown = 0;
    rows.forEach(({node, item, searchable}) => {
      const matches = number ? item.n === Number(number[1]) : terms.every(t => searchable.includes(t));
      node.hidden = !matches || ($('category').value && item.category !== $('category').value) || ($('hide-added').checked && added.has(item.n));
      node.classList.toggle('is-added', added.has(item.n));
      if (!node.hidden) shown++;
    });
    $('count').textContent = `${shown} / 220 shown · original numbers retained`;
    $('empty').hidden = shown !== 0;
    $('progress').value = added.size;
    $('added-count').textContent = `${added.size} / 220 added`;
  }
  function resetFilters() { $('search').value = ''; $('category').value = ''; $('hide-added').checked = false; filter(); }
  function go(n, updateHash = true) {
    if (!Number.isInteger(n) || n < 1 || n > 220) { say('Choose a load-order number from 1 to 220.'); return; }
    resetFilters();
    const id = 'mod-' + String(n).padStart(3, '0');
    if (updateHash) history.replaceState(null, '', '#' + id);
    const row = $(id); row.scrollIntoView({behavior: 'auto', block: 'start'}); row.focus({preventScroll: true});
  }
  async function copyName(name) {
    try {
      if (!navigator.clipboard) throw new Error('Clipboard not available');
      await navigator.clipboard.writeText(name); say('Copied: ' + name);
    } catch (_) {
      $('copy-panel').hidden = false; $('copy-name').value = name; $('copy-name').focus(); $('copy-name').select();
    }
  }
  function makeRow(item) {
    const node = el('li', 'row'); node.id = 'mod-' + String(item.n).padStart(3, '0'); node.value = item.n; node.tabIndex = -1;
    const top = el('div', 'row-top');
    const number = el('a', 'num', String(item.n).padStart(3, '0')); number.href = '#' + node.id; number.setAttribute('aria-label', 'Link to mod ' + item.n);
    const thumb = el('div', 'thumb'); thumb.setAttribute('role', 'img'); thumb.setAttribute('aria-label', 'Recorded Creations thumbnail for ' + item.name);
    const tile = item.thumb % 48;
    thumb.style.backgroundImage = `url("assets/thumbs-${Math.floor(item.thumb / 48)}.avif")`;
    thumb.style.backgroundPosition = `${-(tile % 8) * 96}px ${-Math.floor(tile / 8) * 54}px`;
    const body = el('div'); body.append(el('h2', '', item.name));
    const meta = el('div', 'metadata'); meta.append(el('span', 'size', item.size), el('span', '', item.version), el('span', '', item.category)); body.append(meta);
    top.append(number, thumb, body);
    const actions = el('div', 'row-actions');
    const label = el('label', 'added'); const check = document.createElement('input'); check.type = 'checkbox'; check.checked = added.has(item.n); check.setAttribute('aria-label', 'Added on my console: ' + item.name);
    check.addEventListener('change', () => { if (check.checked) added.add(item.n); else added.delete(item.n); save(); filter(); });
    label.append(check, document.createTextNode('Added on my console'));
    const copy = el('button', '', 'Copy name'); copy.type = 'button'; copy.addEventListener('click', () => copyName(item.name)); actions.append(label, copy);
    const details = document.createElement('details'); details.append(el('summary', '', notes[item.n] ? 'Console title, source & identification note' : 'Console title & recording source'));
    details.append(el('p', '', 'Visible console title (may be clipped): ' + item.title));
    details.append(el('p', '', 'Recorded file size: ' + item.size + ' · Menu version: ' + item.version + ' · Enabled in the video.'));
    if (notes[item.n]) details.append(el('p', 'warning', notes[item.n]));
    const parts = item.time.split(':'); const seconds = Number(parts[0]) * 60 + Number(parts[1]);
    const source = el('a', '', 'View in the recording · ' + item.time); source.href = 'https://www.youtube.com/watch?v=4uyqCADqwPo&t=' + Math.floor(seconds) + 's'; source.target = '_blank'; source.rel = 'noopener noreferrer'; details.append(source);
    details.append(el('p', '', 'Image: thumbnail cropped from this recorded Creations entry, not a newly verified Bethesda web listing. Sizes can change with updates.'));
    node.append(top, actions, details);
    return {node, item, searchable: [item.name, item.title, item.size, item.version, item.category].join(' ').toLowerCase()};
  }
  async function start() {
    try {
      const response = await fetch('load-order.tsv'); if (!response.ok) throw new Error('Load-order request failed');
      const text = await response.text();
      data = text.trim().split(/\r?\n/).map(line => { const [n,name,size,version,time,category,title,thumb] = line.split('\t'); return {n:Number(n),name,size,version,time,category,title,thumb:Number(thumb)}; });
      if (data.length !== 220 || data.some((d,i) => d.n !== i + 1 || !d.name || !d.size || !d.title || !Number.isInteger(d.thumb) || d.thumb < 0 || d.thumb >= 186)) throw new Error('Invalid recorded load-order data');
      const fragment = document.createDocumentFragment(); rows = data.map(makeRow); rows.forEach(r => fragment.append(r.node)); $('mods').append(fragment);
      [...new Set(data.map(d => d.category))].sort().forEach(category => { const option = el('option', '', category); option.value = category; $('category').append(option); });
      document.querySelectorAll('.tools [disabled]').forEach(n => { n.disabled = false; });
      $('search').addEventListener('input', filter); $('category').addEventListener('change', filter); $('hide-added').addEventListener('change', filter);
      $('show-all').addEventListener('click', resetFilters);
      $('next').addEventListener('click', () => { const item = data.find(d => !added.has(d.n)); if (item) go(item.n); else say('All 220 mods are checked off in this browser.'); });
      $('jump-form').addEventListener('submit', e => { e.preventDefault(); go(Number($('jump-number').value)); });
      $('copy-close').addEventListener('click', () => { $('copy-panel').hidden = true; });
      const followHash = () => { const match = /^#mod-(\d{1,3})$/.exec(location.hash); if (match) go(Number(match[1]), false); };
      window.addEventListener('hashchange', followHash);
      if (!canSave) $('storage-status').textContent = 'Browser storage is unavailable. Checkmarks work for this visit only.';
      filter(); followHash();
    } catch (error) { $('error').hidden = false; $('count').textContent = 'Load order unavailable'; console.error(error); }
  }
  start();
})();
