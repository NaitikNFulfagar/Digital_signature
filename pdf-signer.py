#!/usr/bin/env vpython3
# *-* coding: utf-8 *-*
import sys
import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12
import argparse
import pytz
from endesive.pdf import cms
import re

def eprint(error):
    print(error, file=sys.stderr)

def create_args():
    """Creates CLI arguments for the pdfSigner script."""

    parser = argparse.ArgumentParser(description='Script for digitally signing a pdf')
    parser.add_argument('p12_certificate', type=str, help='Specify keystore file in .p12 format (Mandatory)')
    parser.add_argument('password', type=str, help=' Specify password for keystore file (mandatory)')
    parser.add_argument('src', type=str,
        help='Specify the source file (.pdf) that needs to be digitally signed. Only 1 file at a time can be signed. (Mandatory) ')
    
    parser.add_argument('logo', type=str,
        help='Specify the source logo (.png) that needs to be digitally signed. Only 1 file at a time can be signed. (Mandatory) ')
    
    parser.add_argument('-d', '--dest', type=str,
        help='Specify the destination file where digitally signed content will be stored.When not specified, by default it will '
        'digitally sign the source file.(Mandatory) \n'
        'E.g. Given source file /var/hp/some.pdf will be digitally signed')
    parser.add_argument('-c', '--coords', type=str,
        help='Specify the co-ordinates of where you want the digital signature to be placed on the PDF file page.(Optional)\n'
        'Format: Accepts 4 comma-separated float values (without spaces). E.g. 1,2,3,4 ')
    parser.add_argument('-p', '--page', type=int,
        help='You can specify the page number of PDF file where digital signature(Optional)')

    return parser.parse_args()

def validate_args(args):
    """Validating commandline arguments raises valueError exception with if any command
    line arguments are not valid."""

    IS_PFX = lambda p12_certificate: re.match( r'^(.[^,]+)(.p12|.P12){1}$', p12_certificate)
    if not IS_PFX(args.p12_certificate):
        raise ValueError('Not a proper p12 file with .p12 or .P12 extension')
    if args.coords:
        for num in args.coords.split(','):
            if not num.isdigit():
                raise ValueError('Coords are not integers')




def main():
    """args = create_args()

    try:
        validate_args(args)
    except ValueError as e:
        import traceback; traceback.print_exc()
        sys.exit(1)"""
    try:
        date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
        date = date.strftime("Date:%Y-%m-%d")
        
        
        dct = {
            "aligned": 0,
            "sigflags": 3,
            "sigflagsft": 132,
            "sigpage": 0,
            "auto_sigfield": True,
            #"sigandcertify": False,
            "signaturebox": (350, 50, 550, 150),
            "signform": False,
            # "sigfield": "Signature",

            # Text will be in the default font
            # Fields in the list display will be included in the text listing
            # Icon and background can both be set to images by having their
            #   value be a path to a file or a PIL Image object
            # If background is a list it is considered to be an opaque RGB colour
            # Outline is the colour used to draw both the border and the text
            "signature_appearance": {
                # 'background': [0.75, 0.8, 0.95],
                'icon': "n.jpg",
                # 'outline': [0.2, 0.3, 0.5],
                # 'border': 2,
                # 'labels': True,
                'display': 'reason,date'.split(','),
                },
            
            "contact": "abc@example.com",
            "location": "xyz",
            "signingdate": date,
            "reason": "Digitally signed by\nMayank Singh",
            "password": "1234",
        }
        print(dct)

        with open("naitik.p12", "rb") as fp:
            p12 = pkcs12.load_key_and_certificates(
                fp.read(), "Naitik@123".encode(), backends.default_backend()
            )
        fname = "a.pdf"
        if len(sys.argv) > 1:
            fname = sys.argv[1]
        fname = "a.pdf"
        datau = open(fname, "rb").read()
        datas = cms.sign(datau, dct, p12[0], p12[1], p12[2], "sha256")
        fname = fname.replace(".pdf", "-signature_appearance.pdf")
        with open(fname, "wb") as fp:
            fp.write(datau)
            fp.write(datas)
    except Exception as e:
        eprint(e)
        sys.exit(1)
         


main()