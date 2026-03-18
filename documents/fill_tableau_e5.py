"""
Remplit le tableau de synthèse E5 BTS SIO avec les réalisations du portfolio Ilyas Seddiki.
"""
import sys, copy
sys.stdout.reconfigure(encoding='utf-8')

from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P
from odf import teletype

ODS_IN  = "C:/Users/seddi/Documents/PORTFOLIO/ilyasseddiki.github.io/documents/8 - EPREUVE ORALE E5 - MODELE DE TABLEAU DE SYNTHESE ANNEXE VI-1 - BTS SIO 2026.ods"
ODS_OUT = "C:/Users/seddi/Documents/PORTFOLIO/ilyasseddiki.github.io/documents/Tableau_Synthese_E5_Seddiki_Ilyas.ods"

# ── Données ────────────────────────────────────────────────────────────────────
# Colonnes compétences : C2=Gérer, C3=Répondre, C4=Présence, C5=Projet, C6=Service, C7=DévPro
# Numérotation par priorité décroissante. Si 2 compétences à égalité → toutes deux ont "1".

FORMATIONS = [
    # (description, période, C2, C3, C4, C5, C6, C7)
    (
        "TPs Réseau & Système — Configuration d'un serveur web Apache2 (Linux), "
        "mise en place d'un pare-feu pfSense (filtrage, NAT), déploiement de "
        "tunnels VPN (site à site et nomade), installation d'un serveur VoIP "
        "Asterisk (téléphonie IP), création et tests de volumes RAID 1 & RAID 5 "
        "(mdadm).\nDocuments : rapports de TP avec captures d'écran",
        "2024 / 2025",
        #  C2   C3   C4  C5   C6   C7
           "2", "3", "", "", "1", "3"
        # 1=Mettre à dispo (déployer les services) · 2=Gérer patrimoine · 3=Répondre/DévPro
    ),
    (
        "TP GLPI — Déploiement et configuration d'un serveur GLPI pour la gestion "
        "de parc informatique et la gestion des tickets d'assistance. Intégration "
        "des postes, création de catégories d'incidents et suivi des demandes.\n"
        "Document : rapport de TP avec captures d'écran",
        "2024 / 2025",
        #  C2   C3   C4  C5   C6   C7
           "1", "2", "", "", "1", ""
        # 1 ET 1 → Gérer patrimoine ET Mettre à dispo sont co-prioritaires (GLPI = outil de parc)
        # 2 → Répondre incidents (gestion tickets)
    ),
]

STAGE_1AN = []  # Aucun stage 1ère année documenté dans le portfolio

STAGE_2AN = [
    (
        "Monitoring EcoStruxure APC — Recensement, adressage IP et configuration "
        "de 41 équipements de distribution électrique (onduleurs UPS et PDU APC, "
        "EATON, VERTIV, HPE) répartis sur 16 racks du datacenter TD SYNNEX BSC. "
        "Câblage réseau, intégration à la gateway EcoStruxure IT, déploiement de "
        "la supervision centralisée avec alertes temps réel, puis modélisation 3D "
        "du datacenter via EcoStruxure IT Advisor (VM Rocky Linux 8.10 sous Hyper-V).\n"
        "Documents : portfolio en ligne — ilyasseddiki.github.io",
        "01/02/2026 au 28/03/2026",
        #  C2   C3   C4  C5   C6   C7
           "1", "3", "", "2", "1", "3"
        # 1 ET 1 → Gérer patrimoine (41 équipements) ET Mettre à dispo (monitoring déployé)
        # 2 → Travailler en mode projet (4 phases)
        # 3 → Répondre incidents (alertes) · Organiser dév pro (veille/salon)
    ),
    (
        "Déploiement Solution Cisco IA — Réception et vérification du matériel "
        "réseau Cisco IA (2× Nexus 9300-FX3, 3× UCS C220 M8, câblage fibre MPO). "
        "Création d'un inventaire structuré sous Excel (référence, numéro de série, "
        "emplacement). Déballage méthodique, tri et rackage dans une baie 42U selon "
        "le plan d'implantation fourni, avec contrôle de conformité final.\n"
        "Documents : inventaire_cisco_ia.xlsx, portfolio en ligne",
        "01/02/2026 au 28/03/2026",
        #  C2   C3   C4  C5   C6   C7
           "1", "", "", "2", "2", ""
        # 1 → Gérer patrimoine (inventaire matériel, gestion physique des actifs)
        # 2 ET 2 → Travailler projet (3 phases) ET Mettre à dispo (intégration en baie)
    ),
    (
        "Infrastructure Active Directory — Serveur Lenovo ThinkSystem SR645 — "
        "Déploiement d'un environnement virtualisé Hyper-V : création d'un "
        "commutateur virtuel externe et de 2 VMs Windows Server 2025 (SRV-INFRA "
        "et SRV-AUTO). Configuration des rôles : AD DS (forêt bsc-lab.local, DNS "
        "intégré), DHCP (étendue LAN-BSC-LAB 192.168.60.100–200/24), AD CS (PKI "
        "entreprise SHA256 RSA 2048). Création d'OUs, comptes utilisateurs, groupes "
        "de sécurité et GPO (mappage lecteur réseau Z:). Tests de jonction au "
        "domaine, ping, nslookup et validation du lecteur GPO.\n"
        "Document : Compte_rendu_Serveur_Lenovo_SR645_AD.pdf",
        "01/02/2026 au 28/03/2026",
        #  C2   C3   C4  C5   C6   C7
           "1", "3", "", "2", "1", ""
        # 1 ET 1 → Gérer patrimoine (VMs, AD, comptes) ET Mettre à dispo (AD DS, DHCP, AD CS, GPO)
        # 2 → Travailler projet (5 phases structurées)
        # 3 → Répondre incidents (tests de validation)
    ),
    (
        "Interventions techniques & Développement professionnel — "
        "Comptes rendus rédigés : installation caméra Axis V5915 PTZ (mise en "
        "réseau, stockage, flux OBS), mise à jour firmware NMC2 sur PDU APC AP8959 "
        "(résolution corruption applicative), mise en service switch Aruba 3810M "
        "(paramétrage, sécurisation SSH), installation IT Advisor (supervision "
        "avancée et capacity planning datacenter).\n"
        "Sortie professionnelle : Salon IT Expert — La Défense Arena (conférences "
        "infrastructure IT, cloud, cybersécurité, acteurs du secteur).\n"
        "Documents : 5 comptes rendus PDF, portfolio en ligne",
        "01/02/2026 au 28/03/2026",
        #  C2   C3   C4  C5   C6   C7
           "2", "1", "", "", "2", "3"
        # 1 → Répondre incidents (4 CRs = interventions techniques pures)
        # 2 ET 2 → Gérer patrimoine (maintenance équipements) ET Mettre à dispo (remise en service)
        # 3 → Organiser dév pro (salon IT Expert, veille)
    ),
]

# ── Helpers ────────────────────────────────────────────────────────────────────
def get_col_styles(row, max_col=8):
    """Récupère le style de chaque colonne (0..max_col+1)."""
    styles = {}
    col = 0
    for cell in row.getElementsByType(TableCell):
        rep = int(cell.getAttribute('numbercolumnsrepeated') or 1)
        style = cell.getAttribute('stylename')
        for i in range(rep):
            if col + i not in styles:
                styles[col + i] = style
        col += rep
    return styles

def set_text(cell, text):
    """Ajoute le texte dans une cellule (gère les sauts de ligne)."""
    for line in text.split('\n'):
        cell.addElement(P(text=line))

def fill_data_row(row, desc, period, c2, c3, c4, c5, c6, c7):
    """Remplace les cellules d'une ligne de données avec les nouvelles valeurs."""
    styles = get_col_styles(row, max_col=9)

    # Supprimer toutes les cellules existantes
    for child in list(row.childNodes):
        row.removeChild(child)

    comps = [c2, c3, c4, c5, c6, c7]

    # Col 0 – Description
    cell0 = TableCell(stylename=styles.get(0))
    set_text(cell0, desc)
    row.addElement(cell0)

    # Col 1 – Période
    cell1 = TableCell(stylename=styles.get(1))
    if period:
        cell1.addElement(P(text=period))
    row.addElement(cell1)

    # Cols 2-7 – Compétences
    for ci, txt in enumerate(comps):
        c = TableCell(stylename=styles.get(2 + ci))
        if txt:
            c.addElement(P(text=txt))
        row.addElement(c)

    # Fin de ligne (cellules vides répétées)
    rest = TableCell(stylename=styles.get(8), numbercolumnsrepeated="16376")
    row.addElement(rest)

def set_cell_text_in_row(row, col_target, new_text):
    """Modifie le texte d'une cellule simple (non-répétée) à la position col_target."""
    col = 0
    for cell in row.getElementsByType(TableCell):
        rep = int(cell.getAttribute('numbercolumnsrepeated') or 1)
        if rep == 1 and col == col_target:
            for p in cell.getElementsByType(P):
                cell.removeChild(p)
            cell.addElement(P(text=new_text))
            return
        col += rep

# ── Remplissage ────────────────────────────────────────────────────────────────
doc = load(ODS_IN)
sheet = doc.spreadsheet.getElementsByType(Table)[0]
rows  = sheet.getElementsByType(TableRow)

# Infos candidat
set_cell_text_in_row(rows[2], 0, "NOM et prénom : SEDDIKI Ilyas")
# Cocher SISR (remplacer ▢ par ☑)
for cell in rows[3].getElementsByType(TableCell):
    txt = teletype.extractText(cell).strip()
    if "SISR" in txt:
        for p in cell.getElementsByType(P):
            cell.removeChild(p)
        cell.addElement(P(text="☑ SISR"))
# URL portfolio
for cell in rows[4].getElementsByType(TableCell):
    txt = teletype.extractText(cell).strip()
    if "portfolio" in txt.lower():
        for p in cell.getElementsByType(P):
            cell.removeChild(p)
        cell.addElement(P(text="Adresse URL du portfolio : https://ilyasseddiki.github.io"))

# Lignes de formations (R8, R9)
formation_row_indices = [8, 9]
for i, data in enumerate(FORMATIONS):
    if i < len(formation_row_indices):
        fill_data_row(rows[formation_row_indices[i]], *data)

# Lignes stage 2ème année (R13, R14, R15, R16)
stage2_row_indices = [13, 14, 15, 16]
for i, data in enumerate(STAGE_2AN):
    if i < len(stage2_row_indices):
        fill_data_row(rows[stage2_row_indices[i]], *data)

# Sauvegarder
doc.save(ODS_OUT)
print(f"ODS enregistré : {ODS_OUT}")
