"""Render the 1024x1024 Sunday 22 November 2026 world news broadsheet to entry.png."""

from pathlib import Path
from playwright.sync_api import sync_playwright

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body {
    width: 1024px;
    height: 1024px;
    overflow: hidden;
    background: #F5F1E8;
    color: #111827;
    font-family: "Segoe UI", Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
  }
  .page {
    width: 1024px;
    height: 1024px;
    padding: 10px 12px 8px 12px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    background: #F5F1E8;
  }
  /* MASTHEAD */
  .masthead {
    height: 84px;
    background: #0F172A;
    border-radius: 6px;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 4px solid #D97706;
  }
  .mast-left {
    display: flex;
    flex-direction: column;
    gap: 3px;
  }
  .mast-kicker {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .date-pill {
    background: #F59E0B;
    color: #0F172A;
    font-weight: 800;
    font-size: 12px;
    letter-spacing: 0.8px;
    padding: 2px 8px;
    border-radius: 3px;
    text-transform: uppercase;
  }
  .sub-kicker {
    color: #CBD5E1;
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  .mast-title {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 32px;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: 0.3px;
    line-height: 1.08;
  }
  .mast-right {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .mast-stats {
    text-align: right;
    color: #E2E8F0;
    font-size: 11px;
    line-height: 1.35;
    font-weight: 600;
  }
  .mast-stats strong {
    color: #FBBF24;
    font-size: 13px;
    display: block;
  }

  /* HERO TRIO */
  .hero-row {
    height: 234px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
  }
  .hero-card {
    background: #FFFFFF;
    border: 1.5px solid #CBD5E1;
    border-radius: 6px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }
  .hero-tag {
    height: 21px;
    padding: 0 9px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: #FFFFFF;
    font-size: 10.5px;
    font-weight: 800;
    letter-spacing: 0.6px;
    text-transform: uppercase;
  }
  .hero-art {
    height: 104px;
    width: 100%;
    border-bottom: 1px solid #E2E8F0;
  }
  .hero-body {
    padding: 7px 10px 8px 10px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    flex: 1;
  }
  .hero-title {
    font-size: 14px;
    font-weight: 800;
    line-height: 1.18;
    color: #0F172A;
  }
  .hero-desc {
    font-size: 11.2px;
    line-height: 1.28;
    color: #334155;
  }

  /* MIDDLE BAND: MAP + SPOTLIGHTS */
  .mid-row {
    height: 184px;
    display: grid;
    grid-template-columns: 492px 1fr;
    gap: 10px;
  }
  .map-card {
    background: #FFFFFF;
    border: 1.5px solid #CBD5E1;
    border-radius: 6px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }
  .map-header {
    height: 20px;
    background: #1E293B;
    color: #F8FAFC;
    padding: 0 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.6px;
    text-transform: uppercase;
  }
  .map-svg-wrap {
    flex: 1;
    position: relative;
    background: #DCEEF8;
  }
  .map-legend {
    height: 19px;
    background: #F8FAFC;
    border-top: 1px solid #E2E8F0;
    padding: 0 8px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 9.8px;
    font-weight: 700;
    color: #334155;
  }
  .leg-item {
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }
  .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
  }

  .spotlights {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .spot-card {
    flex: 1;
    background: #FFFFFF;
    border: 1.5px solid #CBD5E1;
    border-radius: 6px;
    padding: 7px 10px;
    display: flex;
    gap: 10px;
    align-items: center;
  }
  .spot-art {
    width: 78px;
    height: 70px;
    flex-shrink: 0;
    border-radius: 4px;
    overflow: hidden;
    border: 1px solid #E2E8F0;
  }
  .spot-text {
    display: flex;
    flex-direction: column;
    gap: 2.5px;
  }
  .spot-kicker {
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.6px;
    text-transform: uppercase;
  }
  .spot-title {
    font-size: 13.5px;
    font-weight: 800;
    line-height: 1.15;
    color: #0F172A;
  }
  .spot-desc {
    font-size: 11px;
    line-height: 1.25;
    color: #334155;
  }

  /* LOWER 6-REGION GRID */
  .grid-6 {
    flex: 1;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(2, 1fr);
    gap: 8px 10px;
  }
  .region-card {
    background: #FFFFFF;
    border: 1.5px solid #CBD5E1;
    border-radius: 6px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }
  .region-hdr {
    height: 22px;
    padding: 0 9px;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 10.5px;
    font-weight: 800;
    letter-spacing: 0.4px;
    text-transform: uppercase;
    white-space: nowrap;
  }
  .region-hdr span:last-child {
    font-size: 9.5px;
    font-weight: 700;
    opacity: 0.92;
  }
  .region-list {
    padding: 6px 9px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    flex: 1;
    gap: 4px;
  }
  .news-item {
    display: flex;
    gap: 6px;
    align-items: flex-start;
    font-size: 11.1px;
    line-height: 1.24;
    color: #1E293B;
  }
  .bullet {
    width: 6px;
    height: 6px;
    border-radius: 2px;
    margin-top: 4px;
    flex-shrink: 0;
  }
  .news-item strong {
    color: #0F172A;
    font-weight: 800;
  }

  /* FOOTER */
  .footer {
    height: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 9.8px;
    font-weight: 700;
    color: #475569;
    padding: 0 2px;
  }
</style>
</head>
<body>
<div class="page">

  <!-- MASTHEAD -->
  <header class="masthead">
    <div class="mast-left">
      <div class="mast-kicker">
        <span class="date-pill">Sunday · 22 November 2026</span>
        <span class="sub-kicker">Global Daily Edition · World News in One Image</span>
      </div>
      <div class="mast-title">THE WORLD ON 22 NOVEMBER 2026</div>
    </div>
    <div class="mast-right">
      <div class="mast-stats">
        <strong>35 VERIFIED STORIES</strong>
        6 Continents · Politics, War, Climate,<br/>Space, Markets &amp; Global Sport
      </div>
      <svg width="54" height="54" viewBox="0 0 54 54">
        <circle cx="27" cy="27" r="24" fill="#1E293B" stroke="#F59E0B" stroke-width="2.2"/>
        <ellipse cx="27" cy="27" rx="12" ry="24" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.8"/>
        <line x1="3" y1="27" x2="51" y2="27" stroke="#38BDF8" stroke-width="1.2" opacity="0.8"/>
        <path d="M7 16 Q27 21 47 16" fill="none" stroke="#38BDF8" stroke-width="1" opacity="0.7"/>
        <path d="M7 38 Q27 33 47 38" fill="none" stroke="#38BDF8" stroke-width="1" opacity="0.7"/>
        <path d="M13 18 L20 15 L23 22 L17 28 L12 24 Z" fill="#10B981" opacity="0.85"/>
        <path d="M28 14 L38 16 L41 24 L35 31 L27 26 Z" fill="#10B981" opacity="0.85"/>
        <circle cx="42" cy="12" r="4" fill="#EF4444"/>
      </svg>
    </div>
  </header>

  <!-- HERO TRIO -->
  <section class="hero-row">
    <!-- HERO 1: COP31 -->
    <article class="hero-card">
      <div class="hero-tag" style="background:#0F766E;">
        <span>Climate · Antalya, Turkey</span>
        <span>22 Nov 2026</span>
      </div>
      <svg class="hero-art" viewBox="0 0 320 104">
        <defs>
          <linearGradient id="sky1" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#0F172A"/>
            <stop offset="100%" stop-color="#134E4A"/>
          </linearGradient>
        </defs>
        <rect width="320" height="104" fill="url(#sky1)"/>
        <!-- Broken Earth / Summit Dome -->
        <circle cx="95" cy="56" r="34" fill="#0EA5E9" opacity="0.9"/>
        <path d="M72 42 Q85 33 96 46 Q107 52 98 66 Q82 70 74 56 Z" fill="#22C55E"/>
        <path d="M106 34 Q118 42 115 58 Q106 54 106 34 Z" fill="#22C55E"/>
        <!-- Crack lightning -->
        <polyline points="96,18 90,42 101,56 91,76 97,94" fill="none" stroke="#FEF08A" stroke-width="3"/>
        <!-- Oil Barrel -->
        <rect x="172" y="42" width="38" height="48" rx="4" fill="#334155" stroke="#94A3B8" stroke-width="1.5"/>
        <line x1="172" y1="56" x2="210" y2="56" stroke="#94A3B8" stroke-width="1.5"/>
        <line x1="172" y1="74" x2="210" y2="74" stroke="#94A3B8" stroke-width="1.5"/>
        <text x="191" y="69" text-anchor="middle" fill="#F8FAFC" font-size="9" font-weight="800">OIL</text>
        <!-- Draft Treaty + NO DEAL stamp -->
        <rect x="234" y="22" width="66" height="68" rx="3" fill="#F8FAFC"/>
        <line x1="242" y1="35" x2="290" y2="35" stroke="#94A3B8" stroke-width="2"/>
        <line x1="242" y1="45" x2="285" y2="45" stroke="#94A3B8" stroke-width="2"/>
        <line x1="242" y1="55" x2="288" y2="55" stroke="#94A3B8" stroke-width="2"/>
        <rect x="230" y="56" width="74" height="20" rx="2" fill="#DC2626" transform="rotate(-12 267 66)"/>
        <text x="267" y="70" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="900" transform="rotate(-12 267 66)">NO DEAL</text>
        <text x="160" y="16" text-anchor="middle" fill="#5EEAD4" font-size="10" font-weight="800" letter-spacing="1">UN COP31 DEADLOCK</text>
      </svg>
      <div class="hero-body">
        <div class="hero-title">COP31 Climate Summit Collapses in Antalya</div>
        <div class="hero-desc">Overtime talks of ~200 nations end with no consensus pact; EU &amp; island bloc reject text omitting fossil-fuel phaseout—1st COP failure since 2009.</div>
      </div>
    </article>

    <!-- HERO 2: BENGHAZI MERKURY -->
    <article class="hero-card">
      <div class="hero-tag" style="background:#B91C1C;">
        <span>Conflict · Libya &amp; Ukraine</span>
        <span>22 Nov 2026</span>
      </div>
      <svg class="hero-art" viewBox="0 0 320 104">
        <defs>
          <linearGradient id="sky2" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#1E1B4B"/>
            <stop offset="100%" stop-color="#7F1D1D"/>
          </linearGradient>
        </defs>
        <rect width="320" height="72" fill="url(#sky2)"/>
        <rect y="72" width="320" height="32" fill="#0369A1"/>
        <!-- Smoke & explosion -->
        <circle cx="176" cy="40" r="22" fill="#EA580C" opacity="0.85"/>
        <circle cx="186" cy="28" r="14" fill="#FACC15" opacity="0.85"/>
        <circle cx="162" cy="24" r="16" fill="#475569" opacity="0.75"/>
        <!-- Tilted Russian Corvette Merkury -->
        <g transform="rotate(-14 175 68)">
          <polygon points="110,64 240,64 226,80 124,80" fill="#334155" stroke="#CBD5E1" stroke-width="1"/>
          <rect x="148" y="48" width="46" height="16" fill="#475569"/>
          <rect x="166" y="34" width="8" height="14" fill="#64748B"/>
          <text x="175" y="75" text-anchor="middle" fill="#FCA5A5" font-size="8" font-weight="800">MERKURY</text>
        </g>
        <!-- Naval Drone USV -->
        <polygon points="34,82 78,80 86,86 38,88" fill="#E2E8F0"/>
        <path d="M12 86 Q24 81 36 86" fill="none" stroke="#BAE6FD" stroke-width="2"/>
        <!-- Waves -->
        <path d="M0 78 Q40 73 80 78 T160 78 T240 78 T320 78" fill="none" stroke="#38BDF8" stroke-width="1.5"/>
        <text x="160" y="15" text-anchor="middle" fill="#FECACA" font-size="10" font-weight="800" letter-spacing="0.8">BENGHAZI PORT STRIKE</text>
      </svg>
      <div class="hero-body">
        <div class="hero-title">Sea Drones Sink Russian Corvette in Libya</div>
        <div class="hero-desc">Ukraine confirms naval drones capsized Russian warship <b>Merkury</b> &amp; hit cargo ship <b>Ascalon</b> at Benghazi; Russian drones strike Kyiv apartments.</div>
      </div>
    </article>

    <!-- HERO 3: SPACE -->
    <article class="hero-card">
      <div class="hero-tag" style="background:#3730A3;">
        <span>Space · Vandenberg &amp; Mercury</span>
        <span>22 Nov 2026</span>
      </div>
      <svg class="hero-art" viewBox="0 0 320 104">
        <rect width="320" height="104" fill="#0B1120"/>
        <circle cx="40" cy="22" r="1.2" fill="#FFF"/><circle cx="110" cy="18" r="1" fill="#FFF"/>
        <circle cx="145" cy="40" r="1.3" fill="#FFF"/><circle cx="290" cy="22" r="1.2" fill="#FFF"/>
        <circle cx="205" cy="16" r="1" fill="#FFF"/>
        <!-- Falcon 9 launch -->
        <polygon points="68,68 78,68 82,102 64,102" fill="#F97316"/>
        <polygon points="71,72 75,72 77,98 69,98" fill="#FEF08A"/>
        <rect x="69" y="24" width="8" height="44" rx="2" fill="#F8FAFC"/>
        <polygon points="69,24 73,13 77,24" fill="#E2E8F0"/>
        <rect x="67" y="59" width="12" height="4" fill="#334155"/>
        <text x="108" y="36" fill="#93C5FD" font-size="9.5" font-weight="800">NROL-136</text>
        <text x="108" y="48" fill="#CBD5E1" font-size="8.5" font-weight="700">32h Pad Record</text>
        <!-- Divider -->
        <line x1="176" y1="12" x2="176" y2="94" stroke="#334155" stroke-dasharray="3,3"/>
        <!-- Mercury + BepiColombo -->
        <circle cx="248" cy="58" r="28" fill="#94A3B8"/>
        <circle cx="238" cy="48" r="5" fill="#64748B"/><circle cx="258" cy="64" r="7" fill="#64748B"/>
        <circle cx="256" cy="45" r="3.5" fill="#64748B"/>
        <ellipse cx="248" cy="58" rx="44" ry="15" fill="none" stroke="#38BDF8" stroke-width="1.3" stroke-dasharray="3,2" transform="rotate(-18 248 58)"/>
        <rect x="206" y="44" width="10" height="6" fill="#FBBF24"/>
        <rect x="197" y="45" width="9" height="4" fill="#3B82F6"/>
        <rect x="216" y="45" width="9" height="4" fill="#3B82F6"/>
        <text x="248" y="16" text-anchor="middle" fill="#C7D2FE" font-size="9.5" font-weight="800">BEPICOLOMBO</text>
      </svg>
      <div class="hero-body">
        <div class="hero-title">SpaceX 32h Record; BepiColombo Orbits</div>
        <div class="hero-desc">Falcon 9 launches NROL-136 spy sats from Vandenberg (12:23 UTC) in 32h pad turnaround; ESA/JAXA's BepiColombo safe at Mercury after burn glitch.</div>
      </div>
    </article>
  </section>

  <!-- MIDDLE BAND: WORLD MAP + 2 SPOTLIGHTS -->
  <section class="mid-row">
    <div class="map-card">
      <div class="map-header">
        <span>Global Event Map · 22 Nov 2026</span>
        <span>16 Key Datelines</span>
      </div>
      <div class="map-svg-wrap">
        <svg width="490" height="142" viewBox="0 0 490 142">
          <!-- Ocean & Graticule -->
          <rect width="490" height="142" fill="#D8ECF8"/>
          <line x1="0" y1="36" x2="490" y2="36" stroke="#C2E2F5" stroke-width="0.7"/>
          <line x1="0" y1="71" x2="490" y2="71" stroke="#B6DCF2" stroke-width="0.9" stroke-dasharray="3,3"/>
          <line x1="0" y1="106" x2="490" y2="106" stroke="#C2E2F5" stroke-width="0.7"/>
          <line x1="122" y1="0" x2="122" y2="142" stroke="#C2E2F5" stroke-width="0.7"/>
          <line x1="245" y1="0" x2="245" y2="142" stroke="#B6DCF2" stroke-width="0.9" stroke-dasharray="3,3"/>
          <line x1="368" y1="0" x2="368" y2="142" stroke="#C2E2F5" stroke-width="0.7"/>

          <!-- Greenland -->
          <path d="M164,8 C176,6 188,10 185,20 C180,26 168,26 162,18 Z" fill="#CBD5B6" stroke="#8FA078" stroke-width="0.7"/>
          <!-- North America -->
          <path d="M22,22 C36,15 58,14 78,16 C92,16 105,12 118,16 C132,20 144,28 140,38 C134,44 124,46 118,52 C112,57 109,64 104,63 C101,59 97,56 91,58 C84,61 81,66 86,73 C91,77 96,79 101,80 L96,83 C84,79 75,71 67,62 C55,58 46,48 40,36 C32,31 24,29 22,22 Z" fill="#CBD5B6" stroke="#8FA078" stroke-width="0.8"/>
          <!-- South America -->
          <path d="M101,80 C112,77 124,80 136,86 C148,92 156,100 151,110 C145,119 134,126 125,136 C118,139 112,135 112,126 C110,114 103,104 99,94 C97,87 98,82 101,80 Z" fill="#CBD5B6" stroke="#8FA078" stroke-width="0.8"/>
          <!-- UK & Ireland -->
          <path d="M214,27 C219,25 223,29 221,36 C217,39 213,36 214,27 Z" fill="#CBD5B6" stroke="#8FA078" stroke-width="0.7"/>
          <!-- Europe + Scandinavia -->
          <path d="M225,29 C232,20 245,12 258,13 C266,16 266,24 258,28 C268,28 278,29 286,33 C286,40 278,46 270,47 C262,48 256,43 250,48 C245,45 240,42 234,45 C227,47 220,46 218,41 C219,35 223,32 225,29 Z" fill="#CBD5B6" stroke="#8FA078" stroke-width="0.8"/>
          <!-- Africa -->
          <path d="M218,52 C233,49 252,51 268,54 C276,58 282,68 292,73 C292,80 284,88 279,98 C276,109 268,123 256,128 C247,128 242,118 238,105 C235,95 232,86 222,82 C212,77 209,65 218,52 Z" fill="#CBD5B6" stroke="#8FA078" stroke-width="0.8"/>
          <!-- Madagascar -->
          <path d="M286,104 L291,102 L289,116 L284,115 Z" fill="#CBD5B6" stroke="#8FA078" stroke-width="0.6"/>
          <!-- Asia + Arabian Peninsula + India + SE Asia -->
          <path d="M276,20 C306,13 356,13 406,18 C432,21 446,27 438,34 C428,38 418,41 412,48 C406,55 398,64 388,68 C378,72 373,77 368,84 C362,82 359,75 354,70 C346,69 341,78 336,83 C330,78 326,69 320,66 C311,64 303,69 294,72 C286,68 280,60 278,53 C272,51 269,48 272,44 C278,39 281,32 276,20 Z" fill="#CBD5B6" stroke="#8FA078" stroke-width="0.8"/>
          <!-- Japan -->
          <path d="M414,42 C419,38 424,42 421,50 C417,54 412,51 414,42 Z" fill="#CBD5B6" stroke="#8FA078" stroke-width="0.7"/>
          <!-- Indonesia / Maritime SE Asia -->
          <path d="M362,86 L376,91 L374,94 L360,89 Z M378,92 L396,94 L394,97 L377,95 Z M382,84 L392,84 L391,89 L381,88 Z M404,88 L420,92 L418,96 L402,92 Z" fill="#CBD5B6" stroke="#8FA078" stroke-width="0.65"/>
          <!-- Australia & NZ -->
          <path d="M385,103 C401,97 422,98 432,106 C436,115 430,126 418,127 C406,127 397,122 387,120 C381,115 381,108 385,103 Z" fill="#CBD5B6" stroke="#8FA078" stroke-width="0.8"/>
          <path d="M446,123 L452,118 L453,126 L447,129 Z" fill="#CBD5B6" stroke="#8FA078" stroke-width="0.6"/>

          <!-- Event Pins (16 key datelines) -->
          <g font-size="6.8" font-weight="800" text-anchor="middle" fill="#FFFFFF">
            <!-- 1. Vandenberg / Vegas -->
            <circle cx="54" cy="42" r="5.5" fill="#4F46E5" stroke="#FFF" stroke-width="1.2"/><text x="54" y="44.5">1</text>
            <!-- 2. Florida LPGA / US -->
            <circle cx="96" cy="52" r="5.5" fill="#059669" stroke="#FFF" stroke-width="1.2"/><text x="96" y="54.5">2</text>
            <!-- 3. Colombia -->
            <circle cx="110" cy="84" r="5.5" fill="#2563EB" stroke="#FFF" stroke-width="1.2"/><text x="110" y="86.5">3</text>
            <!-- 4. Brazil Tupancireta -->
            <circle cx="134" cy="116" r="5.5" fill="#D97706" stroke="#FFF" stroke-width="1.2"/><text x="134" y="118.5">4</text>
            <!-- 5. UK Manchester -->
            <circle cx="218" cy="31" r="5.5" fill="#DC2626" stroke="#FFF" stroke-width="1.2"/><text x="218" y="33.5">5</text>
            <!-- 6. Brussels / Portimao -->
            <circle cx="233" cy="37" r="5.5" fill="#059669" stroke="#FFF" stroke-width="1.2"/><text x="233" y="39.5">6</text>
            <!-- 7. Kyiv -->
            <circle cx="268" cy="34" r="5.5" fill="#DC2626" stroke="#FFF" stroke-width="1.2"/><text x="268" y="36.5">7</text>
            <!-- 8. Benghazi Libya -->
            <circle cx="250" cy="53" r="5.5" fill="#DC2626" stroke="#FFF" stroke-width="1.2"/><text x="250" y="55.5">8</text>
            <!-- 9. Antalya Turkey COP31 -->
            <circle cx="273" cy="46" r="5.5" fill="#0F766E" stroke="#FFF" stroke-width="1.2"/><text x="273" y="48.5">9</text>
            <!-- 10. Khartoum Sudan -->
            <circle cx="268" cy="70" r="5.5" fill="#DC2626" stroke="#FFF" stroke-width="1.2"/><text x="268" y="72.5">10</text>
            <!-- 11. South Africa Malgas -->
            <circle cx="252" cy="121" r="5.5" fill="#D97706" stroke="#FFF" stroke-width="1.2"/><text x="252" y="123.5">11</text>
            <!-- 12. Saudi Rabigh / Bahrain -->
            <circle cx="290" cy="60" r="5.5" fill="#DC2626" stroke="#FFF" stroke-width="1.2"/><text x="290" y="62.5">12</text>
            <!-- 13. India / Pakistan / BD -->
            <circle cx="335" cy="64" r="5.5" fill="#2563EB" stroke="#FFF" stroke-width="1.2"/><text x="335" y="66.5">13</text>
            <!-- 14. Indonesia -->
            <circle cx="378" cy="91" r="5.5" fill="#D97706" stroke="#FFF" stroke-width="1.2"/><text x="378" y="93.5">14</text>
            <!-- 15. Korea / HK / Taipei -->
            <circle cx="399" cy="49" r="5.5" fill="#2563EB" stroke="#FFF" stroke-width="1.2"/><text x="399" y="51.5">15</text>
            <!-- 16. Australia -->
            <circle cx="400" cy="114" r="5.5" fill="#D97706" stroke="#FFF" stroke-width="1.2"/><text x="400" y="116.5">16</text>
          </g>
        </svg>
      </div>
      <div class="map-legend">
        <span class="leg-item"><span class="dot" style="background:#DC2626"></span>Conflict/Security</span>
        <span class="leg-item"><span class="dot" style="background:#D97706"></span>Climate/Disaster</span>
        <span class="leg-item"><span class="dot" style="background:#2563EB"></span>Politics/Econ</span>
        <span class="leg-item"><span class="dot" style="background:#4F46E5"></span>Space/Tech</span>
        <span class="leg-item"><span class="dot" style="background:#059669"></span>Sport/Culture</span>
      </div>
    </div>

    <!-- RIGHT SPOTLIGHTS -->
    <div class="spotlights">
      <article class="spot-card">
        <svg class="spot-art" viewBox="0 0 78 70">
          <rect width="78" height="70" fill="#1E293B"/>
          <polyline points="8,18 22,26 32,20 46,42 58,36 70,54" fill="none" stroke="#F87171" stroke-width="3" stroke-linecap="round"/>
          <circle cx="70" cy="54" r="3.5" fill="#EF4444"/>
          <text x="10" y="14" fill="#FBBF24" font-size="9" font-weight="800">AI &amp; MKTS</text>
          <text x="10" y="61" fill="#FCA5A5" font-size="9" font-weight="800">BTC ~$55K</text>
        </svg>
        <div class="spot-text">
          <div class="spot-kicker" style="color:#B45309;">Economy &amp; Tech · Seoul / Washington</div>
          <div class="spot-title">Seoul Preps Market Fund After AI Selloff</div>
          <div class="spot-desc">S. Korea DPM Lee convenes emergency F4 meeting prepping stock-stabilization funds after Anthropic IPO slump, Nvidia probe &amp; BTC ~$55K dip; Sec. Bessent addresses US tech/AI glitches.</div>
        </div>
      </article>

      <article class="spot-card">
        <svg class="spot-art" viewBox="0 0 78 70">
          <rect width="78" height="70" fill="#064E3B"/>
          <!-- Trophy / Checkered flag -->
          <rect x="8" y="10" width="12" height="12" fill="#FFF"/><rect x="20" y="10" width="12" height="12" fill="#111"/>
          <rect x="8" y="22" width="12" height="12" fill="#111"/><rect x="20" y="22" width="12" height="12" fill="#FFF"/>
          <path d="M44,18 H66 L62,36 Q55,44 48,36 Z" fill="#FBBF24"/>
          <rect x="53" y="38" width="4" height="10" fill="#FBBF24"/>
          <rect x="46" y="48" width="18" height="4" fill="#FBBF24"/>
          <text x="39" y="63" text-anchor="middle" fill="#A7F3D0" font-size="9" font-weight="800">F1 · EPL · GP</text>
        </svg>
        <div class="spot-text">
          <div class="spot-kicker" style="color:#047857;">Global Sport · Vegas / Anfield / Portimão / Florida</div>
          <div class="spot-title">Verstappen Vegas, Liverpool 4–0, Márquez 8th</div>
          <div class="spot-desc">Verstappen wins 35-lead-change F1 Las Vegas GP (04:00 UTC); Liverpool routs Man Utd 4–0; Márquez wins 8th MotoGP title; Thitikul 3-peats LPGA ($4M).</div>
        </div>
      </article>
    </div>
  </section>

  <!-- LOWER 6-REGION GRID -->
  <section class="grid-6">
    <!-- AMERICAS -->
    <article class="region-card">
      <div class="region-hdr" style="background:#1D4ED8;">
        <span>Americas</span><span>US · Colombia · Brazil</span>
      </div>
      <div class="region-list">
        <div class="news-item"><span class="bullet" style="background:#1D4ED8"></span><div><strong>US Congress:</strong> NC concession widens House Democratic majority; Speaker-Designate Jeffries outlines 120th Congress agenda.</div></div>
        <div class="news-item"><span class="bullet" style="background:#1D4ED8"></span><div><strong>US Law &amp; Quake:</strong> DOJ admits mistaken deportation of citizen to Mexico; M3.3 tremor hits Los Angeles South Bay.</div></div>
        <div class="news-item"><span class="bullet" style="background:#1D4ED8"></span><div><strong>Colombia:</strong> Pres. De la Espriella orders prison Starlink &amp; phone crackdown alongside anti-ELN Operation Neptuno.</div></div>
        <div class="news-item"><span class="bullet" style="background:#1D4ED8"></span><div><strong>Brazil Calamity:</strong> Federal govt declares public calamity for storm-hit Tupanciretã (5 dead, ~8,000 homes damaged).</div></div>
      </div>
    </article>

    <!-- EUROPE -->
    <article class="region-card">
      <div class="region-hdr" style="background:#4338CA;">
        <span>Europe</span><span>UK · EU · Belgium · Germany</span>
      </div>
      <div class="region-list">
        <div class="news-item"><span class="bullet" style="background:#4338CA"></span><div><strong>UK Arena Scare:</strong> ~12,000 evacuated from Don Toliver Co-op Live concert in Manchester over suspected tear gas; 50+ treated.</div></div>
        <div class="news-item"><span class="bullet" style="background:#4338CA"></span><div><strong>EU Budget Clash:</strong> Council Pres. Costa proposes €204B cut (+232% defense, 3% tech tax), drawing France &amp; Germany pushback.</div></div>
        <div class="news-item"><span class="bullet" style="background:#4338CA"></span><div><strong>Belgium Strike:</strong> ATC provider Skeyes confirms 14h Monday walkout, grounding Brussels &amp; Charleroi commercial flights.</div></div>
        <div class="news-item"><span class="bullet" style="background:#4338CA"></span><div><strong>Stuttgart Chess:</strong> GM Anna Muzychuk defeats Kateryna Lagno 2.5–1.5 to win WR Women's Chess Tour Blitz Final.</div></div>
      </div>
    </article>

    <!-- MIDDLE EAST -->
    <article class="region-card">
      <div class="region-hdr" style="background:#B91C1C;">
        <span>Middle East</span><span>Saudi · Lebanon · Gulf · Israel</span>
      </div>
      <div class="region-list">
        <div class="news-item"><span class="bullet" style="background:#B91C1C"></span><div><strong>Saudi Arabia:</strong> Yemen's Houthis claim drone &amp; projectile strikes targeting Petrol Rabigh oil refinery &amp; Riyadh radar.</div></div>
        <div class="news-item"><span class="bullet" style="background:#B91C1C"></span><div><strong>South Lebanon:</strong> UNIFIL commander Maj. Gen. Abagnara announces handover of border posts to Lebanese Armed Forces.</div></div>
        <div class="news-item"><span class="bullet" style="background:#B91C1C"></span><div><strong>Bahrain &amp; Gulf:</strong> Bahrain reports 2 injured from Iranian strikes; US Embassy in Manama issues heightened security alerts.</div></div>
        <div class="news-item"><span class="bullet" style="background:#B91C1C"></span><div><strong>Israel Politics:</strong> Likud &amp; opposition leaders hold unity-government talks touching Nation-State Law &amp; statehood stance.</div></div>
      </div>
    </article>

    <!-- SUB-SAHARAN AFRICA -->
    <article class="region-card">
      <div class="region-hdr" style="background:#C2410C;">
        <span>Africa</span><span>Sudan · S. Africa · AU</span>
      </div>
      <div class="region-list">
        <div class="news-item"><span class="bullet" style="background:#C2410C"></span><div><strong>Sudan (Khartoum):</strong> Early-morning RSF drone strikes hit residential areas &amp; a UN compound, killing at least 4 civilians.</div></div>
        <div class="news-item"><span class="bullet" style="background:#C2410C"></span><div><strong>Sudan (Blue Nile):</strong> Sudanese military condemns alleged RSF execution of captured soldiers, demanding UN intervention.</div></div>
        <div class="news-item"><span class="bullet" style="background:#C2410C"></span><div><strong>South Africa:</strong> Crews stabilize De Hoop–Malgas wildfire lines after ~25,000 ha &amp; 24 homes burned in Western Cape.</div></div>
        <div class="news-item"><span class="bullet" style="background:#C2410C"></span><div><strong>AU &amp; Ethiopia:</strong> AU Deputy Chair Haddadi urges African security lead in Aswan amid Tigray border troop buildup fears.</div></div>
      </div>
    </article>

    <!-- EAST & SE ASIA -->
    <article class="region-card">
      <div class="region-hdr" style="background:#0F766E;">
        <span>East &amp; SE Asia</span><span>Korea · HK · TW · Indonesia</span>
      </div>
      <div class="region-list">
        <div class="news-item"><span class="bullet" style="background:#0F766E"></span><div><strong>South Korea:</strong> Education Minister Choi Kyo-jin resigns over backlash to Suneung university-exam AI cheating rules.</div></div>
        <div class="news-item"><span class="bullet" style="background:#0F766E"></span><div><strong>Hong Kong:</strong> Election Committee Subsector Ordinary Elections proceed Sunday with high provisional turnout.</div></div>
        <div class="news-item"><span class="bullet" style="background:#0F766E"></span><div><strong>Taiwan:</strong> 63rd Golden Horse Awards in Taipei (<em>We Are Born Good</em> wins); Philippines sweeps Asia Rugby 7s Trophy.</div></div>
        <div class="news-item"><span class="bullet" style="background:#0F766E"></span><div><strong>Indonesia:</strong> M5.4 Bitung &amp; M4.8 Sentani quakes hit Sunday; 24+ bodies recovered at Serang candy factory fire.</div></div>
      </div>
    </article>

    <!-- SOUTH ASIA & OCEANIA -->
    <article class="region-card">
      <div class="region-hdr" style="background:#047857;">
        <span>S. Asia &amp; Oceania</span><span>India · Pak · BD · Australia</span>
      </div>
      <div class="region-list">
        <div class="news-item"><span class="bullet" style="background:#047857"></span><div><strong>India–Pakistan:</strong> ~2,300 Indian Sikh pilgrims cross Attari-Wagah border into Pakistan for Guru Nanak's 557th Prakash Parv.</div></div>
        <div class="news-item"><span class="bullet" style="background:#047857"></span><div><strong>India:</strong> Highway collision on Kota–Udaipur road kills 12+; food regulator FSSAI launches prosecution of Bisleri.</div></div>
        <div class="news-item"><span class="bullet" style="background:#047857"></span><div><strong>Bangladesh:</strong> Garment worker minimum-wage protests &amp; police clashes disrupt industrial zones in Gazipur.</div></div>
        <div class="news-item"><span class="bullet" style="background:#047857"></span><div><strong>Australia:</strong> Climate Min. Bowen decries COP31 deadlock as heavy storms disrupt Western Australia grain harvest.</div></div>
      </div>
    </article>
  </section>

  <!-- FOOTER -->
  <footer class="footer">
    <span>WORLD NEWS ATLAS · SUNDAY, 22 NOVEMBER 2026</span>
    <span>ALL EVENTS OCCURRED OR FIRST REPORTED 22 NOV 2026 (UTC / LOCAL) · 1024×1024</span>
  </footer>

</div>
</body>
</html>
"""

def main() -> None:
    out_path = Path(__file__).resolve().parent / "entry.png"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1024, "height": 1024}, device_scale_factor=1)
        page.set_content(HTML, wait_until="load")
        page.screenshot(path=str(out_path), type="png")
        browser.close()
    print(f"Wrote {out_path} ({out_path.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
