# Builds site/index.html for Don't Just Prompt It. Ship It. (online bootcamp, 27 Oct 2026, 9 AM PT).
# Cloned from the Build Club Brisbane deck; small labels above headings are stripped on purpose.
import os, sys, re, json, html as H_
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import perth_slides
css = open(f'{H}/base.css').read() + open(f'{H}/extra.css').read() + open(f'{H}/theme.css').read() + '''
.cmd{white-space:pre-wrap;text-align:left}
.pair{display:grid;gap:clamp(12px,1.6vw,28px);width:100%;margin-top:1.2rem;align-items:start}
.pair>div{display:flex;flex-direction:column;gap:.6rem;min-width:0}
.pair video{width:100%;max-height:60vh;border-radius:14px;background:#000;object-fit:contain}
.pair .t{font-weight:600;font-size:clamp(1rem,1.6vw,1.8rem)}
.pair .t em{font-style:normal;color:var(--accent)}
'''
PERTH = {perth_slides.label(s): s for s in perth_slides.load()}

C = 'dont-just-prompt-it-2026-10'
UTM = f'utm_source=luma&amp;utm_medium=event&amp;utm_campaign={C}'
PROMO = f'https://adal.sylph.ai/sign-up?redirect_url=%2Fsubscription%3Ftier%3Dpro%26billing_interval%3Dmonthly%26promo%3DSHIPIT1MO&amp;{UTM}&amp;utm_content=jax_slides_promo_1'
INSTALL = f'https://adalagent.ai/install?{UTM}&amp;utm_content=jax_slides_install_1'
LIBRARY = f'https://adalagent.ai/launch-library?{UTM}&amp;utm_content=jax_slides_launch_library_1'
DISCORD = 'https://discord.gg/tRnDmgqfct'
FORM = 'https://docs.google.com/forms/d/e/1FAIpQLSey1MnU7A-8iLWiucdOtUzUCrefLE-E7yw6WzAZwHhvlAZA6w/viewform'

S = []
def add(ag, sec): S.append((ag, sec))

def check(ag, n):
    add(ag, f'''<section class="slide check" data-cp="{n}" data-check="{n}">
    <div class="cpgrid">
      <div><h2 style="margin:1rem 0 1.6rem">Questions<em>?</em></h2><div class="qr"><img alt="Scan to ask" data-qr></div><div class="qurl" data-url></div></div>
      <div class="qlist" data-list="{n}"><div class="none">Scan to ask</div></div>
    </div>
  </section>''')

def part(ag, title, cp):
    add(ag, f'''<section class="slide check center" data-cp="{cp}">
    <h1 style="font-size:clamp(3rem,7.4vw,7.6rem)">{title}</h1>
  </section>''')

def prompt(ag, title, text, cp):
    add(ag, f'''<section class="slide" data-cp="{cp}">
    <h2 style="font-size:clamp(2rem,4.2vw,4.6rem)">{title}</h2>
    <div class="cmd" style="font-size:clamp(1rem,1.6vw,1.9rem);line-height:1.5;padding:1.4rem 1.6rem">{H_.escape(text)}</div>
  </section>''')

def qr(url, label, sub, size='clamp(200px,20vw,320px)'):
    return f'''<div style="display:flex;align-items:center;gap:clamp(20px,3vw,48px);margin-top:2.4rem">
      <a class="qr" href="{url}" target="_blank" rel="noopener" style="width:{size};display:block"><img alt="" data-qr="{url}"></a>
      <div><a class="when" href="{url}" target="_blank" rel="noopener" style="font-size:clamp(1.2rem,2.2vw,2.6rem);text-decoration:underline;text-underline-offset:6px">{label}</a><div style="margin-top:.8rem;font-size:clamp(1rem,1.6vw,1.8rem);color:var(--ink-50)">{sub}</div></div>
    </div>'''

def vid(name, title):
    return f'<div><video src="media/{name}.mp4" poster="media/{name}.jpg" controls playsinline preload="metadata"></video><div class="t">{title}</div></div>'

def pair(ag, title, cells, cp=2):
    add(ag, f'''<section class="slide" data-cp="{cp}">
    <h2 style="font-size:clamp(1.8rem,3.6vw,4rem)">{title}</h2>
    <div class="pair" style="grid-template-columns:repeat({len(cells)},1fr)">{''.join(cells)}</div>
  </section>''')

# ---------- title ----------
add('w', f'''<section class="slide" data-cp="1">
    <div class="two" style="grid-template-columns:1.2fr 1fr">
      <div>
        <h1>Don't just prompt it.<br><em>Ship it.</em></h1>
        <div class="when" style="margin-top:1.4rem;font-size:clamp(1.2rem,2.2vw,2.6rem)">Tue 27 Oct · 9:00 AM PT</div>
      </div>
      <img src="img/poster.png" alt="" style="width:100%;max-height:78vh;object-fit:contain;border-radius:18px;box-shadow:0 30px 60px -30px rgba(28,26,22,.6)">
    </div>
  </section>''')
add('w', f'''<section class="slide" data-cp="1">
    <h2>Before we <em>start</em></h2>
    <div class="steps">
      <div><span class="i">01</span><span class="t">Redeem SHIPIT1MO</span><span class="s">1 month of Pro</span></div>
      <div><span class="i">02</span><span class="t">Install AdaL Desktop</span><span class="s">adalagent.ai/install</span></div>
      <div><span class="i">03</span><span class="t">Open your product folder</span></div>
      <div><span class="i">04</span><span class="t">Say hi in Discord</span><span class="s">#🥷adal-online-hackathon</span></div>
    </div>
  </section>''')
add('w', f'''<section class="slide" data-cp="1">
    <h2>1 month of AdaL Pro, <em>free</em></h2>
    <div class="qrs" style="align-items:center">
      <div class="qr" style="width:clamp(200px,22vw,340px)"><img alt="" data-qr="{PROMO}"></div>
      <div class="grid g2" style="margin-top:0;min-width:44vw;justify-items:stretch;gap:1px">
        <div><span class="label">Code</span><div class="n" style="font-family:var(--mono);font-size:clamp(1.6rem,3.2vw,3.6rem)">SHIPIT1MO</div></div>
        <div><span class="label">Install</span><div class="n" style="font-size:clamp(1.2rem,2.2vw,2.6rem)">adalagent.ai/install</div></div>
      </div>
    </div>
  </section>''')

# ---------- Part 1 ----------
part('p1', 'Everyone builds.<br><em>Nobody ships.</em>', 1)
add('p1', PERTH['Building is cheap now'])
add('p1', '''<section class="slide" data-cp="1">
    <h2>GTM is <em>3 questions</em></h2>
    <div class="steps">
      <div><span class="i">01</span><span class="t">Do people want it?</span><span class="s">validate</span></div>
      <div><span class="i">02</span><span class="t">Can you market it well?</span><span class="s">sell</span></div>
      <div><span class="i">03</span><span class="t">Can it grow beyond your circle?</span><span class="s">scale</span></div>
    </div>
  </section>''')
add('p1', '''<section class="slide center" data-cp="1">
    <div class="grid g4" style="grid-template-columns:repeat(2,1fr);max-width:70vw">
      <div><span class="label">Video producer</span><div class="n">Weeks</div><div class="s">per launch video</div></div>
      <div><span class="label">AdaL</span><div class="n">20 min</div><div class="s">same launch quality</div></div>
    </div>
  </section>''')

# ---------- Part 2 ----------
part('p2', 'Your product at<br><em>their video grade</em>', 2)
add('p2', '''<section class="slide" data-cp="2">
    <h2>The <em>100</em></h2>
    <video class="vid" style="margin-top:.6rem;max-height:72vh;width:auto;max-width:100%" src="media/ll-launch-film.mp4" poster="media/ll-launch-film.jpg" controls playsinline preload="metadata"></video>
  </section>''')
pair('p2', 'Lovable <em>to AdaL</em>', [vid('ll-02-ref', 'Lovable original'), vid('ll-02-out', '<em>AdaL</em> style')])
pair('p2', 'Higgsfield <em>to AdaL</em>', [vid('ll-04-ref', 'Higgsfield original'), vid('ll-04-out', '<em>AdaL</em> style')])
pair('p2', 'OpenAI for law <em>to AdaL for work</em>', [vid('ll-05-ref', 'OpenAI original'), vid('ll-05-out', '<em>AdaL</em> style')])
pair('p2', 'Muse <em>to AdaL</em>', [vid('ll-10-ref', 'Muse original'), vid('ll-10-out', '<em>AdaL</em> style')])
add('p2', f'''<section class="slide" data-cp="2">
    <h2>Pick your <em>reference</em></h2>
    {qr(LIBRARY, 'adalagent.ai/launch-library', 'Every video, its prompts, its model')}
  </section>''')
prompt('p2', 'Prompt <em>1</em>', "Video: LINK\n\n(Use the video attached to this post itself, not videos from related posts on the page. Keep all your files in the folder XXXX.)\n\nreverse engineering this video, how can you use AdaL video producer capabilities to produce such videos, audios, and other types of the assets (including effects, fonts, transitions, animations)", 2)
prompt('p2', 'Prompt <em>2</em>', "ok replicate one using AdaL video producer from scratch", 2)
add('p2', '''<section class="slide center" data-cp="2">
    <h1 style="font-size:clamp(3rem,7vw,7.4rem)">Send prompt 1 <em>now</em></h1>
    <div class="when" style="margin-top:2rem;font-size:clamp(1rem,1.8vw,2rem);line-height:1.6">Post in #🔆hackathon-discussions:<br>which video, which model, a screenshot of your AdaL Desktop</div>
  </section>''')
# ---------- Part 3 (B2B, filled from the registrant research) ----------
part('p3', 'Apply it <em>today</em>', 3)
B2B = json.load(open(f'{H}/b2b.json')) if os.path.exists(f'{H}/b2b.json') else []
for b in B2B:
    cells = [vid(v['v'], v['t']) for v in b.get('videos', [])]
    if b.get('split'):
        cols = ''.join(f'<div><div class="t" style="font-weight:700;margin-bottom:.6rem">{c["label"]}</div><div class="pair" style="grid-template-columns:1fr 1fr">{"".join(vid(v["v"], v["t"]) for v in c["videos"])}</div></div>' for c in b['split'])
        tips = ''.join(f'<div><span class="i">{i+1:02d}</span><span class="t">{t}</span></div>' for i, t in enumerate(b['tips']))
        add('p3', f'<section class="slide" data-cp="3"><h2 style="font-size:clamp(1.8rem,3.6vw,4rem)">{b["title"]}</h2><div style="display:grid;grid-template-columns:1fr 1fr;gap:clamp(16px,2vw,32px)">{cols}</div><div class="steps tight" style="margin-top:1.2rem">{tips}</div></section>')
    elif cells:
        pair('p3', b['title'], cells, 3)
    else:
        steps = ''.join(f'<div><span class="i">{i+1:02d}</span><span class="t">{t}</span></div>' for i, t in enumerate(b['steps']))
        add('p3', f'<section class="slide" data-cp="3"><h2>{b["title"]}</h2><div class="steps">{steps}</div></section>')
add('p3', '''<section class="slide" data-cp="3">
    <h2>Same prompts. <em>Why AdaL style?</em></h2>
    <div class="steps">
      <div><span class="i">01</span><span class="t">Open AdaL in your product folder</span></div>
      <div><span class="i">02</span><span class="t">Product UI skill</span><span class="s">sharp at any zoom</span></div>
      <div><span class="i">03</span><span class="t">Your changelog</span><span class="s">one feature per video</span></div>
      <div><span class="i">04</span><span class="t">Social listening</span><span class="s">your competitors' hooks</span></div>
    </div>
  </section>''')
prompt('p3', 'Product UI <em>skill</em>', "Make a product UI skill for my app. Use browser use to open it (computer use if it's a desktop app), screenshot every main screen and read the real labels from my code. Then rebuild those screens in HTML so you can animate them for my demo videos. Save it as a skill.", 3)
add('p3', '''<section class="slide" data-cp="3">
    <h2>What makes it <em>slop</em></h2>
    <div class="steps">
      <div><span class="i">01</span><span class="t">No reference video</span></div>
      <div><span class="i">02</span><span class="t">A screen recording of your app</span></div>
      <div><span class="i">03</span><span class="t">Lots of tiny text</span></div>
      <div><span class="i">04</span><span class="t">Every feature at once</span></div>
    </div>
  </section>''')

POSTS = [('Desktop on every OS','15 Oct'),('AdaL Videos','16 Oct'),('Connectors','17 Oct'),('New models','18 Oct'),('Pin and rename chats','19 Oct'),('Drag and drop images','20 Oct'),('Windows and Linux','21 Oct'),('Off npm in 2 commands','23 Oct'),('Gemini 4 Argon, Muse, Music v2','26 Oct')]
cells = ''.join(f'<div><video src="media/post-{i+1}.mp4" poster="media/post-{i+1}.jpg" autoplay loop muted playsinline style="width:100%;aspect-ratio:16/10;object-fit:cover;border-radius:10px;border:1px solid var(--line);background:#fff"></video><div style="display:flex;justify-content:space-between;gap:8px;margin-top:4px;font-size:clamp(.7rem,.95vw,1.05rem)"><b>{t}</b><span style="color:var(--ink-50)">{d}</span></div></div>' for i,(t,d) in enumerate(POSTS))
add('p3', f'''<section class="slide" data-cp="3">
    <h2 style="font-size:clamp(1.8rem,3.6vw,4rem)">One feature <em>a day</em></h2>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(10px,1.4vw,24px);width:min(70vw,98vh);margin-top:1rem">{cells}</div>
  </section>''')
add('p3', f'''<section class="slide" data-cp="3">
    <h2 style="font-size:clamp(1.8rem,3.6vw,4rem)">The <em>recipe</em></h2>
    <div class="two" style="grid-template-columns:1.2fr 1fr;align-items:center">
      <div class="steps tight">
        <div><span class="i">01</span><span class="t">Product UI skill</span></div>
        <div><span class="i">02</span><span class="t">One feature, one video</span></div>
        <div><span class="i">03</span><span class="t">Queue it in a Google Sheet</span></div>
        <div><span class="i">04</span><span class="t">AdaL Schedule posts it daily</span></div>
      </div>
      {qr("https://docs.google.com/spreadsheets/d/1TXqwwCclq7N0J_gUkuA-DD6zPOHbDJWWcToFba1tmS4/edit", 'Open the example sheet', 'Queue + schedule prompt', 'clamp(150px,14vw,230px)')}
    </div>
  </section>''')

# ---------- Part 4 ----------
part('p4', 'Ship it <em>this week</em>', 3)
add('p4', f'''<section class="slide" data-cp="3">
    <h2>Post it, <em>get rewarded</em></h2>
    <div class="steps">
      <div><span class="i">01</span><span class="t">Post your video tagging @adalagent</span><span class="s">X or LinkedIn</span></div>
      <div><span class="i">02</span><span class="t">Drop the link in Discord</span><span class="s">#🥷adal-online-hackathon</span></div>
      <div><span class="i">03</span><span class="t">+1 month of AdaL Pro</span></div>
    </div>
    {qr(DISCORD, 'discord.gg/tRnDmgqfct', 'Join the hackathon chat', 'clamp(130px,12vw,200px)')}
  </section>''')
add('p4', f'''<section class="slide" data-cp="3">
    <h2>Hackathon · <em>Nov 2, 11:59 PM PT</em></h2>
    <div class="grid g4" style="grid-template-columns:repeat(3,1fr)">
      <div><span class="label">1st</span><div class="t">1 year of AdaL Pro</div><div class="s">Featured on AdaL channels</div></div>
      <div><span class="label">2nd</span><div class="t">6 months of Pro</div></div>
      <div><span class="label">3rd</span><div class="t">3 months of Pro</div></div>
    </div>
    {qr(FORM, 'Submit your project', 'Video in the launch library, post tagging AdaL', 'clamp(130px,12vw,200px)')}
  </section>''')
add('p4', '''<section class="slide center" data-cp="3">
    <h1>Thank <em>you</em></h1>
    <div class="org" style="margin-top:2rem;justify-content:center;gap:2rem"><img class="logo" src="img/logos/adal.svg" alt=""></div>
  </section>''')

# Strip any small label that sits right above a heading (Jax, 27 Oct 2026: reads as AI slop).
LABEL_ABOVE = re.compile(r'<div class="label">[^<]*(?:<[^/][^>]*>[^<]*</[^>]+>[^<]*)*</div>\s*(?=<h[12])')
FL = ['jump_2', 'jump_1', 'walk_t1', 'avatar_working_t1', 'jump_3']
IC = ['rocket', 'megaphone', 'clapper', 'trophy', 'bulb', 'laptop']
def fl(src, css, r=0):
    return f'<div class="fl" style="{css};--r:{r}deg"><img src="img/ll/{src}.webp" alt=""></div>'
out_s = []
for i, (ag, sec) in enumerate(S):
    sec = LABEL_ABOVE.sub('', sec)
    if ' check' in sec[:60]:
        f = fl(FL[i % 5], 'width:clamp(110px,11vw,190px);right:2.5vw;bottom:14vh', -6) + fl(IC[i % 6], 'width:clamp(60px,5.5vw,100px);left:2vw;bottom:8vh;animation-delay:-2s', 10)
    elif 'class="pair"' in sec:
        f = ''
    else:
        f = fl(IC[i % 6], 'width:clamp(46px,4vw,72px);right:6.5vw;bottom:2.5vh;animation-delay:-%ds' % (i % 5), 10)
    sec = sec.replace('>', '>' + f, 1).replace('<section ', f'<section data-ag="{ag}" ', 1)
    out_s.append(sec)

AGENDA = [('w', '09:00', '09:05', 'Welcome and setup'), ('p1', '09:05', '09:10', 'Everyone builds, nobody ships'),
          ('p2', '09:10', '09:30', 'Your product at their video grade'), ('p3', '09:30', '09:47', 'Apply it today'),
          ('p4', '09:47', '10:00', 'Hackathon, rewards, Q&A')]
agenda_html = '<aside class="ag" id="ag"><button class="ag-pill" id="agPill" type="button"><span class="ag-clock" id="agClock">--:--</span><span class="ag-now" id="agNow"></span><span class="ag-left" id="agLeft"></span></button><div class="ag-panel"><div class="label">Agenda · PT</div><ol id="agList"></ol></div></aside><script>window.AGENDA=' + json.dumps(AGENDA) + '</script>'

js = open(f'{H}/deck.js').read()
out = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ship It</title>
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<main id="deck" onclick="">
{chr(10).join(out_s)}
</main>
{agenda_html}
<div class="toasts" id="toasts"></div>
<div class="qrbar"><a class="slideqr dcqr" href="https://discord.gg/tRnDmgqfct" target="_blank" rel="noopener"><img alt="" src="https://api.qrserver.com/v1/create-qr-code/?size=600x600&amp;margin=0&amp;data=https%3A%2F%2Fdiscord.gg%2FtRnDmgqfct"><div><div class="t">Discord</div><div class="u">Google Docs inside</div></div></a><div class="slideqr"><img alt="" id="slideqr"><div><div class="t">Slides</div><div class="u" id="slideurl"></div><div class="count" id="count">1 / 1</div></div></div></div>
<div class="progress"><i id="bar"></i></div>
<script>{js}</script>
</body>
</html>'''
open(f'{H}/site/index.html', 'w').write(out)
left = len(re.findall(r'<div class="label">[^<]*</div>\s*<h[12]', out))
print(len(out_s), 'slides,', left, 'labels left above headings')
