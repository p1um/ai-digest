"""Embed the guided desktop presentation into the portable atlas (stdlib only)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'research/presentation.json').read_text())
events = json.loads((ROOT / 'research/events.json').read_text())
slide_ids = {slide['id'] for slide in DATA['slides']}
assert len(slide_ids) == len(DATA['slides']), 'Duplicate slide ids'
assert len({event['id'] for event in events}) == len(events), 'Duplicate event ids'
assert all(chapter['id'] in slide_ids for chapter in DATA['chapters'])
assert all(target in slide_ids for target in DATA['aliases'].values())
for slide in DATA['slides']:
    assert slide['chapter'] in {chapter['id'] for chapter in DATA['chapters']}
    assert all(key in DATA['sources'] for key in slide['sources'])
    assert slide['sources'] or slide['layout'] in ('cover', 'final')
src = ROOT / 'src'
markup = (src / 'presentation.html').read_text().replace('%%PRESENTATION_DATA%%', json.dumps(DATA, ensure_ascii=False).replace('<', '\\u003c'))
block = '\n'.join([
    '<!-- PRESENTATION_START -->',
    '<style id="presentation-styles">' + (src / 'presentation.css').read_text() + '</style>',
    markup,
    '<script>' + (src / 'presentation.js').read_text() + '</script>',
    '<!-- PRESENTATION_END -->',
])
path = ROOT / 'dist/index.html'
index = path.read_text()
event_data = json.dumps(events, ensure_ascii=False).replace('<', '\\u003c')
index, replaced = re.subn(r'(<script type="application/json" id="event-data">).*?(</script>)',
                         lambda match: match[1] + event_data + match[2], index, count=1, flags=re.S)
assert replaced == 1, 'Missing event data block'
if '<!-- PRESENTATION_START -->' in index:
    start = index.index('<!-- PRESENTATION_START -->')
    end = index.index('<!-- PRESENTATION_END -->', start) + len('<!-- PRESENTATION_END -->')
    index = index[:start] + block + index[end:]
else:
    index = index.replace('</body>', block + '\n</body>', 1)
path.write_text(index)
print(f'Embedded presentation: {len(DATA["slides"])} screens, {len(events)} catalog events, self-contained index.html')
