// By BFGR based on Zeventig by Segher
// Licensed under the terms of the GNU GPL, version 2
// http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
// BFGR WadTools v0.39a

#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#include "tools.h"

#define ERROR(s) do { fprintf(stderr, s "\n"); exit(1); } while (0)

static FILE *fp;

static u8 *get_wad(u32 len)
{
	u32 rounded_len;
	u8 *p;

	rounded_len = round_up(len, 0x40);
	p = malloc(rounded_len);
	if (p == 0)
		fatal("malloc");
	if (len)
		if (fread(p, rounded_len, 1, fp) != 1)
			fatal("get_wad read, len = %x", len);

	return p;
}

static void do_install_wad(u8 *header)
{
	u32 header_len;
	u32 cert_len;
	u32 tik_len;
	u32 tmd_len;
	u32 app_len;
	u32 trailer_len;
	u8 *cert;
	u8 *tik;
	u8 *tmd;
	u32 ret;

	header_len = be32(header);
	if (header_len != 0x20)
		fatal("bad install header length (%x)", header_len);

	cert_len = be32(header + 8);
	tik_len = be32(header + 0x10);
	tmd_len = be32(header + 0x14);
	app_len = be32(header + 0x18);
	trailer_len = be32(header + 0x1c);

	cert = get_wad(cert_len);
	tik = get_wad(tik_len);
	tmd = get_wad(tmd_len);
		printf("Normal sign check...\n");
		ret = check_cert_chain(tik, tik_len, cert, cert_len);
		if (ret)
			fprintf(stderr, "ticket trucha cert failure (%d)\n", ret);
	
		ret = check_cert_chain(tmd, tmd_len, cert, cert_len);
		if (ret)
			fprintf(stderr, "tmd trucha cert failure (%d)\n", ret);
		printf("Trucha sign check...\n");
		ret = check_cert_chain_trucha(tik, tik_len, cert, cert_len);
		if (ret)
			fprintf(stderr, "ticket cert failure (%d)\n", ret);
	
		ret = check_cert_chain_trucha(tmd, tmd_len, cert, cert_len);
		if (ret)
			fprintf(stderr, "tmd cert failure (%d)\n", ret);

}

static void do_wad(void)
{
	u8 header[0x80];
	u32 header_len;
	u32 header_type;

	if (fread(header, 0x40, 1, fp) != 1) {
		if (!feof(fp))
			fatal("reading wad header");
		else
			return;
	}
	header_len = be32(header);
	if (header_len >= 0x80)
		ERROR("wad header too big\n");
	if (header_len >= 0x40)
		if (fread(header + 0x40, 0x40, 1, fp) != 1)
			fatal("reading wad header (2)");

	header_type = be32(header + 4);
	switch (header_type) {
	case 0x49730000:
		do_install_wad(header);
		break;
	case 0x69620000:
		do_install_wad(header);
		break;
	default:
		fatal("unknown header type %08x", header_type);
	}
}

int main(int argc, char **argv)
{
	printf("--- WAD Sign Checker ---\n");
	
	if (argc!=2) {
		printf("--- USAGE: wadsigncheck wad_file ---\n");
		exit(-1);
	}
	fp = fopen(argv[1], "rb");
	if (!fp) {
		printf("Cannot open file %s.\n", argv[1]);
		exit(-1);
	}

	do_wad();

	fclose(fp);

	return 0;
}
