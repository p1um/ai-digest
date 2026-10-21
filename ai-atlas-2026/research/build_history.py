"""Build the standalone history page from the reviewed history.json (stdlib only)."""
import html
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'research/history.json').read_text())
e = html.escape


def source_link(title, url):
    return f'<a href="{e(url, quote=True)}" target="_blank" rel="noopener noreferrer">{e(title)} <span aria-hidden="true">↗</span></a>'


eras = ''
for i, era in enumerate(DATA['eras']):
    links = ''.join(source_link(s['title'], s['url']) for s in era['sources'])
    anchors = ''.join(f'<li>{e(a)}</li>' for a in era['anchors'])
    eras += f'''<article class="era"><div class="era-top"><span class="era-period">{e(era['period'])}</span><span class="era-index">0{i+1}</span></div>
    <h3>{e(era['title'])}</h3><span class="era-principle">{e(era['principle'])}</span><p>{e(era['summary'])}</p>
    <ul class="era-anchors">{anchors}</ul><details><summary>Контекст и источники <span aria-hidden="true">+</span></summary><p>{e(era['note'])}</p><div class="source-links">{links}</div></details></article>'''

year_buttons = ''.join(f'<button type="button" data-year="{y["year"]}" aria-pressed="false" aria-controls="year-{y["year"]}"><strong>{y["year"]}</strong><span>{e(y["label"])}</span></button>' for y in DATA['years'])
panels = ''
for y in DATA['years']:
    events = ''
    tech = y['technical']
    technical = f'''<div class="technical-details" aria-label="Как это работает · {y['year']}"><div class="technical-heading"><span class="eyebrow">Как это работает</span><span>Механизм и ограничения</span></div><div class="technical-grid"><div><h4>Что изменилось</h4><p>{e(tech['mechanism'])}</p></div><div><h4>Какие есть ограничения</h4><p>{e(tech['tradeoff'])}</p></div></div><div class="technical-foot"><div class="source-links">{''.join(source_link(s['title'], s['url']) for s in tech['sources'])}</div></div></div>'''
    for event in y['events']:
        links = source_link(event['sourceTitle'], event['source']) + ''.join(source_link(s['title'], s['url']) for s in event.get('extraSources', []))
        events += f'''<article class="milestone"><time datetime="{event['date']}">{e(event['dateLabel'])}</time><h4>{e(event['title'])}</h4><p>{e(event['summary'])}</p><div class="source-links">{links}</div></article>'''
    panels += f'''<article class="year-panel" id="year-{y['year']}" aria-labelledby="title-{y['year']}">
    <div class="year-main"><div class="year-number" aria-hidden="true">{y['year']}</div><div class="eyebrow">{e(y['label'])}{' · срез на 21 октября' if y['year'] == 2026 else ''}</div><h3 id="title-{y['year']}">{e(y['title'])}</h3><p class="year-thesis">{e(y['thesis'])}</p>
    <div class="change"><div><span>Раньше в фокусе</span><p>{e(y['before'])}</p></div><b aria-hidden="true">→</b><div><span>Новый акцент</span><p>{e(y['after'])}</p></div></div>
    <div class="takeaway"><span class="eyebrow">Одна мысль для коллег · редакционный вывод</span><p>{e(y['takeaway'])}</p></div></div>
    <div class="year-evidence"><span class="eyebrow evidence-title">Опорные события</span>{events}<details class="year-context"><summary>Нюанс, который важно сохранить <span aria-hidden="true">+</span></summary><p>{e(y['limit'])}</p></details></div>{technical}</article>'''

source_map = {}
for era in DATA['eras']:
    for s in era['sources']:
        source_map.setdefault(s['url'], s['title'])
for year in DATA['years']:
    for s in year['technical']['sources']:
        source_map.setdefault(s['url'], s['title'])
    for event in year['events']:
        source_map.setdefault(event['source'], event['sourceTitle'])
        for s in event.get('extraSources', []):
            source_map.setdefault(s['url'], s['title'])
register = ''.join(f'<li>{source_link(title, url)}</li>' for url, title in source_map.items())

TEMPLATE = r'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#f7f6f2">
<meta name="description" content="История AI широкими штрихами: истоки 1950–2016 и каждый год Transformer-эры 2017–2026. События, смены подходов и первоисточники.">
<title>AI Atlas — как мы пришли к 2026</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='18' fill='%237553df'/%3E%3Cpath d='M32 10v44M10 32h44M17 17l30 30M17 47l30-30' stroke='%23d7f29a' stroke-width='7'/%3E%3C/svg%3E">
<style>
:root{--paper:#f7f6f2;--ink:#272530;--muted:#777480;--line:#e3e0e8;--purple:#7553df;--lavender:#eeebfa;--lime:#d7f29a;--dark:#24202f}
*{box-sizing:border-box}html{scroll-padding-top:30px}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.55 Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;-webkit-font-smoothing:antialiased}h1,h2,h3,h4,p{margin:0}h1,h2,h3,h4{font-weight:550;letter-spacing:-.045em}a{color:inherit;text-decoration:none}button{font:inherit;cursor:pointer;color:inherit}a,button,summary{touch-action:manipulation;outline-offset:5px}a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid var(--purple)}a:hover{text-decoration:underline;text-underline-offset:4px}button:disabled{cursor:default;opacity:.35}svg{display:block}.wrap{width:min(1280px,calc(100% - 96px));margin:auto}.eyebrow{font:10px/1.6 ui-monospace,SFMono-Regular,Consolas,monospace;letter-spacing:.1em;text-transform:uppercase}.skip{position:fixed;top:-80px;left:20px;z-index:10;background:var(--dark);color:white;padding:10px}.skip:focus{top:10px}.masthead{height:88px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line);gap:24px}.brand{display:flex;gap:10px;align-items:center}.brand svg{width:30px;height:30px;color:var(--purple)}.brand-word{font-size:24px;font-weight:650;letter-spacing:-1.2px}.brand-word span{font-weight:400}.brand-word i{font-style:normal;color:var(--purple)}.nav{display:flex;gap:27px;font-size:12px}.nav a:first-child{color:var(--purple)}.back{font-size:11px;color:var(--muted)}.issue-line{display:flex;justify-content:space-between;color:var(--muted);padding:27px 0 22px;font-size:10px}
.history-hero{display:grid;grid-template-columns:1.1fr 1fr;align-items:center;gap:35px;padding:0 0 38px}.hero-copy h1{font-size:clamp(42px,4.5vw,65px);line-height:1.08;letter-spacing:-.06em;max-width:710px}.hero-copy h1 em{font-family:Georgia,serif;color:var(--purple);font-weight:400}.hero-copy>p{max-width:445px;font-size:14px;color:var(--muted);line-height:1.8;margin-top:21px}.hero-actions{display:flex;align-items:center;gap:22px;margin-top:25px}.button{display:inline-flex;align-items:center;justify-content:center;gap:28px;background:var(--purple);color:white;border:1px solid var(--purple);border-radius:9px;padding:12px 18px;font-size:12px;font-weight:550}.button:hover{background:#6545ca;text-decoration:none}.hero-length{font-size:10px;color:var(--muted);line-height:1.8}.hero-map{position:relative;background:var(--dark);color:#f9f7ff;border-radius:22px;padding:26px 30px 23px;overflow:hidden}.hero-map:before{content:"";position:absolute;inset:0;opacity:.15;background:radial-gradient(#a299b3 .7px,transparent .7px);background-size:20px 20px;pointer-events:none}.map-top{display:flex;justify-content:space-between;position:relative;color:#a9a0bb;font-size:9px}.map-flow{list-style:none;position:relative;padding:0;margin:17px 0 12px}.map-flow:before{content:"";position:absolute;left:22px;top:20px;bottom:25px;width:1px;background:#625670}.map-flow li{position:relative;display:flex;align-items:center;gap:18px;padding:9px 0}.map-num{height:44px;width:44px;border:1px solid #6b5b83;border-radius:50%;display:grid;place-items:center;background:#302837;color:#b9a7d7;font:11px ui-monospace,monospace;flex-shrink:0}.map-flow li:nth-child(2) .map-num{background:#4c3a63}.map-flow li:nth-child(3) .map-num{background:#655084;color:#e0ccff}.map-flow li:nth-child(4) .map-num{background:#997fd2;color:white}.map-flow li:last-child .map-num{background:var(--lime);color:var(--dark);border-color:var(--lime)}.map-flow strong{display:block;font-size:17px;letter-spacing:-.025em;font-weight:500}.map-flow small{display:block;font-size:10px;color:#b3a9c2;margin-top:1px}.map-date{white-space:nowrap;flex-shrink:0;margin-left:auto;font:10px ui-monospace,monospace;color:#a89db9}.map-note{font-size:9px;color:#aaa1b9;border-top:1px solid #4a4058;padding-top:13px;position:relative}.framing{display:grid;grid-template-columns:1fr 1fr 1fr;border-block:1px solid var(--line);padding:24px 0}.framing>div{padding:0 30px;border-right:1px solid var(--line)}.framing>div:first-child{padding-left:0}.framing>div:last-child{border:0;padding-right:0}.framing b{font-size:13px;font-weight:550;display:block;margin-bottom:6px}.framing p{font-size:11px;line-height:1.7;color:var(--muted)}
.section{padding-top:55px}.section-heading{display:flex;justify-content:space-between;align-items:end;gap:25px;margin-bottom:24px}.section-heading .eyebrow{color:var(--purple);margin-bottom:8px}.section-heading h2{font-size:35px;line-height:1.14}.section-caption{font-size:11px;color:var(--muted);max-width:330px;line-height:1.8}.era-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border:1px solid var(--line);border-radius:18px;overflow:hidden;background:#fbfaf7}.era{padding:26px 27px 20px;display:flex;flex-direction:column;min-width:0;border-right:1px solid var(--line);border-bottom:1px solid var(--line)}.era:nth-child(3n){border-right:0}.era:nth-child(n+4){border-bottom:0}.era-top{display:flex;justify-content:space-between;align-items:center}.era-period{font:12px ui-monospace,monospace;color:var(--purple)}.era-index{font:10px ui-monospace,monospace;color:#b2abbc}.era h3{font-size:23px;line-height:1.2;margin-top:18px;max-width:300px;min-height:55px}.era-principle{align-self:flex-start;background:var(--lavender);color:#77648f;border-radius:4px;padding:5px 8px;margin:13px 0 15px;font-size:9px;line-height:1.6}.era>p{font-size:12px;line-height:1.8;color:var(--muted)}.era-anchors{padding:0;list-style:none;margin:17px 0 20px;font-size:10px;line-height:1.8;color:#6f657e}.era-anchors li{position:relative;padding-left:12px;margin-top:4px}.era-anchors li:before{content:"";position:absolute;width:4px;height:4px;left:0;top:7px;border-radius:50%;background:#b7a4da}details{font-size:11px}summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:12px}summary::-webkit-details-marker{display:none}summary>span{font-size:16px;color:#a08abd}details[open] summary>span{transform:rotate(45deg)}details>p{font-size:11px;line-height:1.8;color:var(--muted);margin:13px 0}.era details{border-top:1px solid var(--line);padding-top:13px;margin-top:auto}.source-links{display:flex;flex-direction:column;gap:8px}.source-links a{font-size:10px;line-height:1.6;color:#806894;display:flex;justify-content:space-between;gap:10px}.source-links a span{flex-shrink:0}.origin-foot{font-size:10px;color:var(--muted);margin-top:13px;max-width:740px}
.llm{padding-top:61px}.year-controls{display:none}.is-ready .year-controls{display:flex;flex-direction:column;gap:16px}.year-strip{display:grid;grid-template-columns:repeat(10,minmax(0,1fr));border:1px solid #ddd5e8;border-radius:12px;overflow:hidden;background:#f1edf7}.year-strip button{border:0;border-right:1px solid #ddd5e8;background:transparent;padding:14px 5px 12px;display:flex;flex-direction:column;gap:5px;align-items:center}.year-strip button:last-child{border-right:0}.year-strip strong{font:18px ui-monospace,monospace;letter-spacing:-1px}.year-strip button span{font-size:9px;color:#8c7d9b;white-space:nowrap}.year-strip button[aria-pressed="true"]{background:var(--purple);color:#fff}.year-strip button[aria-pressed="true"] span{color:#e1d7f7}.year-strip button:hover:not([aria-pressed="true"]){background:#e5ddf3}.year-toolbar{display:flex;align-items:center;justify-content:space-between;font-size:10px;gap:16px}.year-nav{display:flex;align-items:center;gap:15px}.year-nav button{height:34px;min-width:34px;padding:0 9px;border:1px solid var(--line);background:transparent;border-radius:7px;font-size:14px}.year-nav span{font:10px ui-monospace,monospace;color:var(--muted);min-width:45px;text-align:center}.all-years{background:transparent;border:1px solid var(--line);border-radius:7px;padding:7px 12px;font-size:10px}.all-years[aria-pressed="true"]{background:var(--lavender);color:var(--purple);border-color:#cebfeb}.year-help{color:var(--muted)}.year-panel{display:grid;grid-template-columns:1.1fr 1fr;border:1px solid var(--line);border-radius:18px;overflow:hidden;background:#fcfbf8;margin-top:20px;scroll-margin-top:30px}.is-ready .year-panel:not(.active){display:none}.is-ready.show-all .year-panel{display:grid}.year-main{padding:32px 36px;position:relative;background:var(--lavender);overflow:hidden;display:flex;flex-direction:column;min-height:515px}.year-number{font:80px/.85 ui-monospace,SFMono-Regular,Consolas,monospace;letter-spacing:-8px;color:#d7cdee;margin-bottom:31px}.year-main>.eyebrow{color:var(--purple)}.year-main h3{font-size:34px;line-height:1.13;margin-top:10px;max-width:490px}.year-thesis{font-size:13px;line-height:1.8;color:#82718c;margin-top:16px;max-width:465px}.change{display:grid;grid-template-columns:1fr 22px 1fr;align-items:center;gap:13px;margin-top:25px;border-top:1px solid #d7cfe5;padding-top:18px}.change span{font:8px ui-monospace,monospace;letter-spacing:.05em;text-transform:uppercase;color:#a493b3}.change p{font-size:11px;line-height:1.6;margin-top:6px;color:#766285}.change b{font-size:20px;color:#b19ac9;font-weight:400}.takeaway{border-left:2px solid var(--purple);padding-left:15px;margin-top:25px}.takeaway .eyebrow{font-size:8px;letter-spacing:.06em;color:#a08ab3}.takeaway p{font-size:13px;line-height:1.7;color:#705680;margin-top:7px;max-width:460px}.year-evidence{padding:29px 34px 23px;display:flex;flex-direction:column;min-width:0}.evidence-title{color:#a394ae;margin-bottom:3px}.milestone{padding:17px 0;border-bottom:1px solid var(--line)}.milestone time{font:9px ui-monospace,monospace;color:#a08eae;display:block}.milestone h4{font-size:19px;line-height:1.3;margin-top:7px}.milestone p{font-size:12px;line-height:1.75;color:var(--muted);margin-top:8px}.milestone .source-links{margin-top:11px}.year-context{padding-top:17px;margin-top:auto;color:#80658f}.year-context>p{margin-bottom:0}.llm-bottom{display:flex;align-items:center;justify-content:space-between;gap:20px;padding-top:17px;font-size:10px;color:var(--muted)}.llm-bottom a{color:var(--purple);font-size:12px;white-space:nowrap}.sources{margin-top:54px;padding:29px 0;border-block:1px solid var(--line);display:grid;grid-template-columns:.8fr 1.2fr;gap:70px}.sources h2{font-size:27px;margin-top:7px}.sources-intro{font-size:11px;color:var(--muted);line-height:1.8;margin:13px 0 18px}.source-register{margin-top:15px;padding-left:22px;columns:2;column-gap:25px}.source-register li{break-inside:avoid;padding:0 0 10px;font-size:10px;color:#9c8aa9}.source-register a{color:#806b90;font-size:10px;overflow-wrap:anywhere}.sources summary{color:#806b90;font-size:12px}.source-tools{display:flex;gap:10px}.source-tools button{font-size:10px;border:1px solid var(--line);background:transparent;padding:8px 12px;border-radius:7px}.source-tools button:hover{background:var(--lavender)}.source-method{color:var(--muted);font-size:11px;line-height:1.8}.source-method p+p{margin-top:13px}.sources details{grid-column:1/-1;border-top:1px solid var(--line);padding-top:17px}.next-chapter{display:flex;align-items:center;justify-content:space-between;background:var(--dark);color:white;padding:30px 35px;border-radius:16px;margin-top:35px;gap:25px}.next-chapter .eyebrow{color:#b5a9c5}.next-chapter h2{font-size:28px;margin-top:5px}.next-chapter .button{background:var(--lime);border-color:var(--lime);color:var(--dark);white-space:nowrap}.footer{display:flex;justify-content:space-between;gap:20px;padding:29px 0;font-size:10px;color:var(--muted)}.footer a{color:var(--purple)}
@media(min-width:1600px){.hero-copy h1{font-size:70px}}
@media(max-width:1100px){.wrap{width:calc(100% - 60px)}.back{display:none}.history-hero{gap:28px;grid-template-columns:1.1fr 1fr}.hero-copy h1{font-size:48px}.hero-map{padding:24px}.map-flow strong{font-size:16px}.map-date{font-size:9px}.era{padding:23px 21px 18px}.era h3{font-size:21px}.year-main{padding:29px 27px}.year-main h3{font-size:30px}.year-evidence{padding:26px}.year-strip button span{font-size:8px}.year-help{display:none}.sources{gap:40px}}
@media(max-width:800px){.history-hero{grid-template-columns:1fr 1fr;gap:23px}.hero-copy h1{font-size:39px}.hero-copy>p{font-size:12px}.hero-length{display:none}.map-flow strong{font-size:14px}.map-flow small{font-size:9px}.map-flow li{gap:12px}.map-num{width:36px;height:36px}.map-flow:before{left:18px}.map-date{display:none}.hero-map{padding:23px 20px}.era-grid{grid-template-columns:1fr 1fr}.era:nth-child(3n){border-right:1px solid var(--line)}.era:nth-child(2n){border-right:0}.era:nth-child(n+4){border-bottom:1px solid var(--line)}.era:nth-child(n+5){border-bottom:0}.era h3{min-height:51px}.year-strip{grid-template-columns:repeat(5,minmax(0,1fr))}.year-strip button:nth-child(5){border-right:0}.year-strip button:nth-child(-n+5){border-bottom:1px solid #ddd5e8}.year-strip button{padding:10px 5px 8px}.year-strip button span{font-size:9px}.year-panel{grid-template-columns:1fr 1fr}.year-main h3{font-size:27px}.year-main{padding:25px}.year-number{font-size:65px;margin-bottom:25px}.year-evidence{padding:24px}.change{gap:8px;grid-template-columns:1fr 16px 1fr}.change p{font-size:10px}.takeaway p{font-size:12px}.milestone h4{font-size:17px}.milestone p{font-size:11px}.section-heading h2{font-size:30px}.section-caption{max-width:260px}.source-register{columns:1}.next-chapter h2{font-size:24px}.next-chapter{padding:25px}.framing>div{padding:0 19px}.framing b{font-size:12px}}
@media(max-width:600px){.wrap{width:calc(100% - 36px)}.masthead{height:72px;gap:15px}.brand-word{font-size:20px}.brand svg{width:26px;height:26px}.nav{gap:17px;font-size:10px}.nav a:first-child{display:none}.issue-line{font-size:8px;padding:22px 0 19px;gap:10px}.history-hero{grid-template-columns:1fr;padding-bottom:27px;gap:27px}.hero-copy h1{font-size:47px;max-width:400px}.hero-copy>p{font-size:13px;margin-top:18px}.hero-length{display:block}.hero-actions{margin-top:21px}.hero-map{padding:23px 25px 20px}.map-flow{margin:11px 0}.map-flow strong{font-size:17px}.map-flow small{font-size:10px}.map-flow li{padding:8px 0;gap:17px}.map-num{width:40px;height:40px}.map-flow:before{left:20px}.map-date{display:block;font-size:9px}.framing{grid-template-columns:1fr;padding:0}.framing>div,.framing>div:first-child,.framing>div:last-child{padding:17px 0;border-right:0;border-bottom:1px solid var(--line);display:grid;grid-template-columns:86px 1fr;gap:17px}.framing>div:last-child{border-bottom:0}.framing b{font-size:12px;margin-top:2px}.framing p{font-size:11px}.section{padding-top:38px}.section-heading{flex-direction:column;align-items:start;gap:13px;margin-bottom:20px}.section-heading h2{font-size:29px}.section-caption{max-width:340px}.era-grid{grid-template-columns:1fr}.era{padding:25px 25px 19px}.era:nth-child(n){border-right:0;border-bottom:1px solid var(--line)}.era:last-child{border-bottom:0}.era h3{min-height:0;font-size:25px;max-width:280px;margin-top:17px}.era-period{font-size:13px}.era-principle{font-size:10px;margin:12px 0 15px}.era>p{font-size:12px}.era-anchors{font-size:11px;margin-bottom:18px}.source-links a{font-size:10px}.llm{padding-top:41px}.year-strip strong{font-size:17px}.year-strip button span{font-size:8px}.year-strip button{padding:12px 3px 10px}.year-toolbar{gap:8px}.year-nav{gap:10px}.all-years{padding:8px 10px}.year-panel{grid-template-columns:1fr;margin-top:17px}.is-ready.show-all .year-panel{display:block}.year-main{padding:27px 26px;min-height:0}.year-number{font-size:66px;margin-bottom:27px}.year-main h3{font-size:31px;max-width:360px}.year-thesis{font-size:12px}.change{gap:10px;grid-template-columns:1fr 18px 1fr;margin-top:22px}.change p{font-size:11px}.takeaway p{font-size:12px}.year-evidence{padding:24px 26px}.milestone h4{font-size:20px}.milestone p{font-size:12px}.milestone time{font-size:9px}.year-context{margin-top:4px}.llm-bottom{align-items:start;flex-direction:column;gap:12px;font-size:9px}.sources{grid-template-columns:1fr;gap:24px;margin-top:36px;padding:26px 0}.sources details{grid-column:1}.source-register{columns:1;padding-left:18px}.next-chapter{flex-direction:column;align-items:start;gap:19px;padding:25px;margin-top:27px}.next-chapter h2{font-size:28px}.footer{flex-direction:column;gap:10px;padding:25px 0;font-size:9px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{@page{size:A4;margin:14mm}html{scroll-behavior:auto}body{background:#fff;color:#000;font-size:10pt}.wrap{width:100%}.nav,.back,.hero-actions,.hero-map,.year-controls,.source-tools,.next-chapter,.footer,.llm-bottom{display:none!important}.masthead{height:42px}.history-hero{display:block;padding:15px 0}.hero-copy h1{font-size:32px;max-width:none}.hero-copy>p{max-width:none}.framing{display:block;padding:0}.framing>div{padding:8px 0!important;border:0!important}.section,.llm{padding-top:20px}.section-heading h2{font-size:24px}.section-heading{display:block}.section-caption{max-width:none;margin-top:7px}.era-grid{display:block;border:0}.era{border:0!important;padding:15px 0;break-inside:avoid}.era h3{min-height:0;font-size:20px}.era>p{font-size:11px}.era details{margin-top:0}.is-ready .year-panel,.is-ready.show-all .year-panel,.year-panel{display:block!important;break-before:page;border:0;margin-top:0;overflow:visible}.year-main{min-height:0;background:white;padding:0 0 18px;border-bottom:1px solid #ccc}.year-number{font-size:50px;color:#555;margin:0 0 20px}.year-main h3{font-size:28px;max-width:none}.year-evidence{padding:18px 0}.year-thesis,.takeaway p{max-width:none}.milestone{break-inside:avoid}.milestone p{font-size:11px}.year-context{margin-top:10px}.sources{display:block;break-before:page;margin-top:0}.source-register{columns:1}details>summary{display:none}details:not([open])>:not(summary){display:block}details{content-visibility:visible}.source-links a{font-size:9px}.source-links a:after{content:" (" attr(href) ")";overflow-wrap:anywhere;font-size:7px}.source-links a span{display:none}.sources details{margin-top:20px}}

.audience-bar{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:15px 18px;margin-bottom:18px;background:#e9e5f1;border:1px solid #dcd2e8;border-radius:10px}.audience-bar .eyebrow{color:#9375aa;font-size:9px}.audience-bar p{font-size:11px;color:#826890;margin-top:3px}.technical-toggle{border:1px solid #bda6d1;border-radius:7px;padding:8px 12px;white-space:nowrap;background:transparent;color:#8c6ca0;font-size:10px}.technical-toggle[aria-pressed="true"]{background:#7553df;border-color:#7553df;color:white}.technical-details{display:none;grid-column:1/-1;border-top:1px solid #dcd5e7;padding:23px 30px 20px;background:#f2eff6}.technical .technical-details{display:block}.technical-heading{display:flex;align-items:center;justify-content:space-between;gap:20px;margin-bottom:16px}.technical-heading .eyebrow{font-size:9px;color:#9272a7}.technical-heading>span:last-child{font-size:9px;color:#ab95ba}.technical-grid{display:grid;grid-template-columns:1fr 1fr;gap:27px}.technical-grid>div{min-width:0}.technical-grid h4{font-size:13px;letter-spacing:-.02em;color:#80618f;font-weight:550;margin-bottom:8px}.technical-grid p{font-size:11px;line-height:1.85;color:#6f617c}.technical-foot{display:flex;justify-content:space-between;gap:30px;border-top:1px solid #dfd7e7;padding-top:14px;margin-top:18px}.technical-foot>span{font-size:9px;color:#80698e;max-width:310px}.technical-foot .source-links{max-width:630px;flex:1;gap:5px}.technical-foot .source-links a{font-size:9px}
@media(max-width:800px){.technical-details{padding:22px 25px}.technical-grid{gap:20px}.technical-grid h4{font-size:12px}.technical-grid p{font-size:10px}.technical-foot{gap:20px}.technical-foot>span{max-width:220px}}
@media(max-width:600px){.audience-bar{align-items:start;padding:15px;gap:14px}.audience-bar .eyebrow{font-size:8px}.audience-bar p{font-size:10px}.technical-toggle{font-size:9px;padding:8px 9px}.technical-details{padding:24px 26px}.technical-heading{align-items:start;flex-direction:column;gap:5px;margin-bottom:18px}.technical-grid{grid-template-columns:1fr;gap:19px}.technical-grid h4{font-size:14px;margin-bottom:7px}.technical-grid p{font-size:12px;line-height:1.8}.technical-foot{flex-direction:column;gap:12px}.technical-foot>span{max-width:none}.technical-foot .source-links a{font-size:10px}}
@media print{.audience-bar{display:none!important}.technical-details{display:block!important;background:white;padding:18px 0;border-top:1px solid #ccc}.technical-grid{grid-template-columns:1fr;gap:13px}.technical-grid>div{break-inside:avoid}.technical-grid p{font-size:10px}.technical-heading{display:none}.technical-foot{display:block}.technical-foot>span{display:block;margin-bottom:10px}}
</style>
</head>
<body>
<a class="skip" href="#llm">Перейти к годам LLM</a>
<div class="wrap" id="top">
<header class="masthead"><a class="brand" href="index.html" aria-label="AI Atlas — обзор 2026"><svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 2v28M2 16h28M6.1 6.1l19.8 19.8M6.1 25.9 25.9 6.1" fill="none" stroke="currentColor" stroke-width="3"/></svg><span class="brand-word">ai<span>atlas</span><i>.</i></span></a><nav class="nav" aria-label="Навигация"><a href="#origins">Истоки AI</a><a href="#llm">LLM по годам</a><a href="index.html">Обзор 2026 ↗</a><a href="index.html#present/history-2017">Показ →</a></nav><a href="index.html#events" class="back">Вернуться к событиям года →</a></header>
<main>
<div class="issue-line eyebrow"><span>История технологий → история возможностей</span><span>1950 — 21 октября 2026</span></div>
<section class="history-hero" aria-labelledby="history-title"><div class="hero-copy"><h1 id="history-title">Как мы пришли<br>к AI, которому<br><em>делегируют.</em></h1><p>От правил, написанных человеком, до моделей, которые работают с контекстом и инструментами. История широкими штрихами — для разговора о том, что изменилось к 2026 году.</p><div class="hero-actions"><a class="button" href="#llm">Пройти по годам <span aria-hidden="true">→</span></a><span class="hero-length">6 исторических этапов<br>10 годовых глав о LLM</span></div></div>
<div class="hero-map"><div class="map-top eyebrow"><span>Как менялся подход</span><span>Условная схема</span></div><ol class="map-flow"><li><span class="map-num">01</span><div><strong>Описать правила</strong><small>Знания задаёт человек</small></div><span class="map-date">1950–80-е</span></li><li><span class="map-num">02</span><div><strong>Учиться на данных</strong><small>Находить закономерности</small></div><span class="map-date">1980–2010-е</span></li><li><span class="map-num">03</span><div><strong>Переиспользовать модель</strong><small>Предобучение и контекст</small></div><span class="map-date">2017–2021</span></li><li><span class="map-num">04</span><div><strong>Объяснить задачу</strong><small>Инструкции и диалог</small></div><span class="map-date">2022–2024</span></li><li><span class="map-num">05</span><div><strong>Делегировать действия</strong><small>Инструменты и обратная связь</small></div><span class="map-date">2025–2026</span></li></ol><p class="map-note">Новые акценты дополняют прежние подходы. Даты здесь обозначают выбранные вехи, а не первое появление каждой идеи.</p></div></section>
<div class="framing" aria-label="Как читать историю"><div><b>AI шире LLM</b><p>Робототехника, поиск, компьютерное зрение и научные модели развиваются своими путями.</p></div><div><b>2017 — граница шкалы</b><p>Transformer открывает новую главу; нейронные языковые модели существовали до него.</p></div><div><b>2026 ещё идёт</b><p>Последний год показан по состоянию на 21 октября. Это промежуточная картина.</p></div></div>
<section class="section" id="origins" aria-labelledby="origins-title"><div class="section-heading"><div><div class="eyebrow">01 / До современных LLM</div><h2 id="origins-title">Долгая дорога к универсальным моделям</h2></div><p class="section-caption">Шесть опорных этапов вместо перечня каждого года. Нейросети, правила и поиск долго развивались параллельно.</p></div><div class="era-grid">%%ERAS%%</div><p class="origin-foot">Это выборочная история, а не полный каталог достижений. Периоды условны и местами пересекаются; многие идеи имеют более ранних предшественников.</p></section>
<section class="llm" id="llm" aria-labelledby="llm-title"><div class="section-heading"><div><div class="eyebrow">02 / Новая волна языковых моделей</div><h2 id="llm-title">Каждый год — новый акцент</h2></div><p class="section-caption">2017–2026 · выбирайте год или двигайтесь по порядку.<br>Главная мысль слева, подтверждающие события справа.</p></div><div class="audience-bar"><div><div class="eyebrow">Пояснения к истории</div><p>Как менялись подходы и какие ограничения сохраняются.</p></div><button class="technical-toggle" id="technical-toggle" type="button" aria-pressed="false" aria-controls="year-panels">Как это работает</button></div><div class="year-controls"><div class="year-strip" id="year-strip" role="group" aria-label="Выбрать год">%%BUTTONS%%</div><div class="year-toolbar"><div class="year-nav"><button type="button" id="previous-year" aria-label="Предыдущий год">←</button><span id="year-position" aria-live="polite"></span><button type="button" id="next-year" aria-label="Следующий год">→</button></div><span class="year-help">← → на шкале · Home / End — к краям</span><button type="button" class="all-years" id="all-years" aria-pressed="false">Все годы на странице</button></div></div><div id="year-panels">%%PANELS%%</div><noscript><p>JavaScript отключён: все годы показаны последовательно.</p></noscript><div class="llm-bottom"><span>Названия этапов и выводы — редакционная интерпретация. Даты и события — по источникам.</span><a href="index.html#events">Подробная хронология 2026 →</a></div></section>
<section class="sources" id="sources" aria-labelledby="sources-title"><div><div class="eyebrow">03 / Источники и границы</div><h2 id="sources-title">История с опорой на факты</h2><p class="sources-intro">Оригинальные статьи, публикации авторов и история организаций. Для ранних эпох также использован обзор Stanford AI100.</p><div class="source-tools"><button type="button" id="download-history">Скачать данные · JSON ↓</button><button type="button" id="print-history">Печать всех лет ↗</button></div></div><div class="source-method"><p><b>Что отобрано.</b> Вехи, которые помогают объяснить изменения подходов и практических возможностей. Это не рейтинг компаний, не полный список релизов и не доказательство линейного движения к AGI.</p><p><b>Что означают даты.</b> В карточках указан конкретный этап: публикация, анонс, открытие весов или начало доступа. Дата выпуска продукта может отличаться от даты появления лежащей в его основе идеи.</p><p><b>Как использовать в выступлении.</b> 20 минут рассказа по атласу: около 3 минут на истоки, 6 на ключевые повороты, 8 на достижения и сбои, 3 на направления развития и выводы. До 10 минут — вопросы и подробности выбранных карточек. Пояснения механизмов открываются кнопкой «Как это работает».</p></div><details><summary>Реестр источников · %%SOURCE_COUNT%% <span aria-hidden="true">+</span></summary><ol class="source-register">%%REGISTER%%</ol></details></section>
<section class="next-chapter" aria-label="Следующая глава"><div><div class="eyebrow">Теперь — ближе к практике</div><h2>Что из этого изменилось в 2026?</h2></div><a class="button" href="index.html">Открыть обзор 2026 <span aria-hidden="true">→</span></a></section>
</main><footer class="footer"><p>AI Atlas · Историческая глава · Проверено 21 октября 2026</p><a href="#top">Вернуться наверх ↑</a></footer>
</div>
<script type="application/json" id="history-data">%%DATA%%</script>
<script>
'use strict';
const HISTORY=JSON.parse(document.getElementById('history-data').textContent);
const EMBEDDED=window.parent!==window;
const years=HISTORY.years.map(y=>y.year);
const strip=document.getElementById('year-strip');
const buttons=[...strip.querySelectorAll('[data-year]')];
const panels=[...document.querySelectorAll('.year-panel')];
const prev=document.getElementById('previous-year'),next=document.getElementById('next-year'),all=document.getElementById('all-years');
let selected=2017,showAll=false;
const technicalToggle=document.getElementById('technical-toggle');
function setTechnical(enabled,{updateUrl=true}={}){document.body.classList.toggle('technical',enabled);technicalToggle.setAttribute('aria-pressed',String(enabled));if(updateUrl&&!EMBEDDED){try{const url=new URL(location.href);url.searchParams.set('depth',enabled?'technical':'overview');history.replaceState(null,'',url);}catch{}}}
technicalToggle.addEventListener('click',()=>setTechnical(!document.body.classList.contains('technical')));
setTechnical(new URLSearchParams(location.search).get('depth')==='technical',{updateUrl:false});

function fromHash(){const n=Number(location.hash.match(/^#year-(\d{4})$/)?.[1]);return years.includes(n)?n:null;}
function selectYear(year,{updateHash=true,focus=false}={}){
 if(!years.includes(year))return;
 selected=year;showAll=false;document.body.classList.remove('show-all');all.setAttribute('aria-pressed','false');all.textContent='Все годы на странице';
 buttons.forEach(b=>b.setAttribute('aria-pressed',Number(b.dataset.year)===year));
 panels.forEach(p=>{const active=p.id==='year-'+year;p.classList.toggle('active',active);p.setAttribute('aria-hidden',String(!active));});
 const i=years.indexOf(year);prev.disabled=i===0;next.disabled=i===years.length-1;document.getElementById('year-position').textContent=String(i+1).padStart(2,'0')+' / '+years.length;
 if(updateHash&&!EMBEDDED){try{history.replaceState(null,'','#year-'+year);}catch{location.hash='year-'+year;}}
 if(focus)buttons[i].focus();
}
buttons.forEach(b=>b.addEventListener('click',()=>selectYear(Number(b.dataset.year))));
strip.addEventListener('keydown',event=>{const i=years.indexOf(Number(event.target.dataset.year));if(i<0)return;let target;
 if(event.key==='ArrowRight')target=Math.min(i+1,years.length-1);else if(event.key==='ArrowLeft')target=Math.max(i-1,0);else if(event.key==='Home')target=0;else if(event.key==='End')target=years.length-1;else return;
 event.preventDefault();selectYear(years[target],{focus:true});});
prev.addEventListener('click',()=>selectYear(years[years.indexOf(selected)-1]));next.addEventListener('click',()=>selectYear(years[years.indexOf(selected)+1]));
all.addEventListener('click',()=>{showAll=!showAll;document.body.classList.toggle('show-all',showAll);all.setAttribute('aria-pressed',String(showAll));all.textContent=showAll?'Вернуться к одному году':'Все годы на странице';panels.forEach(p=>p.setAttribute('aria-hidden',String(!showAll&&p.id!=='year-'+selected)));});
addEventListener('hashchange',()=>{const y=fromHash();if(y)selectYear(y,{updateHash:false});});
document.getElementById('print-history').addEventListener('click',()=>window.print());
document.getElementById('download-history').addEventListener('click',()=>{if(EMBEDDED){window.parent.postMessage({type:'ai-atlas:download-history'},'*');return;}const blob=new Blob([JSON.stringify(HISTORY,null,2)],{type:'application/json;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='ai-atlas-history-2026-10-21.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
// Print expands context and exposes every year; restore the reader's view afterwards.
let printDetails=[],printHidden=[];
addEventListener('beforeprint',()=>{printDetails=[...document.querySelectorAll('details')].map(d=>[d,d.open]);printDetails.forEach(([d])=>d.open=true);printHidden=panels.map(p=>[p,p.getAttribute('aria-hidden')]);panels.forEach(p=>p.removeAttribute('aria-hidden'));});
addEventListener('afterprint',()=>{printDetails.forEach(([d,open])=>d.open=open);printHidden.forEach(([p,value])=>value===null?p.removeAttribute('aria-hidden'):p.setAttribute('aria-hidden',value));});
if(EMBEDDED){document.addEventListener('click',event=>{const link=event.target.closest('a');if(!link)return;const href=link.getAttribute('href')||'';if(href.startsWith('index.html')){event.preventDefault();const anchor=href.includes('#')?href.slice(href.indexOf('#')):'#overview';window.parent.postMessage({type:'ai-atlas:overview',anchor},'*');}else if(href.startsWith('#')){event.preventDefault();document.getElementById(href.slice(1))?.scrollIntoView({behavior:'instant'});}});}
selectYear(fromHash()||2017,{updateHash:false});document.body.classList.add('is-ready');
</script>
</body>
</html>
'''

for key, value in {
    'ERAS': eras, 'BUTTONS': year_buttons, 'PANELS': panels,
    'SOURCE_COUNT': str(len(source_map)), 'REGISTER': register,
    'DATA': json.dumps(DATA, ensure_ascii=False).replace('<', '\\u003c'),
}.items():
    TEMPLATE = TEMPLATE.replace(f'%%{key}%%', value)

TEMPLATE = TEMPLATE.replace('</style>', (ROOT / 'src/history-desktop.css').read_text() + '\n</style>', 1)
(ROOT / 'dist/history.html').write_text(TEMPLATE)
print(f'Built history.html: {len(DATA["eras"])} eras, {len(DATA["years"])} years, {len(source_map)} sources')

# Keep the overview portable: changing chapters never loads another local file.
# srcdoc isolates the chapter's CSS and JavaScript; all content is inside index.html.
EMBED_START = '<!-- HISTORY_EMBED_START -->'
EMBED_END = '<!-- HISTORY_EMBED_END -->'
embedded_document = json.dumps(TEMPLATE, ensure_ascii=False).replace('<', '\\u003c')
embedded = EMBED_START + r'''
<style>
#history-frame{display:block;width:100%;height:100dvh;min-height:360px;border:0;background:#f7f6f2}
#history-frame[hidden],.history-open>.wrap,.history-open>.progress{display:none!important}
body.history-open{overflow:hidden}
</style>
<iframe id="history-frame" title="История AI · 1950–2026" hidden sandbox="allow-scripts allow-downloads allow-modals allow-popups allow-popups-to-escape-sandbox"></iframe>
<script type="application/json" id="history-document">''' + embedded_document + r'''</script>
<script>
(() => {
 const frame=document.getElementById('history-frame');
 const overview=document.querySelector('.wrap');
 const overviewTitle=document.title;
 let active=false,loaded=false,overviewScroll=0;
 function route(){
  const show=location.hash==='#history';
  if(show){
   if(!active)overviewScroll=window.scrollY;
   overview.hidden=true;frame.hidden=false;document.body.classList.add('history-open');
   document.title='AI Atlas — история AI и LLM';
   if(!loaded){frame.srcdoc=JSON.parse(document.getElementById('history-document').textContent);loaded=true;}
   window.scrollTo(0,0);frame.focus();
  }else if(active){
   frame.hidden=true;overview.hidden=false;document.body.classList.remove('history-open');document.title=overviewTitle;
   const target=document.getElementById(location.hash.slice(1));
   if(target)target.scrollIntoView({behavior:'instant'});else window.scrollTo(0,overviewScroll);
  }
  active=show;
 }
 window.addEventListener('hashchange',route);
 window.addEventListener('message',event=>{
  if(event.source!==frame.contentWindow)return;
  if(event.data?.type==='ai-atlas:overview'){
   const anchors=['#overview','#events','#top','#sources','#russian-ai','#takeaways','#present/history-2017'];
   location.hash=anchors.includes(event.data.anchor)?event.data.anchor:'#overview';
  }else if(event.data?.type==='ai-atlas:download-history'){
   const chapter=new DOMParser().parseFromString(frame.srcdoc,'text/html');
   const data=JSON.parse(chapter.getElementById('history-data').textContent);
   const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json;charset=utf-8'});
   const url=URL.createObjectURL(blob),link=document.createElement('a');
   link.href=url;link.download='ai-atlas-history-2026-10-21.json';link.click();
   setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
 });
 route();
})();
</script>
''' + EMBED_END
index_path = ROOT / 'dist/index.html'
index = index_path.read_text().replace('href="history.html"', 'href="#history"')
if EMBED_START in index:
    start = index.index(EMBED_START)
    end = index.index(EMBED_END, start) + len(EMBED_END)
    index = index[:start] + embedded + index[end:]
else:
    index = index.replace('</body>', embedded + '\n</body>', 1)
index_path.write_text(index)
print('Embedded history in index.html: single-file chapter navigation')
runpy.run_path(str(ROOT / 'research/build_presentation.py'))
