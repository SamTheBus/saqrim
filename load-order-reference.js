'use strict';
// Optional reference layer. No console, catalog, quest or checklist state is written here.
(() => {
  const labels = {recorded:'Recorded PS5', upstream:'Upstream docs', official:'Official listing match', user:'User-reported test'};
  const state = {pack:null, order:new Map(), failed:false};
  const node = (tag, cls, text) => { const n=document.createElement(tag); if(cls)n.className=cls; if(text!==undefined)n.textContent=text; return n; };
  function safeURL(value, external=false) {
    if(typeof value!=='string')return null;
    try {const u=new URL(value,location.href);if(external)return u.protocol==='https:'?u.href:null;return u.origin===location.origin&&/^(https?:)$/.test(u.protocol)?u.href:null;}catch(_){return null;}
  }
  function validate(pack) {
    if(pack?.version!==1||!pack.entries||!pack.sources)throw Error('Invalid reference pack');
    const ids=new Set();
    for(const [name,e] of Object.entries(pack.entries)) {
      if(!name||!e||!/^[a-z0-9-]+$/.test(e.id)||ids.has(e.id)||!e.summary||!Array.isArray(e.sections))throw Error('Invalid reference entry');
      ids.add(e.id);
      for(const c of [e.summary,...e.sections.flatMap(s=>s.claims||[])]) {
        if(typeof c.text!=='string'||!Array.isArray(c.refs)||!c.refs.length||c.refs.some(id=>!pack.sources[id]))throw Error('Unsourced reference claim');
      }
      if((e.extraSources||[]).some(id=>!pack.sources[id]))throw Error('Missing extra source');
    }
    for(const s of Object.values(pack.sources))if(!labels[s.kind]||(!s.locator&&!safeURL(s.url,true)))throw Error('Invalid source');
    return pack;
  }
  const ready = (async()=>{
    const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),8000);
    try {const r=await fetch('load-order-reference.json?v=1',{signal:controller.signal});if(!r.ok)throw Error('Reference request failed');state.pack=validate(await r.json());}
    catch(_){state.failed=true;state.pack=null;}
    finally{clearTimeout(timer);}
  })();
  function get(name){return state.pack?.entries[name]||null;}
  function sourceIds(e){return [...new Set([e.summary,...e.sections.flatMap(s=>s.claims||[])].flatMap(c=>c.refs).concat(e.extraSources||[]))];}
  function sourceId(e,id){return 'ref-source-'+e.id+'-'+id;}
  function evidence(c,e) {
    const wrap=node('span','ref-evidence');
    if(c.kind==='assessment'){const b=node('span','ref-badge ref-assessment','Assessment');b.title='Interpretation or unresolved question, not a measured result.';wrap.append(b);}
    const all=sourceIds(e);
    c.refs.forEach(id=>{
      const s=state.pack.sources[id],a=node('a','ref-badge ref-'+s.kind,labels[s.kind]+' ['+(all.indexOf(id)+1)+']');a.href='#'+sourceId(e,id);a.title=s.label;
      a.addEventListener('click',()=>{const target=document.getElementById(sourceId(e,id));if(target){for(let p=target.parentElement;p;p=p.parentElement)if(p.tagName==='DETAILS')p.open=true;}});
      wrap.append(a);
    });
    return wrap;
  }
  function claim(c,e){const p=node('p','ref-claim',c.text);p.append(evidence(c,e));return p;}
  function sourceList(e) {
    const d=node('details','ref-sources');d.append(node('summary','','Sources & exact recording timestamps'));
    const list=node('ol');
    for(const id of sourceIds(e)) {
      const s=state.pack.sources[id],li=node('li');li.id=sourceId(e,id);li.tabIndex=-1;
      li.append(node('strong','',labels[s.kind]+' · '+s.label));
      if(s.locator)li.append(node('p','',s.locator));
      const url=safeURL(s.url,true);
      if(url){const a=node('a','','Open source');a.href=url;a.target='_blank';a.rel='noopener noreferrer';li.append(a);}
      if(s.note)li.append(node('p','ref-source-note',s.note));
      list.append(li);
    }
    d.append(list,node('p','ref-source-note','Recorded claims are paraphrases of the supplied PS5 menu, not a live plugin scan. The current video is not publicly hosted; use its filename and exact timestamp to verify the panel.'));
    return d;
  }
  function decorate(item,row) {
    const e=get(item.name);row.dataset.reference=e?'expanded':'pending';if(!e)return;
    row.dataset.referenceAttention=String(Boolean(e.attention));
    const body=row.querySelector('.row-top h2')?.parentElement;
    if(body){body.append(node('p','ref-teaser',e.summary.text));const badges=node('div','ref-row-badges');badges.append(node('span','ref-badge','Description expanded'));if(e.attention)badges.append(node('span','ref-badge ref-attention','Recorded warning / open question'));body.append(badges);}
    const details=node('details','ref-card');details.id='reference-'+e.id;
    details.append(node('summary','','Read mod reference · requirements, compatibility & sources'));
    const inner=node('div','ref-body');inner.append(claim(e.summary,e));
    e.sections.forEach(s=>{const section=node('section','ref-section');section.append(node('h3','',s.title));(s.claims||[]).forEach(c=>section.append(claim(c,e)));inner.append(section);});
    const related=(e.related||[]).filter(name=>state.order.has(name));
    if(related.length){const section=node('section','ref-section');section.append(node('h3','','Related entries · current positions'));const links=node('div','ref-related');related.forEach(name=>{const n=state.order.get(name),a=node('a','','#'+n+' · '+name);a.href='load-order.html#mod-'+String(n).padStart(3,'0');links.append(a);});section.append(links);inner.append(section);}
    if(e.guides?.length){const links=node('div','ref-related');e.guides.forEach(g=>{const url=safeURL(g.url);if(url){const a=node('a','',g.label);a.href=url;links.append(a);}});inner.append(links);}
    inner.append(sourceList(e),node('p','ref-source-note','Description reviewed '+state.pack.reviewed+' · '+state.pack.batch+'. Recorded mod versions are preserved in the console metadata panel below.'));
    details.append(inner);row.append(details);
  }
  function setOrder(data){state.order=new Map(data.map(d=>[d.name,d.n]));}
  function expandedNames(){return state.pack?Object.keys(state.pack.entries).filter(n=>state.order.has(n)):[];}
  function searchText(name){const e=get(name);return e?JSON.stringify(e):'';}
  function matches(name,view){const e=get(name);return !state.pack||!view||(view==='expanded'?Boolean(e):view==='attention'?Boolean(e?.attention):true);}
  function mountControls(filter,total) {
    const header=document.querySelector('body>header');if(!header||document.getElementById('reference-overview'))return;
    const overview=node('section','ref-overview');overview.id='reference-overview';overview.setAttribute('aria-label','Description research coverage');
    if(state.failed||!state.pack){overview.append(node('p','','Reference notes could not load. The 210-mod checklist and saved checkmarks still work. Reload to retry.'));header.append(overview);return;}
    const names=expandedNames(),flagged=names.filter(n=>get(n).attention);
    overview.append(node('p','ref-kicker','REFERENCE OVERHAUL · BATCH 01'),node('h2','',names.length+' / '+total+' descriptions expanded'));
    overview.append(node('p','','Foundations, Lux modules and the animation block now have sourced reference cards. The other '+(total-names.length)+' entries retain their existing metadata; they have not been marked reviewed.'));
    overview.append(node('p','ref-alert',flagged.length+' expanded cards contain recorded compatibility warnings or unresolved requirements. A successful back-draw test does not certify the rest of the setup.'));
    const select=document.createElement('select');select.id='reference-view';select.append(new Option('All '+total+' entries',''),new Option('Expanded descriptions · '+names.length,'expanded'),new Option('Warnings / open questions · '+flagged.length,'attention'));select.addEventListener('change',filter);
    const label=node('label','reference-filter','Description research');label.htmlFor=select.id;label.append(select);document.querySelector('.tools .filters')?.append(label);
    const actions=node('div','ref-actions');
    for(const [text,value] of [['Browse this batch','expanded'],['Review flagged cards','attention']]){const b=node('button','',text);b.type='button';b.addEventListener('click',()=>{document.getElementById('show-all')?.click();select.value=value;filter();document.getElementById('mods')?.scrollIntoView({block:'start',behavior:'auto'});});actions.append(b);}
    const a=node('a','','Research notes & scope');a.href='REFERENCE-OVERHAUL.md';actions.append(a);overview.append(actions);
    const legend=node('details','ref-legend');legend.append(node('summary','','What the evidence labels mean'));
    legend.append(node('p','','Recorded PS5: visible in your uploaded menu. Official listing match: identity or indexed excerpt only, with limitations shown. Upstream docs: original author information, not guaranteed PS5 parity. User-reported test: your observation, not an independent plugin inspection. Assessment: an interpretation or unresolved question tied to its sources.'));
    overview.append(legend);header.append(overview);
    const requested=new URLSearchParams(location.search).get('reference');if(['expanded','attention'].includes(requested))select.value=requested;
  }
  window.SaqrimReference={ready,decorate,setOrder,searchText,matches,mountControls,expandedNames,get failed(){return state.failed;}};
})();
