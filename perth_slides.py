# Loads the Perth AI deck's slide list (without writing its site) so slides can be reused by label.
import re
P = '/Users/jaxkoh/adal/design/perth-ai-talk-2026-10-05'
def load():
    src = open(f'{P}/build.py').read().replace("os.path.dirname(os.path.abspath(__file__))", repr(P))
    src = src.split("js = open(")[0]
    ns = {}
    exec(src, ns)
    return ns['S']
def label(s):
    m = re.search(r'class="label">([^<]*)', s); return m.group(1) if m else ''
