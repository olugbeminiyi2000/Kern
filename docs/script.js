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
let activeKey   = null;
let scrollRafId = null;
const termContent  = document.getElementById('terminal-content');
const termLabel    = document.getElementById('term-section-label');
const fabLabel     = document.getElementById('fab-label');
const modalContent = document.getElementById('terminal-content-modal');
const modalTitle   = document.getElementById('term-modal-title');

// ─── Render terminal ───
function renderTerminal(key) {
  if (!TERMINALS[key] || activeKey === key) return;
  activeKey = key;

  const html = TERMINALS[key].map(([cls, text]) => {
    const content = text === '' ? '&nbsp;' : text;
    return cls
      ? `<span class="tl ${cls}">${content}</span>`
      : `<span class="tl">${content}</span>`;
  }).join('');

  // Update all targets instantly — no setTimeout, no opacity fade.
  // A timer here gets cancelled every 16ms by rapid scroll and never fires.
  termContent.innerHTML = html;
  if (termLabel)    termLabel.textContent    = LABELS[key] || 'kern';
  if (fabLabel)     fabLabel.textContent     = LABELS[key] || 'kern';
  if (modalContent) modalContent.innerHTML   = html;
  if (modalTitle)   modalTitle.textContent   = LABELS[key] || 'kern';
}

// ─── Scroll-based terminal switching ───
// Picks whichever [data-terminal] section's center is closest to the viewport center.
// More reliable than IntersectionObserver thresholds for tall sections.
function updateTerminalFromScroll() {
  const vh  = window.innerHeight;
  const mid = vh / 2;
  let best     = null;
  let bestDist = Infinity;

  document.querySelectorAll('[data-terminal]').forEach(section => {
    const rect = section.getBoundingClientRect();
    if (rect.bottom < 0 || rect.top > vh) return; // off-screen — skip
    const dist = Math.abs((rect.top + rect.height / 2) - mid);
    if (dist < bestDist) { bestDist = dist; best = section; }
  });

  if (best) renderTerminal(best.dataset.terminal);
}

function scheduleTerminalUpdate() {
  if (scrollRafId) cancelAnimationFrame(scrollRafId);
  scrollRafId = requestAnimationFrame(updateTerminalFromScroll);
}

// Desktop: left panel scrolls independently inside sticky split-screen
const leftPanel = document.querySelector('.left-panel');
leftPanel?.addEventListener('scroll', scheduleTerminalUpdate, { passive: true });

// Mobile fallback: left panel is overflow:visible, so window scroll drives content
window.addEventListener('scroll', scheduleTerminalUpdate, { passive: true });

// ─── Slide-in animations ───
const slideObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      slideObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.08 });

document.querySelectorAll('.slide-in').forEach(el => slideObserver.observe(el));

// ─── Boot ───
updateTerminalFromScroll();

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

// ─── Mobile terminal FAB + modal ───
const termFab        = document.getElementById('term-fab');
const termModal      = document.getElementById('term-modal');
const termModalClose = document.getElementById('term-modal-close');

function openModal() {
  termModal?.classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeModal() {
  termModal?.classList.remove('open');
  document.body.style.overflow = '';
}

termFab?.addEventListener('click', openModal);
termModalClose?.addEventListener('click', closeModal);

// close on backdrop tap (outside the sheet)
termModal?.addEventListener('click', (e) => {
  if (e.target === termModal) closeModal();
});

// close on Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && termModal?.classList.contains('open')) closeModal();
});
