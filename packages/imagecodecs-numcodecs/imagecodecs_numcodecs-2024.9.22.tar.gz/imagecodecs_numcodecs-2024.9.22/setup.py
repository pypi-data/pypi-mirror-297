"""
Imagecodecs_numcodecs is a Python package that registers the following 
`Numcodecs <https://github.com/zarr-developers/numcodecs>`_ entry points 
for the `Imagecodecs <https://github.com/cgohlke/imagecodecs>`_ package::

    imagecodecs_aec = imagecodecs.numcodecs:Aec
    imagecodecs_apng = imagecodecs.numcodecs:Apng
    imagecodecs_avif = imagecodecs.numcodecs:Avif
    imagecodecs_bitorder = imagecodecs.numcodecs:Bitorder
    imagecodecs_bitshuffle = imagecodecs.numcodecs:Bitshuffle
    imagecodecs_blosc = imagecodecs.numcodecs:Blosc
    imagecodecs_blosc2 = imagecodecs.numcodecs:Blosc2
    imagecodecs_bmp = imagecodecs.numcodecs:Bmp
    imagecodecs_brotli = imagecodecs.numcodecs:Brotli
    imagecodecs_byteshuffle = imagecodecs.numcodecs:Byteshuffle
    imagecodecs_bz2 = imagecodecs.numcodecs:Bz2
    imagecodecs_checksum = imagecodecs.numcodecs:Checksum
    imagecodecs_cms = imagecodecs.numcodecs:Cms
    imagecodecs_dds = imagecodecs.numcodecs:Dds
    imagecodecs_deflate = imagecodecs.numcodecs:Deflate
    imagecodecs_delta = imagecodecs.numcodecs:Delta
    imagecodecs_dicomrle = imagecodecs.numcodecs:Dicomrle
    imagecodecs_eer = imagecodecs.numcodecs:Eer
    imagecodecs_float24 = imagecodecs.numcodecs:Float24
    imagecodecs_floatpred = imagecodecs.numcodecs:Floatpred
    imagecodecs_gif = imagecodecs.numcodecs:Gif
    imagecodecs_heif = imagecodecs.numcodecs:Heif
    imagecodecs_jetraw = imagecodecs.numcodecs:Jetraw
    imagecodecs_jpeg = imagecodecs.numcodecs:Jpeg
    imagecodecs_jpeg2k = imagecodecs.numcodecs:Jpeg2k
    imagecodecs_jpegls = imagecodecs.numcodecs:Jpegls
    imagecodecs_jpegxl = imagecodecs.numcodecs:Jpegxl
    imagecodecs_jpegxr = imagecodecs.numcodecs:Jpegxr
    imagecodecs_jpegxs = imagecodecs.numcodecs:Jpegxs
    imagecodecs_lerc = imagecodecs.numcodecs:Lerc
    imagecodecs_ljpeg = imagecodecs.numcodecs:Ljpeg
    imagecodecs_lz4 = imagecodecs.numcodecs:Lz4
    imagecodecs_lz4f = imagecodecs.numcodecs:Lz4f
    imagecodecs_lz4h5 = imagecodecs.numcodecs:Lz4h5
    imagecodecs_lzf = imagecodecs.numcodecs:Lzf
    imagecodecs_lzfse = imagecodecs.numcodecs:Lzfse
    imagecodecs_lzham = imagecodecs.numcodecs:Lzham
    imagecodecs_lzma = imagecodecs.numcodecs:Lzma
    imagecodecs_lzo = imagecodecs.numcodecs:Lzo
    imagecodecs_lzw = imagecodecs.numcodecs:Lzw
    imagecodecs_packbits = imagecodecs.numcodecs:Packbits
    imagecodecs_packints = imagecodecs.numcodecs:Packints
    imagecodecs_pcodec = imagecodecs.numcodecs:Pcodec
    imagecodecs_pglz = imagecodecs.numcodecs:Pglz
    imagecodecs_png = imagecodecs.numcodecs:Png
    imagecodecs_qoi = imagecodecs.numcodecs:Qoi
    imagecodecs_quantize = imagecodecs.numcodecs:Quantize
    imagecodecs_rcomp = imagecodecs.numcodecs:Rcomp
    imagecodecs_rgbe = imagecodecs.numcodecs:Rgbe
    imagecodecs_snappy = imagecodecs.numcodecs:Snappy
    imagecodecs_sperr = imagecodecs.numcodecs:Sperr
    imagecodecs_spng = imagecodecs.numcodecs:Spng
    imagecodecs_sz3 = imagecodecs.numcodecs:Sz3
    imagecodecs_szip = imagecodecs.numcodecs:Szip
    imagecodecs_tiff = imagecodecs.numcodecs:Tiff
    imagecodecs_ultrahdr = imagecodecs.numcodecs:Ultrahdr
    imagecodecs_webp = imagecodecs.numcodecs:Webp
    imagecodecs_xor = imagecodecs.numcodecs:Xor
    imagecodecs_zfp = imagecodecs.numcodecs:Zfp
    imagecodecs_zlib = imagecodecs.numcodecs:Zlib
    imagecodecs_zlibng = imagecodecs.numcodecs:Zlibng
    imagecodecs_zopfli = imagecodecs.numcodecs:Zopfli
    imagecodecs_zstd = imagecodecs.numcodecs:Zstd

"""

import inspect
import pprint

from setuptools import setup

import imagecodecs
import imagecodecs.numcodecs

entry_points = [
    f'{cls.codec_id} = imagecodecs.numcodecs:{name}'
    for name, cls in inspect.getmembers(imagecodecs.numcodecs)
    if hasattr(cls, 'codec_id') and name != 'Codec'
]

pprint.pprint(entry_points)

setup(
    name='imagecodecs-numcodecs',
    version=imagecodecs.__version__,
    description='Numcodecs entry points for the imagecodecs package',
    long_description=__doc__,
    long_description_content_type='text/x-rst',
    author='Christoph Gohlke',
    author_email='cgohlke@cgohlke.com',
    url='https://www.cgohlke.com',
    project_urls={
        'Bug Tracker': 'https://github.com/cgohlke/imagecodecs/issues',
        'Source Code': 'https://github.com/cgohlke/imagecodecs',
        # 'Documentation': 'https://',
    },
    python_requires='>=3.9',
    install_requires=['numcodecs', f'imagecodecs>={imagecodecs.__version__}'],
    entry_points={'numcodecs.codecs': entry_points},
    platforms=['any'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
