/* ═══════════════════════════════════════════
   Kern Docs — script.js
═══════════════════════════════════════════ */

'use strict';

// ─── Terminal content per section ───
const TERMINALS = {
  problem: [
    ['t-comment', '# Without kern — the old way'],
    ['', ''],
    ['', '<span class="t-prompt">$</span><span class="t-cmd"> python app.py</span>'],
    ['t-output', '  Starting AI session...'],
    ['t-output', '  Context loaded: 2,847 tokens'],
    ['', ''],
    ['t-comment', '  # You edit a file...'],
    ['', ''],
    ['t-error',   '  ^C  Process killed.'],
    ['', '<span class="t-prompt">$</span><span class="t-cmd"> python app.py</span>'],
    ['t-output', '  Starting AI session...'],
    ['t-error',   '  Context loaded: 0 tokens'],
    ['', ''],
    ['t-comment', '  # State gone. Every single time.'],
  ],

  installation: [
    ['', '<span class="t-prompt">$</span><span class="t-cmd"> git clone github.com/olugbeminiyi2000/Kern.git</span>'],
    ['', ''],
    ['', '<span class="t-prompt">$</span><span class="t-cmd"> cd Kern</span>'],
    ['', ''],
    ['', '<span class="t-prompt">$</span><span class="t-cmd"> pip install -e .</span>'],
    ['t-output', '  Collecting kern...'],
    ['t-output', '  Installing packages...'],
    ['t-success', '  Successfully installed kern-0.1.0'],
    ['', ''],
    ['', '<span class="t-prompt">$</span><span class="t-cmd"> kern info</span>'],
    ['t-accent',  '  --- Kern Development Engine ---'],
    ['t-output', '  Version: 0.1.0'],
    ['t-output', '  Authors: Emmanuel Obolo &amp; Abiodun Kumuyi'],
    ['t-output', '  Status:  Active and Monitoring'],
  ],

  quickstart: [
    ['', '<span class="t-prompt">$</span><span class="t-cmd"> kern run app.py</span>'],
    ['t-accent',  '  &gt;&gt;&gt; Kern Engine Ignited...'],
    ['t-accent',  '  --- Kern Engine Ignited ---'],
    ['t-accent',  '  Monitoring: app. Press Ctrl+C to stop.'],
    ['t-success', '  [*] app reconstructed successfully.'],
    ['t-accent',  '  --- Executing app.run() ---'],
    ['t-output', '  Hello from kern!'],
    ['t-accent',  '  ──────────────────────────────'],
    ['', ''],
    ['t-comment', '  # [you edit utils/helper.py]'],
    ['', ''],
    ['t-warn',    '  [v] Stable change detected. Attempting recovery...'],
    ['t-warn',    '  [Reloader] Evicting: utils.helper'],
    ['t-warn',    '  [Reloader] Evicting: app'],
    ['t-success', '  [*] app reconstructed successfully.'],
    ['t-output', '  Hello from kern! (updated)'],
  ],

  scanner: [
    ['t-comment', '# DependencyTracker — tracker/dependency.py'],
    ['', ''],
    ['t-output',  '  Entry point: <span class="t-path">app.py</span>'],
    ['t-output',  '  Method: ast.parse() — no execution'],
    ['', ''],
    ['t-output',  '  Dependency graph:'],
    ['t-tree',    '  ┌─ app.py'],
    ['t-tree',    '  ├── utils/colors.py'],
    ['t-tree',    '  ├── core/engine.py'],
    ['t-tree',    '  │   └── tracker/watcher.py'],
    ['t-tree',    '  └── hot_reload/reloader.py'],
    ['', ''],
    ['t-output',  '  All files resolved to absolute paths.'],
    ['t-output',  '  Syntax errors: file stays in watch list.'],
    ['t-success', '  FileWatcher polling every 0.3s ✓'],
  ],

  evictor: [
    ['t-comment', '# ModuleReloader — hot_reload/reloader.py'],
    ['', ''],
    ['t-warn',    '  [v] Stable change detected. Attempting recovery...'],
    ['', ''],
    ['t-output',  '  Changed: <span class="t-path">core/engine.py</span>'],
    ['t-output',  '  Finding all dependents...'],
    ['', ''],
    ['t-warn',    '  [Reloader] Evicting: core.engine'],
    ['t-warn',    '  [Reloader] Evicting: app'],
    ['', ''],
    ['t-output',  '  Children cleared before parents.'],
    ['t-output',  '  No ghost imports remain in sys.modules.'],
    ['', ''],
    ['t-success', '  [*] app reconstructed successfully.'],
    ['t-accent',  '  --- Executing app.run() ---'],
  ],

  orchestrator: [
    ['t-comment', '# Engine loop — core/engine.py'],
    ['', ''],
    ['t-output',  '  while True:'],
    ['t-output',  '    if watcher.change_detected:'],
    ['t-output',  '      wait for debounce (0.5s)'],
    ['t-output',  '      reloader.reload_affected()'],
    ['t-output',  '      module = importlib.import()'],
    ['t-output',  '      module.run()'],
    ['t-output',  '    time.sleep(0.1)  # heartbeat'],
    ['', ''],
    ['t-warn',    '  [v] Stable change detected. Attempting recovery...'],
    ['t-success', '  [*] app reconstructed successfully.'],
    ['t-accent',  '  --- Executing app.run() ---'],
    ['', ''],
    ['t-success', '  Engine: still running ✓'],
  ],

  cli: [
    ['', '<span class="t-prompt">$</span><span class="t-cmd"> kern run app.py</span>'],
    ['t-accent',  '  &gt;&gt;&gt; Kern Engine Ignited...'],
    ['t-accent',  '  --- Kern Engine Ignited ---'],
    ['t-accent',  '  Monitoring: app. Press Ctrl+C to stop.'],
    ['t-success', '  [*] app reconstructed successfully.'],
    ['', ''],
    ['t-comment', '# ─────────────────────────────────────'],
    ['', ''],
    ['', '<span class="t-prompt">$</span><span class="t-cmd"> kern info</span>'],
    ['t-accent',  '  --- Kern Development Engine ---'],
    ['t-output',  '  Version: 0.1.0'],
    ['t-output',  '  Authors: Emmanuel Obolo Oluwapelumi &amp; Abiodun Kumuyi'],
    ['t-output',  '  Status:  Active and Monitoring'],
  ],

  config: [
    ['t-comment', '# core/engine.py'],
    ['', ''],
    ['t-output',  '  self.DEBOUNCE_SECONDS = <span class="t-warn">0.5</span>'],
    ['t-comment', '  # instance attr — editable at runtime'],
    ['', ''],
    ['t-comment', '# tracker/watcher.py (hardcoded)'],
    ['t-output',  '  time.sleep(<span class="t-warn">0.3</span>)  # poll interval'],
    ['', ''],
    ['t-comment', '# core/engine.py (hardcoded)'],
    ['t-output',  '  time.sleep(<span class="t-warn">0.1</span>)  # heartbeat'],
    ['', ''],
    ['t-comment', '# run() contract — can be pass:'],
    ['t-output',  '  def <span class="t-accent">run</span>():'],
    ['t-output',  '      pass  <span class="t-comment"># still valid</span>'],
    ['t-success', '  # kern reloads and calls run() ✓'],
  ],
};

const LABELS = {
  problem:      'The Problem',
  installation: 'Installation',
  quickstart:   'Quick Start',
  scanner:      'Layer 1 — Scanner',
  evictor:      'Layer 2 — Evictor',
  orchestrator: 'Layer 3 — Orchestrator',
  cli:          'CLI Reference',
  config:       'Configuration',
};

// ─── State ───
let activeKey = null;
const termContent = document.getElementById('terminal-content');
const termLabel   = document.getElementById('term-section-label');

// ─── Render terminal ───
function renderTerminal(key) {
  if (!TERMINALS[key] || activeKey === key) return;
  activeKey = key;

  termContent.style.opacity = '0';

  setTimeout(() => {
    const lines = TERMINALS[key];
    const html  = lines.map(([cls, text]) => {
      const content = text === '' ? '&nbsp;' : text;
      return cls
        ? `<span class="tl ${cls}">${content}</span>`
        : `<span class="tl">${content}</span>`;
    }).join('');

    termContent.innerHTML = html;
    if (termLabel) termLabel.textContent = LABELS[key] || 'kern';
    termContent.style.opacity = '1';
  }, 180);
}

// ─── IntersectionObserver: terminal switching ───
// Track every observed section's latest ratio so we always pick the most visible one,
// not just whichever happened to fire in this batch of entries.
const sectionRatios = new Map();

const termObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    sectionRatios.set(entry.target, entry.intersectionRatio);
  });

  let best = null;
  let bestRatio = 0;
  sectionRatios.forEach((ratio, el) => {
    if (ratio > bestRatio) {
      bestRatio = ratio;
      best = el;
    }
  });

  if (best && bestRatio > 0) {
    const key = best.dataset.terminal;
    if (key) renderTerminal(key);
  }
}, {
  threshold: [0, 0.1, 0.25, 0.5, 0.75],
  rootMargin: '-80px 0px 0px 0px',
});

// ─── IntersectionObserver: slide-in animations ───
const slideObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      slideObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.08 });

// ─── Attach observers ───
document.querySelectorAll('[data-terminal]').forEach(el => {
  sectionRatios.set(el, 0);
  termObserver.observe(el);
});
document.querySelectorAll('.slide-in').forEach(el => slideObserver.observe(el));

// ─── Boot: show first terminal ───
renderTerminal('problem');

// ─── Mobile nav toggle ───
const toggle     = document.querySelector('.nav-toggle');
const mobileMenu = document.getElementById('mobile-menu');

toggle?.addEventListener('click', () => {
  const isOpen = mobileMenu.classList.toggle('open');
  toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  mobileMenu.setAttribute('aria-hidden', isOpen ? 'false' : 'true');
});

// close menu when any link is tapped
mobileMenu?.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    mobileMenu.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    mobileMenu.setAttribute('aria-hidden', 'true');
  });
});

// close menu on outside click
document.addEventListener('click', (e) => {
  if (!toggle?.contains(e.target) && !mobileMenu?.contains(e.target)) {
    mobileMenu?.classList.remove('open');
    toggle?.setAttribute('aria-expanded', 'false');
    mobileMenu?.setAttribute('aria-hidden', 'true');
  }
});
