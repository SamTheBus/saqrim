'use strict';
(() => {
  const $ = id => document.getElementById(id);
  const key = 'saqrim-load-order-224-october-v1';
  const priorKey = 'saqrim-load-order-210-2026-09-23-v2';
  const priorToCurrent = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "11": 11, "12": 12, "13": 13, "14": null, "15": null, "16": null, "17": 16, "18": 17, "19": 18, "20": 19, "21": 20, "22": 21, "23": 22, "24": 23, "25": 24, "26": 25, "27": 26, "28": 27, "29": 28, "30": 29, "31": 30, "32": 31, "33": 32, "34": 33, "35": 34, "36": 35, "37": 36, "38": 37, "39": 38, "40": 39, "41": 40, "42": 41, "43": 42, "44": 43, "45": 44, "46": 45, "47": 46, "48": 47, "49": 48, "50": 49, "51": 50, "52": 51, "53": 52, "54": 53, "55": 54, "56": 55, "57": 56, "58": 57, "59": 59, "60": 60, "61": 61, "62": 62, "63": 63, "64": 64, "65": 65, "66": 66, "67": 67, "68": 68, "69": 69, "70": 70, "71": 71, "72": 72, "73": 73, "74": 74, "75": 75, "76": 76, "77": 77, "78": 78, "79": 79, "80": 80, "81": 81, "82": 82, "83": 83, "84": null, "85": 85, "86": 86, "87": 87, "88": 88, "89": 89, "90": 94, "91": 95, "92": 97, "93": 99, "94": 100, "95": 101, "96": 102, "97": 103, "98": 104, "99": 105, "100": 106, "101": 107, "102": 108, "103": 109, "104": 111, "105": 112, "106": 113, "107": 114, "108": 115, "109": 116, "110": 117, "111": 118, "112": 119, "113": 120, "114": 121, "115": 122, "116": 123, "117": 124, "118": 125, "119": 126, "120": 127, "121": 128, "122": 129, "123": 130, "124": 132, "125": 133, "126": 134, "127": 135, "128": 136, "129": 137, "130": 138, "131": 139, "132": 140, "133": 141, "134": 144, "135": 145, "136": 146, "137": 147, "138": 148, "139": 149, "140": 150, "141": 151, "142": 152, "143": 153, "144": 154, "145": 155, "146": 156, "147": 157, "148": 159, "149": 160, "150": 161, "151": 162, "152": 163, "153": 164, "154": 165, "155": 166, "156": 167, "157": 168, "158": 169, "159": 170, "160": 171, "161": 172, "162": 173, "163": 174, "164": 175, "165": 176, "166": 177, "167": 178, "168": 179, "169": 180, "170": 181, "171": 182, "172": 183, "173": 184, "174": 185, "175": 186, "176": 187, "177": 188, "178": 189, "179": 190, "180": 191, "181": 192, "182": 193, "183": 194, "184": 195, "185": 196, "186": 197, "187": 198, "188": 199, "189": 200, "190": 201, "191": 202, "192": 203, "193": 204, "194": 205, "195": 206, "196": 207, "197": 208, "198": 209, "199": 210, "200": 211, "201": 212, "202": 213, "203": 214, "204": 215, "205": 218, "206": 220, "207": 221, "208": 222, "209": 223, "210": 224};
  const notes = {
    'Beyond Reach Part 2 (PS)': 'The recorded description says it belongs below ESM/master files. Its current position is preserved here; this page does not silently reorder it.',
    'Comprehensive First Person Animation Overhaul - alternative Lite port': 'Alternative Lite port, 962.9 KB. Full menu title is clipped. Do not substitute the earlier full-size animation package just because the names resemble each other.',
    'Echoes of Oblivion - Inn-Tegrated NPCs Patch': 'Inn-Tegrated NPCs patch: variant identified by Sam. The recorded description is sparse; this is not a second copy of the main Echoes of Oblivion pack.',
    'Cities of the North AIO (COTN AIO.ESP)': 'Identified as Cities of the North AIO from the filename and companion patch description. The visible title is COTN AIO.ESP; the exact web listing is not matched.',
    "The Great Cities of JK's North - COTN AIO port": 'The recorded port description warns against Lux / Lux Orbis. Lux - PS5 is now at current position #214. This page preserves that warning without changing the order.',
    'Become High King of Skyrim TNG - Great Cities / minor cities patch': 'Great Cities / minor cities compatibility role is described in the recording, but the full published title is clipped. Match the patch carefully; no web-listing verification is claimed.'
  };
  let data = [], rows = [], added = new Set(), canSave = true, bethesdaMeta = {}, snapshotMeta = {};
  try {
    const existing = localStorage.getItem(key);
    const stored = JSON.parse(existing !== null ? existing : (localStorage.getItem(priorKey) || '[]'));
    if (Array.isArray(stored)) {
      const numbers = stored.filter(v => Number.isInteger(v) && v >= 1 && v <= (existing !== null ? 224 : 210));
      added = new Set(numbers.map(n => existing !== null ? n : priorToCurrent[n]).filter(n => Number.isInteger(n) && n >= 1 && n <= 224));
    }
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
    $('count').textContent = `${shown} / 224 shown · current numbers retained`;
    $('empty').hidden = shown !== 0;
    $('progress').value = added.size;
    $('added-count').textContent = `${added.size} / 224 added`;
  }
  function resetFilters() { if ($('reference-view')) $('reference-view').value = ''; $('search').value = ''; $('category').value = ''; $('hide-added').checked = false; filter(); }
  function go(n, updateHash = true) {
    if (!Number.isInteger(n) || n < 1 || n > 224) { say('Choose a load-order number from 1 to 224.'); return; }
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
      compare.append(el('p', '', 'Stored console metadata (see source dates below): ' + recorded + '.'));
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
    if (item.thumb < 0) {
      thumb.textContent = 'SAQ';
      thumb.classList.add('thumb-pending');
      thumb.setAttribute('aria-label', 'Thumbnail not captured for ' + item.name);
    } else if (item.thumb >= 186) {
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
    details.append(el('h3', 'recording-heading', 'Recorded metadata & current changes'));
    const provenance = item.provenance;
    details.append(el('p', '', 'Identification label (may be clipped or normalized): ' + item.title));
    details.append(el('p', '', 'Size: ' + item.size + ' · Menu version label: ' + item.version));
    if (provenance) {
      details.append(el('p', '', 'Size source: ' + provenance.sizeSource + '.'));
      details.append(el('p', '', 'Version source: ' + provenance.versionSource + '.'));
      details.append(el('p', '', 'Title source: ' + provenance.titleSource + '.'));
      if (provenance.sourceKind === 'recorded') details.append(el('p', '', 'Recording: ' + provenance.sourceFile + ' · ' + provenance.locator + '. The opening browse results are not installed entries.'));
      else details.append(el('p', '', 'Added/replaced after the recording, as confirmed by Sam. No video timestamp or version is invented.'));
      (provenance.notes || []).forEach(note => details.append(el('p', '', note)));
      details.append(el('p', '', 'Image: ' + provenance.thumbnailSource + '.'));
    } else {
      details.append(el('p', '', 'October capture / user updates: ' + item.time + '. Detailed provenance is temporarily unavailable; retained version labels may be from the earlier recording.'));
    }
    if (notes[item.name]) details.append(el('p', 'warning', notes[item.name]));
    node.append(top, actions);
    if (window.SaqrimReference) window.SaqrimReference.decorate(item, node);
    node.append(details);
    return {node, item, searchable: [item.name, item.title, item.size, item.version, item.category, JSON.stringify(item.bethesda || {}), window.SaqrimReference?.searchText(item.name) || ''].join(' ').toLowerCase()};
  }
  async function start() {
    try {
      const response = await fetch('load-order.tsv?v=october-sync-1'); if (!response.ok) throw new Error('Load-order request failed');
      const text = await response.text();
      try {
        const listingResponse = await fetch('load-order-bethesda.json?v=october-sync-1');
        if (listingResponse.ok) {
          const pack = await listingResponse.json();
          bethesdaMeta = pack.entries || {};
        }
      } catch (_) { bethesdaMeta = {}; }
      try {
        const snapshotResponse = await fetch('load-order-snapshot.json?v=october-sync-1');
        if (snapshotResponse.ok) snapshotMeta = (await snapshotResponse.json()).entries || {};
      } catch (_) { snapshotMeta = {}; }
      data = text.trim().split(/\r?\n/).map(line => {
        const [n,name,size,version,time,category,title,thumb] = line.split('\t');
        return {n:Number(n),name,size,version,time,category,title,thumb:Number(thumb),bethesda:bethesdaMeta[name] || null,provenance:snapshotMeta[name] || null};
      });
      if (data.length !== 224 || data.some((d,i) => d.n !== i + 1 || !d.name || !d.size || !d.title || !Number.isInteger(d.thumb) || d.thumb < -1 || d.thumb >= 188)) throw new Error('Invalid recorded load-order data');
      if (window.SaqrimReference) { await window.SaqrimReference.ready; window.SaqrimReference.setOrder(data); }
      const fragment = document.createDocumentFragment(); rows = data.map(makeRow); rows.forEach(r => fragment.append(r.node)); $('mods').append(fragment);
      [...new Set(data.map(d => d.category))].sort().forEach(category => { const option = el('option', '', category); option.value = category; $('category').append(option); });
      if (window.SaqrimReference) window.SaqrimReference.mountControls(filter, data.length);
      document.querySelectorAll('.tools [disabled]').forEach(n => { n.disabled = false; });
      $('search').addEventListener('input', filter); $('category').addEventListener('change', filter); $('hide-added').addEventListener('change', filter);
      $('show-all').addEventListener('click', resetFilters);
      $('next').addEventListener('click', () => { const item = data.find(d => !added.has(d.n)); if (item) go(item.n); else say('All 224 mods are checked off in this browser.'); });
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
