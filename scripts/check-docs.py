#!/usr/bin/env python3
"""Check the public Docs release, including archive/source equality and links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re, zipfile, hashlib, subprocess
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,s):
  super().__init__();self.links=[];self.ids=[];self.h1=0;self.feed(s)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='h1':self.h1+=1
  for key in ['href','src']:
   if key in a:self.links.append(a[key])
new=[ROOT/'docs/index.html',ROOT/'docs/data-room/index.html',ROOT/'legal/awake-cofounder-agreement/v2/index.html',ROOT/'legal/awake-advisor-agreement/index.html']
for p in new:
 s=p.read_text();page=Page(s);assert page.h1==1,(p,'h1 count',page.h1)
 assert len(page.ids)==len(set(page.ids)),p
 for href in page.links:
  u=urlsplit(href)
  if u.scheme or u.netloc:continue
  target=(ROOT/u.path.lstrip('/')) if u.path.startswith('/') else p.parent/u.path if u.path else p
  if target.is_dir():target=target/'index.html'
  assert target.exists(),(p,href)
  if u.fragment and target.suffix=='.html':assert unquote(u.fragment) in Page(target.read_text()).ids,(p,href)
 assert 'docs-nav.js' in s and 'docs.css' in s
for p in ROOT.rglob('*.html'):
 s=p.read_text()
 if 'book-nav' in s:
  assert not re.search(r'<a\b[^>]*>Legal</a>',s),p
starter=ROOT/'docs/data-room/starter';zpath=ROOT/'docs/data-room/newco-data-room-v1.0.zip'
with zipfile.ZipFile(zpath) as z:
 assert z.testzip() is None
 for p in starter.rglob('*'):
  rel='newco-financing-data-room/'+p.relative_to(starter).as_posix()
  if p.is_file():assert z.read(rel)==p.read_bytes(),rel
  elif not any(p.iterdir()):assert rel+'/' in z.namelist(),rel
 assert all(n.startswith('newco-financing-data-room/') and '..' not in Path(n).parts for n in z.namelist())
 assert not any('Leaser' in n or '.DS_Store' in n for n in z.namelist())
index=(starter/'00-index-and-diligence-tracker/document-index.md').read_text();ids=re.findall(r'^\| (\d\d-[\d-]+) \|',index,re.M)
assert len(ids)==72 and len(set(ids))==72
for p in starter.rglob('*.md'):
 for href in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if not urlsplit(href).scheme:assert (p.parent/href).exists(),(p,href)
public='\n'.join(p.read_text() for base in [ROOT/'docs',ROOT/'legal/awake-cofounder-agreement/v2'] for p in base.rglob('*.md'))
for private in ['Chris Miller','Leaser AI','Data Centriq','/Users/amit/Downloads']:assert private not in public,private
# Existing v1 downloadable records must remain byte-for-byte equal to HEAD.
for p in (ROOT/'legal/awake-cofounder-agreement').iterdir():
 if p.suffix in ['.pdf','.docx','.md']:
  rel=p.relative_to(ROOT).as_posix();old=subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT);assert old==p.read_bytes(),rel
print('Public links, headings, anchors, 72 unique records, archive/source equality, empty folders, private-content checks and unchanged v1 files passed.')
