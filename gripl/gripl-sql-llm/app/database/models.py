from sqlalchemy import Column, String, Text, ForeignKey, Integer, Boolean, Date, Table
from sqlalchemy.orm import relationship
from .db import Base

verarbeitung_frist = Table(
    "verarbeitung_frist",
    Base.metadata,
    Column("verarbeitungstaetigkeit_id", Integer, ForeignKey("verarbeitungstaetigkeiten.id"), primary_key=True),
    Column("frist_id", Integer, ForeignKey("aufbewahrungsfrist.id"), primary_key=True)
)

#### Rechtlicher Auslöser <-> Pflichten Join ####
# in Tabelle Rechtlicher auslöse alle unterschiedlichen Sachen/ Szenarien gespeichert werden muss -> und darausfolgenden Pflichten für den Auslöser ?

class RechtlicherAusloeser(Base):
    __tablename__ = "rechtlicher_ausloeser"
    id = Column(Integer, primary_key=True)
    ausloeser = Column(String(255), nullable=False)
    article_number = Column(String(255), nullable=False)
    absatz_number = Column(String(255), nullable=False)
    literature = Column(String(255), nullable=False)
    pflichten = relationship(
        "Pflicht",
        secondary="rechtlicher_ausloeser_pflicht",
        back_populates="rechtlicher_ausloeser"
    )
    bedingungen = relationship(
        "Bedingung",
        secondary="rechtlicher_ausloeser_bedingung",
        back_populates="rechtliche_ausloeser"
    )

class RechtlicherAusloeserPflicht(Base):
    __tablename__ = "rechtlicher_ausloeser_pflicht"

    rechtlicher_ausloeser_id = Column(
        Integer,
        ForeignKey("rechtlicher_ausloeser.id"),
        primary_key=True,
        nullable=False
    )
    pflicht_id = Column(
        Integer,
        ForeignKey("pflicht.id"),
        primary_key=True,
        nullable=False
    )

#### Akteur <-> Aufgaben Join ####
#### Akteure <-> Pflichten Join ####
#### Akteure <-> Recht Join ####

recht_akteur = Table(
    "recht_akteur",
    Base.metadata,
    Column("recht_id", Integer, ForeignKey("recht.id"), primary_key=True),
    Column("akteur_id", Integer, ForeignKey("dsgvo_akteur.id"), primary_key=True)
)

class DSGVOAkteur(Base):
    __tablename__ = "dsgvo_akteur"

    id = Column(Integer, primary_key=True, index=True)
    akteur = Column(String(255), nullable=False)

    aufgaben = relationship("Aufgaben", back_populates="besitzer")

    pflichten = relationship(
        "Pflicht",
        back_populates="akteur"
    )

    einwilligungen_als_betroffener = relationship("Einwilligung", back_populates="betroffener")

    verhaltenskodizes = relationship(
        "VerhaltenskodexAkteur",
        back_populates="akteur",
        cascade="all, delete-orphan"
    )

    avv_rollen = relationship("AVVAkteur", back_populates="akteur")

    gemeinsame_verantwortlichkeit_rollen = relationship(
        "GemeinsameVerantwortlichkeitAkteur",
        back_populates="akteur"
    )

    datenpanne_rollen = relationship("DatenpanneAkteur", back_populates="akteur")

    rechte = relationship(
        "Recht",
        secondary=recht_akteur,
        back_populates="akteure"
    )

class Aufgaben(Base):
    __tablename__ = "aufgaben"

    id = Column(Integer, primary_key=True, index=True)
    beschreibung = Column(String(255))

    akteur_id = Column(Integer, ForeignKey("dsgvo_akteur.id"), nullable=False)

    besitzer = relationship("DSGVOAkteur", back_populates="aufgaben")



####  Verarbeitungstätigkeit <-> Zweck Join ####
####  Verarbeitungstätigkeit <-> Datenkategorie Join ####
#### Verarbeitungstätigkeit <-> TOM Join ####

class Verarbeitungstaetigkeit(Base):
    __tablename__ = "verarbeitungstaetigkeiten"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    name = Column(String(255), nullable=False)

    daten = relationship("PersonenbezogeneDaten", back_populates="verarbeitung")

    zwecke = relationship(
        "Zweck",
        back_populates="verarbeitung",
        cascade="all, delete"
    )

    personen = relationship("Person",
                            back_populates="verarbeitung",
                            cascade="all, delete"
                            )

    rechtsgrundlagen = relationship(
        "Rechtsgrundlage",
        secondary="verarbeitung_rechtsgrundlage",
        back_populates="verarbeitungen"
    )

    risiko_faktoren = relationship(
        "Risikofaktor",
        secondary="verarbeitung_risikofaktoren",
        back_populates="verarbeitungen"
    )

    dsfa = relationship(
        "DSFA",
        back_populates="verarbeitung",
        uselist=False,
        cascade="all, delete"
    )

    datenkategorie_assocs = relationship(
        "VerarbeitungZuDatenkategorie",
        back_populates="verarbeitung",
        cascade="all, delete-orphan"
    )

    tom_assocs = relationship(
        "VerarbeitungZuTOM",
        back_populates="verarbeitung",
        cascade="all, delete-orphan"
    )

    einwilligungen = relationship("Einwilligung", back_populates="verarbeitung")
    prinzipien = relationship(
        "GrundPrinzipienDSGVO",
        back_populates="verarbeitung",
        cascade="all, delete-orphan"
    )

    empfaengerkategorien = relationship(
        "VerarbeitungEmpfaengerkategorie",
        back_populates="verarbeitung",
        cascade="all, delete-orphan"
    )

    avvs = relationship("AuftragsVerarbeitungsVertrag", secondary="avv_verarbeitungstaetigkeit",
                        back_populates="verarbeitungstaetigkeiten")

    gemeinsame_verantwortlichkeiten = relationship(
        "GemeinsameVerantwortlichkeit",
        secondary="gemeinsame_verantwortlichkeit_verarbeitung",
        back_populates="verarbeitungstaetigkeiten"
    )

    datenpannen = relationship("Datenpanne", secondary="datenpanne_verarbeitung",
                               back_populates="verarbeitungstaetigkeiten")

    verarbeitungsform_id = Column(Integer, ForeignKey("verarbeitungsform.id"), nullable=True)
    verarbeitungsform = relationship("Verarbeitungsform", back_populates="verarbeitungstaetigkeiten")

    fristen = relationship(
        "Frist",
        secondary=verarbeitung_frist,
        back_populates="verarbeitungstaetigkeiten"
    )

    interne_personen_gruppen = relationship(
        "InternePersonenGruppen",
        secondary="interne_personen_gruppen_verarbeitung",
        back_populates="verarbeitungstaetigkeiten"
    )

    gruppen = relationship(
        "Gruppe",
        secondary="gruppe_verarbeitungstaetigkeit",
        back_populates="verarbeitungstaetigkeiten"
    )


class Zweck(Base):
    __tablename__ = "zweck"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    verarbeitung_id = Column(
        Integer,
        ForeignKey("verarbeitungstaetigkeiten.id"),
        nullable=False
    )

    verarbeitung = relationship(
        "Verarbeitungstaetigkeit",
        back_populates="zwecke"
    )

    aufbewahrungsfristen = relationship(
        "Frist",
        secondary="aufbewahrungsfrist_zweck",
        back_populates="zwecke"
    )

#### Grundprinzipien <-> Pflicht Join ###ä#

class GrundPrinzipienDSGVO(Base):
    __tablename__ = "grund_prinzipien_dsgvo"
    id = Column(Integer, primary_key=True, index=True)
    prinzip = Column(String(255), nullable=False)
    article_number = Column(String(255), nullable=False)
    absatz_number = Column(String(255), nullable=False)
    literature = Column(String(255), nullable=False)
    beschreibung = Column(Text, nullable=False)

    verarbeitungen = relationship(
        "Verarbeitungstaetigkeit",
        back_populates="grund_prinzip",
        cascade="all, delete-orphan"
    )

    verhaltenskodizes = relationship(
        "VerhaltenskodexPrinzip",
        back_populates="prinzip",
        cascade="all, delete-orphan"
    )

    pflichten = relationship("Pflicht", secondary="pflicht_grundprinzip", back_populates="grundprinzipien")

class PflichtGrundprinzip(Base):
    __tablename__ = "pflicht_grundprinzip"
    pflicht_id = Column(Integer, ForeignKey("pflicht.id"), primary_key=True)
    grundprinzip_id = Column(Integer, ForeignKey("grund_prinzipien_dsgvo.id"), primary_key=True)

class EmpfaengerKategorie(Base):
    __tablename__ = "empfaenger_kategorie"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)


class VerarbeitungEmpfaengerkategorie(Base):
    __tablename__ = "verarbeitung_empfaengerkategorie"

    verarbeitung_id = Column(Integer, ForeignKey("verarbeitungstaetigkeiten.id", ondelete="CASCADE"), primary_key=True)
    empfaengerkategorie_id = Column(Integer, ForeignKey("empfaenger_kategorie.id", ondelete="CASCADE"), primary_key=True)
    kommentar = Column(Text, nullable=True)

    verarbeitung = relationship("Verarbeitungstätigkeit", back_populates="empfaengerkategorien")
    empfaengerkategorie = relationship("Empfaengerkategorie", back_populates="verarbeitungen")

#### Rechtsgrundlage <-> Verarbeitungstätigkeit Join ####
#### Rechtsgrundlage <-> Pflichten Join ####
#### Rechtsgrundlage <-> Rechte betroffener Person ####

class VerarbeitungRechtsgrundlage(Base):
    __tablename__ = "verarbeitung_rechtsgrundlage"

    verarbeitung_id = Column(
        Integer,
        ForeignKey("verarbeitungstaetigkeiten.id"),
        primary_key=True
    )

    rechtsgrundlage_id = Column(
        Integer,
        ForeignKey("rechtsgrundlage.id"),
        primary_key=True
    )

class Rechtsgrundlage(Base):
    __tablename__ = "rechtsgrundlage"
    id = Column(Integer, primary_key=True, index=True)
    rechts_grundlage = Column(String(255), nullable=False)
    artikel_number =Column(Integer, nullable=False)
    absatz_number = Column(Integer, nullable=False)
    literature = Column(String(255), nullable=False)
    verarbeitungen = relationship(
        "Verarbeitungstaetigkeit",
        secondary="verarbeitung_rechtsgrundlage",
        back_populates="rechtsgrundlagen"
    )

    pflichten = relationship(
        "Pflicht",
        secondary="rechtsgrundlage_pflicht",
        back_populates="rechtsgrundlagen"
    )


    voraussetzung = relationship("Voraussetzung", back_populates="rechtsgrundlage")
    einwilligungen = relationship("Einwilligung", back_populates="rechtsgrundlage")

#### Pflicht <-> Grundprinzip Join ####
#### Pflicht <-> Kategory Join ####
#### Pflicht <-> technische organisatorische Masnahmen Join ####

class Pflicht(Base):
    __tablename__ = "pflicht"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    beschreibung = Column(Text)
    artikel_number = Column(String(50))
    absatz_number = Column(String(50))
    literature = Column(String(50))

    rechtsgrundlagen = relationship(
        "Rechtsgrundlage",
        secondary="rechtsgrundlage_pflicht",
        back_populates="pflichten"
    )

    akteur_id = Column(
        Integer,
        ForeignKey("dsgvo_akteur.id"),
        nullable=False
    )

    akteur = relationship(
        "DSGVOAkteur",
        back_populates="pflichten"
    )

    rechte = relationship(
        "Recht",
        secondary="recht_pflicht",
        back_populates="pflichten"
    )

    rechtlicher_ausloeser = relationship(
        "RechtlicherAusloeser",
        secondary="rechtlicher_ausloeser_pflicht",
        back_populates="pflichten"
    )

    verhaltenskodizes = relationship(
        "VerhaltenskodexPflicht",
        back_populates="pflicht",
        cascade="all, delete-orphan"
    )

    avvs = relationship("AuftragsVerarbeitungsVertrag", secondary="avv_pflichten", back_populates="pflichten")

    gemeinsame_verantwortlichkeiten = relationship(
        "GemeinsameVerantwortlichkeit",
        secondary="gemeinsame_verantwortlichkeit_pflichten",
        back_populates="pflichten"
    )

    datenpannen = relationship("Datenpanne", secondary="datenpanne_pflichten", back_populates="pflichten")

    ausnahmen = relationship(
        "Ausnahme",
        secondary="ausnahme_pflicht",
        back_populates="pflichten"
    )

    bedingungen = relationship(
        "Bedingung",
        secondary="pflicht_bedingung",
        back_populates="pflichten"
    )

    tomassnahmen = relationship("TechnischeOrganisatorischMasnahmen", secondary="pflicht_tom", back_populates="pflichten")

    grundprinzipien = relationship("GrundPrinzipienDSGVO", secondary="pflicht_grundprinzip", back_populates="pflichten")
    kategorie_id = Column(Integer, ForeignKey("pflichtenkategorie.id"), nullable=True)
    kategorie = relationship("Pflichtenkategorie", back_populates="pflichten")


class Pflichtenkategorie(Base):
    __tablename__ = "pflichtenkategorie"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    beschreibung = Column(Text, nullable=True)

    pflichten = relationship("Pflicht", back_populates="kategorie")

class PflichtBedingung(Base):
    __tablename__ = "pflicht_bedingung"

    pflicht_id = Column(Integer, ForeignKey("pflicht.id"), primary_key=True, nullable=False)
    bedingung_id = Column(Integer, ForeignKey("bedingung.id"), primary_key=True, nullable=False)


class PflichtTOM(Base):
    __tablename__ = "pflicht_tom"
    pflicht_id = Column(Integer, ForeignKey("pflicht.id"), primary_key=True)
    tom_id = Column(Integer, ForeignKey("technische_organisatorisch_masnahmen.id"), primary_key=True)

#### Recht <-> Ausnahme Join ####

class Recht(Base):
    __tablename__ = "recht"
    id = Column(Integer, primary_key=True)
    recht = Column(String(255), nullable=False)
    erklaerung = Column(Text)
    artikel_number = Column(String(50))
   # absatz_number = Column(String(50))
  #  literature = Column(String(50))

    pflichten = relationship(
        "Pflicht",
        secondary="recht_pflicht",
        back_populates="rechte"
    )


    akteure = relationship(
        "DSGVOAkteur",
        secondary=recht_akteur,
        back_populates="rechte"
    )

    bedingungen = relationship("Bedingung", secondary="recht_bedingung", back_populates="rechte")
    ausnahmen = relationship("Ausnahme", secondary="recht_ausnahme", back_populates="rechte")


class RechtAusnahme(Base):
    __tablename__ = "recht_ausnahme"

    recht_id = Column(Integer, ForeignKey("recht.id"), primary_key=True, nullable=False)
    ausnahme_id = Column(Integer, ForeignKey("ausnahme.id"), primary_key=True, nullable=False)

class Voraussetzung(Base):
    __tablename__ = "voraussetzung"
    id = Column(Integer, primary_key=True, index=True)
    beschreibung = Column(String(500), nullable=False)
    typ = Column(String(50), nullable=False)

    rechtsgrundlage_id = Column(Integer, ForeignKey("rechtsgrundlage.id"))
    rechtsgrundlage = relationship("Rechtsgrundlage", back_populates="voraussetzung")

class Einwilligung(Base):
    __tablename__ = "einwilligung"
    id = Column(Integer, primary_key=True, index=True)
    einwilligung = Column(String(500), nullable=False)

    rechtsgrundlage_id = Column(Integer, ForeignKey("rechtsgrundlage.id"))
    verarbeitungstaetigkeit_id = Column(Integer, ForeignKey("verarbeitungstaetigkeiten.id"))
    akteur_id = Column(Integer, ForeignKey("dsgvo_akteur.id"))

class RechtPflicht(Base):
    __tablename__ = "recht_pflicht"

    recht_id = Column(
        Integer,
        ForeignKey("recht.id"),
        primary_key=True
    )

    pflicht_id = Column(
        Integer,
        ForeignKey("pflicht.id"),
        primary_key=True
    )


class RechtsgrundlagePflicht(Base):
    __tablename__ = "rechtsgrundlage_pflicht"

    rechtsgrundlage_id = Column(
        Integer,
        ForeignKey("rechtsgrundlage.id"),
        primary_key=True
    )

    pflicht_id = Column(
        Integer,
        ForeignKey("pflicht.id"),
        primary_key=True
    )


class DSGVODatenKategorie(Base):
    __tablename__ = "dsgvo_datenkategorie"
    id = Column(Integer, primary_key=True)
    category = Column(String(255), nullable=False)
    is_sensible = Column(Boolean)
    verarbeitung_assocs = relationship("VerarbeitungZuDatenkategorie", back_populates="datenkategorie")

    aufbewahrungsfristen = relationship(
        "Frist",
        secondary="aufbewahrungsfrist_datenkategorie",
        back_populates="datenkategorien"
    )

class VerarbeitungZuDatenkategorie(Base):
    __tablename__ = "verarbeitung_zu_datenkategorie"

    verarbeitung_id = Column(Integer, ForeignKey("verarbeitungstaetigkeiten.id"), primary_key=True)
    datenkategorie_id = Column(Integer, ForeignKey("dsgvo_datenkategorie.id"), primary_key=True)
    aufbewahrungsfrist_id = Column(Integer, ForeignKey("aufbewahrungsfrist.id"))

#### Sichheitsmassnahmen Schutzziel Join ####
#### Sichheitsmasnahmen Übermittlung Join ####

class Sicherheitsmasnahme(Base):
    __tablename__ = "sicherheitsmasnahme"
    id = Column(Integer, primary_key=True)
    masnahme = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False) # technisch oder organisatorisch und gibt es noch mehr ?
    artikel_number = Column(String(50))
    absatz_number = Column(String(50))
    literature = Column(String(50))

    schutzziele_assocs = relationship("SicherheitsmassnahmenSchutzziel", back_populates="sicherheitsmassnahme")

class Sicherheitsniveau(Base):
    __tablename__ = "sicherheitsniveau"
    id = Column(Integer, primary_key=True)
    niveau = Column(String(255), nullable=False)


class SicherheitsmassnahmenSchutzziel(Base):
    __tablename__ = "sicherheitsmassnahmen_schutzziel"
    fk_sicherheitsmassnahmen_id = Column(Integer, ForeignKey("sicherheitsmasnahme.id", ondelete="CASCADE"), primary_key=True)
    fk_schutzziel_id = Column(Integer, ForeignKey("schutzziel.id", ondelete="CASCADE"), primary_key=True)

    sicherheitsmassnahme = relationship("Sicherheitsmassnahme", back_populates="schutzziele_assocs")
    schutzziel = relationship("SchutzZiel", back_populates="sicherheitsmassnahmen_assocs")


#### Verstoss <-> Pflichten Join ####
#### Verstoss <-> Sanktionen Join ####

class Verstoss(Base):
    __tablename__ = "verstoss"

    id = Column(Integer, primary_key=True)

    beschreibung = Column(Text)

    schweregrad = Column(String(50))
    vorsatz = Column(Boolean)


class Sanktion(Base):
    __tablename__ = "sanktion"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    typ = Column(String(50), nullable=False)  # 'Verwarnung', 'Anordnung', 'Aussetzung', 'Geldbuße', 'Schadensersatz'
    beschreibung = Column(Text, nullable=False)
    artikel_number = Column(String(50))
    absatz_number = Column(String(50))
    literature = Column(String(50))

    verstoesse = relationship("Verstoss", secondary="sanktion_verstoss", back_populates="sanktionen")


class SanktionVerstoss(Base):
    __tablename__ = "sanktion_verstoss"
    sanktion_id = Column(Integer, ForeignKey("sanktion.id"), primary_key=True)
    verstoss_id = Column(Integer, ForeignKey("verstoss.id"), primary_key=True)

class PflichtVerstoss(Base):
    __tablename__ = "pflicht_verstoss"

    pflicht_id = Column(
        Integer,
        ForeignKey("pflicht.id"),
        primary_key=True
    )

    verstoss_id = Column(
        Integer,
        ForeignKey("verstoss.id"),
        primary_key=True
    )

#### Verstoss <-> Strafe Join ####


class StrafenDSGVO(Base):
    __tablename__ = "dsgvo_strafen"
    id = Column(Integer, primary_key=True)
    strafe = Column(String(255), nullable=False)


class VerstossStrafe(Base):
    __tablename__ = "verstoss_strafe"

    verstoss_id = Column(
        Integer,
        ForeignKey("verstoss.id"),
        primary_key=True
    )

    strafe_id = Column(
        Integer,
        ForeignKey("dsgvo_strafen.id"),
        primary_key=True
    )


#### Risikofaktor <-> Verarbeitungstätigkeit Join ####

class Risikofaktor(Base):
    __tablename__ = "risikofaktoren"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    beschreibung = Column(String, nullable=True)
    gewichtung = Column(Integer, default=1)

    verarbeitungen = relationship(
        "Verarbeitungstaetigkeit",
        secondary="verarbeitung_risikofaktoren",
        back_populates="risiko_faktoren"
    )

    datenpannen = relationship("Datenpanne", secondary="datenpanne_risikofaktor", back_populates="risikofaktoren")


class VerarbeitungRisikofaktor(Base):
    __tablename__ = "verarbeitung_risikofaktoren"

    verarbeitung_id = Column(Integer, ForeignKey("verarbeitungstaetigkeiten.id"), primary_key=True)
    risikofaktor_id = Column(Integer, ForeignKey("risikofaktoren.id"), primary_key=True)

#### DSFA <-> Verarbeitungstätigkeit Join ####

class DSFA(Base):
    __tablename__ = "dsfas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    verarbeitung_id = Column(Integer, ForeignKey("verarbeitungstaetigkeiten.id"), unique=True)

    status = Column(String(50), default="In Prüfung")
    datum_erstellung = Column(Date)
    datum_letzte_pruefung = Column(Date)

    rest_risiko_stufe = Column(String(20))

    verarbeitung = relationship("Verarbeitungstaetigkeit", back_populates="dsfa")

    gemeinsame_verantwortlichkeiten = relationship(
        "GemeinsameVerantwortlichkeit",
        secondary="gemeinsame_verantwortlichkeit_dsfa",
        back_populates="dsfas"
    )


#### TOM <-> Sichherheitsziel Join ####

class SchutzZiel(Base):
    __tablename__ = "schutzziel"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    schutz_ziel = Column(String(255), nullable=False)
    tom_assocs = relationship("TOMZuSchutzZiel", back_populates="schutzziel")

    sicherheitsmassnahmen_assocs = relationship("SicherheitsmassnahmenSchutzziel", back_populates="schutzziel")


class TechnischeOrganisatorischMasnahmen(Base):
    __tablename__ = "technische_organisatorisch_masnahmen"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    masnahme = Column(String(255), nullable=False)
    beschreibung = Column(String, nullable=True)
    is_technical = Column(Boolean)

    verarbeitung_assocs = relationship("VerarbeitungZuTOM", back_populates="tom")
    schutzziele_assocs = relationship("TOMZuSchutzZiel", back_populates="tom")
    avvs = relationship("AuftragsVerarbeitungsVertrag", secondary="avv_tomassnahmen", back_populates="tomassnahmen")
    pflichten = relationship("Pflicht", secondary="pflicht_tom", back_populates="tomassnahmen")


class TOMZuSchutzZiel(Base):
    __tablename__ = "tom_zu_schutz_ziel"

    fk_tom_id = Column(
        Integer,
        ForeignKey("technische_organisatorisch_masnahmen.id", ondelete="CASCADE"),
        primary_key=True
    )
    fk_schutz_ziel_id = Column(
        Integer,
        ForeignKey("schutzziel.id", ondelete="CASCADE"),
        primary_key=True
    )

    tom = relationship("TechnischeOrganisatorischMasnahmen", back_populates="schutzziele_assocs")
    schutzziel = relationship("SchutzZiel", back_populates="tom_assocs")

class VerarbeitungZuTOM(Base):
    __tablename__ = "verarbeitung_zu_tom"

    verarbeitung_id = Column(Integer, ForeignKey("verarbeitungstaetigkeiten.id"), primary_key=True)
    tom_id = Column(Integer, ForeignKey("technische_organisatorisch_masnahmen.id"), primary_key=True)


class Frist(Base):
    __tablename__ = "aufbewahrungsfrist"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    beschreibung = Column(String(255), nullable=False)
    dauer_in_tagen = Column(Integer)
    article_number = Column(String(255), nullable=False)
    absatz_number = Column(String(255), nullable=False)
    literature = Column(String(255), nullable=False)

    zwecke = relationship("Zweck", secondary="aufbewahrungsfrist_zweck", back_populates="aufbewahrungsfristen")
    datenkategorien = relationship("DSGVODatenKategorie", secondary="aufbewahrungsfrist_datenkategorie")

    verarbeitungstaetigkeiten = relationship(
        "Verarbeitungstaetigkeit",
        secondary=verarbeitung_frist,
        back_populates="fristen"
    )


class AufbewahrungsfristZweck(Base):
    __tablename__ = "aufbewahrungsfrist_zweck"

    aufbewahrungsfrist_id = Column(
        Integer,
        ForeignKey("aufbewahrungsfrist.id"),
        primary_key=True,
        nullable=False
    )
    zweck_id = Column(
        Integer,
        ForeignKey("zweck.id"),
        primary_key=True,
        nullable=False
    )


class AufbewahrungsfristDatenkategorie(Base):
    __tablename__ = "aufbewahrungsfrist_datenkategorie"

    aufbewahrungsfrist_id = Column(
        Integer,
        ForeignKey("aufbewahrungsfrist.id"),
        primary_key=True,
        nullable=False
    )
    datenkategorie_id = Column(
        Integer,
        ForeignKey("dsgvo_datenkategorie.id"),
        primary_key=True,
        nullable=False
    )

class Drittland(Base):
    __tablename__ = "drittland"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    angemessenheit = Column(String(255), nullable=False) # nur werte vorhanden , teilweise , keiner

class Uebertragungsgarantie(Base):
    __tablename__ = "uebertragungsgarantie"
    id = Column(Integer, primary_key=True)
    bedingung = Column(String(255), nullable=False)
    artikel_number = Column(String(255), nullable=False)
    absatz_number = Column(String(255), nullable=False)
    literature = Column(String(255), nullable=False)
    erklaerung = Column(String(255), nullable=False)

    regelungen = relationship("UebermittlungsRegelung", secondary="uebermittlungs_regelung_garantie",
                              back_populates="garantien")

class Uebermittlung(Base):
    __tablename__ = "uebermittlung"

    id = Column(Integer, primary_key=True, autoincrement=True)

    fk_verarbeitungstaetigkeit_id = Column(
        Integer,
        ForeignKey("verarbeitungstaetigkeiten.id", ondelete="CASCADE"),
        nullable=False
    )
    fk_drittland_id = Column(
        Integer,
        ForeignKey("drittland.id", ondelete="CASCADE"),
        nullable=False
    )
    fk_uebertragungsgarantie_id = Column(
        Integer,
        ForeignKey("uebertragungsgarantie.id", ondelete="CASCADE"),
        nullable=False
    )

    beschreibung = Column(Text, nullable=True)
    gueltig_ab = Column(Date, nullable=True)

    verarbeitungstaetigkeit = relationship(
        "Verarbeitungstätigkeit",
        back_populates="uebermittlungen"
    )
    drittland = relationship(
        "Drittland",
        back_populates="uebermittlungen"
    )
    uebertragungsgarantie = relationship(
        "Uebertragungsgarantie",
        back_populates="uebermittlungen"
    )

    fk_ausnahme_id = Column(
        Integer,
        ForeignKey("uebermittlungsausnahme.id", ondelete="CASCADE"),
        nullable=True
    )

class Uebermittlungsausnahme(Base):
    __tablename__ = "uebermittlungsausnahme"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ausnahme = Column(String(255), nullable=False)
    artikel_number = Column(String(255), nullable=False)
    absatz_number = Column(String(255), nullable=False)
    literature = Column(String(255), nullable=False)
    uebermittlungen = relationship("Uebermittlung", back_populates="uebermittlungsausnahme")

class Verhaltenskodex(Base):
    __tablename__ = "verhaltenskodex"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    beschreibung = Column(Text, nullable=False)
    herausgeber_verband = Column(String(255))
    genehmigungsbehoerde = Column(String(255))
    article_number = Column(String(255), nullable=False)
    absatz_number = Column(String(255), nullable=False)
    literature = Column(String(255), nullable=False)
    drittland_geeignet = Column(Boolean, default=False)


    pflichten = relationship(
        "Pflicht",
        back_populates="verhaltenskodex",
        cascade="all, delete-orphan"
    )
    prinzipien = relationship(
        "GrundPrinzipienDSGVO",
        back_populates="verhaltenskodex",
        cascade="all, delete-orphan"
    )
    akteure = relationship(
        "DSGVOAkteur",
        back_populates="verhaltenskodex",
        cascade="all, delete-orphan"
    )


class VerhaltenskodexPflicht(Base):
    __tablename__ = "verhaltenskodex_pflicht"

    verhaltenskodex_id = Column(
        Integer,
        ForeignKey("verhaltenskodex.id", ondelete="CASCADE"),
        primary_key=True
    )
    pflicht_id = Column(
        Integer,
        ForeignKey("pflicht.id", ondelete="CASCADE"),
        primary_key=True
    )
    praezisierung = Column(Text)

    verhaltenskodex = relationship("Verhaltenskodex", back_populates="pflichten")
    pflicht = relationship("Pflicht", back_populates="verhaltenskodizes")


class VerhaltenskodexPrinzip(Base):
    __tablename__ = "verhaltenskodex_prinzip"

    verhaltenskodex_id = Column(
        Integer,
        ForeignKey("verhaltenskodex.id", ondelete="CASCADE"),
        primary_key=True
    )
    prinzip_id = Column(
        Integer,
        ForeignKey("grund_prinzipien_dsgvo.id", ondelete="CASCADE"),
        primary_key=True
    )

    verhaltenskodex = relationship("Verhaltenskodex", back_populates="prinzipien")
    prinzip = relationship("GrundPrinzipienDSGVO", back_populates="verhaltenskodizes")


class VerhaltenskodexAkteur(Base):
    __tablename__ = "verhaltenskodex_akteur"

    verhaltenskodex_id = Column(
        Integer,
        ForeignKey("verhaltenskodex.id", ondelete="CASCADE"),
        primary_key=True
    )
    akteur_id = Column(
        Integer,
        ForeignKey("dsgvo_akteur.id", ondelete="CASCADE"),
        primary_key=True
    )

    verhaltenskodex = relationship("Verhaltenskodex", back_populates="akteure")
    akteur = relationship("DSGVOAkteur", back_populates="verhaltenskodizes")


#### AVV <-> AVV vertreter  Join ####
#### AVV vertreter <-> DSGVO akteur Join ####
#### AVV <-> Pflicht Join ####
#### AVV <-> TechnischeOrganisationMasnahme Join ####
#### AVV <-> Verarbeitungstätigkeit Join ####


class AuftragsVerarbeitungsVertrag(Base):
    __tablename__ = "auftragsverarbeitungs_vertrag"
    id = Column(Integer,autoincrement=True, primary_key=True)
    name = Column(String(255), nullable=False)
    beschreibung = Column(String(255), nullable=False)
    gesetzliche_grundlage = Column(String(255), nullable=False)

    akteur_rollen = relationship("AVVAkteur", back_populates="avv", cascade="all, delete-orphan")

    pflichten = relationship("Pflicht", secondary="avv_pflichten", back_populates="avvs")
    tomassnahmen = relationship("TechnischeOrganisatorischMasnahmen", secondary="avv_tomassnahmen", back_populates="avvs")
    verarbeitungstaetigkeiten = relationship("Verarbeitungstaetigkeit", secondary="avv_verarbeitungstaetigkeit",
                                             back_populates="avvs")

class AVVAkteur(Base):
    __tablename__ = "avv_akteure"

    id = Column(Integer, primary_key=True, index=True)
    avv_id = Column(Integer, ForeignKey("auftragsverarbeitungs_vertrag.id"), nullable=False)
    akteur_id = Column(Integer, ForeignKey("dsgvo_akteur.id"), nullable=False)
    rolle = Column(String(50), nullable=False)  # 'verantwortlicher', 'auftragsverarbeiter', ggf. 'unterauftragsverarbeiter'

    avv = relationship("AuftragsVerarbeitungsVertrag", back_populates="akteur_rollen")
    akteur = relationship("DSGVOAkteur", back_populates="avv_rollen")

class AVVPflicht(Base):
    __tablename__ = "avv_pflichten"

    avv_id = Column(Integer, ForeignKey("auftragsverarbeitungs_vertrag.id"), primary_key=True)
    pflicht_id = Column(Integer, ForeignKey("pflicht.id"), primary_key=True)


class AVVTOMassnahme(Base):
    __tablename__ = "avv_tomassnahmen"

    avv_id = Column(Integer, ForeignKey("auftragsverarbeitungs_vertrag.id"), primary_key=True)
    tom_id = Column(Integer, ForeignKey("technische_organisatorisch_masnahmen.id"), primary_key=True)


class AVVVerarbeitungstaetigkeit(Base):
    __tablename__ = "avv_verarbeitungstaetigkeit"

    avv_id = Column(Integer, ForeignKey("auftragsverarbeitungs_vertrag.id"), primary_key=True)
    verarbeitung_id = Column(Integer, ForeignKey("verarbeitungstaetigkeiten.id"), primary_key=True)


#### Gemeinsame Verantwortung <-> GemeinsameVerantwortlichkeitAkteur Join ####
#### Gemeinsame Verantwortung <->  Pflicht Join ####
#### Gemeinsame Verantwortung <-> Verarbeitungstaetigkeit Join ####
#### Gemeinsame Verantwortung <-> DSFA Join ####


class GemeinsameVerantwortlichkeit(Base):
    __tablename__ = "gemeinsame_verantwortlichkeit"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    beschreibung = Column(Text, nullable=True)
    gesetzliche_grundlage = Column(String(255), default="Art. 26 DSGVO")
    transparenzvereinbarung = Column(Text, nullable=True)


    akteur_rollen = relationship(
        "GemeinsameVerantwortlichkeitAkteur",
        back_populates="gemeinsame_verantwortlichkeit",
        cascade="all, delete-orphan"
    )

    pflichten = relationship(
        "Pflicht",
        secondary="gemeinsame_verantwortlichkeit_pflichten",
        back_populates="gemeinsame_verantwortlichkeiten"
    )

    verarbeitungstaetigkeiten = relationship(
        "Verarbeitungstaetigkeit",
        secondary="gemeinsame_verantwortlichkeit_verarbeitung",
        back_populates="gemeinsame_verantwortlichkeiten"
    )

    dsfas = relationship(
        "DSFA",
        secondary="gemeinsame_verantwortlichkeit_dsfa",
        back_populates="gemeinsame_verantwortlichkeiten"
    )

class GemeinsameVerantwortlichkeitAkteur(Base):
    __tablename__ = "gemeinsame_verantwortlichkeit_akteur"

    id = Column(Integer, primary_key=True, index=True)
    gemeinsame_verantwortlichkeit_id = Column(
        Integer,
        ForeignKey("gemeinsame_verantwortlichkeit.id"),
        nullable=False
    )
    akteur_id = Column(Integer, ForeignKey("dsgvo_akteur.id"), nullable=False)
    rolle = Column(String(50), nullable=False)

    gemeinsame_verantwortlichkeit = relationship(
        "GemeinsameVerantwortlichkeit",
        back_populates="akteur_rollen"
    )
    akteur = relationship("DSGVOAkteur", back_populates="gemeinsame_verantwortlichkeit_rollen")


class GemeinsameVerantwortlichkeitPflicht(Base):
    __tablename__ = "gemeinsame_verantwortlichkeit_pflichten"

    gemeinsame_verantwortlichkeit_id = Column(
        Integer,
        ForeignKey("gemeinsame_verantwortlichkeit.id"),
        primary_key=True
    )
    pflicht_id = Column(Integer, ForeignKey("pflicht.id"), primary_key=True)


class GemeinsameVerantwortlichkeitVerarbeitung(Base):
    __tablename__ = "gemeinsame_verantwortlichkeit_verarbeitung"

    gemeinsame_verantwortlichkeit_id = Column(
        Integer,
        ForeignKey("gemeinsame_verantwortlichkeit.id"),
        primary_key=True
    )
    verarbeitung_id = Column(
        Integer,
        ForeignKey("verarbeitungstaetigkeiten.id"),
        primary_key=True
    )


class GemeinsameVerantwortlichkeitDSFA(Base):
    __tablename__ = "gemeinsame_verantwortlichkeit_dsfa"

    gemeinsame_verantwortlichkeit_id = Column(
        Integer,
        ForeignKey("gemeinsame_verantwortlichkeit.id"),
        primary_key=True
    )
    dsfa_id = Column(Integer, ForeignKey("dsfas.id"), primary_key=True)

#### Vorherige Konsultation <-> DSGVO Akteur Join ####
#### Vorherige Konsultation <-> Pficht Join ####
#### Vorherige Konsultation <-> Verarbeitungstätigkeit Join ####

class VorherigeKonsultation(Base):
    __tablename__ = "vorherige_konsultation"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    beschreibung = Column(Text, nullable=True)
    gesetzliche_grundlage = Column(String(255), default="Art. 36 DSGVO")

    dsfa_id = Column(Integer, ForeignKey("dsfas.id"), unique=True, nullable=False)
    dsfa = relationship("DSFA", back_populates="konsultation")

    behoerden = relationship(
        "DSGVOAkteur",
        secondary="konsultation_behoerde",
        back_populates="konsultationen_als_behoerde"
    )

    pflichten = relationship(
        "Pflicht",
        secondary="konsultation_pflichten",
        back_populates="vorherige_konsultationen"
    )

    verarbeitungstaetigkeiten = relationship(
        "Verarbeitungstaetigkeit",
        secondary="konsultation_verarbeitung",
        back_populates="vorherige_konsultationen"
    )

class KonsultationBehoerde(Base):
    __tablename__ = "konsultation_behoerde"
    konsultation_id = Column(Integer, ForeignKey("vorherige_konsultation.id"), primary_key=True)
    behoerde_id = Column(Integer, ForeignKey("dsgvo_akteur.id"), primary_key=True)



class KonsultationPflicht(Base):
    __tablename__ = "konsultation_pflichten"
    konsultation_id = Column(Integer, ForeignKey("vorherige_konsultation.id"), primary_key=True)
    pflicht_id = Column(Integer, ForeignKey("pflicht.id"), primary_key=True)


class KonsultationVerarbeitung(Base):
    __tablename__ = "konsultation_verarbeitung"
    konsultation_id = Column(Integer, ForeignKey("vorherige_konsultation.id"), primary_key=True)
    verarbeitung_id = Column(Integer, ForeignKey("verarbeitungstaetigkeiten.id"), primary_key=True)

#### Datenpanne <-> Pflicht Join ####
#### Datenpanne <-> Akteur Join ####
#### Datenpanne <-> Verarbeitungstätigkeit ####
#### Datenpanne <-> Risikofaktoren ####

class Datenpanne(Base):
    __tablename__ = "datenpanne"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    beschreibung = Column(Text, nullable=True)
    gesetzliche_grundlage = Column(String(255), default="Art. 33, 34 DSGVO")
    meldefrist_stunden = Column(Integer, default=72)


    pflichten = relationship(
        "Pflicht",
        secondary="datenpanne_pflichten",
        back_populates="datenpannen"
    )

    akteur_rollen = relationship(
        "DatenpanneAkteur",
        back_populates="datenpanne",
        cascade="all, delete-orphan"
    )

    verarbeitungstaetigkeiten = relationship(
        "Verarbeitungstaetigkeit",
        secondary="datenpanne_verarbeitung",
        back_populates="datenpannen"
    )

    risikofaktoren = relationship(
        "Risikofaktor",
        secondary="datenpanne_risikofaktor",
        back_populates="datenpannen"
    )

class DatenpanneAkteur(Base):
    __tablename__ = "datenpanne_akteur"

    id = Column(Integer, primary_key=True, index=True)
    datenpanne_id = Column(Integer, ForeignKey("datenpanne.id"), nullable=False)
    akteur_id = Column(Integer, ForeignKey("dsgvo_akteur.id"), nullable=False)
    rolle = Column(String(50), nullable=False)
    datenpanne = relationship("Datenpanne", back_populates="akteur_rollen")
    akteur = relationship("DSGVOAkteur", back_populates="datenpanne_rollen")

class DatenpannePflicht(Base):
    __tablename__ = "datenpanne_pflichten"
    datenpanne_id = Column(Integer, ForeignKey("datenpanne.id"), primary_key=True)
    pflicht_id = Column(Integer, ForeignKey("pflicht.id"), primary_key=True)


class DatenpanneVerarbeitung(Base):
    __tablename__ = "datenpanne_verarbeitung"
    datenpanne_id = Column(Integer, ForeignKey("datenpanne.id"), primary_key=True)
    verarbeitung_id = Column(Integer, ForeignKey("verarbeitungstaetigkeiten.id"), primary_key=True)


class DatenpanneRisikofaktor(Base):
    __tablename__ = "datenpanne_risikofaktor"
    datenpanne_id = Column(Integer, ForeignKey("datenpanne.id"), primary_key=True)
    risikofaktor_id = Column(Integer, ForeignKey("risikofaktoren.id"), primary_key=True)


class Ausnahme(Base):
    __tablename__ = "ausnahme"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    beschreibung = Column(Text, nullable=True)
    gesetzliche_grundlage = Column(String(255), nullable=False)
    artikel_number = Column(String(50))
    absatz_number = Column(String(50))
    literature = Column(String(50))

    pflichten = relationship(
        "Pflicht",
        secondary="ausnahme_pflicht",
        back_populates="ausnahmen"
    )

    bedingungen = relationship(
        "Bedingung",
        back_populates="ausnahme",
        cascade="all, delete-orphan"
    )

    rechte = relationship("Recht", secondary="recht_ausnahme", back_populates="ausnahmen")


class AusnahmePflicht(Base):
    __tablename__ = "ausnahme_pflicht"

    ausnahme_id = Column(Integer, ForeignKey("ausnahme.id"), primary_key=True)
    pflicht_id = Column(Integer, ForeignKey("pflicht.id"), primary_key=True)

#### Bedingung <-> rechtlicher Auslöser Join ####

class Bedingung(Base):
    __tablename__ = "bedingung"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    beschreibung = Column(Text, nullable=True)
    artikel_number = Column(String(50))
    absatz_number = Column(String(50))
    literature = Column(String(50))

    ausnahme_id = Column(Integer, ForeignKey("ausnahme.id"), nullable=False)

    ausnahme = relationship("Ausnahme", back_populates="bedingungen")

    rechtliche_ausloeser = relationship(
        "RechtlicherAusloeser",
        secondary="rechtlicher_ausloeser_bedingung",
        back_populates="bedingungen"
    )

    pflichten = relationship(
        "Pflicht",
        secondary="pflicht_bedingung",
        back_populates="bedingungen"
    )

    rechte = relationship("Recht", secondary="recht_bedingung", back_populates="bedingungen")

class RechtlicherAusloeserBedingung(Base):
    __tablename__ = "rechtlicher_ausloeser_bedingung"

    rechtlicher_ausloeser_id = Column(
        Integer,
        ForeignKey("rechtlicher_ausloeser.id"),
        primary_key=True,
        nullable=False
    )
    bedingung_id = Column(
        Integer,
        ForeignKey("bedingung.id"),
        primary_key=True,
        nullable=False
    )

class RechtBedingung(Base):
    __tablename__ = "recht_bedingung"

    recht_id = Column(Integer, ForeignKey("recht.id"), primary_key=True, nullable=False)
    bedingung_id = Column(Integer, ForeignKey("bedingung.id"), primary_key=True, nullable=False)

class DSGVOZiel(Base):
    __tablename__ = "dsgvo_ziel"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ziel = Column(String(255), nullable=False)
    article_number = Column(String(50))
    absatz_number = Column(String(50))

#### Verarbeitungsform <-> Verarbeitungstätigkeit Join ####

class Verarbeitungsform(Base):
    __tablename__ = "verarbeitungsform"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    beschreibung = Column(Text)
    artikel_relevant = Column(String(255))   # z.B. Art. 4 Nr. 2, 6

    verarbeitungstaetigkeiten = relationship(
        "Verarbeitungstaetigkeit",
        back_populates="verarbeitungsform"
    )

#### Interne Personen/ Gruppen <-> Verarbeitungsätätigkeit Join ####
class InternePersonenGruppen(Base):
    __tablename__ = "interne_personen_gruppen"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

    verarbeitungstaetigkeiten = relationship(
        "Verarbeitungstaetigkeit",
        secondary="interne_personen_gruppen_verarbeitung",
        back_populates="interne_personen_gruppen"
    )

class InternePersonenGruppenVerarbeitung(Base):
    __tablename__ = "interne_personen_gruppen_verarbeitung"

    interne_person_gruppe_id = Column(
        Integer,
        ForeignKey("interne_personen_gruppen.id"),
        primary_key=True
    )

    verarbeitungstaetigkeit_id = Column(
        Integer,
        ForeignKey("verarbeitungstaetigkeiten.id"),
        primary_key=True
    )


#### Gruppe <-> Verarbeitungstätigkeiten Join ####

class Gruppe(Base):
    __tablename__ = "gruppe"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

    verarbeitungstaetigkeiten = relationship(
        "Verarbeitungstaetigkeit",
        secondary="gruppe_verarbeitungstaetigkeit",
        back_populates="gruppen"
    )


class GruppeVerarbeitungstaetigkeit(Base):
    __tablename__ = "gruppe_verarbeitungstaetigkeit"

    gruppe_id = Column(
        Integer,
        ForeignKey("gruppe.id"),
        primary_key=True
    )

    verarbeitungstaetigkeit_id = Column(
        Integer,
        ForeignKey("verarbeitungstaetigkeiten.id"),
        primary_key=True
    )


class ComplianceEmpfehlung(Base):
    __tablename__ = "compliance_empfehlung"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    typ = Column(String(50), nullable=False)
    beschreibung = Column(Text, nullable=False)
    verbindlichkeit = Column(String(50), nullable=False)
    artikle_number = Column(String(255))
    absatz_number = Column(String(50))
    literature = Column(String(50))

class Definition(Base):
    __tablename__ = "definition"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    definition = Column(Text, nullable=False)


class UebermittlungsRegelung(Base):
    __tablename__ = "uebermittlungs_regelung"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    beschreibung = Column(Text, nullable=False)
    artikel_number = Column(String(50))
    absatz_number = Column(String(50))
    literature = Column(String(50))

    garantien = relationship(
        "Uebertragungsgarantie",
        secondary="uebermittlungs_regelung_garantie",
        back_populates="regelungen"
    )

    ausnahmen = relationship(
        "Uebermittlungsausnahme",
        secondary="uebermittlungs_regelung_ausnahme",
        back_populates="regelungen"
    )


class UebermittlungsRegelungGarantie(Base):
    __tablename__ = "uebermittlungs_regelung_garantie"
    regelung_id = Column(Integer, ForeignKey("uebermittlungs_regelung.id"), primary_key=True)
    garantie_id = Column(Integer, ForeignKey("uebertragungsgarantie.id"), primary_key=True)

class UebermittlungsRegelungAusnahme(Base):
    __tablename__ = "uebermittlungs_regelung_ausnahme"
    regelung_id = Column(Integer, ForeignKey("uebermittlungs_regelung.id"), primary_key=True)
    ausnahme_id = Column(Integer, ForeignKey("uebermittlungsausnahme.id"), primary_key=True)

    regelungen = relationship("UebermittlungsRegelung", secondary="uebermittlungs_regelung_ausnahme",
                              back_populates="ausnahmen")