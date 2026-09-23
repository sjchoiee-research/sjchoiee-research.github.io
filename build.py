"""Build the static website from content.json. Python 3, standard library only."""
import json, pathlib, html, re, urllib.parse
from sections import hero_visual, featured_papers, scholar_metrics
ROOT=pathlib.Path(__file__).resolve().parent
C=json.loads((ROOT/'content.json').read_text(encoding='utf8'))
P=C['profile']
PUBS=C['publications']
E=lambda s:html.escape(str(s if s is not None else ''),quote=True)
NAV=[('index','Home'),('research','Research'),('publications','Publications'),('patents','Patents & Awards'),('team','Team'),('media','Media'),('about','About')]
def ext(url,label,cls=''):return f'<a href="{E(url)}" target="_blank" rel="noopener noreferrer" class="{cls}">{label}</a>'
def tl(url,label):return f'<a class="text-link" href="{E(url)}">{label}<span class="arrow" aria-hidden="true">↗</span></a>'
def page_intro(kicker,title,desc):
 return f'<div class="page-intro"><div class="eyebrow">{E(kicker)}</div><h1 class="{("long-title" if len(title)>20 else "")}">{E(title)}</h1><p>{E(desc)}</p></div>'
def header(page):
 nav=''.join(f'<a href="{slug}.html"'+(' class="active" aria-current="page"' if page==slug else '')+f'>{E(label)}</a>' for slug,label in NAV)
 return f'''<a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="index.html" aria-label="Sung-Jin Choi home"><span class="brand-mark" aria-hidden="true"></span><span><span class="brand-name">Sung-Jin Choi</span><span class="brand-sub">Kookmin University</span></span></a><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-nav">Menu <span aria-hidden="true">☰</span></button><nav id="main-nav" class="main-nav" aria-label="Main navigation">{nav}</nav></div></header>'''
def footer():
 return f'''<footer class="site-footer"><div class="wrap"><div class="footer-top"><div><a class="footer-name" href="index.html">Sung-Jin Choi<span style="color:var(--red)">.</span></a><p class="footer-sub">Semiconductor devices & nanoelectronics<br>Kookmin University · Seoul, Republic of Korea</p></div><div class="footer-links">{ext(P['scholar_url'],'Google Scholar ↗')}{ext(P['lab']['url'],'S!LK ↗')}<a href="mailto:{E(P['contact']['email'])}">Email ↗</a></div></div><div class="footer-bottom"><span>© 2026 Sung-Jin Choi</span><span><a href="credits.html">Sources & image credits</a> · Updated September 2026</span></div></div></footer>'''
def write(page,title,body,desc=None):
 description=desc or 'Sung-Jin Choi, Professor at Kookmin University. Research in semiconductor devices, carbon nanotubes, memory and three-dimensional integration.'
 payload=json.dumps({'publications':PUBS if page=='publications' else [p for p in PUBS if p.get('selected')]},ensure_ascii=False).replace('</','<\\/')
 scripts=f'<script>window.SITE_DATA={payload};</script>' if page in ['publications','index'] else ''
 schema=json.dumps({'@context':'https://schema.org','@type':'Person','name':P['name'],'jobTitle':'Professor','affiliation':{'@type':'CollegeOrUniversity','name':'Kookmin University'},'sameAs':[P['scholar_url'],P['lab']['url']]},ensure_ascii=False)
 doc=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{E(description)}"><meta name="theme-color" content="#ae1e32"><meta property="og:title" content="{E(title)} · Sung-Jin Choi"><meta property="og:description" content="{E(description)}"><meta property="og:type" content="website"><title>{E(title)} · Sung-Jin Choi</title><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/style.css"><link rel="stylesheet" href="assets/sections.css"><script type="application/ld+json">{schema}</script></head><body>{header(page)}<main id="main">{body}</main>{footer()}{scripts}<script src="assets/app.js" defer></script></body></html>'''
 (ROOT/(page+'.html')).write_text(doc,encoding='utf8')
def byid(s):return next(p for p in PUBS if p['id']==s['publication_id'])
def author_markup(s):
 s=E(s)
 return re.sub(r'(?<!\w)(Sung[- ]Jin Choi|S\.?\s*[-‐‑–]?\s*J\.?\s+Choi|최성진)(?!\w)',r'<strong>\1</strong>',s,flags=re.I)
def pubrow(p,selected_label=False,catalog=False):
 url=p.get('doi_url') or ('https://doi.org/'+p['doi'] if p.get('doi') else p['source_url'])
 label='DOI ↗' if p.get('doi') else 'Source ↗'
 search=' '.join(str(p.get(k) or '') for k in ['title','authors','venue','year']).lower()
 attr=f' data-publication="{E(p["id"])}" data-search="{E(search)}" data-year="{E(p.get("year"))}" data-type="{E(p["type"])}" data-selected="{str(p.get("selected",False)).lower()}"' if catalog else ''
 venue=E(p['venue'])+' · '+E(p.get('year') or 'Year not listed')
 if p.get('volume'):
  venue+=' · '+E(p['volume'])+(f"({E(p['issue'])})" if p.get('issue') else '')
  if p.get('pages') or p.get('article_number'):venue+=', '+E(p.get('pages') or p['article_number'])
 return f'''<article class="pub-row"{attr}><div class="pub-year">{E(p.get('year') or '—')}</div><div>{('<div class="pub-selected">Selected publication</div>' if selected_label else '')}<h3 class="pub-title">{ext(url,E(p['title']))}</h3><p class="pub-authors">{author_markup(p['authors'])}</p><p class="pub-venue">{venue}</p></div><div class="pub-actions">{ext(url,label)}<button type="button" data-cite="{E(p['id'])}" aria-label="Copy citation for {E(p['title'])}">Cite</button></div></article>'''
def home():
 areas=''.join(f'<a class="research-card" href="research.html#{r["id"]}"><div class="research-number">0{i+1}<span aria-hidden="true">↗</span></div><h3>{E(r["title"])}</h3><p>{E(r["short"])}</p></a>' for i,r in enumerate(P['research']))
 featured=[C['media'][0],next(m for m in C['media'] if m['id']=='cnt-floating-memory-2022'),next(m for m in C['media'] if m['id']=='neuromorphic-cnt-2017')]
 news=''.join(f'<article class="news-card"><div class="news-meta"><span>{E(m["date"])}</span><span>{E(m["category"])}</span></div><h3><a href="media.html#{m["id"]}">{E(m["title_en"])}</a></h3><p>{E(m["summary_en"])}</p>{tl("media.html#"+m["id"],"Read the story")}</article>' for m in featured)
 photos=''.join(f'<img src="{E(t["photo"])}" alt="{E(t["display_name_en"])}" width="62" height="74" loading="lazy">' for t in C['team'][:5])
 return f'''<div class="wrap"><section class="hero"><div><div class="eyebrow">Semiconductor devices & nanoelectronics</div><h1 class="hero-group-title"><span class="hero-group-name">Sung-Jin Choi</span> Research Group<span>.</span></h1><p class="hero-role">School of Electrical Engineering<br>Kookmin University</p><p class="hero-description">Exploring semiconductor devices, carbon nanotube electronics and three-dimensional integration.</p><div class="hero-links"><a href="research.html" class="button">Explore research <span aria-hidden="true">↗</span></a>{tl("publications.html","Publications")}</div><div class="hero-socials">{ext(P['scholar_url'],'Google Scholar ↗')}{ext(P['lab']['url'],'S!LK laboratory ↗')}<a href="mailto:{E(P['contact']['email'])}">Email ↗</a></div></div>{hero_visual(C)}</section>{scholar_metrics(C)}<div class="credentials"><span><strong>KAIST</strong><span class="dot">·</span>Ph.D. in Electrical Engineering</span><span><strong>UC Berkeley</strong><span class="dot">·</span>Postdoctoral research</span><span><strong>Kookmin University</strong><span class="dot">·</span>Since 2013</span></div><section class="section"><div class="section-head"><div><div class="section-label">From materials to devices</div><h2>Research directions</h2></div>{tl("research.html","Our research")}</div><div class="research-grid">{areas}</div></section>{featured_papers(C)}</div><section class="section soft"><div class="wrap"><div class="section-head"><div><div class="section-label">Research, people & recognition</div><h2>In the news</h2></div>{tl("media.html","Media archive")}</div><div class="news-grid">{news}</div></div></section><div class="wrap"><section class="team-teaser"><div><div class="eyebrow">The people behind the research</div><h2 style="margin-top:16px">Meet our team.</h2><p>Eight graduate researchers working together within the shared S!LK laboratory.</p></div><div><a href="team.html" class="small-portraits" aria-label="Meet our eight current team members">{photos}</a><div style="margin-top:20px">{tl("team.html","Current team")}</div></div></section></div>'''
def research():
 items=''
 for i,r in enumerate(P['research']):
  related=[s for s in C.get('research_reading',C['selected']) if s['research_theme']==r['id']]
  if r['id']=='low-dimensional':related=[s for s in C['selected'] if s['research_theme']=='low-dimensional']
  side=''.join(ext(s['url'],E(s['title'])+'<br><span class="side-year">'+E(s['journal_abbreviation'])+' · '+str(s['year'])+'</span>') for s in related)
  query={'transistors-3d':'transistor','low-dimensional':'nanotube','memory-neuromorphic':'memory','sensors':'sensor'}[r['id']]
  items+=f'''<section class="research-detail" id="{r['id']}"><div class="large-number">0{i+1}</div><div><h2>{E(r['title'])}</h2><p>{E(r['description'])}</p><div class="keywords">{''.join('<span>'+E(k)+'</span>' for k in r['keywords'])}</div></div><aside class="research-side"><div class="small-label">Related reading</div>{side}<a href="publications.html?q={query}" style="color:var(--red)">Explore related publications ↗</a></aside></section>'''
  if r['id']=='memory-neuromorphic':
   items+='''<figure class="research-visual"><img src="assets/research/memory-news2.jpg" alt="Cover artwork for all-solution-processed CNT floating-gate memories" loading="lazy"><figcaption><strong>Carbon nanotubes, from channels to charge storage.</strong>Metallic and semiconducting nanotubes serve different roles in an all-CNT floating-gate memory platform.<br><br><a href="https://doi.org/10.1021/acsanm.2c00851" target="_blank" rel="noopener noreferrer">Read the 2022 paper ↗</a><br><a href="credits.html">Cover image credit</a></figcaption></figure>'''
  if r['id']=='sensors':
   items+='''<figure class="research-visual"><img src="assets/research/biosensor.jpg" alt="Figure 1: silicon nanowire sensing element integrated with a MOSFET amplifier" loading="lazy"><figcaption><strong>Sensing with integrated amplification.</strong>A silicon nanowire–MOSFET hybrid structure connects a nanoscale sensing element to an electronic amplifier.<br><br><a href="https://www.nature.com/articles/srep12286" target="_blank" rel="noopener noreferrer">J. Lee et al., Scientific Reports (2015) ↗</a><br><a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener noreferrer">Figure 1 · CC BY 4.0</a></figcaption></figure>'''
 return '<div class="wrap content-bottom">'+page_intro('Research','Small devices. New possibilities.','Understanding materials, designing devices and connecting their behavior to integrated electronic systems.')+items+'</div>'
def publications():
 years=sorted({p['year'] for p in PUBS if p.get('year')},reverse=True)
 options=''.join(f'<option value="{y}">{y}</option>' for y in years)
 filters=f'''<div class="filters"><div class="filter-left"><div class="field"><label for="pub-search">Search publications</label><input id="pub-search" type="search" placeholder="Title, author or journal…" autocomplete="off"></div><div class="field"><label for="pub-year">Year</label><select id="pub-year"><option value="">All years</option>{options}</select></div><div class="field"><label for="pub-type">Type</label><select id="pub-type"><option value="">All types</option><option value="journal">Journal articles</option><option value="conference">Conference papers</option><option value="book_chapter">Book chapters</option></select></div><div class="field"><label for="pub-selected">Collection</label><select id="pub-selected"><option value="">Full list</option><option value="selected">Selected papers</option></select></div></div></div><div class="result-line"><span id="pub-count" role="status" aria-live="polite">{len(PUBS)} publications</span><div class="download-links"><button id="download-bib" type="button">Download BibTeX ↓</button><button id="download-csv" type="button">Download CSV ↓</button></div></div>'''
 rows=''.join(pubrow(p,p.get('selected',False),True) for p in PUBS)
 return '<div class="wrap content-bottom">'+page_intro('Publications','A record of our research.','Journal articles, conference contributions and book chapters, organized by year. Search the archive or explore selected papers.')+filters+'<div id="publication-list" class="catalog">'+rows+'</div><p class="empty" id="pub-empty" hidden>No matching publications. Try another keyword or year.</p><button class="load-more" id="pub-more" type="button" hidden>Show more publications ↓</button><p class="source-note">Bibliography compiled from <a href="https://silk.kookmin.ac.kr/myboard/sub3_1" target="_blank" rel="noopener noreferrer">S!LK</a> and <a href="'+E(P['scholar_url'])+'" target="_blank" rel="noopener noreferrer">Google Scholar</a>. Author identities and overlapping records have been reconciled. Updated September 2026.</p></div>'
def patents():
 pats=''
 for p in sorted(C['patents'],key=lambda p:p.get('date') or p.get('date_raw') or '',reverse=True):
  date=p.get('date_display') or p.get('date_raw') or ''
  year=str(date)[:4]
  number=p.get('registration_number') or p.get('publication_number') or p.get('application_number') or p.get('number_raw')
  source_status=p.get('status_en') or p.get('status_raw')
  country=p.get('country_en') or 'Republic of Korea'
  original_title=f'<p class="original-title" lang="ko">{E(p["title_ko"])}</p>' if p.get('title_ko') else ''
  details='Inventors: '+E(p.get('inventors_raw',''))+'<br>Applicant: '+E(p.get('applicant_ko',''))
  if p.get('related_domestic_numbers'):details+='<br>Related Korean filings: '+E(', '.join(p['related_domestic_numbers']))
  if p.get('notes'):details+='<br>'+E(' '.join(p['notes']))
  pats+=f'''<article class="achievement"><div class="record-year">{E(year)}</div><div><span class="label">{E(country)} · {E(source_status)}</span><h3>{E(p['title_en'])}</h3>{original_title}<div class="record-meta"><span>{E(number)}</span><span>{E(date)}</span>{ext(p['source_url'],'Record ↗')}</div><details class="record-details"><summary>Inventors & record details</summary><p>{details}</p></details></div></article>'''
 awards=''
 labels={'coauthored_paper_award':'Co-authored paper','student_team_award':'Student paper recognition','paper_recognition':'Paper highlight'}
 for a in C['awards']:
  category=a.get('category','')
  label=labels.get(category,'Paper recognition')
  paper_title=a.get('paper_title_short_en') or a.get('paper_title_en') or a.get('paper_title_raw','')
  awards+=f'''<article class="achievement"><div class="record-year">{E(a['year'])}</div><div><span class="label">{E(label)}</span><h3>{E(a['title_en'])}</h3><p class="original-title" lang="ko">{E(a['award_name_ko'])}</p><p class="record-details">{E(paper_title)}</p><details class="record-details"><summary>Authors & source</summary><p>{author_markup(a.get('authors_raw',''))}</p>{ext(a['source_url'],'View source record ↗')}</details></div></article>'''
 awards+='<p class="source-note"><a href="media.html#ieee-student-awards-2025">Recent student awards and team news ↗</a></p>'
 return '<div class="wrap content-bottom">'+page_intro('Innovation & recognition','Patents & awards.','Inventions, award-winning papers and recognition of collaborative research.')+'''<div class="tab-buttons" role="tablist" aria-label="Achievement type"><button id="tab-patents" role="tab" type="button" data-tab="patents" class="active" aria-selected="true" aria-controls="panel-patents">Patents</button><button id="tab-awards" role="tab" type="button" data-tab="awards" aria-selected="false" aria-controls="panel-awards">Paper awards & recognition</button></div>'''+f'''<section id="panel-patents" data-panel="patents" role="tabpanel" aria-labelledby="tab-patents"><p class="source-note" style="margin:0 0 16px">Korean titles are retained alongside short English descriptions. Korean records follow S!LK; U.S. records link to the published patent documents. Related national filings are listed separately, with patent-family connections noted in the record details.</p>{pats}</section><section id="panel-awards" data-panel="awards" role="tabpanel" aria-labelledby="tab-awards" hidden><p class="source-note" style="margin:0 0 16px">Recognition for co-authored papers and student research. The individual recipients and authors are credited in each source.</p>{awards}</section></div>'''
def team():
 cards=''.join(f'''<article class="person"><div class="person-photo"><img src="{E(t['photo'])}" alt="{E(t['display_name_en'])}" width="300" height="300" loading="lazy"></div><h2>{E(t['display_name_en'])}</h2><p class="name-ko" lang="ko">{E(t['name_ko'])}</p><p class="person-role">Graduate researcher</p></article>''' for t in C['team'])
 return '<div class="wrap content-bottom">'+page_intro('People','Our team.','Working together at the intersection of materials, semiconductor devices and integrated electronics.')+'''<p class="team-intro-rule">Current members of Sung-Jin Choi’s research team within the shared <a href="https://silk.kookmin.ac.kr/" target="_blank" rel="noopener noreferrer">S!LK laboratory ↗</a></p>'''+f'<div class="team-grid">{cards}</div><p class="people-caption">Portraits courtesy of S!LK. Current team: September 2026.</p></div>'
def media():
 cards=''
 for m in C['media']:
  links=''.join(ext(s['url'],E(s['publisher_ko'])+' ↗') for s in m['sources'])
  originals=''.join('<li lang="ko">'+E(s['title_ko'])+' · '+E(s['date'])+'</li>' for s in m['sources'])
  cards+=f'''<article class="media-item" id="{m['id']}" data-media-category="{E(m['category'])}"><div class="media-date">{E(m['date'])}<span>{E(m['category'])}</span></div><div><h2>{E(m['title_en'])}</h2><p>{E(m['summary_en'])}</p><div class="media-sources">{links}</div><details class="media-original"><summary>Original headline{('s' if len(m['sources'])>1 else '')} <span lang="ko">· 한국어</span></summary><ul>{originals}</ul></details></div></article>'''
 return '<div class="wrap content-bottom">'+page_intro('News & media','Research beyond the paper.','Selected coverage from the university and the press, with original articles and stories from our team.')+'''<div class="filters"><div class="field"><label for="media-type">Explore stories</label><select id="media-type"><option value="">All stories</option><option value="Research">Research</option><option value="Team news">Team news</option><option value="Recognition">Recognition</option></select></div><span class="section-label">University news & press coverage</span></div>'''+f'<div class="media-list">{cards}</div></div>'
def about():
 edu=''.join(f'<div class="timeline"><div class="date">{E(e["display_date"])}</div><div><h3>{E(e["degree"])} · {E(e["institution"])}</h3><p>{E(e["field"])}</p></div></div>' for e in P['education'])
 appt=''.join(f'<div class="timeline"><div class="date">{E(a["display_date"])}</div><div><h3>{E(a["institution"])}</h3><p>{E(a["role"])}</p></div></div>' for a in P['appointments'])
 co=P['contact']
 return '<div class="wrap content-bottom">'+page_intro('About','Sung-Jin Choi.','Professor · School of Electrical Engineering · Kookmin University')+f'''<section class="about-top"><div><div class="about-subtitle" lang="ko">최성진 · 국민대학교 전자공학부</div><p class="bio">{E(P['intro'])}</p><div class="profile-actions">{tl(P['scholar_url'],'Google Scholar')}<button id="print-profile" type="button">Print this profile ↓</button></div></div><figure><img src="assets/research/sung-jin-choi.jpg" width="280" height="335" alt="Sung-Jin Choi"><figcaption class="people-caption" style="margin-top:10px">Sung-Jin Choi · 최성진</figcaption></figure></section><div class="about-grid"><section><h2>Appointments</h2>{appt}<h2 style="margin-top:39px">Education</h2>{edu}</section><section><div class="contact-panel"><div class="eyebrow">Get in touch</div><h2 style="margin-top:18px">Contact</h2><a class="email" href="mailto:{E(co['email'])}">{E(co['email'])}</a><p style="margin-top:13px"><a href="tel:{E(co['phone'])}">{E(co['phone'])}</a></p><address>{E(co['office'])}<br>{E(co['address'])}</address><div style="margin-top:23px">{tl(P['lab']['url'],'S!LK laboratory')}</div></div><p class="source-note">Biography and contact: <a href="https://silk.kookmin.ac.kr/myboard/sub2_1" target="_blank" rel="noopener noreferrer">S!LK</a> · <a href="https://ee.kookmin.ac.kr/intro/professor" target="_blank" rel="noopener noreferrer">Kookmin faculty directory</a></p></section></div></div>'''
def selected_credits():
 rows=''
 for i,p in enumerate(C['selected'],start=1):
  figure_labels=[f['label'] for f in p.get('figures',[])]
  for key in ('main_figure','detail_figure','additional_figure'):
   f=C.get('hero',{}).get(key,{})
   if f.get('source_url')==p['url'] and f.get('label') and f['label'] not in figure_labels:
    figure_labels.append(f['label'])
  labels='; '.join(figure_labels)
  homepage_note=' Homepage excerpts are cropped for layout, with panel letters omitted.' if p['url']==C.get('hero',{}).get('source_url') else ''
  rows+=f'<article class="achievement"><div class="record-year">{i:02}</div><div><h3>{E(p["title"])}</h3><p class="record-details">{E(p["journal"])} ({E(p["year"])}). {E(labels)}. Original figure panels excerpted from the published paper.{homepage_note}</p><div class="record-meta">{ext(p["url"],"Published article ↗")}{ext(p["pdf_url"],"Author-hosted paper ↗")}</div></div></article>'
 return '<section class="section"><h2 style="font-size:30px;margin-bottom:25px">Selected-paper figures</h2>'+rows+'</section>'

def credits():
 return '<div class="wrap content-bottom">'+page_intro('Credits','Sources & images.','Research records and visual material are connected to their original sources.')+'''<div style="max-width:800px"><article class="achievement"><div class="record-year">01</div><div><h3>CNT memory cover artwork</h3><p class="record-details">ACS Applied Nano Materials, volume 5, issue 6 (2022), supplementary cover associated with Y. Lee et al., “All-Solution-Processed Carbon Nanotube Floating Gate Memories.” Artwork shown without altering the original image.</p><div class="record-meta"><a href="https://ee.kookmin.ac.kr/community/board/ee_news/276" target="_blank" rel="noopener noreferrer">Kookmin University cover story ↗</a><a href="https://doi.org/10.1021/acsanm.2c00851" target="_blank" rel="noopener noreferrer">Article ↗</a></div></div></article><article class="achievement"><div class="record-year">02</div><div><h3>Silicon nanowire biosensor</h3><p class="record-details">J. Lee et al., Scientific Reports 5, 12286 (2015), Figure 1. The original figure is reproduced without modification under the Creative Commons Attribution 4.0 International license.</p><div class="record-meta"><a href="https://www.nature.com/articles/srep12286" target="_blank" rel="noopener noreferrer">Original article ↗</a><a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener noreferrer">CC BY 4.0 ↗</a></div></div></article><article class="achievement"><div class="record-year">03</div><div><h3>Portraits</h3><p class="record-details">Faculty and student portraits from the S!LK laboratory website.</p><div class="record-meta"><a href="https://silk.kookmin.ac.kr/myboard/sub2_1" target="_blank" rel="noopener noreferrer">Faculty ↗</a><a href="https://silk.kookmin.ac.kr/myboard/sub2_2" target="_blank" rel="noopener noreferrer">Students ↗</a></div></div></article><article class="achievement"><div class="record-year">04</div><div><h3>Research records</h3><p class="record-details">Publication records draw on the S!LK bibliography and Google Scholar, with selected citations checked against publisher metadata. Patent and paper-recognition records retain Korean titles from S!LK. Each media entry links to the original article; English titles and summaries are editorial translations.</p></div></article></div></div>'''
write('index','Home',home())
write('research','Research',research())
write('publications','Publications',publications())
write('patents','Patents & Awards',patents())
write('team','Team',team())
write('media','Media',media())
write('about','About',about())
write('credits','Sources & Credits',credits()+'<div class="wrap">'+selected_credits()+'</div>')
(ROOT/'.nojekyll').write_text('',encoding='utf8')
(ROOT/'404.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found · Sung-Jin Choi</title><link rel="stylesheet" href="assets/style.css"><link rel="stylesheet" href="assets/sections.css"><main class="wrap"><div class="page-intro"><div class="eyebrow">404</div><h1>Page not found.</h1><p>The page may have moved.</p><p><a href="index.html" class="button">Return home ↗</a></p></div></main></html>',encoding='utf8')
print(json.dumps({'pages':8,'publications':len(PUBS),'team':len(C['team']),'patents':len(C['patents']),'awards':len(C['awards']),'media':len(C['media'])}))
