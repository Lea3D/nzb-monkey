import re

SAMPLE_XML = """
<item>
<link>https://nzbindex.com/download/9ea37891-5706-35a6-a1eb-575ad6725f1d.nzb</link>
</item>
"""

REGEX = re.compile(r'<link>https://nzbindex\.com/download/(?P<id>[0-9a-fA-F-]{36})\.nzb</link>')


def test_nzbindex_regex():
    match = REGEX.search(SAMPLE_XML)
    assert match, "No match for NZBIndex regex"
    nzb_id = match.group('id')
    assert nzb_id == '9ea37891-5706-35a6-a1eb-575ad6725f1d'
    download_url = f"https://nzbindex.com/download/{nzb_id}.nzb"
    assert download_url == 'https://nzbindex.com/download/9ea37891-5706-35a6-a1eb-575ad6725f1d.nzb'
