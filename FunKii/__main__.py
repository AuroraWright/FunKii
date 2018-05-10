#!/usr/bin/python
# -*- coding: utf-8 -*-
#  FunKii

from __future__ import unicode_literals, print_function

__VERSION__ = 1.0

import argparse
import binascii
import os
import re
import sys

try:
    from urllib.request import urlopen
    from urllib.error import URLError, HTTPError
except ImportError:
    from urllib2 import urlopen, URLError, HTTPError

try:
    real_input = raw_input  # Python2
except NameError:
    real_input = input  # Python3

SYMBOLS = {
    'customary': ('B', 'KB', 'MB', 'GB', 'T', 'P', 'E', 'Z', 'Y'),
}
MAGIC = binascii.a2b_hex('00010000B3ADB3226B3C3DFF1B4B407716FF4F7AD76486C895AC562D21F10601D4F66428191C07768FDF1AE2CE7B27C90FBC0AD0312578EC0779B657D4372413A7F86F0C14C0EF6E0941ED2B05EC3957360789004A878D2E9DF8C7A5A9F8CAB311B1187957BBF898E2A25402CF5439CF2BBFA0E1F85C066E839AE094CA47E01558F56E6F34E92AA2DC38937E37CD8C5C4DFD2F114FE868C9A8D9FED86E0C2175A2BD7E89B9C7B513F41A7961443910EFF9D7FE572218D56DFB7F497AA4CB90D4F1AEB176E4685DA7944060982F0448401FCFC6BAEBDA1630B473B415233508070A9F4F8978E62CEC5E9246A5A8BDA0857868750C3A112FAF95E838C8990E87B162CD10DAB3319665EF889B541BB336BB67539FAFC2AE2D0A2E75C02374EA4EAC8D99507F59B95377305F2635C608A99093AC8FC6DE23B97AEA70B4C4CF66B30E58320EC5B6720448CE3BB11C531FCB70287CB5C27C674FBBFD8C7FC94220A473231D587E5A1A1A82E37579A1BB826ECE0171C97563474B1D46E679B282376211CDC7002F4687C23C6DC0D5B5786EE1F273FF0192500FF4C7506AEE72B6F43DF608FEA583A1F9860F87AF524454BB47C3060C94E99BF7D632A7C8AB4B4FF535211FC18047BB7AFA5A2BD7B884AD8E564F5B89FF379737F1F5013B1F9EC4186F922AD5C4B3C0D5870B9C04AF1AB5F3BC6D0AF17D4708E443E973F7B7707754BAF3ECD2AC49000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000526F6F7400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001434130303030303030310000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000005BFA7D5CB279C9E2EEE121C6EAF44FF639F88F078B4B77ED9F9560B0358281B50E55AB721115A177703C7A30FE3AE9EF1C60BC1D974676B23A68CC04B198525BC968F11DE2DB50E4D9E7F071E562DAE2092233E9D363F61DD7C19FF3A4A91E8F6553D471DD7B84B9F1B8CE7335F0F5540563A1EAB83963E09BE901011F99546361287020E9CC0DAB487F140D6626A1836D27111F2068DE4772149151CF69C61BA60EF9D949A0F71F5499F2D39AD28C7005348293C431FFBD33F6BCA60DC7195EA2BCC56D200BAF6D06D09C41DB8DE9C720154CA4832B69C08C69CD3B073A0063602F462D338061A5EA6C915CD5623579C3EB64CE44EF586D14BAAA8834019B3EEBEED3790001000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100014E005FF13F86758DB69C45630FD49BF4CC5D54CFCC22347257ABA4BA53D2B33DE6EC9EA1575453AE5F933D96BFF7CC7A79566E847B1B6077C2A93871301A8CD3C93D4DB326E9879266E9D3BA9F79BC4638FA2D20A03A7067A411A7A0B7D912AD116A3AC46E324247C208BAB4949CC52ED02F19F651E0DF2E3653AAAF97A692BBA91DD86E242EB308775511CE98F6A2F426C92704D0FC8DD4809ED761BD11B785948CD6D07ADBA408D0F086F65AAE1914B2889AA8AE4AA2AAC761A90D412CB15009AB3E93FCA924DECE4F7C06ABDC2E609D68BE0073FA80576A145EEDC48B7432870793C8FCA6D83E096EC5F2A9C421E748B373405BE2FA8AE15878E9D5238875000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000526F6F742D43413030303030303031000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000143503030303030303034000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000F1B8A064C16DF3832955C3295B72F0332E97EF14848A68049CA68EACDE145033B86C108D48335C5D0CAB770462544755452A900070B156925C1786E2CD206DCCDC2C2E376E27FCB42066CC0A8CE9FEE85704E6CA631A2E7E917E947C3991773629D1556185BBD7B773CA37479E5FAAA3B605E001E1ACE58DD8F84782D645FCE3A1CD03AB36F0F386B1A2D13740A1948A53BA1B0D8C4863CD6B2C2E206494804C62FAA93A7E33A9EA786B59CAE3AB3645F4CB8FD7906B8268CDACF17B3AEC46831B91F6DE186183BC4B326793C72E50D91E36A0DCE2B97DA0213E4696021F331CBEAE8DFC928732AA44DC78E7199A3DDD57227E9E77DE326386936C11ACA70F8119D33A990001000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100017D9D5EBA5281DCA7065D2F0868DB8AC73ACE7EA991F1969FE1D0F2C11FAEC0C3F01ADCB446ADE5CA03B625219462C6E1410DB9E63FDE98D1AF263B4CB28784278272EF27134B87C258D67B62F2B5BF9CB6BA8C89192EC50689AC7424A022094003EE98A4BD2F013B593FE5666CD5EB5AD7A49310F34EFBB43D46CBF1B523CF82F68EB56DB904A7C2A82BE11D78D39BA20D90D30742DB5E7AC1EFF221510962CFA914A880DCF417BA99930AEE08B0B0E51A3E9FAFCDC2D7E3CBA12F3AC00790DE447AC3C538A8679238078BD4C4B245AC2916886D2A0E594EED5CC835698B4D6238DF05724DCCF681808A7074065930BFF8514137E815FABAA172B8E0696C61E4000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000526F6F742D43413030303030303031000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000158533030303030303033000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000F1B89FD1AD07A9378A7B100C7DC739BE9EDDB7320089AB25B1F871AF5AA9F4589ED18302328E811A1FEFD009C8063643F854B9E13BBB613A7ACF8714856BA45BAAE7BBC64EB2F75D87EBF267ED0FA441A933665E577D5ADEABFB462E7600CA9CE94DC4CB983992AB7A2FB3A39EA2BF9C53ECD0DCFA6B8B5EB2CBA40FFA4075F8F2B2DE973811872DF5E2A6C38B2FDC8E57DDBD5F46EB27D61952F6AEF862B7EE9AC682A2B19AA9B558FBEBB3892FBD50C9F5DC4A6E9C9BFE458034A942182DDEB75FE0D1B3DF0E97E39980877018C2B283F135757C5A30FC3F3084A49AAAC01EE706694F8E1448DA123ACC4FFA26AA38F7EFBF278F369779775DB7C5ADC78991DCF8438D0001000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
TIKTEM = binascii.a2b_hex('0001000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000526F6F742D434130303030303030312D58533030303030303033000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001ACE5E38E4C68000000000000000000000000FFFF000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
execname = 'wadpacker'

parser = argparse.ArgumentParser()
parser.add_argument('-outputdir', action='store', dest='output_dir',
                    help='The custom output directory to store output in, if desired')
parser.add_argument('-nobuild', action='store_false', default=True, dest='build',
                    help='Turn OFF generation of WAD files, titles will be downloaded only.')
parser.add_argument('-retry', type=int, default=4, dest='retry_count',
                    choices=range(0, 10), help='How many times a file download will be attempted')
parser.add_argument('-title', nargs='+', dest='titles', default=[],
                    help='Give TitleIDs to be specifically downloaded')
parser.add_argument('-key', nargs='+', dest='keys', default=[],
                    help='Encrypted Title Key for the Title IDs. Must be in the same order as TitleIDs if multiple')
parser.add_argument('-getcetk', action='store_true', default=False, dest='getcetk',
                    help='Get legit cetk from the CDN, this is only available for system titles and some other free titles.')


def bytes2human(n, f='%(value).2f %(symbol)s', symbols='customary'):
    n = int(n)
    if n < 0:
        raise ValueError("n < 0")
    symbols = SYMBOLS[symbols]
    prefix = {}
    for i, s in enumerate(symbols[1:]):
        prefix[s] = 1 << (i + 1) * 10
    for symbol in reversed(symbols[1:]):
        if n >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return f % locals()
    return f % dict(symbol=symbols[0], value=n)


RE_16_HEX = re.compile(r'^[0-9a-f]{16}$', re.IGNORECASE)
RE_32_HEX = re.compile(r'^[0-9a-f]{32}$', re.IGNORECASE)

check_title_id = RE_16_HEX.match
check_title_key = RE_32_HEX.match


def retry(count):
    for i in range(1, count + 1):
        if i > 1:
            print("*Attempt {} of {}".format(i, count))
        yield i


def progress_bar(part, total, length=10, char='#', blank=' ', left='[', right=']'):
    percent = int((float(part) / float(total) * 100) % 100)
    bar_len = int((float(part) / float(total) * length) % length)
    bar = char * bar_len
    blanks = blank * (length - bar_len)
    return '{}{}{}{} {} of {}, {}%'.format(
        left, bar, blanks, right, bytes2human(part), bytes2human(total), percent
    ) + ' ' * 20


def download_file(url, outfname, retry_count=3, ignore_404=False, expected_size=None, chunk_size=0x4096):
    for _ in retry(retry_count):
        try:
            infile = urlopen(url)
            # start of modified code
            if os.path.isfile(outfname):
                statinfo = os.stat(outfname)
                diskFilesize = statinfo.st_size
            else:
                diskFilesize = 0 
            log('-Downloading {}.\n-File size is {}.\n-File in disk is {}.'.format(outfname, expected_size,diskFilesize))
  
            if expected_size is None or expected_size > diskFilesize:
                with open(outfname, 'wb') as outfile:
                    downloaded_size = 0
                    while True:
                         buf = infile.read(chunk_size)
                         if not buf:
                             break
                         downloaded_size += len(buf)
                         if expected_size and len(buf) == chunk_size:
                             print(' Downloaded {}'.format(progress_bar(downloaded_size, expected_size)), end='\r')
                         outfile.write(buf)
            else:
                print('-File skipped.')
                downloaded_size = statinfo.st_size
            # end of modified code

            if expected_size is not None:
                if int(os.path.getsize(outfname)) < expected_size:
                    print('Content download not correct size\n')
                    continue
                else:
                    print('Download complete: {}\n'.format(bytes2human(downloaded_size)) + ' ' * 40)
        except HTTPError as e:
            if e.code == 404 and ignore_404:
                # We are ignoring this because its a 404 error, not a failure
                return True
        except URLError:
            print('Could not download file...\n')
        else:
            return True
    return False


def make_ticket(title_id, title_key, title_version, fulloutputpath):
    tikdata = bytearray(TIKTEM)
    tikdata[0x1E6:0x01E8] = title_version
    tikdata[0x01DC:0x01E4] = binascii.a2b_hex(title_id)
    tikdata[0x01BF:0x01CF] = binascii.a2b_hex(title_key)
    if title_id[0:8] == '00010005':
    	tikdata[0x1EC:0x01F0] = binascii.a2b_hex('FFFFFFFF')
    open(fulloutputpath, 'wb').write(tikdata)

def process_title_id(title_id, title_key, output_dir=None, build=False, retry_count=3, tickets_only=False):

    typecheck = title_id[0:8]

    isupdate = title_key == 1 or typecheck == '00000001' or typecheck == '00010002' or typecheck == '00010008'

    rawdir = os.path.join('raw', title_id)

    log('Starting work in: "{}"'.format(rawdir))

    if output_dir is not None:
        rawdir = os.path.join(output_dir, rawdir)

    if not os.path.exists(rawdir):
        os.makedirs(os.path.join(rawdir))

    # download stuff
    print('Downloading TMD...')

    baseurl = 'http://ccs.cdn.c.shop.nintendowifi.net/ccs/download/{}'.format(title_id)
    tmd_path = os.path.join(rawdir, 'title.tmd')
    if not download_file(baseurl + '/tmd', tmd_path, retry_count):
        print('ERROR: Could not download TMD...')
        print('MAYBE YOU ARE BLOCKING CONNECTIONS TO NINTENDO? IF YOU ARE, DON\'T...! :)')
        print('Skipping title...')
        return

    with open(tmd_path, 'rb+') as f:
        tmd = f.read()
        content_count = int(binascii.hexlify(tmd[0x1DE:0x1E0]), 16)
        tmdsize = 0x1E4 + (36 * content_count)
        if isupdate:
            f.seek(tmdsize + 0x300)
            cetk = f.read(0x400)
            f.seek(tmdsize)
            cetk = cetk + f.read(0x300)
        f.truncate(tmdsize)

    title_version = tmd[0x1DC:0x1DE]

    # get ticket from keysite, from cdn if game update, or generate ticket
    if isupdate:
        print('\nWe are getting the legit ticket straight from Nintendo.')
        tik_path = os.path.join(rawdir, 'title.tik')
        if not download_file(baseurl + '/cetk', tik_path, retry_count):
            print('ERROR: Could not download ticket from {}'.format(baseurl + '/cetk'))
            print('Skipping title...')
            return
        with open(tik_path, 'rb+') as f:
            tik = f.read(0x2A4)
            cetk = cetk + f.read(0x300)
            f.truncate(0x2A4)
        with open(os.path.join(rawdir, 'title.cert'), 'wb') as f:
            print('Building cert...')
            f.write(cetk)
    else:
        make_ticket(title_id, title_key, title_version, os.path.join(rawdir, 'title.tik'))
        with open(os.path.join(rawdir, 'title.cert'), 'wb') as f:
            f.write(MAGIC)

    print('Downloading Contents...')
    
    total_size = 0
    for i in range(content_count):
        c_offs = 0x1E4 + (0x24 * i)
        total_size += int(binascii.hexlify(tmd[c_offs + 0x08:c_offs + 0x10]), 16)
    print('Total size is {}\n'.format(bytes2human(total_size)))

    for i in range(content_count):
        c_offs = 0x1E4 + (0x24 * i)
        c_id = binascii.hexlify(tmd[c_offs:c_offs + 0x04]).decode()
        i_id = '0000' + binascii.hexlify(tmd[c_offs + 0x04:c_offs + 0x06]).decode()
        expected_size = int(binascii.hexlify(tmd[c_offs + 0x08:c_offs + 0x10]), 16)
        print('Downloading {} of {}.'.format(i + 1, content_count))
        outfname = os.path.join(rawdir, i_id + '.app')

        if not download_file('{}/{}'.format(baseurl, c_id), outfname, retry_count, expected_size=expected_size):
            print('ERROR: Could not download content file... Skipping title')
            return

    log('\nTitle download complete in "{}"\n'.format(rawdir))

    if build:
        waddir = os.path.join('wad', title_id)

        if output_dir is not None:
            waddir = os.path.join(output_dir, waddir)

        if not os.path.exists(waddir):
            os.makedirs(os.path.join(waddir))

        path = os.path.join(waddir, title_id) + '.wad'

        makecommand = ' ' + os.path.join(rawdir) + ' ' + path + ' -e'
        if not isupdate:
            makecommand = makecommand + ' -T'
        os.system(execname + makecommand)
        if(os.path.isfile(path)):
            print('WAD created ok!')
        else:
            print('WAD not created...')
        print('')
        print('')


def main(args=None):
    if len(sys.argv) == 1:
        parser.print_usage()
        sys.exit(1)

    arguments = parser.parse_args()
    titles=arguments.titles
    keys=arguments.keys
    output_dir=arguments.output_dir
    build=arguments.build
    getcetk=arguments.getcetk
    retry_count=arguments.retry_count

    print('*******\nFunKii {} by cearp, the cerea1killer and AuroraWright\n*******\n'.format(__VERSION__))
    titlekeys_data = []

    if (not getcetk) and keys and (len(keys)!=len(titles)):
        print('Number of keys and Title IDs do not match up')
        sys.exit(0)
    if titles and (not keys) and (not getcetk):
        print('You also need to provide \'-keys\'')
        sys.exit(0)

    for title_id in titles:
        title_id = title_id.lower()
        if not check_title_id(title_id):
            print('The Title ID(s) must be 16 hexadecimal characters long')
            print('{} - is not ok.'.format(title_id))
            sys.exit(0)
        title_key = 1 if getcetk else None

        if (not getcetk) and keys:
            title_key = keys.pop()
            if not check_title_key(title_key):
                print('The key(s) must be 32 hexadecimal characters long')
                print('{} - is not ok.'.format(title_id))
                sys.exit(0)

        if not (title_key):
            print('ERROR: Could not find title or ticket for {}'.format(title_id))
            continue

        process_title_id(title_id, title_key, output_dir, build, retry_count)

def log(output):
    output = output.encode(sys.stdout.encoding, errors='replace')
    if sys.version_info[0] == 3:
        output = output.decode(sys.stdout.encoding, errors='replace')
    print(output)


if __name__ == '__main__':
    main()
