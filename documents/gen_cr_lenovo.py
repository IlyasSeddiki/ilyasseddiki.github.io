import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, Image as RLImage
)

OUT  = "Compte_rendu_Serveur_Lenovo_SR645_AD.pdf"
IMGS = "C:/Users/seddi/Documents/PORTFOLIO/ilyasseddiki.github.io/documents/imgs_temp"

doc = SimpleDocTemplate(OUT, pagesize=A4,
    topMargin=2*cm, bottomMargin=2*cm,
    leftMargin=2.5*cm, rightMargin=2.5*cm)

W = A4[0] - 5*cm   # zone texte

# ── styles ────────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def sty(name, parent="Normal", **kw):
    return ParagraphStyle(name, parent=base[parent], **kw)

S = {
    "cover_title" : sty("ct", "Title",   fontSize=20, leading=24,
                         textColor=colors.HexColor("#0f172a"), spaceAfter=6),
    "cover_sub"   : sty("cs", "Normal",  fontSize=11,
                         textColor=colors.HexColor("#475569"), alignment=TA_CENTER, spaceAfter=4),
    "cover_meta"  : sty("cm", "Normal",  fontSize=9.5,
                         textColor=colors.HexColor("#64748b"), alignment=TA_CENTER),
    "h1"          : sty("h1", "Heading1",fontSize=12, fontName="Helvetica-Bold",
                         textColor=colors.HexColor("#1d4ed8"),
                         spaceBefore=16, spaceAfter=4, leading=15),
    "caption"     : sty("cap","Normal",  fontSize=9.5,
                         textColor=colors.HexColor("#1e293b"),
                         leading=13, spaceAfter=10),
}

def hr():
    return HRFlowable(width="100%", thickness=0.6,
                      color=colors.HexColor("#cbd5e1"), spaceAfter=6)

def sp(h=0.3):
    return Spacer(1, h*cm)

def section(title):
    return [Paragraph(title, S["h1"]), hr()]

def shot(fname, caption):
    """Image centrée dans un tableau 1×1 bordure noire + légende."""
    path = os.path.join(IMGS, fname)
    img  = RLImage(path)

    # mise à l'échelle : max W×12cm en conservant ratio
    max_w, max_h = W, 12*cm
    ratio = img.imageWidth / img.imageHeight
    if img.imageWidth / max_w > img.imageHeight / max_h:
        iw, ih = max_w, max_w / ratio
    else:
        ih, iw = max_h, max_h * ratio
    img._restrictSize(iw, ih)

    tbl = Table([[img]], colWidths=[W])
    tbl.setStyle(TableStyle([
        ("BOX",        (0,0), (-1,-1), 1,   colors.black),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
    ]))
    return [tbl, Paragraph(caption, S["caption"]), sp(0.2)]

# ── construction ──────────────────────────────────────────────────────────────
story = []

# PAGE DE GARDE
story += [
    sp(3.5),
    Paragraph("Compte Rendu d'Activité", S["cover_sub"]),
    sp(0.4),
    Paragraph("Serveur Lenovo ThinkSystem SR645", S["cover_title"]),
    Paragraph("Mise en place d'un environnement Active Directory<br/>sous Windows Server 2025", S["cover_sub"]),
    sp(0.6),
    HRFlowable(width="50%", thickness=2, color=colors.HexColor("#1d4ed8"), hAlign="CENTER"),
    sp(0.8),
    Paragraph("Ilyas Seddiki &nbsp;|&nbsp; TD SYNNEX — BSC-LAB &nbsp;|&nbsp; Mars 2026", S["cover_meta"]),
    PageBreak(),
]

# 1. HYPER-V
story += section("1. Installation et configuration de Hyper-V")
story += shot("img_01.png",
    "Sélection du rôle Hyper-V et des Services de fichiers dans l'assistant d'ajout de rôles "
    "sur SRV-ILYAS — ce rôle transforme le serveur en hyperviseur de type 1.")
story += shot("img_04.png",
    "Interface du Gestionnaire Hyper-V après installation — SRV-ILYAS est enregistré "
    "comme hôte de virtualisation.")
story += shot("img_05.png",
    "Création d'un commutateur virtuel de type Externe dans le Gestionnaire Hyper-V, "
    "lié à la carte réseau physique pour donner aux VMs un accès au réseau.")

# 2. VMs
story += section("2. Création des machines virtuelles")
story += shot("img_02.png",
    "Création de la VM SRV-INFRA dans l'assistant Hyper-V — nom "
    "\"Infrastructure\" défini, stockée dans le répertoire par défaut.")
story += shot("img_03.png",
    "Configuration du disque virtuel dynamique SRV-INFRA.vhdx de 127 Go — "
    "le fichier ne grossit que lorsque des données y sont écrites.")
story += shot("img_07.png",
    "Carte réseau de SRV-AUTO connectée au commutateur virtuel vSwitch-External "
    "pour communiquer avec SRV-INFRA et accéder aux services du domaine.")

# 3. AD DS
story += section("3. Déploiement de l'Active Directory (AD DS)")
story += shot("img_06.png",
    "Configuration de déploiement AD DS — ajout d'une nouvelle forêt avec le "
    "domaine racine bsc-lab.local sur SRV-INFRA.")
story += shot("img_08.png",
    "Options du contrôleur de domaine — niveau fonctionnel Windows Server 2025, "
    "DNS intégré et Catalogue Global activés.")
story += shot("img_09.png",
    "Vérification de la configuration AD DS — toutes les conditions sont "
    "satisfaites, le serveur est prêt pour la promotion.")
story += shot("img_10.png",
    "Commande Get-ADDomain confirmant la création du domaine bsc-lab.local "
    "avec SRV-INFRA comme contrôleur principal (PDCEmulator).")

# 4. DHCP
story += section("4. Configuration du DHCP")
story += shot("img_11.png",
    "Console DHCP ouverte sur srv-infra.bsc-lab.local — "
    "une étendue IPv4 doit être créée pour distribuer les adresses IP.")
story += shot("img_12.png",
    "Autorisation du serveur DHCP dans l'Active Directory "
    "avec le compte BSC-LAB\\Administrateur.")
story += shot("img_14.png",
    "Nom de l'étendue DHCP défini : LAN-BSC-LAB.")
story += shot("img_15.png",
    "Plage d'adresses IP configurée : 192.168.60.100 à 192.168.60.200, "
    "masque /24 (255.255.255.0).")
story += shot("img_17.png",
    "Console DHCP — étendue LAN-BSC-LAB [192.168.60.0] créée, "
    "autorisée et active.")

# 5. AD CS
story += section("5. Configuration de l'autorité de certification (AD CS)")
story += shot("img_18.png",
    "Lancement de la configuration AD CS avec les informations "
    "d'identification BSC-LAB\\Administrateur.")
story += shot("img_19.png",
    "Type d'installation sélectionné : Autorité de certification d'entreprise "
    "(intégrée à l'Active Directory).")
story += shot("img_20.png",
    "Type d'AC sélectionné : Autorité de certification racine, "
    "première AC de la hiérarchie PKI.")
story += shot("img_22.png",
    "Nom commun de l'autorité de certification défini : "
    "bsc-lab-SRV-INFRA-CA.")
story += shot("img_25.png",
    "Page de confirmation avant configuration — algorithme SHA256, "
    "clé RSA 2048 bits, validité 5 ans.")
story += shot("img_26.png",
    "Configuration AD CS terminée avec succès — l'autorité de "
    "certification est opérationnelle sur SRV-INFRA.")

# 6. NTP
story += section("6. Synchronisation NTP")
story += shot("img_27.png",
    "Commande w32tm /query /status sur SRV-INFRA — "
    "la synchronisation NTP est active et à jour (05/03/2026 16:11:09).")

# 7. OUs / utilisateurs / groupes
story += section("7. Gestion des OUs, utilisateurs et groupes")
story += shot("img_34.png",
    "Création de l'unité d'organisation (OU) \"Serveurs\" "
    "dans le domaine bsc-lab.local.")
story += shot("img_35.png",
    "Création de l'OU \"Utilisateurs_BSC\" pour regrouper "
    "les comptes utilisateurs du domaine.")
story += shot("img_36.png",
    "Création de l'OU \"Groupes_BSC\" pour héberger "
    "les groupes de sécurité du domaine.")
story += shot("img_37.png",
    "Création du compte utilisateur Ilyas Seddiki avec le login "
    "iseddiki@bsc-lab.local dans l'OU Utilisateurs_BSC.")
story += shot("img_39.png",
    "Console ADUC — utilisateur Ilyas Seddiki présent dans l'OU "
    "Utilisateurs_BSC, structure des OUs complète et conforme.")
story += shot("img_40.png",
    "Création du groupe de sécurité global \"Techniciens_Datacenter\" "
    "dans l'OU Groupes_BSC.")
story += shot("img_41.png",
    "Propriétés du groupe Techniciens_Datacenter — "
    "Ilyas Seddiki ajouté comme membre.")

# 8. GPO
story += section("8. Stratégie de groupe (GPO)")
story += shot("img_28.png",
    "Création de la GPO \"gpo_lecteur_reseau\" liée "
    "au domaine bsc-lab.local dans la console Gestion de stratégie de groupe.")
story += shot("img_29.png",
    "Éditeur GPO — section Mappages de lecteurs dans "
    "Configuration utilisateur > Préférences > Paramètres Windows.")
story += shot("img_30.png",
    "Configuration du lecteur réseau Z: pointant vers "
    "\\\\SRV-INFRA\\partage avec reconnexion automatique à chaque session.")

# 9. TESTS
story += section("9. Tests et vérifications")
story += shot("img_31.png",
    "Jonction de SRV-AUTO au domaine bsc-lab.local via les "
    "Propriétés système — confirme que DNS, AD DS et DHCP fonctionnent ensemble.")
story += shot("img_33.png",
    "Tests ping et nslookup sur bsc-lab.local depuis SRV-AUTO — "
    "résolution DNS correcte vers 192.168.60.10, 0% de perte.")
story += shot("img_32.png",
    "Explorateur Windows sur SRV-AUTO — lecteur réseau Z: "
    "(\\\\SRV-INFRA\\partage, 106 Go libres) monté automatiquement par la GPO.")

doc.build(story)
print(f"PDF généré : {OUT}")
