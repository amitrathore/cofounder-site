#!/usr/bin/env python3
"""Build public Docs pages and ZIP from checked-in generic sources (Python stdlib)."""
from pathlib import Path
from html import escape
import re, zipfile, posixpath, hashlib
ROOT=Path(__file__).resolve().parents[1]
DR=ROOT/'docs/data-room';V2=ROOT/'legal/awake-cofounder-agreement/v2'

def inline(s):
 s=escape(s)
 s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:f'<a href="{m[2]}">{m[1]}</a>',s)
 s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
 s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
 s=s.replace('&lt;br&gt;','<br>')
 return s

def md(s):
 out=[]
 for block in s.strip().split('\n\n'):
  if block.strip()=='---':out.append('<hr>');continue
  if block.startswith('#'):
   m=re.match(r'(#{1,6}) (.*)',block);n=min(len(m[1])+1,6);out.append(f'<h{n}>{inline(m[2])}</h{n}>');continue
  lines=block.splitlines()
  if block.startswith('|'):
   rs=[[c.strip() for c in l.strip().strip('|').split('|')] for l in lines]
   out.append('<div class="docs-table"><table><thead><tr>'+''.join('<th scope="col">'+inline(c)+'</th>' for c in rs[0])+'</tr></thead><tbody>')
   for r in rs[2:]:out.append('<tr>'+''.join('<td>'+inline(c)+'</td>' for c in r)+'</tr>')
   out.append('</tbody></table></div>');continue
  if all(re.match(r'^(?:- |\d+\. )',l) for l in lines):
   tag='ol' if re.match(r'\d',lines[0]) else 'ul'
   out.append(f'<{tag}>'+''.join('<li>'+inline(re.sub(r'^(?:- |\d+\. )','',l)).replace('[ ] ','')+'</li>' for l in lines)+f'</{tag}>');continue
  if block.startswith('> '):out.append('<blockquote>'+inline(re.sub(r'^> ?','',block,flags=re.M))+'</blockquote>');continue
  out.append('<p>'+inline(block)+'</p>')
 return '\n'.join(out)

def docs_menu(current):
 links=[('/docs/','All Docs','Guides and open templates'),('/legal/','Agreements','Founder and venture relationships'),('/docs/data-room/','Data Room','Prepare for investor diligence')]
 items=''.join(f'<a href="{url}"'+(' aria-current="page"' if url==current else '')+f'><strong>{name}</strong><span>{desc}</span></a>' for url,name,desc in links)
 return '<details class="docs-nav"><summary aria-expanded="false">Docs <span aria-hidden="true">▾</span></summary><div class="docs-dropdown">'+items+'</div></details>'

base=(ROOT/'legal/index.html').read_text()
nav=re.search(r'<nav class="book-nav">.*?</nav>',base,re.S)[0]
nav=re.sub(r'href="\.\./', 'href="/',nav)
nav=re.sub(r'<details class="docs-nav">.*?</details>',docs_menu('/legal/'),nav,flags=re.S)
nav=re.sub(r'<a href="\./" class="active">Legal</a>',docs_menu('/legal/'),nav)
# Normalize an already rewritten navigation for a generated page.
def navigation(current):return re.sub(r'<details class="docs-nav">.*?</details>',docs_menu(current),nav,flags=re.S)

def page(path,title,description,content,current='/docs/'):
 path.parent.mkdir(parents=True,exist_ok=True)
 url='/'+str(path.relative_to(ROOT).parent)+'/'
 path.write_text(f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} · Cofounder Docs</title><meta name="description" content="{escape(description,quote=True)}">
<link rel="canonical" href="https://cofounder.community{url}"><meta property="og:title" content="{escape(title,quote=True)} · Cofounder Docs"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:url" content="https://cofounder.community{url}"><meta property="og:type" content="website"><meta property="og:image" content="https://cofounder.community/assets/og-cofounder-v2.png"><meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/book.css"><link rel="stylesheet" href="/assets/program.css"><link rel="stylesheet" href="/assets/docs.css"><script src="/assets/docs-nav.js" defer></script></head>
<body>{navigation(current)}<main class="program-page docs-page">{content}</main>
<footer class="book-foot"><span>© 2026 · <a href="/">cofounder.community</a> · <a href="/docs/">Docs</a> · <a href="https://awake.vc">An Awake Venture ↗</a></span></footer></body></html>''')

def card(kicker,title,desc,links):
 return f'<article class="docs-card"><div class="program-eyebrow">{kicker}</div><h2>{title}</h2><p>{desc}</p><div class="docs-actions">'+''.join(f'<a class="program-button" href="{u}"'+(' download' if u.endswith('.zip') else '')+f'>{label}</a>' for u,label in links)+'</div></article>'

hub='''<header class="docs-hero"><div class="program-eyebrow">Open resources for founders</div><h1>Practical documents for building and funding a company<span class="dot">.</span></h1><p>Start with clear founder relationships. Prepare the records investors need. Download, adapt, and build on open resources from AwakeVC.</p></header><div class="docs-grid">'''
hub+=card('Agreements · Public review draft','Cofounder Agreement v2','A shared founder holding structure, minority protections, service terms, optional milestone awards, and tax records. Independent legal review has not been recorded.',[('/legal/awake-cofounder-agreement/v2/','Explore v2'),('/legal/','All agreements')])
hub+=card('Fundraising · Starter kit','Your first financing data room','Ten folders and 72 checklist items for a SAFE, convertible note, or priced round. A practical guide and an editable folder package.',[('/docs/data-room/','Read the guide'),('/docs/data-room/newco-data-room-v1.0.zip','Download starter ZIP')])
hub+='</div><section class="docs-section"><h2>Agreements for working together</h2><div class="docs-grid">'
for title,path,desc in [('Cofounder Agreement v1','awake-cofounder-agreement','The previously published founder agreement. Remains available alongside v2 for reference.'),('Open Collaboration Agreement','awake-open-collaboration-agreement','A mutual framework for exploring opportunities and collaborating.'),('Venture Memorandum of Understanding','awake-venture-memorandum-of-understanding','Record the initial intent, structure, roles, economics, and exit expectations.'),('Territory Agreement','awake-territory-agreement','Set territory boundaries, performance expectations, and income sharing.')]:
 hub+=card('Agreements',title,desc,[(f'/legal/{path}/','Read agreement')])
hub+='</div></section><p class="docs-note">Educational resources, not individualized legal, tax, or investment advice. Complete agreements with qualified advisers. Publishing a new template does not amend an existing agreement.</p>'
page(ROOT/'docs/index.html','Docs','Open agreements, founder guides and a financing data room starter kit.',hub)

starter=DR/'starter'
# A public license is deliberately limited to the generic template text.
(starter/'LICENSE.md').write_text('''# Template license

NewCo Financing Data Room Starter v1.0. Copyright © 2026 Amit Rathore. Contributed by AwakeVC and cofounder.community under [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/).

You may use, copy, adapt and share the generic template text, including commercially, with attribution, a license link and an indication of changes. Suggested attribution: Based on the NewCo Financing Data Room Starter v1.0 from cofounder.community / AwakeVC; modified by [name] on [date]. No endorsement is implied.

The license does not cover names/logos/trademarks, third-party materials, or confidential company documents and information you add. Linked YC/NVCA materials retain their own terms; they are not bundled here.
''')
(starter/'DISCLAIMER.md').write_text('''# Educational-use disclaimer

This is an organizational starter kit, not completed company documents, a legal opinion, a financing-readiness certification, or a guarantee of investment. Requirements depend on the company, transaction, law and investor. Obtain appropriate legal, tax and financial advice. Configure actual sharing permissions; folder labels do not enforce access controls. Do not put credentials, raw personal data, or privileged advice in a generally shared room.
''')
p=starter/'02-formation-and-governance/README.md'
t=p.read_text();extra='\nFor a possible founder-governance starting point, see the [Cofounder Agreement v2 public review draft](https://cofounder.community/legal/awake-cofounder-agreement/v2/). Use of that template is optional, not a financing requirement.\n'
if extra not in t:p.write_text(t+extra)
p=starter/'README.md';t=p.read_text();extra='\n## Use and sharing\n\nThe Markdown (`.md`) files are plain text: edit them in a text editor or import/copy their contents into your preferred document tool. Upload the extracted folders to your chosen private storage platform. Access labels do not set permissions. See [LICENSE.md](LICENSE.md) and [DISCLAIMER.md](DISCLAIMER.md).\n'
if extra not in t:p.write_text(t+extra)
for transaction in ['01-safe', '02-convertible-note', '03-priced-round', '04-common-closing']:
 for stage in ['drafts', 'executed', 'superseded']:
  (starter/'09-current-financing-and-closing'/transaction/stage).mkdir(parents=True,exist_ok=True)
files=sorted(p for p in starter.rglob('*') if p.is_file() and not any(part.startswith('.') for part in p.relative_to(starter).parts))
with zipfile.ZipFile(DR/'newco-data-room-v1.0.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in files:
  info=zipfile.ZipInfo('newco-financing-data-room/'+p.relative_to(starter).as_posix(),(2026,9,19,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,p.read_bytes())
 for p in sorted(starter.rglob('*')):
  if p.is_dir() and not any(p.iterdir()):z.writestr(zipfile.ZipInfo('newco-financing-data-room/'+p.relative_to(starter).as_posix()+'/',(2026,9,19,0,0,0)),b'')
index=(starter/'00-index-and-diligence-tracker/document-index.md').read_text();count=len(re.findall(r'^\| \d\d-',index,re.M));assert count==72
body=f'''<header class="docs-hero"><a class="docs-back" href="/docs/">← All Docs</a><div class="program-eyebrow">Fundraising · Starter kit</div><h1>A starter data room for your next financing<span class="dot">.</span></h1><p>Organize what investors are funding, who owns it, what obligations exist, and how the financing changes ownership.</p><div class="docs-actions"><a class="program-button primary" href="./newco-data-room-v1.0.zip" download>Download Data Room Starter ZIP</a><a class="program-button" href="#included">See what’s included</a></div><p class="docs-meta">Version 1.0 · Updated September 19, 2026 · 10 folders · {count} checklist items · CC BY 4.0</p></header>
<section class="docs-section"><h2>Start with the records you actually have</h2><p>For a U.S. startup raising a SAFE, convertible note, or priced equity round. The default is a Delaware C corporation, with founder holding-LLC and existing-business transfer records where applicable. A pre-revenue NewCo can mark genuinely absent items “None” or “Not applicable.” Unknown is a different status.</p><p>The ZIP contains editable Markdown instructions, a document index, and folders. It contains no company evidence or completed financing agreements. Markdown files are plain text and can be edited in a text editor or copied into your preferred document tool.</p></section>
<section class="docs-section"><h2>Set up your room</h2><ol class="docs-steps"><li><strong>Download and unzip.</strong> Keep a clean copy of the starter package.</li><li><strong>Copy the folders</strong> into your company’s chosen private storage platform.</li><li><strong>Assign a room owner</strong> and complete company details in folder 00.</li><li><strong>Work through the index.</strong> Assign document owners, status, dates, and links to authoritative copies.</li><li><strong>Add your records.</strong> Separate signed documents from drafts; give confirmed “None” and “Not applicable” entries an explanation.</li><li><strong>Reconcile the evidence.</strong> Ownership, financials, IP rights, and financing assumptions should agree.</li><li><strong>Configure and test access</strong> before sharing. Folder names do not enforce permissions.</li></ol></section>
<section id="included" class="docs-section"><h2>What’s included</h2><p>Expand a folder to see its checklist. The downloadable index starts with every item marked “Not assessed.”</p>'''
for folder in sorted(p for p in starter.iterdir() if p.is_dir()):
 title=(folder/'README.md').read_text().splitlines()[0].lstrip('# ')
 text=(folder/'README.md').read_text();rendered=md('\n'.join(text.splitlines()[1:]))
 # Make package-relative links resolve to public starter source files.
 rendered=re.sub(r'href="(?!https?://|/|#)([^"]+)"',lambda m:'href="./starter/'+posixpath.normpath(folder.name+'/'+m[1])+'"',rendered)
 if folder.name.startswith('09'):
  for sub in sorted(p for p in folder.iterdir() if p.is_dir()):rendered+=md((sub/'README.md').read_text())
 body+=f'<details class="docs-checklist"><summary>{folder.name[:2]} · {escape(title)}</summary><div class="docs-detail">{rendered}</div></details>'
body+='</section><section class="docs-section"><h2>Share in stages</h2><div class="docs-grid">'
for name,desc in [('Initial review','Deck, team, demo, summarized traction, financing ask and operating plan.'),('Serious diligence','Corporate records, capitalization, IP and technology summaries, commercial evidence and detailed financials.'),('Restricted diligence and closing','Sensitive people and tax records, unredacted contracts, and investor-specific closing documents.')]:body+=f'<article class="docs-card"><h3>{name}</h3><p>{desc}</p></article>'
body+='</div><p>Use named-user access and test permissions. Keep credentials, raw customer personal data, and privileged advice out of the general room. Share wire instructions through a separately verified closing process.</p></section><section class="docs-section">'+md((starter/'READINESS.md').read_text())+'</section>'
body+='''<section class="docs-section"><h2>Founder structure and financing</h2><p>If founders use a holding LLC, include its ownership, vesting, authority and consent records alongside the corporation’s documents. For a NewCo receiving existing assets, document ownership, transfers or licenses, approvals and assumed obligations.</p><p>The <a href="/legal/awake-cofounder-agreement/v2/">Cofounder Agreement v2 public review draft</a> offers one possible starting point. Using it is not a financing requirement.</p><p>For transaction documents, consult <a href="https://www.ycombinator.com/safe">YC’s SAFE forms and guidance</a> and the <a href="https://nvca.org/model-legal-documents/">NVCA priced-round model documents</a>. A standard YC SAFE is not a debt note and has no interest or maturity date.</p></section><aside class="docs-note"><p>Contributed by Amit Rathore and AwakeVC. Free to use, adapt, and share under <a href="./starter/LICENSE.md">CC BY 4.0</a>. Your company’s confidential records are not covered by the template license.</p><p>This organizational starter is educational; it is not legal, tax or investment advice, or a financing-readiness certification. <a href="./starter/DISCLAIMER.md">Read the disclaimer.</a></p></aside><div class="docs-actions"><a class="program-button primary" href="./newco-data-room-v1.0.zip" download>Download starter ZIP</a></div>'''
page(DR/'index.html','Data Room','A free ten-folder, 72-item financing data room starter with instructions for SAFE, convertible note and priced rounds.',body,'/docs/data-room/')

vbody='''<header class="docs-hero"><a href="/legal/" class="docs-back">← Agreements</a><div class="program-eyebrow">Version 2.0 · Public review draft</div><h1>Build the founder relationship deliberately<span class="dot">.</span></h1><p>A California founder holding LLC and Delaware operating corporation, with minority protections, explicit service terms, optional awards, and tax records.</p><p class="docs-meta">Revised September 19, 2026 · Independent legal review has not been recorded · CC BY 4.0</p></header><aside class="docs-note"><strong>For public review; not approved for signature.</strong> Complete the fields and companion documents with qualified legal and tax advisers. Publishing this draft does not amend existing signed agreements. <a href="../">Version 1 remains available.</a></aside><section class="docs-section"><h2>Read, review, and adapt</h2><div class="docs-grid">'''
for stem,title in [('awake-cofounder-agreement-v2-review','Agreement'),('guide','Completion guide'),('change-summary','Change summary')]:
 vbody+=card('Public review draft',title,'Editable Word, fixed-layout PDF, and online text.',[(f'./{stem}.docx','Download Word'),(f'./{stem}.pdf','Download PDF'),('#'+stem,'Read online')])
vbody+='</div><p><a href="./LICENSE.md">License</a> · <a href="./DISCLAIMER.md">Disclaimer</a> · <a href="/docs/data-room/">Prepare your data room</a> · <a href="https://github.com/amitrathore/cofounder-site/issues/new">Suggest an improvement ↗</a></p></section>'
for stem,title in [('awake-cofounder-agreement-v2-review','Agreement'),('guide','Completion guide'),('change-summary','Change summary')]:
 content=md((V2/(stem+'.md')).read_text());content=re.sub(r'<h1>(.*?)</h1>',r'<h2>\1</h2>',content)
 vbody+=f'<details id="{stem}" class="docs-checklist docs-agreement"><summary>{title} — read online</summary><div class="docs-detail">{content}<p><a href="./{stem}.md">Canonical Markdown source</a></p></div></details>'
page(V2/'index.html','Cofounder Agreement v2 — Public Review Draft','Founder governance, service terms, optional milestone awards and QSBS records. Public review draft; independent legal review not recorded.',vbody,'/legal/')

# Existing pages keep their content and canonical addresses; only their Docs navigation changes.
for path in ROOT.rglob('*.html'):
 s=path.read_text();rel=path.relative_to(ROOT).as_posix();current='/legal/' if rel.startswith('legal/') else '/docs/data-room/' if rel.startswith('docs/data-room/') else '/docs/' if rel.startswith('docs/') else ''
 def replace_nav(m):
  n=m[0]
  n=re.sub(r'<details class="docs-nav">.*?</details>',docs_menu(current),n,flags=re.S)
  n=re.sub(r'<a\b[^>]*>Legal</a>',docs_menu(current),n)
  return n
 s=re.sub(r'<nav\b.*?</nav>',replace_nav,s,flags=re.S)
 if 'docs-nav' in s:
  if '/assets/docs.css' not in s:s=s.replace('</head>','<link rel="stylesheet" href="/assets/docs.css">\n<script src="/assets/docs-nav.js" defer></script>\n</head>')
 if rel=='index.html':s=s.replace('<li><a href="./legal/">Legal</a></li>','<li><a href="/docs/">Docs</a></li><li><a href="/docs/data-room/">Data Room</a></li>')
 if rel=='legal/index.html':
  s=s.replace('Legal · Cofounder','Agreements · Cofounder Docs')
  s=s.replace('Open legal infrastructure for founders','Open agreements · <a href="/docs/">All Docs</a>')
  feature=card('Public review draft · September 19, 2026','Cofounder Agreement v2','Expanded service terms, milestone choices, IP records and coordinated equity implementation. Independent legal review has not been recorded. Version 1 remains available below.',[('/legal/awake-cofounder-agreement/v2/','Explore v2 and downloads'),('/docs/data-room/','Data Room guide')])
  if '<!-- v2-feature -->' not in s:s=s.replace('<section class="legal-path"','<!-- v2-feature -->'+feature+'<!-- /v2-feature -->\n<section class="legal-path"')
  else:s=re.sub(r'<!-- v2-feature -->.*?<!-- /v2-feature -->','<!-- v2-feature -->'+feature+'<!-- /v2-feature -->',s,flags=re.S)
 if rel.startswith('legal/') and rel.count('/')==2 and not 'v2/' in rel:
  # Preserve the local Agreements return link beside a Docs menu.
  marker='<div class="book-nav-links">'
  if marker in s and '>Agreements</a>' not in s:s=s.replace(marker,marker+'<a href="/legal/">Agreements</a>')
 path.write_text(s)
print('Built Docs hub, Data Room (72 entries), deterministic ZIP, public v2 page, and site-wide navigation.')
