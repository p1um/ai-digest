(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('presentation-data').textContent);
  const safe = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const byId = id => document.getElementById(id);
  const source = event => `<a class="presenter-source" href="${safe(event.source)}" target="_blank" rel="noopener noreferrer">${safe(event.sourceTitle)} ↗</a>`;
  const takeaways = () => `<div class="takeaways-grid">${data.takeaways.map(item => `<article class="takeaway-card"><div class="eyebrow">${safe(item.label)}</div><h3>${safe(item.title)}</h3><p>${safe(item.text)}</p></article>`).join('')}</div>`;

  // Labels form a conventional legend: color and a visible count identify each arc.
  const legend = document.createElement('div');
  legend.className = 'orbit-legend';
  legend.setAttribute('role', 'group');
  legend.setAttribute('aria-label', 'Направления и число событий');
  for (const topic of Object.keys(TOPICS)) {
    const button = document.querySelector(`.orbit-tag[data-topic="${topic}"]`);
    const n = EVENTS.filter(event => event.category === topic).length;
    button.innerHTML = `<i aria-hidden="true"></i><span>${TOPICS[topic].label}</span><b>${n}</b>`;
    button.setAttribute('aria-label', `${TOPICS[topic].label} · событий: ${n}`);
    legend.append(button);
  }
  document.querySelector('.orbit').after(legend);
  byId('takeaways-content').innerHTML = takeaways();

  const slides = data.slides;
  byId('presentation-chapters').innerHTML = data.chapters.map(chapter => `<button type="button" data-chapter="${safe(chapter.id)}">${safe(chapter.label)}</button>`).join('');
  const stage = byId('presenter');
  const slide = byId('presentation-slide');
  const picker = byId('presentation-picker');
  const previous = byId('presentation-prev');
  const next = byId('presentation-next');
  const dialog = byId('presentation-dialog');
  let current = 0, active = false, returnHash = '#overview', returnScroll = 0, opener = null, dialogOpener = null;
  let atlasTitle = document.title;
  picker.innerHTML = slides.map(item => `<option value="${item.id}">${safe(item.label)}</option>`).join('');

  const heading = (kicker, title, lead = '') => `<header><div class="presenter-kicker">${safe(kicker)}</div><h2 id="presentation-title" tabindex="-1">${safe(title)}</h2>${lead ? `<p class="presenter-lead">${safe(lead)}</p>` : ''}</header>`;
  const path = steps => `<ol class="story-path">${steps.map((step,i)=>`<li><span>${String(i+1).padStart(2,'0')}</span>${safe(step)}</li>`).join('')}</ol>`;
  const cards = (items,extra='') => `<div class="story-cards ${extra}">${items.map((card,i)=>`<article class="story-card"><div class="story-card-mark" aria-hidden="true">${String(i+1).padStart(2,'0')}</div><div class="presenter-label">${safe(card.tag)}</div><h3>${safe(card.title)}</h3><p>${safe(card.text)}</p></article>`).join('')}</div>`;
  function visual(item) {
    const v=item.visual;
    if(item.layout==='moe')return `<div class="moe-visual"><div class="moe-router"><span class="presenter-label">Один токен → маршрутизатор</span><div class="moe-experts" role="img" aria-label="Условная схема: выбрана только часть экспертов">${Array.from({length:8},(_,i)=>`<span class="${[1,4].includes(i)?'selected':''}">E${i+1}</span>`).join('')}</div><p>Выбранные эксперты → общий результат</p><small>Схема условная: число блоков не отражает архитектуру модели.</small></div><div class="moe-models">${v.models.map(m=>`<article><h3>${safe(m.name)}</h3><p><strong>${safe(m.total)}</strong> всего <span>→</span> <b>${safe(m.active)}</b> активны</p><div class="moe-bar" aria-hidden="true"><i style="width:${m.ratio*100}%"></i></div></article>`).join('')}<p class="moe-caption">Параметры на токен · полные веса всё ещё требуют памяти</p></div></div>`;
    if(item.layout==='workflow')return `<div class="story-workflow">${path(v.steps)}${cards(v.cards,'story-two story-small')}<p class="workflow-return">↶ Результат проверки уточняет требования и следующий шаг</p></div>`;
    if(item.layout==='timeline'||item.layout==='systems')return cards(v.cards,item.layout==='systems'?'story-two':'');
    if(item.layout==='compare')return `<div class="story-compare">${v.cards.map((card,i)=>`<article class="story-card"><span class="presenter-label">${safe(card.tag)}</span><h3>${safe(card.title)}</h3><p>${safe(card.text)}</p>${path(v.paths[i])}</article>`).join('')}</div>`;
    if(item.layout==='attention')return `<div class="story-attention"><div class="attention-map" role="img" aria-label="Условная схема связей между словами через механизм внимания"><svg viewBox="0 0 800 135" preserveAspectRatio="none" aria-hidden="true"><path d="M100 125Q200 -35 300 125M100 125Q300 -80 500 125M100 125Q400 -110 700 125M300 125Q400 30 500 125M300 125Q500 -30 700 125M500 125Q600 30 700 125" fill="none" stroke="currentColor" stroke-width="2"/></svg><div>${v.tokens.map(t=>`<span>${safe(t)}</span>`).join('')}</div></div>${cards(v.cards,'story-two story-small')}</div>`;
    if(item.layout==='conversation')return `<div class="story-conversation"><div class="conversation-bubble user"><span>Задача</span><p>${safe(v.prompt)}</p></div><div class="conversation-bubble assistant"><span>Ответ</span><p>${safe(v.response)}</p></div><div class="conversation-bubble user"><span>Уточнение</span><p>${safe(v.followup)}</p></div><div class="conversation-caption">Условный пример · диалог позволяет уточнять результат</div></div>`;
    if(item.layout==='metrics')return `<div class="story-evidence ${item.id==='swarm'?'story-caution':''}"><div class="story-metrics">${v.metrics.map(m=>`<div><strong>${safe(m.value)}</strong><span>${safe(m.label)}</span></div>`).join('')}</div>${path(v.steps)}</div>`;
    if(item.layout==='loop')return `<div class="story-loop"><div class="loop-track">${v.steps.map((step,i)=>`<div><span>${String(i+1).padStart(2,'0')}</span><b>${safe(step)}</b></div>`).join('')}<p>↻ Обратная связь запускает следующий цикл</p></div><aside class="story-callout"><span class="presenter-label">${safe(v.callout.tag)}</span><h3>${safe(v.callout.title)}</h3><p>${safe(v.callout.text)}</p></aside></div>`;
    if(item.layout==='channels')return `<div class="story-cards story-channels">${v.cards.map((c,i)=>`<article class="story-card"><div class="channel-visual channel-${i}" aria-hidden="true">${i===0?'<i></i><b></b><span></span>':i===1?'<i></i><i></i><i></i><i></i><i></i><i></i><i></i>':'<i></i><b></b><span></span>'}</div><span class="presenter-label">${safe(c.tag)}</span><h3>${safe(c.title)}</h3><p>${safe(c.text)}</p></article>`).join('')}</div>`;
    if(item.layout==='future')return `<div class="story-cards story-future">${v.cards.map(c=>`<article class="story-card"><span class="presenter-label">${safe(c.tag)}</span><h3>${safe(c.title)}</h3><p>${safe(c.now)}</p><p class="future-next">${safe(c.next)}</p><p class="future-barrier">${safe(c.barrier)}</p></article>`).join('')}</div>`;
    return takeaways();
  }
  function renderSlide(item) {
    if(item.layout==='cover')return `<div class="presenter-intro"><div><div class="presenter-kicker">${safe(item.era)} · история и направления развития</div><h2 id="presentation-title" tabindex="-1">Как AI научился<br><em>действовать.</em></h2><p class="presenter-lead">${safe(item.lead)}</p><p class="presenter-footnote" style="margin-top:28px">${safe(item.caveat)}</p></div><div class="presenter-flow"><div class="presenter-label">Четыре вопроса к истории AI</div><ol><li><span>01</span> С чего всё началось?</li><li><span>02</span> Что изменило траекторию?</li><li><span>03</span> Что уже получается?</li><li><span>04</span> Куда движется развитие?</li></ol><p>От идей и исследований — к конкретным достижениям, ошибкам и новым задачам.</p></div></div>`;
    const links=item.layout==='final'?`<div class="presenter-links"><a class="presenter-detail" href="#events">Открыть каталог для вопросов ↗</a><a class="presenter-source" href="#history">История по годам ↗</a><a class="presenter-source" href="#sources">Первоисточники ↗</a></div>`:`<div class="story-evidence-footer"><button type="button" class="presenter-detail" data-story-details="${safe(item.id)}">Факты и источники <span aria-hidden="true">↗</span></button><p>${safe(item.caveat)}</p></div>`;
    return heading(item.era,item.title,item.lead)+visual(item)+`<div class="story-takeaway"><span class="presenter-label">${item.layout==='final'?'Вопрос для обсуждения':'Главная мысль'}</span><p>${safe(item.takeaway)}</p></div>`+links;
  }

  function render() {
    const item = slides[current];
    slide.className = `presenter-slide story-slide story-layout-${item.layout}`;
    slide.dataset.slide = item.id;
    slide.innerHTML = renderSlide(item);
    slide.setAttribute('aria-labelledby','presentation-title');
    picker.value = item.id;
    previous.disabled = current === 0;
    next.disabled = current === slides.length - 1;
    byId('presentation-position').textContent = `${String(current+1).padStart(2,'0')} / ${slides.length}`;
    byId('presentation-progress').style.width = `${(current+1)/slides.length*100}%`;
    stage.querySelectorAll('[data-chapter]').forEach(button => {
      if (button.dataset.chapter === item.chapter) button.setAttribute('aria-current','step');
      else button.removeAttribute('aria-current');
    });
    document.title = `AI Atlas · ${item.label}`;
    byId('presentation-body').scrollTop = 0;
    byId('presentation-title').focus({preventScroll:true});
  }
  function go(index) {
    if (index < 0 || index >= slides.length) return;
    current = index;
    history.replaceState(null,'',location.pathname + location.search + '#present/' + slides[current].id);
    render();
  }
  function route() {
    const match = location.hash.match(/^#present\/([a-z0-9-]+)$/);
    const requested = match ? (data.aliases[match[1]] || match[1]) : null;
    const index = slides.findIndex(item => item.id === requested);
    if(index >= 0 && requested !== match[1]) history.replaceState(null,'',location.pathname + location.search + '#present/' + requested);
    if (index >= 0) {
      if (!active) atlasTitle = document.title;
      active = true; current = index;
      stage.hidden = false;
      document.body.classList.add('presentation-open');
      render();
    } else if (active) {
      active = false;
      stage.hidden = true;
      document.body.classList.remove('presentation-open');
      document.title = location.hash === '#history' ? 'AI Atlas — история AI и LLM' : atlasTitle;
      if (document.fullscreenElement === stage) document.exitFullscreen().catch(() => {});
      const target = byId(location.hash.slice(1));
      if (target) target.scrollIntoView({behavior:'instant'});
    }
  }
  function exit() {
    location.hash = returnHash;
    // Wait for the atlas route to become visible before restoring the launch position.
    requestAnimationFrame(() => {window.scrollTo({top:returnScroll,behavior:'instant'});if(opener?.isConnected)opener.focus({preventScroll:true});});
  }
  document.addEventListener('click',event => {
    const link = event.target.closest('a[href^="#present/"]');
    if (link && !active) {returnHash=location.hash||'#overview';returnScroll=scrollY;opener=link;}
  });
  previous.addEventListener('click',()=>go(current-1));
  next.addEventListener('click',()=>go(current+1));
  picker.addEventListener('change',()=>go(slides.findIndex(item=>item.id===picker.value)));
  stage.querySelectorAll('[data-chapter]').forEach(button=>button.addEventListener('click',()=>go(slides.findIndex(item=>item.id===button.dataset.chapter))));
  byId('presentation-exit').addEventListener('click',exit);
  if (!document.fullscreenEnabled) byId('presentation-fullscreen').hidden=true;
  byId('presentation-fullscreen').addEventListener('click',async()=>{
    try {if(document.fullscreenElement===stage)await document.exitFullscreen();else await stage.requestFullscreen();}
    catch {byId('presentation-fullscreen').textContent='Полный экран недоступен';}
  });
  document.addEventListener('fullscreenchange',()=>{byId('presentation-fullscreen').textContent=document.fullscreenElement===stage?'В окно':'На весь экран';});
  document.addEventListener('keydown',event=>{
    if(!active||event.defaultPrevented||event.metaKey||event.ctrlKey||event.altKey||document.querySelector('dialog[open]'))return;
    if(event.target.closest('input,textarea,select,[contenteditable="true"]')&&event.key!=='Escape')return;
    if(event.key===' '&&event.target.closest('button,a'))return;
    if(event.key==='ArrowRight'||event.key==='PageDown'||event.key===' '){event.preventDefault();go(current+1);}
    else if(event.key==='ArrowLeft'||event.key==='PageUp'){event.preventDefault();go(current-1);}
    else if(event.key==='Home'){event.preventDefault();go(0);}
    else if(event.key==='End'){event.preventDefault();go(slides.length-1);}
    else if(event.key==='Escape'){event.preventDefault();exit();}
  });
  slide.addEventListener('click',event=>{
    const eventControl=event.target.closest('[data-event]');
    if(eventControl){openEvent(eventControl.dataset.event);return;}
    const control=event.target.closest('[data-story-details]');
    if(!control)return;
    const item=slides.find(item=>item.id===control.dataset.storyDetails);
    dialogOpener=control;
    byId('presentation-dialog-body').innerHTML=`<button type="button" class="modal-close" aria-label="Закрыть пояснения">×</button><div class="presenter-kicker">${safe(item.era)} · проверено 21 октября 2026</div><h2 id="presentation-dialog-title">${safe(item.title)}</h2><div class="presenter-dialog-copy"><h3>${item.chapter==='directions'?'На чём основан вывод':'Что подтверждено'}</h3><p>${safe(item.details.facts)}</p><h3>Границы вывода</h3><p>${safe(item.details.limits)}</p><h3>Первоисточники</h3><div class="story-source-list">${item.sources.map(key=>{const s=data.sources[key];return source({source:s.url,sourceTitle:s.title});}).join('')}</div><details class="story-speaker-notes"><summary>Заметка для выступления</summary><p>${safe(item.notes)}</p></details></div>`;
    dialog.querySelector('.modal-close').addEventListener('click',()=>dialog.close());
    dialog.showModal();dialog.scrollTop=0;
  });
  dialog.addEventListener('close',()=>{if(dialogOpener?.isConnected)dialogOpener.focus({preventScroll:true});});
  dialog.addEventListener('click',event=>{if(event.target===dialog){const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close();}});
  window.addEventListener('hashchange',route);
  route();
})();
