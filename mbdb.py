# loosely based on http://stackoverflow.com/questions/3085153/how-to-parse-the-manifest-mbdb-file-in-an-ios-4-0-itunes-backup


import sys
import hashlib
import struct


def hashfile(filepath):
    sha1 = hashlib.sha1()
    f = open(filepath, 'rb')
    try:
        sha1.update(f.read())
    finally:
        f.close()
    return sha1.digest()

def filesize(filepath):
    size = -1
    f = open(filepath, 'rb')
    try:
        f.seek(0,2)
        size = f.tell()
    finally:
        f.close()
    return size

def getint(data, offset, intsize):
    value = 0
    while intsize > 0:
        value = (value<<8) + ord(data[offset])
        offset = offset + 1
        intsize = intsize - 1
    return value, offset

def getstring(data, offset):
    if data[offset] == chr(0xFF) and data[offset+1] == chr(0xFF):
        return '', offset+2 # Blank string
    length, offset = getint(data, offset, 2) # 2-byte length
    value = data[offset:offset+length]
    return value, (offset + length)

def process_mbdb_file(data):
    mbdb = {} # Map offset of info in this file => file info
    if data[0:4] != "mbdb": raise Exception("This does not look like an MBDB file")
    offset = 4
    offset = offset + 2 # value x05 x00, not sure what this is
    while offset < len(data):
        fileinfo = {}
        fileinfo['start_offset'] = offset
        fileinfo['domain'], offset = getstring(data, offset)
        fileinfo['filename'], offset = getstring(data, offset)
        fileinfo['linktarget'], offset = getstring(data, offset)
        fileinfo['datahash_offset'] = offset
        fileinfo['datahash'], offset = getstring(data, offset)
        fileinfo['unknown1'], offset = getstring(data, offset)
        fileinfo['mode'], offset = getint(data, offset, 2)
        fileinfo['unknown2'], offset = getint(data, offset, 4)
        fileinfo['unknown3'], offset = getint(data, offset, 4)
        fileinfo['userid'], offset = getint(data, offset, 4)
        fileinfo['groupid'], offset = getint(data, offset, 4)
        fileinfo['mtime'], offset = getint(data, offset, 4)
        fileinfo['atime'], offset = getint(data, offset, 4)
        fileinfo['ctime'], offset = getint(data, offset, 4)
        fileinfo['filelen_offset'] = offset
        fileinfo['filelen'], offset = getint(data, offset, 8)
        fileinfo['flag'], offset = getint(data, offset, 1)
        fileinfo['numprops'], offset = getint(data, offset, 1)
        fileinfo['properties'] = {}
        for ii in range(fileinfo['numprops']):
            propname, offset = getstring(data, offset)
            propval, offset = getstring(data, offset)
            fileinfo['properties'][propname] = propval
        mbdb[fileinfo['start_offset']] = fileinfo
    return mbdb


data = open('Manifest.mbdb').read()
mbdb = process_mbdb_file(data)
smsdb = '3d0d7e5fb2ce288813306e4d4636395e047a3d28'

bdata = bytearray(data)

for record in mbdb:
    
    r = mbdb[record]
    if(r['filename']!='Library/SMS/sms.db'):
        continue
    
    filelen_offset = r['filelen_offset']
    len = filesize(smsdb)
    
    s = struct.pack('>q', len)
    _offset = filelen_offset
    for c in s:
        bdata[_offset] = c
        _offset+=1

    datahash_offset = r['datahash_offset']
    hash = hashfile(smsdb)
    
    print('new hash')
    print(':'.join('{0:x}'.format(ord(c)) for c in hash))
    
    _offset = datahash_offset+2 # 20/0x14 character sha1
    for c in hash:
        bdata[_offset] = c
        _offset+=1

    f = open('Manifest.mbdb.new', 'wb')
    f.write(bdata)
    f.close()

