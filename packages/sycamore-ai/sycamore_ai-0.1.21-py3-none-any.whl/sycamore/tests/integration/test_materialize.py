import tempfile
import unittest

import sycamore
from sycamore.data import Document


# class TestMaterializeRead(test_materialize.TestMaterializeRead):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.exec_mode = ExecMode.RAY


class TestIntegration(unittest.TestCase):
    def test_groupby_materialize(self):
        """
        When running the groupby_count, ray will cause re-execution of earlier stages. An earlier version of
        materialize would reject this when it discovered that the same document was being written twice.
        You can verify the failure by adding assert False into materialize.py before the
        'Duplicate name {path} generated for clean root' error message.
        """
        ctx = sycamore.init()
        ds = ctx.read.document(self.make_docs())
        with tempfile.TemporaryDirectory() as tmpdir:
            out = (
                ds.materialize(path=tmpdir)
                .groupby_count("properties.entity.location", "properties.entity.accidentNumber")
                .take_all()
            )
            print(out)

    def make_docs(self):
        properties = get_ntsb_properties()
        return [Document(properties={"entity": {"location": p[0], "accidentNumber": p[1]}}) for p in properties]


def get_ntsb_properties():
    return [
        ["Bolingbrook, Illinois", "CEN23LA080"],
        ["Tomball, TX", "CEN23LA088"],
        ["Calhoun, Georgia", "ERA23LA102"],
        ["Agua Caliente Springs, California", "WPR23LA088"],
        ["Bolingbrook, Illinois", "CEN23LA080"],
        ["Auburn, NE", "CEN23FA077"],
        ["Wauchula, Florida", "ERA23LA114"],
        ["Williston, Florida", "ERA23LA153"],
        ["Dayton, VA", "ERA23FA108"],
        ["New Harmony, UT", "WPR23FA083"],
        ["Raleigh/Durham, North Carolina", "ERA23LA118"],
        ["Wauchula, Florida", "ERA23LA114"],
        ["New York, NY", "DCA23LA114"],
        ["Honolulu, HI", "DCA23LA133"],
        ["Queens, NY", "DCA23LA125"],
        ["Brashear, Texas", "CEN23LA083"],
        ["Eden Prairie, Minnesota", "CEN23LA092"],
        ["Calhoun, GA", "ERA23LA120"],
        ["Tomball, TX", "CEN23LA088"],
        ["Sylacauga, AL", "ERA23LA122"],
        ["Watsonville, California", "WPR23LA082"],
        ["Yukon, Oklahoma", "CEN23LA075"],
        ["Council Bluffs, Iowa", "CEN23LA076"],
        ["Eagle River, Wisconsin", "CEN23LA098"],
        ["Hooker, OK", "CEN23FA095"],
        ["Modesto, CA", "WPR23FA092"],
        ["Ridgeland, South Carolina", "ERA23LA168"],
        ["Kent, WA", "WPR23LA086"],
        ["San Antonio, Texas", "CEN23LA089"],
        ["Dawsonville, GA", "ERA23FA109"],
        ["Yoakum, TX", "CEN23FA084"],
        ["Brashear, Texas", "CEN23LA083"],
        ["Wauchula, Florida", "ERA23LA114"],
        ["Somerville, Tennessee", "ERA23LA111"],
        ["Calhoun, GA", "ERA23LA120"],
        ["Yelm, Washington", "WPR23LA089"],
        ["Queens, NY", "DCA23LA125"],
        ["Paris, Kentucky", "ERA23LA105"],
        ["Somerville, Tennessee", "ERA23LA111"],
        ["Anchorage, Alaska", "ANC23LA015"],
        ["Agua Caliente Springs, California", "WPR23LA088"],
        ["Council Bluffs, Iowa", "CEN23LA076"],
        ["Minidoka, Idaho", "WPR23LA090"],
        ["Sweet Home, OR", "WPR23LA097"],
        ["Wauchula, Florida", "ERA23LA114"],
        ["Indianapolis, Indiana", "CEN23LA093"],
        ["Honolulu, HI", "DCA23LA133"],
        ["Atlantic Ocean, Atlantic Ocean", "ERA23LA101"],
        ["Calhoun, Georgia", "ERA23LA102"],
        ["Atlantic Ocean, Atlantic Ocean", "ERA23LA101"],
        ["Suffolk, VA", "ERA23FA103"],
        ["Fowlerton, Texas", "CEN23LA086"],
        ["Sandpoint, Idaho", "WPR23LA106"],
        ["Paris, Kentucky", "ERA23LA105"],
        ["Skull Valley, Arizona", "WPR23LA135"],
        ["Middlefield, OH", "ERA23LA112"],
        ["Wauchula, Florida", "ERA23LA114"],
        ["Dayton, VA", "ERA23FA108"],
        ["San Diego, California", "WPR23LA091"],
        ["San Antonio, Texas", "CEN23LA089"],
        ["Brush, Colorado", "CEN23LA085"],
        ["Honolulu, HI", "DCA23LA133"],
        ["Orlando, Florida", "ERA23LA116"],
        ["Miami, FL", "ERA23LA119"],
        ["Kualapuu, Hawaii", "ANC23LA012"],
        ["Minidoka, Idaho", "WPR23LA090"],
        ["Paris, Kentucky", "ERA23LA105"],
        ["Somerville, Tennessee", "ERA23LA111"],
        ["Eden Prairie, Minnesota", "CEN23LA092"],
        ["New Harmony, UT", "WPR23FA083"],
        ["New York, NY", "DCA23LA114"],
        ["Hyannis, Nebraska", "CEN23LA090"],
        ["Poplar, Montana", "WPR23LA087"],
        ["Dawsonville, GA", "ERA23FA109"],
        ["Minidoka, Idaho", "WPR23LA090"],
        ["Watsonville, California", "WPR23LA082"],
        ["San Diego, California", "WPR23LA091"],
        ["Skull Valley, Arizona", "WPR23LA135"],
        ["Council Bluffs, Iowa", "CEN23LA076"],
        ["Fowlerton, Texas", "CEN23LA086"],
        ["Eden Prairie, Minnesota", "CEN23LA092"],
        ["Kualapuu, Hawaii", "ANC23LA012"],
        ["Shreveport, LA", "CEN23LA087"],
        ["Indianapolis, Indiana", "CEN23LA093"],
        ["Minidoka, Idaho", "WPR23LA090"],
        ["Hyannis, Nebraska", "CEN23LA090"],
        ["Ridgeland, South Carolina", "ERA23LA168"],
        ["Ridgeland, South Carolina", "ERA23LA168"],
        ["Sandpoint, Idaho", "WPR23LA106"],
        ["Ridgeland, South Carolina", "ERA23LA168"],
        ["Tomball, TX", "CEN23LA088"],
        ["Fayetteville, AR", "CEN23FA074"],
        ["Opa-locka, Florida", "ERA23LA104"],
        ["Miami, FL", "ERA23LA119"],
        ["Raleigh/Durham, North Carolina", "ERA23LA118"],
        ["Mesa, AZ", "WPR23LA096"],
        ["Kualapuu, Hawaii", "ANC23LA012"],
        ["Ridgeland, South Carolina", "ERA23LA168"],
        ["Indianapolis, Indiana", "CEN23LA093"],
        ["Somerville, Tennessee", "ERA23LA111"],
        ["Yelm, Washington", "WPR23LA089"],
        ["Eden Prairie, Minnesota", "CEN23LA092"],
        ["Tomball, TX", "CEN23LA088"],
        ["Agua Caliente Springs, California", "WPR23LA088"],
        ["Brush, Colorado", "CEN23LA085"],
        ["Dawsonville, GA", "ERA23FA109"],
        ["Bolingbrook, Illinois", "CEN23LA080"],
        ["Honolulu, HI", "DCA23LA133"],
        ["San Diego, California", "WPR23LA091"],
        ["Modesto, CA", "WPR23FA092"],
        ["San Antonio, Texas", "CEN23LA089"],
        ["Calhoun, Georgia", "ERA23LA102"],
        ["Calhoun, GA", "ERA23LA120"],
        ["Old Bridge, New Jersey", "ERA23LA107"],
        ["North Castle, NY", "ERA23FA113"],
        ["Conway, Arkansas", "CEN23LA073"],
        ["Fowlerton, Texas", "CEN23LA086"],
        ["Calexico, California", "WPR23LA095"],
        ["Glennallen, Alaska", "ANC23LA018"],
        ["Orlando, Florida", "ERA23LA116"],
        ["Conway, Arkansas", "CEN23LA073"],
        ["Somerville, Tennessee", "ERA23LA111"],
        ["Poplar, Montana", "WPR23LA087"],
        ["Ridgeland, South Carolina", "ERA23LA168"],
        ["Watsonville, California", "WPR23LA082"],
        ["Dawsonville, GA", "ERA23FA109"],
        ["Sandpoint, Idaho", "WPR23LA106"],
        ["Agua Caliente Springs, California", "WPR23LA088"],
        ["Carlsbad, CA", "WPR23LA094"],
        ["Rich County, Utah", "WPR23LA099"],
        ["Eagle River, Wisconsin", "CEN23LA098"],
        ["Queens, NY", "DCA23LA125"],
        ["Paris, Kentucky", "ERA23LA105"],
        ["Yukon, Oklahoma", "CEN23LA075"],
        ["Raleigh/Durham, North Carolina", "ERA23LA118"],
        ["Somerville, Tennessee", "ERA23LA111"],
        ["Fowlerton, Texas", "CEN23LA086"],
        ["Dallesport, Washington", "WPR23LA101"],
        ["Dallesport, Washington", "WPR23LA101"],
        ["Council Bluffs, Iowa", "CEN23LA076"],
        ["Brush, Colorado", "CEN23LA085"],
        ["Rich County, Utah", "WPR23LA099"],
        ["Yukon, Oklahoma", "CEN23LA075"],
        ["Council Bluffs, Iowa", "CEN23LA076"],
        ["Chickala, Arkansas", "CEN23LA096"],
        ["Wasilla, Alaska", "ANC23LA013"],
        ["Eden Prairie, Minnesota", "CEN23LA092"],
        ["Dawsonville, GA", "ERA23FA109"],
        ["Williston, Florida", "ERA23LA153"],
        ["San Antonio, Texas", "CEN23LA089"],
        ["Anchorage, Alaska", "ANC23LA015"],
        ["Kenai, Alaska", "ANC23LA011"],
        ["Hartford, CT", "ERA23LA121"],
        ["Brashear, Texas", "CEN23LA083"],
        ["Cleveland, Texas", "CEN23LA097"],
        ["Benton, Tennessee", "ERA23LA115"],
        ["New York, NY", "DCA23LA114"],
        ["Wasilla, Alaska", "ANC23LA013"],
        ["Orlando, Florida", "ERA23LA116"],
        ["Council Bluffs, Iowa", "CEN23LA076"],
        ["Rich County, Utah", "WPR23LA099"],
        ["New Harmony, UT", "WPR23FA083"],
        ["Yukon, Oklahoma", "CEN23LA075"],
        ["Cleveland, Texas", "CEN23LA097"],
        ["Sweet Home, OR", "WPR23LA097"],
        ["Fowlerton, Texas", "CEN23LA086"],
        ["Dayton, VA", "ERA23FA108"],
        ["Dallesport, Washington", "WPR23LA101"],
        ["Hartford, CT", "ERA23LA121"],
        ["Raleigh/Durham, North Carolina", "ERA23LA118"],
        ["Conway, Arkansas", "CEN23LA073"],
        ["Opa-locka, Florida", "ERA23LA104"],
        ["Old Bridge, New Jersey", "ERA23LA107"],
        ["Agua Caliente Springs, California", "WPR23LA088"],
        ["Yoakum, TX", "CEN23FA084"],
        ["Mesa, AZ", "WPR23LA096"],
        ["Skull Valley, Arizona", "WPR23LA135"],
        ["Conway, Arkansas", "CEN23LA073"],
        ["Calexico, California", "WPR23LA095"],
        ["Las Animas, CO", "CEN23LA082"],
        ["Kualapuu, Hawaii", "ANC23LA012"],
        ["Yelm, Washington", "WPR23LA089"],
        ["Brush, Colorado", "CEN23LA085"],
        ["Paris, Kentucky", "ERA23LA105"],
        ["Indianapolis, Indiana", "CEN23LA093"],
        ["Middlefield, OH", "ERA23LA112"],
        ["Hyannis, Nebraska", "CEN23LA090"],
        ["Atlantic Ocean, Atlantic Ocean", "ERA23LA101"],
        ["Auburn, NE", "CEN23FA077"],
        ["Yukon, Oklahoma", "CEN23LA075"],
        ["Poplar, Montana", "WPR23LA087"],
        ["Kenai, Alaska", "ANC23LA011"],
        ["Old Bridge, New Jersey", "ERA23LA107"],
        ["North Castle, NY", "ERA23FA113"],
        ["Dallesport, Washington", "WPR23LA101"],
        ["Dayton, VA", "ERA23FA108"],
        ["Fowlerton, Texas", "CEN23LA086"],
        ["Dawsonville, GA", "ERA23FA109"],
        ["Eagle River, Wisconsin", "CEN23LA098"],
        ["Yelm, Washington", "WPR23LA089"],
        ["Bolingbrook, Illinois", "CEN23LA080"],
        ["Honolulu, HI", "DCA23LA133"],
        ["Minidoka, Idaho", "WPR23LA090"],
        ["Eden Prairie, Minnesota", "CEN23LA092"],
        ["Sylacauga, AL", "ERA23LA122"],
        ["Murrieta, CA", "WPR23LA098"],
        ["Atlantic Ocean, Atlantic Ocean", "ERA23LA101"],
        ["Queens, NY", "DCA23LA125"],
        ["Atlantic Ocean, Atlantic Ocean", "ERA23LA101"],
        ["Paris, Kentucky", "ERA23LA105"],
        ["Council Bluffs, Iowa", "CEN23LA076"],
        ["Indianapolis, Indiana", "CEN23LA093"],
        ["Hyannis, Nebraska", "CEN23LA090"],
        ["Paris, Kentucky", "ERA23LA105"],
        ["Atlantic Ocean, Atlantic Ocean", "ERA23LA101"],
        ["Kenai, Alaska", "ANC23LA011"],
        ["Yelm, Washington", "WPR23LA089"],
        ["Fowlerton, Texas", "CEN23LA086"],
        ["Kualapuu, Hawaii", "ANC23LA012"],
        ["Mesa, AZ", "WPR23LA096"],
        ["San Antonio, Texas", "CEN23LA089"],
        ["Eagle River, Wisconsin", "CEN23LA098"],
        ["Conway, Arkansas", "CEN23LA073"],
        ["Chickala, Arkansas", "CEN23LA096"],
        ["Sandpoint, Idaho", "WPR23LA106"],
        ["Honolulu, HI", "DCA23LA133"],
        ["Kingfisher, OK", "CEN23FA079"],
        ["San Diego, California", "WPR23LA091"],
        ["Benton, Tennessee", "ERA23LA115"],
        ["Sandpoint, Idaho", "WPR23LA106"],
        ["Glennallen, Alaska", "ANC23LA018"],
        ["Hyannis, Nebraska", "CEN23LA090"],
        ["Cleveland, Texas", "CEN23LA097"],
        ["Benton, Tennessee", "ERA23LA115"],
        ["Yoakum, TX", "CEN23FA084"],
        ["Watsonville, California", "WPR23LA082"],
        ["Watsonville, California", "WPR23LA082"],
        ["North Castle, NY", "ERA23FA113"],
        ["Anchorage, Alaska", "ANC23LA015"],
        ["Hooker, OK", "CEN23FA095"],
        ["Auburn, NE", "CEN23FA077"],
        ["Dayton, VA", "ERA23FA108"],
        ["Coeur d'Alene, ID", "WPR23LA102"],
        ["Sandpoint, Idaho", "WPR23LA106"],
        ["Kingfisher, OK", "CEN23FA079"],
        ["San Diego, California", "WPR23LA091"],
        ["Calexico, California", "WPR23LA095"],
        ["San Diego, California", "WPR23LA091"],
        ["Glennallen, Alaska", "ANC23LA018"],
        ["Somerville, Tennessee", "ERA23LA111"],
        ["Opa-locka, Florida", "ERA23LA104"],
        ["Rich County, Utah", "WPR23LA099"],
        ["Coeur d'Alene, ID", "WPR23LA102"],
        ["Queens, NY", "DCA23LA125"],
        ["Carlsbad, CA", "WPR23LA094"],
        ["Poplar, Montana", "WPR23LA087"],
        ["Orlando, Florida", "ERA23LA116"],
        ["Raleigh/Durham, North Carolina", "ERA23LA118"],
        ["Ridgeland, South Carolina", "ERA23LA168"],
        ["Paris, Kentucky", "ERA23LA105"],
        ["Calhoun, Georgia", "ERA23LA102"],
        ["Council Bluffs, Iowa", "CEN23LA076"],
        ["Anchorage, Alaska", "ANC23LA015"],
        ["Kingfisher, OK", "CEN23FA079"],
        ["Opa-locka, Florida", "ERA23LA104"],
        ["Suffolk, VA", "ERA23FA103"],
        ["Bolingbrook, Illinois", "CEN23LA080"],
        ["Brashear, Texas", "CEN23LA083"],
        ["Fayetteville, AR", "CEN23FA074"],
        ["Sweet Home, OR", "WPR23LA097"],
        ["Fayetteville, AR", "CEN23FA074"],
        ["Las Animas, CO", "CEN23LA082"],
        ["Queens, NY", "DCA23LA125"],
        ["Hyannis, Nebraska", "CEN23LA090"],
        ["Kenai, Alaska", "ANC23LA011"],
        ["Brashear, Texas", "CEN23LA083"],
        ["San Diego, California", "WPR23LA091"],
        ["Skull Valley, Arizona", "WPR23LA135"],
        ["Somerville, Tennessee", "ERA23LA111"],
        ["Minidoka, Idaho", "WPR23LA090"],
        ["Miami, FL", "ERA23LA119"],
        ["New Harmony, UT", "WPR23FA083"],
        ["Watsonville, California", "WPR23LA082"],
        ["Opa-locka, Florida", "ERA23LA104"],
        ["Brush, Colorado", "CEN23LA085"],
        ["Hartford, CT", "ERA23LA121"],
        ["Honolulu, HI", "DCA23LA133"],
        ["Williston, Florida", "ERA23LA153"],
        ["Dallesport, Washington", "WPR23LA101"],
        ["Conroe, TX", "CEN23LA081"],
        ["Modesto, CA", "WPR23FA092"],
        ["Honolulu, HI", "DCA23LA133"],
        ["Kenai, Alaska", "ANC23LA011"],
        ["Yukon, Oklahoma", "CEN23LA075"],
        ["Sylacauga, AL", "ERA23LA122"],
        ["Yelm, Washington", "WPR23LA089"],
        ["Kualapuu, Hawaii", "ANC23LA012"],
        ["Wauchula, Florida", "ERA23LA114"],
        ["Kent, WA", "WPR23LA086"],
        ["Calhoun, GA", "ERA23LA120"],
        ["Murrieta, CA", "WPR23LA098"],
        ["Chickala, Arkansas", "CEN23LA096"],
        ["Benton, Tennessee", "ERA23LA115"],
        ["Raleigh/Durham, North Carolina", "ERA23LA118"],
        ["Hartford, CT", "ERA23LA121"],
        ["Calhoun, Georgia", "ERA23LA102"],
        ["Rich County, Utah", "WPR23LA099"],
        ["Kent, WA", "WPR23LA086"],
        ["Skull Valley, Arizona", "WPR23LA135"],
        ["San Antonio, Texas", "CEN23LA089"],
        ["Benton, Tennessee", "ERA23LA115"],
        ["Cleveland, Texas", "CEN23LA097"],
        ["Dawsonville, GA", "ERA23FA109"],
        ["Provo, UT", "WPR23FA080"],
        ["Calexico, California", "WPR23LA095"],
        ["Buford, GA", "ERA23LA117"],
        ["Old Bridge, New Jersey", "ERA23LA107"],
        ["Opa-locka, Florida", "ERA23LA104"],
        ["Calexico, California", "WPR23LA095"],
        ["Williston, Florida", "ERA23LA153"],
        ["Benton, Tennessee", "ERA23LA115"],
        ["Indianapolis, Indiana", "CEN23LA093"],
        ["Chickala, Arkansas", "CEN23LA096"],
        ["Murrieta, CA", "WPR23LA098"],
        ["Suffolk, VA", "ERA23FA103"],
        ["Buford, GA", "ERA23LA117"],
        ["Glennallen, Alaska", "ANC23LA018"],
        ["Agua Caliente Springs, California", "WPR23LA088"],
        ["Middlefield, OH", "ERA23LA112"],
        ["Hyannis, Nebraska", "CEN23LA090"],
        ["Minidoka, Idaho", "WPR23LA090"],
        ["Eden Prairie, Minnesota", "CEN23LA092"],
        ["Dayton, VA", "ERA23FA108"],
        ["Wasilla, Alaska", "ANC23LA013"],
        ["Shreveport, LA", "CEN23LA087"],
        ["Poplar, Montana", "WPR23LA087"],
        ["New Harmony, UT", "WPR23FA083"],
        ["Council Bluffs, Iowa", "CEN23LA076"],
        ["New Harmony, UT", "WPR23FA083"],
        ["Auburn, NE", "CEN23FA077"],
        ["Conroe, TX", "CEN23LA081"],
        ["Cleveland, Texas", "CEN23LA097"],
        ["Suffolk, VA", "ERA23FA103"],
        ["Sweet Home, OR", "WPR23LA097"],
        ["Indianapolis, Indiana", "CEN23LA093"],
        ["Yelm, Washington", "WPR23LA089"],
        ["Modesto, CA", "WPR23FA092"],
        ["Williston, Florida", "ERA23LA153"],
        ["Kenai, Alaska", "ANC23LA011"],
        ["North Castle, NY", "ERA23FA113"],
        ["Brashear, Texas", "CEN23LA083"],
        ["Atlantic Ocean, Atlantic Ocean", "ERA23LA101"],
        ["Honolulu, HI", "DCA23LA133"],
        ["Honolulu, HI", "DCA23LA133"],
        ["Buford, GA", "ERA23LA117"],
        ["Atlantic Ocean, Atlantic Ocean", "ERA23LA101"],
        ["Provo, UT", "WPR23FA080"],
        ["Provo, UT", "WPR23FA080"],
        ["Kingfisher, OK", "CEN23FA079"],
        ["Hooker, OK", "CEN23FA095"],
        ["Sylacauga, AL", "ERA23LA122"],
        ["Shreveport, LA", "CEN23LA087"],
        ["San Diego, California", "WPR23LA091"],
        ["Poplar, Montana", "WPR23LA087"],
        ["Conroe, TX", "CEN23LA081"],
        ["San Antonio, Texas", "CEN23LA089"],
        ["Brush, Colorado", "CEN23LA085"],
        ["North Castle, NY", "ERA23FA113"],
        ["Orlando, Florida", "ERA23LA116"],
        ["Middlefield, OH", "ERA23LA112"],
        ["Brashear, Texas", "CEN23LA083"],
        ["Fayetteville, AR", "CEN23FA074"],
        ["Honolulu, HI", "DCA23LA133"],
        ["San Diego, California", "WPR23LA091"],
        ["Brashear, Texas", "CEN23LA083"],
        ["Hartford, CT", "ERA23LA121"],
        ["Provo, UT", "WPR23FA080"],
        ["Anchorage, Alaska", "ANC23LA015"],
        ["Wasilla, Alaska", "ANC23LA013"],
        ["North Castle, NY", "ERA23FA113"],
        ["Glennallen, Alaska", "ANC23LA018"],
        ["Bolingbrook, Illinois", "CEN23LA080"],
        ["Honolulu, HI", "DCA23LA133"],
        ["Hooker, OK", "CEN23FA095"],
        ["Rich County, Utah", "WPR23LA099"],
        ["Glennallen, Alaska", "ANC23LA018"],
        ["Provo, UT", "WPR23FA080"],
        ["Anchorage, Alaska", "ANC23LA015"],
        ["Rich County, Utah", "WPR23LA099"],
        ["Wasilla, Alaska", "ANC23LA013"],
        ["Calexico, California", "WPR23LA095"],
        ["Anchorage, Alaska", "ANC23LA015"],
        ["Williston, Florida", "ERA23LA153"],
        ["Coeur d'Alene, ID", "WPR23LA102"],
        ["Cleveland, Texas", "CEN23LA097"],
        ["Old Bridge, New Jersey", "ERA23LA107"],
        ["Dawsonville, GA", "ERA23FA109"],
        ["Calexico, California", "WPR23LA095"],
        ["Chickala, Arkansas", "CEN23LA096"],
        ["Wasilla, Alaska", "ANC23LA013"],
        ["Kualapuu, Hawaii", "ANC23LA012"],
        ["Auburn, NE", "CEN23FA077"],
        ["Provo, UT", "WPR23FA080"],
        ["Poplar, Montana", "WPR23LA087"],
        ["Conroe, TX", "CEN23LA081"],
        ["Wauchula, Florida", "ERA23LA114"],
        ["Las Animas, CO", "CEN23LA082"],
        ["Wasilla, Alaska", "ANC23LA013"],
        ["Benton, Tennessee", "ERA23LA115"],
        ["Somerville, Tennessee", "ERA23LA111"],
        ["Wasilla, Alaska", "ANC23LA013"],
        ["Coeur d'Alene, ID", "WPR23LA102"],
        ["Agua Caliente Springs, California", "WPR23LA088"],
        ["Modesto, CA", "WPR23FA092"],
        ["Skull Valley, Arizona", "WPR23LA135"],
        ["Chickala, Arkansas", "CEN23LA096"],
        ["Suffolk, VA", "ERA23FA103"],
        ["Williston, Florida", "ERA23LA153"],
        ["Yukon, Oklahoma", "CEN23LA075"],
        ["Las Animas, CO", "CEN23LA082"],
        ["Cleveland, Texas", "CEN23LA097"],
        ["Buford, GA", "ERA23LA117"],
        ["Williston, Florida", "ERA23LA153"],
        ["Chickala, Arkansas", "CEN23LA096"],
        ["Orlando, Florida", "ERA23LA116"],
        ["Conway, Arkansas", "CEN23LA073"],
        ["Eagle River, Wisconsin", "CEN23LA098"],
        ["Eagle River, Wisconsin", "CEN23LA098"],
        ["Skull Valley, Arizona", "WPR23LA135"],
        ["Glennallen, Alaska", "ANC23LA018"],
        ["Raleigh/Durham, North Carolina", "ERA23LA118"],
        ["Cleveland, Texas", "CEN23LA097"],
        ["Dallesport, Washington", "WPR23LA101"],
        ["Eagle River, Wisconsin", "CEN23LA098"],
        ["Hooker, OK", "CEN23FA095"],
        ["Calhoun, Georgia", "ERA23LA102"],
        ["Carlsbad, CA", "WPR23LA094"],
        ["Orlando, Florida", "ERA23LA116"],
        ["Murrieta, CA", "WPR23LA098"],
        ["Bolingbrook, Illinois", "CEN23LA080"],
        ["Old Bridge, New Jersey", "ERA23LA107"],
        ["Kent, WA", "WPR23LA086"],
        ["Yoakum, TX", "CEN23FA084"],
        ["Orlando, Florida", "ERA23LA116"],
        ["Kingfisher, OK", "CEN23FA079"],
        ["Sandpoint, Idaho", "WPR23LA106"],
        ["Indianapolis, Indiana", "CEN23LA093"],
        ["Old Bridge, New Jersey", "ERA23LA107"],
        ["Brashear, Texas", "CEN23LA083"],
        ["New Harmony, UT", "WPR23FA083"],
        ["San Diego, California", "WPR23LA091"],
        ["Sylacauga, AL", "ERA23LA122"],
        ["Opa-locka, Florida", "ERA23LA104"],
        ["Middlefield, OH", "ERA23LA112"],
        ["Calhoun, GA", "ERA23LA120"],
        ["Brush, Colorado", "CEN23LA085"],
        ["Shreveport, LA", "CEN23LA087"],
        ["Opa-locka, Florida", "ERA23LA104"],
        ["Calhoun, Georgia", "ERA23LA102"],
        ["Carlsbad, CA", "WPR23LA094"],
        ["Fayetteville, AR", "CEN23FA074"],
        ["Dallesport, Washington", "WPR23LA101"],
        ["Kenai, Alaska", "ANC23LA011"],
        ["Wasilla, Alaska", "ANC23LA013"],
        ["Poplar, Montana", "WPR23LA087"],
    ]
