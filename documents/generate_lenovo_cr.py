from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

OUTPUT = "Compte_rendu_Serveur_Lenovo_SR645_AD.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    topMargin=2.2*cm, bottomMargin=2*cm,
    leftMargin=2.5*cm, rightMargin=2.5*cm,
)

W = A4[0] - 5*cm  # text width

# ── Couleurs ──────────────────────────────────────────────────────────────────
ACCENT = colors.HexColor("#1d4ed8")
LIGHT  = colors.HexColor("#eff6ff")
GRAY   = colors.HexColor("#64748b")
DARK   = colors.HexColor("#0f172a")
LINE   = colors.HexColor("#cbd5e1")

# ── Styles ────────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def style(name, parent="Normal", **kw):
    return ParagraphStyle(name, parent=base[parent], **kw)

S = {
    "title"   : style("title",   "Title",    fontSize=18, textColor=DARK,
                       leading=22, spaceAfter=4),
    "subtitle": style("subtitle","Normal",   fontSize=10, textColor=GRAY,
                       alignment=TA_CENTER, spaceAfter=2),
    "meta"    : style("meta",    "Normal",   fontSize=9,  textColor=GRAY,
                       alignment=TA_CENTER, spaceAfter=16),
    "h1"      : style("h1",      "Heading1", fontSize=12, textColor=ACCENT,
                       spaceBefore=14, spaceAfter=4, leading=16,
                       fontName="Helvetica-Bold"),
    "h2"      : style("h2",      "Heading2", fontSize=10.5, textColor=DARK,
                       spaceBefore=10, spaceAfter=3, leading=14,
                       fontName="Helvetica-Bold"),
    "body"    : style("body",    "Normal",   fontSize=9.5, textColor=DARK,
                       leading=14, spaceAfter=6, alignment=TA_JUSTIFY),
    "bullet"  : style("bullet",  "Normal",   fontSize=9.5, textColor=DARK,
                       leading=13, spaceAfter=3, leftIndent=14,
                       bulletIndent=4),
    "caption" : style("caption", "Normal",   fontSize=8.5, textColor=GRAY,
                       alignment=TA_CENTER, spaceAfter=8, fontName="Helvetica-Oblique"),
    "note"    : style("note",    "Normal",   fontSize=9, textColor=GRAY,
                       leading=13, spaceAfter=6, fontName="Helvetica-Oblique"),
}

def H(level, text):
    return Paragraph(text, S["h1"] if level == 1 else S["h2"])

def P(text):
    return Paragraph(text, S["body"])

def B(text):
    return Paragraph(f"• {text}", S["bullet"])

def spacer(h=0.3):
    return Spacer(1, h*cm)

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=LINE, spaceAfter=6, spaceBefore=2)

def table(data, col_widths=None, header=True):
    t = Table(data, colWidths=col_widths or [W/len(data[0])]*len(data[0]))
    cmds = [
        ("FONTNAME",    (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE",    (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, colors.HexColor("#f8fafc")]),
        ("GRID",        (0,0), (-1,-1), 0.4, LINE),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",  (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]
    if header:
        cmds += [
            ("BACKGROUND",  (0,0), (-1,0), ACCENT),
            ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
            ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
        ]
    t.setStyle(TableStyle(cmds))
    return t

# ── Contenu ───────────────────────────────────────────────────────────────────
story = []

# ── PAGE DE GARDE ─────────────────────────────────────────────────────────────
story += [
    spacer(3),
    Paragraph("Compte Rendu d'Activité", S["subtitle"]),
    spacer(0.4),
    Paragraph("Serveur Lenovo ThinkSystem SR645", S["title"]),
    Paragraph(
        "Mise en place d'un environnement Active Directory complet<br/>sous Windows Server 2025",
        S["subtitle"]
    ),
    spacer(0.6),
    HRFlowable(width="60%", thickness=2, color=ACCENT, hAlign="CENTER"),
    spacer(0.8),
    Paragraph("Ilyas Seddiki &nbsp;|&nbsp; TD SYNNEX — BSC-LAB &nbsp;|&nbsp; Mars 2026", S["meta"]),
    PageBreak(),
]

# ── 1. INTRODUCTION ───────────────────────────────────────────────────────────
story += [
    H(1, "1. Introduction et contexte du projet"),
    hr(),
    P(
        "Un serveur Lenovo ThinkSystem SR645 a été mis à disposition pour la réalisation d'un projet "
        "d'infrastructure complète sous Windows Server 2025 Datacenter. L'objectif est de déployer un "
        "environnement virtualisé sous Hyper-V hébergeant deux machines virtuelles :"
    ),
    B("<b>SRV-INFRA</b> — contrôleur de domaine, DNS, DHCP, AD CS, serveur de fichiers, NTP, GPO"),
    B("<b>SRV-AUTO</b> — poste client joint au domaine pour les tests de validation"),
    spacer(),

    H(2, "1.1 Caractéristiques du serveur physique"),
    table([
        ["Composant", "Détail"],
        ["Modèle", "Lenovo ThinkSystem SR645 (1U rack)"],
        ["Processeur", "AMD EPYC"],
        ["Réseau", "Contrôleurs 10 Gbps"],
        ["Système d'exploitation hôte", "Windows Server 2025 Datacenter"],
        ["Nom d'hôte", "SRV-ILYAS"],
    ], col_widths=[6*cm, 10*cm]),
    spacer(),

    H(2, "1.2 Architecture réseau"),
    P("L'infrastructure repose sur le plan d'adressage 192.168.60.0/24. SRV-ILYAS fait office d'hôte Hyper-V, hébergeant les deux VMs connectées via un commutateur virtuel externe."),
    table([
        ["Serveur", "Adresse IP", "Masque", "Passerelle"],
        ["SRV-ILYAS", "192.168.60.1", "/24", "192.168.60.254"],
        ["SRV-INFRA", "192.168.60.10", "/24", "192.168.60.254"],
    ], col_widths=[4*cm, 4*cm, 3*cm, 5*cm]),
    P("Les rôles déployés sur SRV-INFRA : AD DS, DNS, DHCP, AD CS, Serveur de fichiers, NTP, GPO."),
]

# ── 2. HYPER-V ────────────────────────────────────────────────────────────────
story += [
    spacer(),
    H(1, "2. Installation et préparation Hyper-V"),
    hr(),
    P(
        "La première étape consiste à activer le rôle Hyper-V sur SRV-ILYAS via le Gestionnaire de serveur "
        "Windows Server 2025. Ce rôle transforme le serveur en hyperviseur de type 1."
    ),

    H(2, "2.1 Activation du rôle Hyper-V"),
    P(
        "Dans l'assistant d'ajout de rôles, on sélectionne <b>Hyper-V</b> ainsi que les "
        "<b>Services de fichiers et de stockage</b>. Une fois le rôle installé et le serveur redémarré, "
        "le Gestionnaire Hyper-V est accessible et affiche SRV-ILYAS comme hôte de virtualisation."
    ),

    H(2, "2.2 Création du commutateur virtuel externe"),
    P(
        "Un commutateur virtuel de type <b>Externe</b> est configuré afin de lier la carte réseau physique "
        "du serveur aux VMs. Sans ce commutateur, les machines virtuelles seraient isolées et ne pourraient "
        "pas communiquer avec le reste du réseau."
    ),
]

# ── 3. MACHINES VIRTUELLES ────────────────────────────────────────────────────
story += [
    spacer(),
    H(1, "3. Création des machines virtuelles"),
    hr(),
    P("Deux machines virtuelles sont créées sur l'hôte Hyper-V SRV-ILYAS."),

    H(2, "3.1 SRV-INFRA"),
    table([
        ["Paramètre", "Valeur"],
        ["Nom", "Infrastructure (SRV-INFRA)"],
        ["Disque virtuel", "SRV-INFRA.vhdx — 127 Go (format dynamique)"],
        ["Rôle", "Cœur de l'infrastructure (AD, DNS, DHCP, fichiers…)"],
        ["Adresse IP", "192.168.60.10"],
    ], col_widths=[5*cm, 11*cm]),
    P(
        "Le format VHDX dynamique permet d'optimiser l'utilisation de l'espace disque physique : "
        "le fichier ne croît que lorsque des données y sont réellement écrites."
    ),

    H(2, "3.2 SRV-AUTO"),
    P(
        "La VM SRV-AUTO est connectée au commutateur virtuel externe (vSwitch-External), lui permettant "
        "de communiquer avec SRV-INFRA et d'accéder aux services du domaine (DNS, DHCP, partage de fichiers)."
    ),
]

# ── 4. ACTIVE DIRECTORY ───────────────────────────────────────────────────────
story += [
    spacer(),
    H(1, "4. Déploiement de l'Active Directory (AD DS)"),
    hr(),
    P(
        "Active Directory Domain Services (AD DS) est le service central de l'infrastructure. "
        "Il gère l'authentification, les autorisations et les stratégies du domaine <b>bsc-lab.local</b>."
    ),

    H(2, "4.1 Promotion en contrôleur de domaine"),
    P("L'option <b>« Ajouter une nouvelle forêt »</b> est choisie pour créer un domaine entièrement nouveau."),
    table([
        ["Paramètre", "Valeur"],
        ["Nom de domaine racine", "bsc-lab.local"],
        ["Niveau fonctionnel", "Windows Server 2025"],
        ["Rôle FSMO", "Émulateur PDC, RID Master, Infrastructure Master…"],
        ["Dossier NTDS", "C:\\Windows\\NTDS"],
        ["Dossier SYSVOL", "C:\\Windows\\SYSVOL"],
    ], col_widths=[6*cm, 10*cm]),
]

# ── 5. DNS ────────────────────────────────────────────────────────────────────
story += [
    spacer(),
    H(1, "5. Configuration du DNS"),
    hr(),
    P(
        "Le rôle DNS est intégré à l'AD DS lors de la promotion. Une zone de recherche directe "
        "<b>bsc-lab.local</b> et une zone de recherche inversée sont créées automatiquement."
    ),
    B("Zone directe : bsc-lab.local → enregistrements A pour SRV-INFRA et SRV-AUTO"),
    B("Zone inversée : 60.168.192.in-addr.arpa → enregistrements PTR"),
    B("Enregistrement A manuel ajouté pour SRV-AUTO après jonction au domaine"),
]

# ── 6. DHCP ───────────────────────────────────────────────────────────────────
story += [
    spacer(),
    H(1, "6. Configuration du DHCP"),
    hr(),
    P("Le service DHCP est installé sur SRV-INFRA et autorisé dans l'Active Directory."),
    table([
        ["Paramètre", "Valeur"],
        ["Étendue", "192.168.60.0/24"],
        ["Plage d'adresses", "192.168.60.100 – 192.168.60.200"],
        ["Passerelle (option 3)", "192.168.60.254"],
        ["DNS (option 6)", "192.168.60.10 (SRV-INFRA)"],
        ["Durée du bail", "8 jours"],
    ], col_widths=[6*cm, 10*cm]),
    P(
        "Des exclusions sont définies pour les adresses statiques (SRV-ILYAS : .1, SRV-INFRA : .10). "
        "L'étendue est ensuite autorisée et activée."
    ),
]

# ── 7. SERVEUR DE FICHIERS ────────────────────────────────────────────────────
story += [
    spacer(),
    H(1, "7. Partage réseau (Serveur de fichiers)"),
    hr(),
    P(
        "Un partage réseau <b>\\\\SRV-INFRA\\partage</b> est créé pour être utilisé comme lecteur "
        "réseau mappé via GPO. Les permissions sont configurées pour les utilisateurs du domaine."
    ),
    B("Dossier créé : C:\\partage sur SRV-INFRA"),
    B("Partage SMB activé avec les droits Lecture/Écriture pour les Utilisateurs authentifiés"),
    B("Chemin UNC : \\\\SRV-INFRA\\partage"),
]

# ── 8. UTILISATEURS ET GROUPES ────────────────────────────────────────────────
story += [
    spacer(),
    H(1, "8. Gestion des utilisateurs et groupes"),
    hr(),
    P("La structure organisationnelle (OU) du domaine bsc-lab.local est la suivante :"),
    table([
        ["Unité d'organisation (OU)", "Contenu"],
        ["Serveurs_BSC", "Objets ordinateurs serveurs du domaine"],
        ["Utilisateurs_BSC", "Comptes utilisateurs (ex. Ilyas Seddiki)"],
        ["Groupes_BSC", "Groupes de sécurité (ex. Techniciens_Datacenter)"],
    ], col_widths=[6*cm, 10*cm]),
    spacer(0.3),
    P(
        "L'utilisateur <b>Ilyas Seddiki</b> (login : ilyas.seddiki@bsc-lab.local) est créé dans l'OU "
        "Utilisateurs_BSC et ajouté au groupe de sécurité global <b>Techniciens_Datacenter</b>, "
        "lui conférant les droits d'accès aux partages et GPO associés."
    ),
]

# ── 9. GPO ────────────────────────────────────────────────────────────────────
story += [
    spacer(),
    H(1, "9. Stratégies de groupe (GPO)"),
    hr(),
    P(
        "Une GPO nommée <b>gpo_lecteur_reseau</b> est créée et liée au domaine bsc-lab.local. "
        "Elle monte automatiquement le lecteur réseau <b>Z:</b> sur <b>\\\\SRV-INFRA\\partage</b> "
        "à chaque ouverture de session utilisateur."
    ),
    table([
        ["Paramètre GPO", "Valeur"],
        ["Nom", "gpo_lecteur_reseau"],
        ["Liée à", "bsc-lab.local (domaine entier)"],
        ["Type de mappage", "Configuration utilisateur > Préférences > Mappages de lecteurs"],
        ["Lettre de lecteur", "Z:"],
        ["Chemin UNC", "\\\\SRV-INFRA\\partage"],
        ["Reconnexion", "Automatique à chaque session"],
    ], col_widths=[6*cm, 10*cm]),
]

# ── 10. TESTS ─────────────────────────────────────────────────────────────────
story += [
    spacer(),
    H(1, "10. Tests et vérifications"),
    hr(),
    P("Une série de tests valide l'ensemble des configurations réalisées."),

    H(2, "10.1 Jonction de SRV-AUTO au domaine"),
    P(
        "SRV-AUTO est jointe au domaine bsc-lab.local via les Propriétés système. "
        "Le DNS primaire de SRV-AUTO pointe sur SRV-INFRA (192.168.60.10) pour la résolution AD."
    ),

    H(2, "10.2 Tests DNS et connectivité"),
    table([
        ["Test", "Commande", "Résultat"],
        ["Résolution DNS", "ping bsc-lab.local", "→ 192.168.60.10 — 0% perte, < 1 ms"],
        ["Vérification DNS", "nslookup bsc-lab.local", "→ Serveur 192.168.60.10 — résolution OK"],
    ], col_widths=[4*cm, 5*cm, 7*cm]),

    H(2, "10.3 Validation du lecteur réseau par GPO"),
    P(
        "Après connexion d'un utilisateur du domaine sur SRV-AUTO, la GPO <b>gpo_lecteur_reseau</b> "
        "est appliquée et le lecteur <b>Z:</b> est automatiquement monté sur <b>\\\\SRV-INFRA\\partage</b> "
        "(106 Go disponibles). La reconnexion automatique est active."
    ),
    spacer(),
    Paragraph(
        "✓ Tous les tests sont concluants — l'environnement Active Directory est pleinement opérationnel.",
        style("ok", "Normal", fontSize=9.5, textColor=colors.HexColor("#059669"),
              leading=14, fontName="Helvetica-Bold", spaceBefore=4)
    ),
]

# ── BUILD ─────────────────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF généré : {OUTPUT}")
