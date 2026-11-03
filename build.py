#!/usr/bin/env python3
"""Build the BBMAC preview: Home, Lap Swim, About the Aquatics Complex, Masters Swimming, Youth Water Polo and Booking
the Pool, with every lap swim hour, Masters workout and closure read live from Pool Relay by finder.js (#today, #week,
data-live). Nothing about WHEN the pools are open is typed here; only rates, temperatures, policies and facts about
the water.
Run: python3 build.py"""
import hashlib, html, json

E = html.escape
V = {"bbmac": "vvrn1HWdluEYCLgwunF2nq"}  # Pool Relay share token: BBMAC, lane by lane
SITE = "https://bbmac.org/"
FACILITRON = "https://www.facilitron.com/bbmac92118"
POOLS = [
    dict(slug="bbmac", name="Brian Bent Memorial Aquatics Complex", short="BBMAC", facility="Brian Bent Memorial Aquatics Complex",
         area="Coronado", kind="yearRound", address="818 Sixth Street, Coronado, CA 92118", phone="(619) 437-0227", href="index.html"),
]

def live(mode, **kw):
    attrs = "".join(f' data-{k.replace("_", "-")}="{E(str(v))}"' for k, v in kw.items())
    return f'data-live="{mode}" data-view="{V["bbmac"]}" data-pool="bbmac"{attrs}'

MENU = [("About", None, 0), ("About the Aquatics Complex", "about.html", 1), ("About Brian Bent", None, 1), ("Pool Rules", None, 1),
        ("Programs", None, 0), ("Swim Lessons - Legacy Swim Academy", None, 1), ("Youth Swim", None, 1),
        ("Youth Water Polo", "youth-water-polo.html", 1), ("Masters Swimming", "masters.html", 1), ("Additional Programs", None, 1),
        ("Visiting Teams", None, 0), ("Booking the Pool", "booking.html", 1), ("Lap Swim", "lap-swim.html", 0), ("Family Swim", None, 0)]

VER = hashlib.sha1((open("finder.js").read() + open("style.css").read()).encode()).hexdigest()[:8]  # cache-busts both on change

def page(file, title, body, contact):
    menu = "".join(f'<a class="{"sub" if sub else ""}{" here" if href == file else ""}" href="{href or "#"}">{E(label)}</a>'
                   for label, href, sub in MENU)
    doc = f"""<!doctype html>
<!-- UNOFFICIAL PREVIEW. Not a Coronado Unified School District website. A mock-up of {SITE}
     with both BBMAC pools on one live Pool Relay schedule. -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{E(title)} | BBMAC preview</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;700&family=Oswald:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v={VER}">
</head>
<body>
<div class="preview-note"><b>Unofficial preview.</b> Not a Coronado Unified page &mdash; a mock-up of <a href="{SITE}" target="_blank" rel="noopener noreferrer">bbmac.org</a> with both pools on one live schedule.</div>
<header class="site"><div class="hdr">
  <a class="brand" href="index.html"><small>Brian Bent Memorial Aquatics Complex</small><span>BBMAC</span></a>
  <div class="right"><div class="util"><span>Coronado Unified School District</span><span>Translate</span><span>Search</span></div>
    <nav aria-label="Main"><span>Programs</span><span>Train With Us</span><span>Jobs</span><span>Donate</span><span>Directory</span></nav></div>
</div></header>
<div class="page">
  <aside class="side"><h2>BBMAC</h2><nav aria-label="BBMAC">{menu}</nav></aside>
  <main class="main"><h1>{E(title)}</h1>{body}</main>
  <aside class="contact"><h2>Contact</h2>{contact}</aside>
</div>
<footer class="site"><div class="in">
  <div><h4>BBMAC Brian Bent Memorial</h4><p>818 Sixth Street, Coronado, CA 92118<br>(619) 437-0227<br>info@bbmac.org</p></div>
  <div><h4>About this preview</h4><p>Built to demonstrate embedded <a href="https://www.poolrelay.com" target="_blank" rel="noopener">Pool Relay</a> schedules. Not operated by or affiliated with Coronado Unified School District. Schedule entered from BBMAC's November 2026 lap swim calendar and Coronado Masters Association's November notes on November 2, 2026; which lanes Masters uses is our estimate.</p></div>
</div></footer>
<script>window.POOLS = {json.dumps(POOLS)};</script>
<script src="finder.js?v={VER}"></script>
</body>
</html>
"""
    open(file, "w").write(doc)

CONTACT = """<p><b>BBMAC</b>818 Sixth Street<br>Coronado, CA 92118<br>(619) 437-0227</p>
<p><b>Email</b>info@bbmac.org</p>
<p><b>Aquatics Director</b>Brianna Englehart<br>brianna.englehart@coronadousd.net</p>
<p><b>Parking</b>Free street parking all around the facility.</p>"""

WEEK = f'<div id="week" data-view="{V["bbmac"]}" data-pool="bbmac" data-pools="Competition Pool|Instructional Pool"><p class="muted">Loading the week…</p></div>'
LANES = (f'<div class="frame"><iframe src="https://www.poolrelay.com/embed/{V["bbmac"]}" height="820" '
         f'title="BBMAC, lane by lane" loading="lazy"></iframe></div>')

# ── Home ─────────────────────────────────────────────────────────────────────
page("index.html", "Brian Bent Memorial Aquatics Complex", f"""
    <p class="lede">Coronado Unified's aquatics complex beside Coronado High School: an Olympic-size competition pool set up long course or
      short course, and a warm six-lane instructional pool. Lap swim, Masters, youth swim and water polo clubs, swim lessons, Coronado High
      teams and visiting teams all share the water. Every time on these pages comes from the pools' live schedule, so when BBMAC changes it,
      these pages change with it.</p>
    <div class="top2">
      <section class="now" aria-live="polite"><h2>Right now</h2>
        <div id="today" data-view="{V['bbmac']}" data-pool="bbmac"><p class="muted">Loading today’s schedule…</p></div></section>
      <aside class="hours"><h2>Lap swim this week</h2>
        <div {live("hours", format="dl", title="Lap Swim (Short Course)|Lap Swim (Long Course)|Lap Swim (Instructional Pool)", whole=0)}><p class="muted">…</p></div>
        <div class="adjusted" {live("closures")} hidden></div>
        <p class="small muted" style="margin:6px 0 0">Details and rates on <a href="lap-swim.html">Lap Swim</a>.</p>
      </aside>
    </div>
    <h2>This week, pool by pool</h2>
    {WEEK}
    <h2>Lane by lane</h2>
    <p class="small muted">Pick a day to see who is in each lane, and whether the competition pool is set up long course or short course.</p>
    {LANES}

    <div class="replaces">
      <h2>What this replaces</h2>
      <ul>
        <li><b>A PDF calendar every month, revised mid-month.</b> Lap swim lives in monthly PDFs ("October 2026 - Revised"), so a change means
          re-making and re-posting the file. Here the staff change the schedule once and every page follows.</li>
        <li><b>"*Revised - Comp Pool - lap swim open 10am-2pm."</b> The Lap Swim page carries a revision note without saying which day it means.
          Here the change is on the day it applies, in the pool it applies to.</li>
        <li><b>"Hours can fluctuate based on rental needs and events on a day by day basis."</b> Rentals, meets and tournaments aren't on the
          calendar, so swimmers can't tell which lanes are left. Here every booking holds its lanes, and lap swim shows what is really open.</li>
        <li><b>Long course or short course?</b> The calendar says LC or SC in each day's box. Here the lane-by-lane view shows the pool the way
          it is set up that day.</li>
        <li><b>Masters and clubs on their own websites.</b> Coronado Masters, Different Strokes, five youth water polo clubs and Sea to Desert
          each post their own times, and BBMAC's pages send you off to find them. Here they can be one schedule.</li>
        <li><b>Visiting teams booking blind.</b> Teams request water through Facilitron without seeing what's already booked. Here the
          lane-by-lane calendar shows the open water first.</li>
      </ul>
    </div>
""", CONTACT)

# ── Lap Swim ─────────────────────────────────────────────────────────────────
page("lap-swim.html", "Lap Swim", f"""
    <p class="lede">Adult lap swim in both pools. Please sign in and/or pay when you arrive: the sign-in sheets are at the front window, and
      signing is also the participant liability waiver. For a drop-in or a punch pass, see a lifeguard in the office or on deck.</p>
    <div class="top2">
      <aside class="hours"><h2>Competition pool</h2>
        <div {live("hours", format="dl", title="Lap Swim (Short Course)|Lap Swim (Long Course)", whole=0)}><p class="muted">…</p></div>
        <div class="adjusted" {live("exceptions", title="Lap Swim (Short Course)|Lap Swim (Long Course)")} hidden></div>
      </aside>
      <aside class="hours"><h2>Instructional pool</h2>
        <div {live("hours", format="dl", title="Lap Swim (Instructional Pool)", whole=0)}><p class="muted">…</p></div>
        <div class="adjusted" {live("exceptions", title="Lap Swim (Instructional Pool)")} hidden></div>
      </aside>
    </div>
    <div class="adjusted" {live("closures")} hidden></div>
    <h2>Rates</h2>
    <p class="small muted" style="margin-top:0">As of July 1, 2025</p>
    <div class="tblwrap"><table class="prog">
      <tr><th>Drop-in</th><td>$10 per person</td></tr>
      <tr><th>Punch pass, 10 swims</th><td>$70</td></tr>
      <tr><th>Punch pass, 30 swims</th><td>$150</td></tr>
      <tr><th>Annual pass</th><td>$600 per person</td></tr>
    </table></div>
    <p class="small">To buy a pass ahead of time, email info@bbmac.org. The competition pool is kept at 79–80°F and the instructional pool at
      85–86°F. Priority goes to CUSD programs and contracted groups, so lanes may be limited.</p>
    <h2>Lane by lane</h2>
    <p class="small muted">Who else is in the water during lap swim, and how many lanes are left.</p>
    {LANES}
""", CONTACT)

# ── About the Aquatics Complex ───────────────────────────────────────────────
page("about.html", "About the Aquatics Complex", f"""
    <p class="lede">The BBMAC facility is versatile, allowing us to accommodate the specific needs of our patrons.</p>
    <div class="facts">
      <div><h3>Competition pool</h3><ul><li>Olympic size</li><li>Long course: eight 50-meter lanes</li><li>Short course: 20 × 25-yard lanes</li>
        <li>Two full-size water polo courses</li><li>7 ft 0 in deep throughout</li><li>79–80°F</li></ul></div>
      <div><h3>Instructional pool</h3><ul><li>25 yards, six lanes</li><li>3 ft 6 in to 5 ft 6 in deep</li><li>86–89°F, for children's swim lessons and water therapy</li>
        <li>Handicap lift available</li></ul></div>
    </div>
    <p>Each combined restroom/locker room has two showers and lockers for day use; locks are not provided. A family restroom and several
      outdoor heated showers are available.</p>
    <h2>Cross training</h2>
    <p>BBMAC has direct access to a weight room and to Coronado High School's track-and-field facilities. Coronado also offers ocean and bay
      swimming, and bike, kayak and stand-up paddleboard rentals.</p>
    <h2>This week, pool by pool</h2>
    {WEEK}
    <h2>Lane by lane</h2>
    {LANES}
""", CONTACT)

# ── Masters Swimming ─────────────────────────────────────────────────────────
page("masters.html", "Masters Swimming", f"""
    <p class="lede">Two U.S. Masters Swimming clubs train at BBMAC.</p>
    <h2>Coronado Masters Association</h2>
    <p>Coached workouts in the 25-yard competition pool. CMA's rental contract with BBMAC requires USMS membership.
      <a href="https://www.swimcma.org/" target="_blank" rel="noopener">swimcma.org</a></p>
    <div class="tblwrap"><table class="prog">
      <tr><th>Workouts</th><td class="when" {live("when", title="Coronado Masters", gap=-1)}>…</td></tr>
    </table></div>
    <div class="adjusted" {live("exceptions", title="Coronado Masters")} hidden></div>
    <h2>Different Strokes Swim Team</h2>
    <p>San Diego's supportive and welcoming USMS club benefiting the LGBTQIA+ community, open to swimmers 18+ of all levels who can swim one
      length of a 25-yard pool, with a one-month free trial. DSST practices at locations across greater San Diego, including BBMAC; see
      <a href="https://dsst.org/calendar" target="_blank" rel="noopener">dsst.org</a> for current days and times. Membership questions:
      membership@dsst.org.</p>
    <p class="small muted">DSST's BBMAC practices can go on this schedule too, so swimmers see them next to lap swim.</p>
""", CONTACT)

# ── Youth Water Polo ─────────────────────────────────────────────────────────
CLUBS = [("Coronado Aquatics Club", "https://nadopolo.com/", "nadopolo.com"),
         ("Crown City Water Polo", "https://crowncitypolo.com/", "crowncitypolo.com"),
         ("Primo Polo Aquatics", "https://www.primopoloaquatics.com/", "primopoloaquatics.com"),
         ("Rogue 619 Water Polo Club", "https://sites.google.com/view/rogue619waterpolo/home", "sites.google.com/view/rogue619waterpolo"),
         ("San Diego Shores", "https://sdshores.org/", "sdshores.org")]
clubs = "".join(f'<div class="card"><h3>{E(n)}</h3><p class="small"><a href="{u}" target="_blank" rel="noopener">{E(t)}</a></p></div>' for n, u, t in CLUBS)
page("youth-water-polo.html", "Youth Water Polo", f"""
    <p class="lede">Five youth water polo clubs train at BBMAC, and the competition pool hosts tournaments and CIF playoff games on its two
      full-size courses.</p>
    <div class="cards">{clubs}</div>
    <h2>Games and tournaments</h2>
    <p class="small muted" style="margin-top:0">From the live schedule.</p>
    <div {live("dates", group="CIF San Diego Section boys wapo, 2026", show_title="", empty="No games in the next four weeks")}>…</div>
    <div class="adjusted" {live("closures", label="Pool closed")} hidden></div>
    <p class="small muted">Club practice times can go on this schedule too, so families see every club's water in one place.</p>
""", CONTACT)

# ── Booking the Pool ─────────────────────────────────────────────────────────
page("booking.html", "Booking the Pool", f"""
    <p class="lede">Whether your team or organization needs just a few lanes or the entire pool, BBMAC is happy to work with you. BBMAC has
      hosted water polo tournaments, swim meets, fitness competitions and end-of-year pool parties.</p>
    <h2>Check what's open</h2>
    <p class="small muted" style="margin-top:0">Every booking holds its lanes, so the empty water below is what's available.</p>
    {LANES}
    <h2>Booking through Facilitron</h2>
    <p>Request water on <a href="{FACILITRON}" target="_blank" rel="noopener">facilitron.com/bbmac92118</a> or ask the Aquatics Director,
      Brianna Englehart (brianna.englehart@coronadousd.net), for a quote. Facilitron sets up organization and user accounts, verifies
      non-profit status if applicable, and collects payment and insurance certificates on Coronado Unified's behalf. Facilitron support:
      support@facilitron.com, 800-272-2962 ext 1.</p>
""", CONTACT)
print("built 6 pages, assets", VER)
