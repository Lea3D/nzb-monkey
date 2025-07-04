import os
import sys
import types
from unittest.mock import patch, Mock

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

# Provide a minimal distutils.spawn module required by nzblnkconfig
distutils_module = types.ModuleType('distutils')
spawn_module = types.ModuleType('distutils.spawn')
def _find_executable(_):
    return '/usr/bin/true'
spawn_module.find_executable = _find_executable
distutils_module.spawn = spawn_module
sys.modules.setdefault('distutils', distutils_module)
sys.modules.setdefault('distutils.spawn', spawn_module)

from nzbmonkey import NZBDownload


def test_binsearch_download():
    sample_html = '<a href="https://binsearch.info/details/ABC123">link</a>'

    search_response = Mock()
    search_response.text = sample_html
    search_response.status_code = 200

    nzb_response = Mock()
    nzb_response.text = 'NZB DATA'
    nzb_response.status_code = 200

    with patch('nzbmonkey.requests.get', side_effect=[search_response, nzb_response]):
        downloader = NZBDownload(
            'https://binsearch.info/search?q={0}',
            r'href="https?://(?:www\.)?binsearch\.info/(?:details/|\?action=nzb&id=)(?P<id>[^"&/]+)',
            'https://binsearch.info/nzb?{id}=on',
            'test'
        )
        success, nzb = downloader.download_nzb()
        assert success
        assert nzb == 'NZB DATA'
        assert downloader.nzb_url == 'https://binsearch.info/nzb?ABC123=on'


def test_binsearch_regex_new_style():
    sample_html = '<a href="https://binsearch.info/?action=nzb&id=XYZ789">link</a>'

    search_response = Mock()
    search_response.text = sample_html
    search_response.status_code = 200

    nzb_response = Mock()
    nzb_response.text = 'NZB DATA'
    nzb_response.status_code = 200

    with patch('nzbmonkey.requests.get', side_effect=[search_response, nzb_response]):
        downloader = NZBDownload(
            'https://binsearch.info/search?q={0}',
            r'href="https?://(?:www\.)?binsearch\.info/(?:details/|\?action=nzb&id=)(?P<id>[^"&/]+)',
            'https://binsearch.info/nzb?{id}=on',
            'test'
        )
        success, nzb = downloader.download_nzb()
        assert success
        assert nzb == 'NZB DATA'
        assert downloader.nzb_url == 'https://binsearch.info/nzb?XYZ789=on'

