# encoding: utf8

import putio

client = putio.Client('')

f = client.File({
    'id': 'file',
    'name': 'Röyksopp',
    'size': 0,
    'content_type': 'text/plain',
    'crc32': '00000000',
})

f.download('/tmp')
