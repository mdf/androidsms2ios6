androidsms2ios6
===============

quickly hacked together scripts to insert SMS from an Android backup into ios6 sms.db, work in progress

- androidsms2ios6.py translates and imports a copy of sms.db from Android into an existing sms.db for IOS 6, as copied from an ITunes backup

- mbdb.py updates the sha1 hash and filesize in the ITunes backup Manifest.mbdb to allow ITunes to properly restore the modified sms.db back to the phone