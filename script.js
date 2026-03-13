/* ── Theme Toggle ─────────────────────── */
(function() {
    var saved = localStorage.getItem('theme');
    if (saved) document.documentElement.setAttribute('data-theme', saved);
})();

function initThemeToggle() {
    var btn = document.getElementById('themeToggle');
    if (!btn) return;
    function updateIcon() {
        var dark = document.documentElement.getAttribute('data-theme') === 'dark';
        btn.innerHTML = dark ? '<i class="fa-solid fa-sun"></i>' : '<i class="fa-solid fa-moon"></i>';
    }
    updateIcon();
    btn.addEventListener('click', function() {
        var dark = document.documentElement.getAttribute('data-theme') === 'dark';
        var next = dark ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
        updateIcon();
    });
}

/* ── Active Nav Link ─────────────────────── */
function initActiveNav() {
    var page = location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('nav ul a').forEach(function(a) {
        var href = a.getAttribute('href');
        if (href === page || (page === '' && href === 'index.html')) {
            a.classList.add('active');
        }
    });
}

/* ── Hamburger Menu ─────────────────────── */
function initHamburger() {
    var btn = document.getElementById('hamburger');
    var menu = document.getElementById('navMenu');
    if (!btn || !menu) return;
    btn.addEventListener('click', function() {
        var open = menu.classList.toggle('open');
        btn.setAttribute('aria-expanded', open);
    });
    menu.querySelectorAll('a').forEach(function(a) {
        a.addEventListener('click', function() {
            menu.classList.remove('open');
            btn.setAttribute('aria-expanded', 'false');
        });
    });
}

/* ── Typing Effect (hero only) ─────────────────────── */
function initTyping() {
    var el = document.getElementById('tw');
    if (!el) return;
    var phrases = [
        'Administration Systèmes & Réseaux',
        'Cybersécurité',
        'Réseaux Cisco & Infrastructure',
        'Technicien SISR'
    ];
    var pi = 0, ci = 0, del = false;
    function type() {
        var cur = phrases[pi];
        el.textContent = del ? cur.slice(0, --ci) : cur.slice(0, ++ci);
        var spd = del ? 45 : 95;
        if (!del && ci === cur.length) { del = true; spd = 1800; }
        if (del && ci === 0) { del = false; pi = (pi + 1) % phrases.length; spd = 400; }
        setTimeout(type, spd);
    }
    type();
}

/* ── Scroll Reveal ─────────────────────── */
function reveal() {
    document.querySelectorAll('.rv').forEach(function(el) {
        if (el.getBoundingClientRect().top < window.innerHeight - 80) el.classList.add('show');
    });
}

/* ── Modal Helpers ─────────────────────── */
function show(id) { document.getElementById(id).classList.add('on'); document.body.style.overflow = 'hidden'; }
function hide(id) { document.getElementById(id).classList.remove('on'); document.body.style.overflow = ''; }

/* ── Projets Modal ─────────────────────── */
function openProjModal() { show('projModal'); }
function closeProjModal() { hide('projModal'); }

/* ── Monit (EcoStruxure) Modal ─────────────────────── */
function openMonitModal() {
    if (document.getElementById('projModal')) hide('projModal');
    setTimeout(function() { backParts(); show('monitModal'); }, 280);
}
function closeMonitModal() { hide('monitModal'); backParts(); }

var subtitles = {
    p1: 'Recensement & Configuration — Datacenter',
    p2: 'Câblage',
    p3: 'Déploiement de la supervision via EcoStruxure IT Expert',
    p4: 'Modélisation 3D du datacenter'
};

function showPartsGrid() {
    document.getElementById('overview').style.display = 'none';
    document.getElementById('pgrid').style.display = 'grid';
    document.getElementById('msub').textContent = 'Sélectionnez la partie à consulter';
}

function showPart(id) {
    document.getElementById('overview').style.display = 'none';
    document.getElementById('pgrid').style.display = 'none';
    ['p1','p2','p3','p4'].forEach(function(p) { document.getElementById(p).classList.remove('on'); });
    document.getElementById(id).classList.add('on');
    document.getElementById('msub').textContent = subtitles[id];
    document.querySelector('#monitModal .mbox').scrollTop = 0;
}

function backToGrid() {
    document.getElementById('overview').style.display = 'none';
    document.getElementById('pgrid').style.display = 'grid';
    ['p1','p2','p3','p4'].forEach(function(p) { document.getElementById(p).classList.remove('on'); });
    document.getElementById('msub').textContent = 'Choisir une des 4 parties du projet';
    document.querySelector('#monitModal .mbox').scrollTop = 0;
}

function backParts() {
    document.getElementById('overview').style.display = 'block';
    document.getElementById('pgrid').style.display = 'none';
    ['p1','p2','p3','p4'].forEach(function(p) { document.getElementById(p).classList.remove('on'); });
    document.getElementById('msub').textContent = 'Vue d\'ensemble du projet';
}

/* ── CR Modal ─────────────────────── */
function openCRModal() {
    if (document.getElementById('projModal')) hide('projModal');
    setTimeout(function() { show('crModal'); }, 280);
}
function closeCRModal() { hide('crModal'); }

/* ── Cisco Modal ─────────────────────── */
function openCiscoModal() {
    if (document.getElementById('projModal')) hide('projModal');
    setTimeout(function() { backCiscoParts(); show('ciscoModal'); }, 280);
}
function closeCiscoModal() { hide('ciscoModal'); backCiscoParts(); }

var ciscoSubtitles = {
    cp1: 'Inventaire technique du matériel',
    cp2: 'Préparation et déballage des équipements',
    cp3: 'Rackage selon le plan d\'implantation'
};

function showCiscoPartsGrid() {
    document.getElementById('ciscoOverview').style.display = 'none';
    document.getElementById('ciscoPgrid').style.display = 'grid';
    ['cp1','cp2','cp3'].forEach(function(p) { document.getElementById(p).classList.remove('on'); });
    document.getElementById('ciscoSub').textContent = 'Choisir une des 3 parties du projet';
    document.querySelector('#ciscoModal .mbox').scrollTop = 0;
}

function showCiscoPart(id) {
    document.getElementById('ciscoOverview').style.display = 'none';
    document.getElementById('ciscoPgrid').style.display = 'none';
    ['cp1','cp2','cp3'].forEach(function(p) { document.getElementById(p).classList.remove('on'); });
    document.getElementById(id).classList.add('on');
    document.getElementById('ciscoSub').textContent = ciscoSubtitles[id];
    document.querySelector('#ciscoModal .mbox').scrollTop = 0;
}

function backCiscoToGrid() {
    document.getElementById('ciscoOverview').style.display = 'none';
    document.getElementById('ciscoPgrid').style.display = 'grid';
    ['cp1','cp2','cp3'].forEach(function(p) { document.getElementById(p).classList.remove('on'); });
    document.getElementById('ciscoSub').textContent = 'Choisir une des 3 parties du projet';
    document.querySelector('#ciscoModal .mbox').scrollTop = 0;
}

function backCiscoParts() {
    document.getElementById('ciscoOverview').style.display = 'block';
    document.getElementById('ciscoPgrid').style.display = 'none';
    ['cp1','cp2','cp3'].forEach(function(p) { document.getElementById(p).classList.remove('on'); });
    document.getElementById('ciscoSub').textContent = 'Vue d\'ensemble du projet';
}

/* ── Global Event Listeners ─────────────────────── */
document.addEventListener('DOMContentLoaded', function() {
    initThemeToggle();
    initActiveNav();
    initHamburger();
    initTyping();
    reveal();
});

window.addEventListener('scroll', reveal, { passive: true });

document.addEventListener('click', function(e) {
    if (e.target.id === 'projModal') closeProjModal();
    if (e.target.id === 'monitModal') closeMonitModal();
    if (e.target.id === 'crModal') closeCRModal();
    if (e.target.id === 'ciscoModal') closeCiscoModal();
});

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeProjModal();
        closeMonitModal();
        closeCRModal();
        closeCiscoModal();
    }
});
