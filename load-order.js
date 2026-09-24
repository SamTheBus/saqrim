'use strict';
(() => {
  const $ = id => document.getElementById(id);
  const key = 'saqrim-load-order-210-2026-09-23-v2';
  const notes = {
    'Beyond Reach Part 2 (PS)': 'The recorded description says it belongs below ESM/master files. Its current position is preserved here; this page does not silently reorder it.',
    'Comprehensive First Person Animation Overhaul - alternative Lite port': 'Alternative Lite port, 962.9 KB. Full menu title is clipped. Do not substitute the earlier full-size animation package just because the names resemble each other.',
    'Echoes of Oblivion - Inn-Tegrated NPCs Patch': 'Inn-Tegrated NPCs patch: variant identified by Sam. The recorded description is sparse; this is not a second copy of the main Echoes of Oblivion pack.',
    'Cities of the North AIO (COTN AIO.ESP)': 'Identified as Cities of the North AIO from the filename and companion patch description. The visible title is COTN AIO.ESP; the exact web listing is not matched.',
    "The Great Cities of JK's North - COTN AIO port": 'The recorded port description warns against Lux / Lux Orbis. Lux - PS5 is now at current position #203. This page preserves that warning without changing the order.',
    'Become High King of Skyrim TNG - Great Cities / minor cities patch': 'Great Cities / minor cities compatibility role is described in the recording, but the full published title is clipped. Match the patch carefully; no web-listing verification is claimed.'
  };
  let data = [], rows = [], added = new Set(), canSave = true, bethesdaMeta = {};
  try {
    const stored = JSON.parse(localStorage.getItem(key) || '[]');
    if (Array.isArray(stored)) added = new Set(stored.filter(v => Number.isInteger(v) && v >= 1 && v <= 210));
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
      node.hidden = !matches || (window.SaqrimReference && !window.SaqrimReference.matches(item.name, $('reference-view')?.value || '')) || ($('category').value && item.category !== $('category').value) || ($('hide-added').checked && added.has(item.n));
      node.classList.toggle('is-added', added.has(item.n));
      if (!node.hidden) shown++;
    });
    $('count').textContent = `${shown} / 210 shown · current numbers retained`;
    $('empty').hidden = shown !== 0;
    $('progress').value = added.size;
    $('added-count').textContent = `${added.size} / 210 added`;
  }
  function resetFilters() { if ($('reference-view')) $('reference-view').value = ''; $('search').value = ''; $('category').value = ''; $('hide-added').checked = false; filter(); }
  function go(n, updateHash = true) {
    if (!Number.isInteger(n) || n < 1 || n > 210) { say('Choose a load-order number from 1 to 210.'); return; }
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
  function listBlock(label, values) {
    if (!Array.isArray(values) || !values.length) return null;
    const wrap = el('div', 'listing-block');
    wrap.append(el('h4', '', label));
    const list = el('ul');
    values.forEach(value => list.append(el('li', '', value)));
    wrap.append(list);
    return wrap;
  }
  function bethesdaPanel(item) {
    const meta = item.bethesda;
    const box = el('section', 'bethesda-info');
    box.append(el('h3', '', 'Bethesda / Creations listing'));
    if (!meta) {
      box.classList.add('listing-pending');
      box.append(el('p', 'listing-status', 'Official Bethesda listing not yet matched'));
      box.append(el('p', '', 'No Nexus or other third-party description is substituted here. The recorded console information below is still preserved.'));
      return box;
    }
    box.append(el('p', 'listing-status', meta.sourceStatus || 'Official Bethesda listing matched'));
    if (meta.bethesdaTitle) {
      const title = el('p');
      const strong = el('strong', '', meta.bethesdaTitle);
      title.append(strong);
      if (meta.author) title.append(document.createTextNode(' · by ' + meta.author));
      box.append(title);
    }
    if (meta.overview) box.append(el('p', 'listing-overview', meta.overview));
    for (const [label, keyName] of [['What the listing says it does','features'],['Requirements','requirements'],['Compatibility / load-order notes','compatibility'],['Credits / porter notes','credits']]) {
      const block = listBlock(label, meta[keyName]);
      if (block) box.append(block);
    }
    if (meta.bethesdaVersion || meta.bethesdaInstallSize) {
      const current = [meta.bethesdaVersion && 'version ' + meta.bethesdaVersion, meta.bethesdaInstallSize && meta.bethesdaInstallSize].filter(Boolean).join(' · ');
      const recorded = [item.version && 'version ' + item.version, item.size].filter(Boolean).join(' · ');
      const compare = el('div', 'listing-compare');
      compare.append(el('h4', '', 'Listing vs. your recording'));
      compare.append(el('p', '', 'Stored Bethesda listing snapshot: ' + current + '.'));
      compare.append(el('p', '', 'Recorded on your console: ' + recorded + '.'));
      if ((meta.bethesdaVersion && meta.bethesdaVersion !== item.version) || (meta.bethesdaInstallSize && meta.bethesdaInstallSize !== item.size)) {
        compare.append(el('p', 'warning', 'The stored listing metadata differs from the recorded menu. Both are kept because the listing can change after your recording.'));
      }
      box.append(compare);
    }
    if (!meta.overview) {
      box.append(el('p', 'listing-pending-note', 'The official listing URL is matched, but its description text has not been verified yet. No alternate description is being substituted.'));
    }
    if (meta.source) {
      const source = el('a', 'bethesda-link', 'Open official Bethesda listing');
      source.href = meta.source; source.target = '_blank'; source.rel = 'noopener noreferrer';
      box.append(source);
    }
    if (meta.checked) box.append(el('p', 'listing-checked', 'Bethesda listing checked ' + meta.checked + '.'));
    return box;
  }
  function makeRow(item) {
    const node = el('li', 'row'); node.id = 'mod-' + String(item.n).padStart(3, '0'); node.value = item.n; node.tabIndex = -1;
    const top = el('div', 'row-top');
    const number = el('a', 'num', String(item.n).padStart(3, '0')); number.href = '#' + node.id; number.setAttribute('aria-label', 'Link to mod ' + item.n);
    const thumb = el('div', 'thumb'); thumb.setAttribute('role', 'img'); thumb.setAttribute('aria-label', 'Recorded Creations thumbnail for ' + item.name);
    if (item.thumb >= 186) {
      const tile = item.thumb - 186;
      thumb.style.backgroundImage = 'url("assets/load-order-new-2026-09-23.jpg")';
      thumb.style.backgroundPosition = `${-tile * 96}px 0`;
    } else {
      const tile = item.thumb % 48;
      thumb.style.backgroundImage = `url("assets/thumbs-${Math.floor(item.thumb / 48)}.avif")`;
      thumb.style.backgroundPosition = `${-(tile % 8) * 96}px ${-Math.floor(tile / 8) * 54}px`;
    }
    const body = el('div'); body.append(el('h2', '', item.name));
    const meta = el('div', 'metadata'); meta.append(el('span', 'size', item.size), el('span', '', item.version), el('span', '', item.category)); body.append(meta);
    top.append(number, thumb, body);
    const actions = el('div', 'row-actions');
    const label = el('label', 'added'); const check = document.createElement('input'); check.type = 'checkbox'; check.checked = added.has(item.n); check.setAttribute('aria-label', 'Added on my console: ' + item.name);
    check.addEventListener('change', () => { if (check.checked) added.add(item.n); else added.delete(item.n); save(); filter(); });
    label.append(check, document.createTextNode('Added on my console'));
    const copy = el('button', '', 'Copy name'); copy.type = 'button'; copy.addEventListener('click', () => copyName(item.name)); actions.append(label, copy);
    const details = document.createElement('details');
    details.append(el('summary', '', item.bethesda ? 'Earlier listing snapshot & console metadata' : 'Listing match status & console metadata'));
    details.append(bethesdaPanel(item));
    details.append(el('h3', 'recording-heading', 'Your recorded Creations entry'));
    details.append(el('p', '', 'Visible console title (may be clipped): ' + item.title));
    details.append(el('p', '', 'Recorded file size: ' + item.size + ' · Menu version: ' + item.version + ' · Enabled in the video.'));
    if (notes[item.name]) details.append(el('p', 'warning', notes[item.name]));
    details.append(el('p', '', 'Latest recording timestamp · ' + item.time + ' · source: Skyrim_LO.mp4 supplied 23 September 2026.'));
    details.append(el('p', '', 'Image: matching recorded Creations artwork. Existing entries retain their prior menu crop; the two newly added entries use crops from the 23 September recording. Sizes can change with updates.'));
    node.append(top, actions);
    if (window.SaqrimReference) window.SaqrimReference.decorate(item, node);
    node.append(details);
    return {node, item, searchable: [item.name, item.title, item.size, item.version, item.category, JSON.stringify(item.bethesda || {}), window.SaqrimReference?.searchText(item.name) || ''].join(' ').toLowerCase()};
  }
  async function start() {
    try {
      const response = await fetch('load-order.tsv?v=20260923b'); if (!response.ok) throw new Error('Load-order request failed');
      const text = await response.text();
      try {
        const listingResponse = await fetch('load-order-bethesda.json?v=3');
        if (listingResponse.ok) {
          const pack = await listingResponse.json();
          bethesdaMeta = pack.entries || {};
        }
      } catch (_) { bethesdaMeta = {}; }
      data = text.trim().split(/\r?\n/).map(line => {
        const [n,name,size,version,time,category,title,thumb] = line.split('\t');
        return {n:Number(n),name,size,version,time,category,title,thumb:Number(thumb),bethesda:bethesdaMeta[name] || null};
      });
      if (data.length !== 210 || data.some((d,i) => d.n !== i + 1 || !d.name || !d.size || !d.title || !Number.isInteger(d.thumb) || d.thumb < 0 || d.thumb >= 188)) throw new Error('Invalid recorded load-order data');
      if (window.SaqrimReference) { await window.SaqrimReference.ready; window.SaqrimReference.setOrder(data); }
      const fragment = document.createDocumentFragment(); rows = data.map(makeRow); rows.forEach(r => fragment.append(r.node)); $('mods').append(fragment);
      [...new Set(data.map(d => d.category))].sort().forEach(category => { const option = el('option', '', category); option.value = category; $('category').append(option); });
      if (window.SaqrimReference) window.SaqrimReference.mountControls(filter, data.length);
      document.querySelectorAll('.tools [disabled]').forEach(n => { n.disabled = false; });
      $('search').addEventListener('input', filter); $('category').addEventListener('change', filter); $('hide-added').addEventListener('change', filter);
      $('show-all').addEventListener('click', resetFilters);
      $('next').addEventListener('click', () => { const item = data.find(d => !added.has(d.n)); if (item) go(item.n); else say('All 210 mods are checked off in this browser.'); });
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

// Saqrim reference layer v1
