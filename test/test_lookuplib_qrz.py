import pytest
from datetime import datetime

from apikey import QRZ_USERNAME, QRZ_PWD
from pyhamtools.lookuplib import LookupLib
#from pyhamtools.exceptions import APIKeyMissingError
from pyhamtools.consts import LookupConventions as const

import pytz
UTC = pytz.UTC

#Fixtures
#===========================================================


response_XX1XX = {
     u'addr2': u'Not QSL',
     u'adif': 0,
     u'bio': u'0',
     u'biodate': datetime(2017, 7, 21, 0, 47, 25, tzinfo=UTC),
     u'callsign': u'XX1XX',
     u'ccode': 10,
     u'country': u'Antarctica',
#     u'eqsl': True,
     u'fname': u'Test page',
     u'geoloc': u'dxcc',
     u'land': u'NON-DXCC',
#     u'latitude': 23.644524,
#     u'locator': u'LL73ep',
#     u'longitude': 54.382324,
#     u'lotw': True,
     u'moddate': datetime(2017, 7, 21, 0, 56, 15, tzinfo=UTC),
#     u'mqsl': True,
     u'name': u'~',
#     u'user': u'XX1XX',
     u'license_class': u'1',
 }

response_XX2XX = {
    u'addr1': u'1234 Main Road.',
    u'addr2': u'Las Vegasvillee',
    u'adif': 446,
    u'bio': u'218',
    u'biodate': datetime(2017, 6, 16, 15, 47, 47, tzinfo=UTC),
    u'born': 1932,
    u'callsign': u'XX2XX',
    u'ccode': 1230,
    u'codes': u'ZZ',
    u'country': u'Temotu',
    u'cqz': 4,
    u'email': 'dummy2@qrz.com',
    u'eqsl': False,
    u'fname': u'Gooberd',
    u'geoloc': u'user',
    u'image': u'https://s3.amazonaws.com/files.qrz.com/x/xx2xx/oval_bumper_sticker4.png',
    u'imageinfo': u'285:500:44218',
    u'iota': u'NA-022',
    u'ituz': 5,
    u'land': u'Morocco',
    u'latitude': 52.195073,
    u'license_class': u'A',
    u'locator': u'JO02be',
    u'longitude': 0.124962,
    u'lotw': False,
    u'moddate': datetime(2017, 6, 16, 19, 22, 21, tzinfo=UTC),
    u'mqsl': False,
    u'name': u'Blufferd',
    u'qslmgr': u'nobody here.   gone fishing, permanently',
    u'state': u'mt',
    u'user': u'XX2XX',
    u'zipcode': u'112233'
}

response_XX3XX = {
     u'addr1': u'1234 Main St.3',
     u'addr2': u'Shady Circle Roads',
     u'adif': 79,
     u'aliases': [u'XX3XX/W7'],
     u'bio': u'1940',
     u'biodate': datetime(2015, 8, 13, 23, 14, 38, tzinfo=UTC),
     u'born': 2010,
     u'callsign': u'XX3XX',
     u'ccode': 130,
     u'country': u'Jamaica',
     u'email': u'fred@qrz.com',
     u'eqsl': False,
     u'fname': u'TEST CALLSIGN',
     u'geoloc': u'user',
     u'image': u'https://s3.amazonaws.com/files.qrz.com/x/xx3xx/oval_bumper_sticker_600.png',
     u'imageinfo': u'600:600:87971',
     u'land': u'Guadeloupe',
     u'latitude': 51.396953,
     u'license_class': u'3',
     u'locator': u'FO51sj',
     u'longitude': -68.41959,
     u'lotw': False,
     u'moddate': datetime(2016, 4, 21, 19, 19, 6, tzinfo=UTC),
     u'mqsl': False,
     u'name': u'DO NOT QSL',
     u'qslmgr': u'Via BURO or AA7BQ',
     u'state': u'JJ',
    #  u'user': u'KF7WIS',
     u'zipcode': u'00033'
}


response_333 = {
    const.COUNTRY: u'Iraq',
    u'cc': u'IQ',
    const.LONGITUDE: 44.362793,
    const.CQZ: 21,
    const.ITUZ: 39,
    const.LATITUDE: 33.358062,
    u'timezone': 3.0,
    const.ADIF: 333,
    const.CONTINENT: u'AS',
    u'ccc': u'IRQ'
}

#TESTS
#===========================================================


class TestQrzConstructur:

    def test_get_session_key(self):
        lib = LookupLib(lookuptype="qrz", username=QRZ_USERNAME, pwd=QRZ_PWD)
        assert len(lib._apikey) == 32

    def test_get_session_key_with_invalid_username(self):
        with pytest.raises(ValueError):
            lib = LookupLib(lookuptype="qrz", username="hello", pwd=QRZ_PWD)

    def test_get_session_key_with_invalid_password(self):
        with pytest.raises(ValueError):
            lib = LookupLib(lookuptype="qrz", username=QRZ_USERNAME, pwd="hello")

    def test_get_session_key_with_empty_username_and_password(self):
        with pytest.raises(ValueError):
            lib = LookupLib(lookuptype="qrz", username="", pwd="")


class TestQrz_Callsign_Lookup:

    def test_lookup_callsign(self, fix_qrz):
        data = fix_qrz._lookup_qrz_callsign("xx1xx", fix_qrz._apikey)
        data.pop('u_views', None)
        assert data == response_XX1XX #check content
        assert len(data) == len(response_XX1XX) #ensure all fields are included

        data = fix_qrz._lookup_qrz_callsign("XX1XX", fix_qrz._apikey)
        data.pop('u_views', None)
        assert data == response_XX1XX

        data = fix_qrz._lookup_qrz_callsign("XX2XX", fix_qrz._apikey)
        data.pop('u_views', None)
        assert data == response_XX2XX
        assert len(data) == len(response_XX2XX)

        data = fix_qrz._lookup_qrz_callsign("XX3XX", fix_qrz._apikey)
        data.pop('u_views', None)
        assert data == response_XX3XX
        assert len(data) == len(response_XX3XX)

    def test_lookup_callsign_with_unicode_escaping(self, fix_qrz):
        data = fix_qrz._lookup_qrz_callsign("XX2XX", fix_qrz._apikey)
        data.pop('u_views', None)
        assert data == response_XX2XX

    def test_lookup_callsign_does_not_exist(self, fix_qrz):
        with pytest.raises(KeyError):
            fix_qrz._lookup_qrz_callsign("XX8XX", fix_qrz._apikey)

    def test_lookup_callsign_with_empty_input(self, fix_qrz):
        with pytest.raises(ValueError):
            fix_qrz._lookup_qrz_callsign("", fix_qrz._apikey)

    def test_lookup_callsign_with_invalid_input(self, fix_qrz):
        with pytest.raises(AttributeError):
            fix_qrz._lookup_qrz_callsign(3, fix_qrz._apikey)


class TestQrz_DXCC_Lookup:

    def test_lookup_dxcc_with_int(self, fix_qrz):
        data = fix_qrz._lookup_qrz_dxcc(333, fix_qrz._apikey)
        assert data == response_333 #check content
        assert len(data) == len(response_333) #ensure all fields are included

    def test_lookup_dxcc_with_string(self, fix_qrz):
        data = fix_qrz._lookup_qrz_dxcc("333", fix_qrz._apikey)
        assert data == response_333 #check content
        assert len(data) == len(response_333) #ensure all fields are included

    def test_lookup_dxcc_does_not_exist(self, fix_qrz):
        with pytest.raises(KeyError):
            fix_qrz._lookup_qrz_dxcc('854', fix_qrz._apikey)

    def test_lookup_dxcc_wrong_input(self, fix_qrz):
        with pytest.raises(ValueError):
            fix_qrz._lookup_qrz_dxcc('', fix_qrz._apikey)

    def test_lookup_dxcc(self, fix_qrz):
        data = fix_qrz.lookup_entity(333)
        assert data == response_333 #check content
