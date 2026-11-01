import importlib.util, time, re, html, sys
spec = importlib.util.spec_from_loader("cs", loader=None)
import types
m = types.ModuleType("cs"); m.__file__ = "claudex-sessions"
exec(open("claudex-sessions").read().split('if __name__ == "__main__"')[0], m.__dict__)

now = int(time.time()*1000)
def S(name, cwd, ago_s, status="idle", pid=None, user=True, ai=None):
    d = {"sessionId": name if not user else "x", "cwd": cwd, "status": status, "pid": pid,
         "alive": pid is not None, "updatedAt": now - ago_s*1000,
         "name": name, "nameSource": "user" if user else "ai", "aiTitle": ai}
    if not user:
        d["sessionId"] = name; d["name"] = ai
    return d
H = "~/code"
rows = [
 S("api-refactor",      f"{H}/backend",              9,     "busy", 48213),
 S("payments-webhooks", f"{H}/backend",              3*3600,"idle", 51907),
 S("landing-page",      f"{H}/website",              5*3600,"idle", 52288),
 S("3f9a2c1d", f"{H}/backend", 19*3600, user=False, ai="Add rate limiting to API"),
 S("infra-terraform",   f"{H}/infra",                22*3600),
 S("b7e0d4a9", f"{H}/mobile-app", 2*86400, user=False, ai="Fix crash on login screen"),
 S("release-2.4",       f"{H}/backend",              2*86400),
 S("c12e88f0", f"{H}/website", 3*86400, user=False, ai="Migrate blog to MDX"),
 S("data-pipeline",     f"{H}/analytics/etl",        4*86400),
 S("d4c7b1e2", f"{H}/analytics/notebooks", 4*86400, user=False, ai="Weekly retention cohort analysis dashboard"),
 S("e9a1f3c5", "~", 5*86400, user=False, ai="Set up AWS CLI"),
 S("f0b2d6a8", f"{H}/backend", 7*86400, user=False, ai="Investigate slow Postgres query on orders"),
 S("a3d5e7f9", f"{H}/mobile-app", 9*86400, user=False, ai="Add dark mode support"),
 S("onboarding-docs",   f"{H}/docs",                 12*86400),
 S("b8c0d2e4", f"{H}/infra", 14*86400, user=False, ai="Rotate Kubernetes secrets"),
 S("c5e7a9b1", f"{H}/website", 18*86400, user=False, ai="Fix Lighthouse accessibility warnings"),
]
width = 112
lines = [f"{m.CYAN}❯{m.RESET} {m.DIM}▏{m.RESET}  {m.DIM}{len(rows)}/{len(rows)}{m.RESET}"]
for i, d in enumerate(rows):
    lines.append(m.row(d, width, selected=(i == 0)))

def ansi_to_html(s):
    out, open_ = [], []
    css = {"1":"b","2":"dim","7":"sel","32":"green","33":"yellow","36":"cyan","31":"red","35":"magenta"}
    pos = 0
    for mt in re.finditer(r"\x1b\[([0-9;]*)m", s):
        out.append(html.escape(s[pos:mt.start()])); pos = mt.end()
        for code in (mt.group(1) or "0").split(";"):
            if code == "0":
                out.append("</span>"*len(open_)); open_.clear()
            elif code in css:
                out.append(f'<span class="{css[code]}">'); open_.append(code)
    out.append(html.escape(s[pos:])); out.append("</span>"*len(open_))
    return "".join(out)

body = "\n".join(ansi_to_html(l) for l in lines)
prompt = '<span class="cyan b">➜</span> <span class="b">~</span> <span class="green b">cs</span>'
open(sys.argv[1], "w").write(f"""<!doctype html><meta charset=utf-8><style>
body{{margin:0;background:#1e1f22;}}
.win{{width:{width*8.43+40}px;background:#1e1f22;border-radius:10px;padding:0 0 14px;font:14px/1.5 Menlo,monospace;color:#d8d8d8;overflow:hidden}}
.bar{{height:36px;display:flex;align-items:center;padding-left:14px;gap:8px;background:#2b2c30}}
.bar i{{width:12px;height:12px;border-radius:50%;display:inline-block}}
pre{{margin:12px 20px 0;font:inherit;white-space:pre}}
.b{{font-weight:bold;color:#fff}} .dim{{color:#8a8d93}} .green{{color:#5fd75f}} .yellow{{color:#f0c674}} .cyan{{color:#5fd7ff}}
.sel{{background:#e8e8e8;color:#1e1f22;font-weight:bold}}
</style><div class=win><div class=bar><i style=background:#ff5f57></i><i style=background:#febc2e></i><i style=background:#28c840></i></div>
<pre>{prompt}
{body}</pre></div>""")
