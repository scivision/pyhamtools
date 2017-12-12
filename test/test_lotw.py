import os
import datetime

import pytest

from pyhamtools.qsl import get_lotw_users

class Test_lotw_methods:

    def test_check_content_with_mocked_http_server(self, httpserver):
        httpserver.serve_content(open('./fixtures/lotw-user-activity.csv').read())

        exec(open(os.path.join("./fixtures/","lotw_fixture.py")).read())
        assert get_lotw_users(url=httpserver.url) == lotw_fixture

    def test_download_lotw_list_and_check_types(self):

        data = get_lotw_users()
        assert isinstance(data, dict)
        for key, value in data.iteritems():
            assert isinstance(key, str)
            assert isinstance(value, datetime.datetime)
        assert len(data) > 1000

    def test_with_invalid_url(self):
        with pytest.raises(IOError):
            get_lotw_users(url="https://lotw.arrl.org/lotw-user-activity_FAKE.csv")

    def test_with_more_than_10_invalid_dates(self, httpserver):
        httpserver.serve_content(open('./fixtures/lotw_data_with_errors.html').read())

        with pytest.raises(ValueError):
            get_lotw_users(url=httpserver.url)


