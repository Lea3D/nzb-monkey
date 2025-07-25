# -*- coding: utf-8 -*-
"""
History
v0.2.11
- Updated BinSearch and NZBIndex rules
v0.2.10
- Fix for Nzbindex search and download urls and regex
- Fix for Binsearch search and download urls and regex
- Remove Binsearch Alternativ Server (no longer available)

v0.2.9
- NZBKing is dead, long live the King

v0.2.8
- Fix #40 SABnzbd API compatibility
- Remove NZBKing (Rip!)

v0.2.7
- Fix #15 (Linux KDE/Plasma konsole option removed, thx @PietroPizzi69)
- Provider fail save (thx @kwaaak)
- Fix DSM7 compatibility

v0.2.6
- fixed NZBKing (thx @macearl)
- small fixes (thx @c-kr)

v0.2.5
- NzbindexBeta removed, its out of beta
- Fixed NzbKing (good for old nzblnks)

v0.2.4
- NzbindexBeta indexer regex fix

v0.2.3
- NzbindexBeta indexer added

v0.2.2
- Newzleech indexer added
- Synology Downloadstation API fixed

v0.2.1
- Fixed category settings

v0.2.0
- Added categories (automatic and manual)
- Added new target: Synology Downloadstation
- Removed offline indexers

v0.1.13
+ Timeout doubled for SABNzbd

v0.1.12
+ Bugfix SABNzbd

v0.1.11
+ Basepath added (thx ralle12345)
+ Sanitized searchstring (thx plintogo)
+ Basic auth for SABNzbd (thx MarcLandis)

v0.1.10
+ requests 2.13.0 (incl openssl)
+ Bugfixes
+ Newzleech search engine

v0.1.9
+ Added option addpaused
+ Lot of bugfixes

v0.1.8
+ Reorg code
+ Added verbose output
+ Added debug log writer to file

v0.1.7
+ Added Search for best NZB
+ Added NZB Folder clean up

v0.1.6
+ Added colorama
+ Added argparse to control NZB-Monkey by arguments
+ Searchengines can be disabled if down or faulted

v0.1.5
+ Separate missing module check
+ Exception Handling for external module import

v0.1.4
+ Switched to configobj

v0.1.3
+ Added dontexecute

v0.1.2
+ Added clipboard parsing

v0.1.1
+ Added NZB-validation

v0.1.0
+ Complete rewrite in python

"""

__version__ = '0.2.11'
__requires__ = ['pyperclip', 'requests', 'configobj', 'colorama', 'cryptography']
