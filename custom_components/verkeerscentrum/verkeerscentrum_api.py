"""API client for verkeerscentrum"""
from .const import RSS_URI
from requests import get
from xml.etree import ElementTree


class VerkeerscentrumAPI:
    def getRSS(self, ids):
        headers = {"Accept-Encoding": "gzip", "Host": "rss.opendata.belfla.be"}

        try:
            response = get(RSS_URI, headers=headers)
            root = ElementTree.fromstring(response.text)
            data = VerkeerscentrumRSSData()

            for child in root:
                if child.tag == "tijd_publicatie":
                    data.tijd_publicatie = child.text

                if child.tag == "tijd_laatste_config_wijziging":
                    data.tijd_laatste_config_wijziging = child.text

                if child.tag == "tijd_laatste_boodschappen_wijziging":
                    data.tijd_laatste_boodschappen_wijziging = child.text

                if child.tag == "rss_bord":
                    unieke_id = child.attrib.get("unieke_id")

                    if not unieke_id in ids:
                        continue

                    bord = VerkeerscentrumRSSBord(unieke_id)

                    for bord_child in child:
                        if bord_child.tag == "abbameldanaam":
                            bord.abbameldanaam = bord_child.text

                        if bord_child.tag == "technische_toestand":
                            for technische_toestand_child in bord_child:
                                if technische_toestand_child.tag == "inDienst":
                                    bord.inDienst = technische_toestand_child.text
                                if technische_toestand_child.tag == "defect":
                                    bord.defect = technische_toestand_child.text

                        if bord_child.tag == "aangevraagde_boodschap":
                            for aangevraagde_boodschap_child in bord_child:
                                if (
                                    aangevraagde_boodschap_child.tag
                                    == "laatst_gewijzigd"
                                ):
                                    bord.laatst_gewijzigd = (
                                        aangevraagde_boodschap_child.text
                                    )
                                if (
                                    aangevraagde_boodschap_child.tag
                                    == "verkeersteken_status"
                                ):
                                    bord.verkeersteken_status = (
                                        aangevraagde_boodschap_child.text
                                    )
                                if (
                                    aangevraagde_boodschap_child.tag
                                    == "onderbord_status"
                                ):
                                    bord.onderbord_status = (
                                        aangevraagde_boodschap_child.text
                                    )
                                if aangevraagde_boodschap_child.tag == "pijl_status":
                                    bord.pijl_status = aangevraagde_boodschap_child.text
                                if (
                                    aangevraagde_boodschap_child.tag
                                    == "knipperlicht_status"
                                ):
                                    bord.knipperlicht_status = (
                                        aangevraagde_boodschap_child.text
                                    )

                    data.rss_borden.append(bord)

            return data
        except:
            raise VerkeerscentrumAPIError()


class VerkeerscentrumAPIError(Exception):
    pass


class VerkeerscentrumRSSBord:
    def __init__(self, unieke_id):
        self.unieke_id = unieke_id
        self.abbameldanaam = None
        self.laatst_gewijzigd = None
        self.inDienst = None
        self.defect = None
        self.verkeersteken_status = None
        self.onderbord_status = None
        self.pijl_status = None
        self.knipperlicht_status = None


class VerkeerscentrumRSSData:
    def __init__(self):
        self.rss_borden = []
        self.tijd_publicatie = None
        self.tijd_laatste_config_wijziging = None
        self.tijd_laatste_boodschappen_wijziging = None
