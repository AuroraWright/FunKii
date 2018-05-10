// By BFGR
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

int main(int argc, char **argv)
{
	u64 imet_len;
	u8 *imet;
	u8 hash[16];
	FILE *fp;
	u32 i,j;
	u8 *text;
	u8 add = 0x00;
	u8 *banner;
	u8 *author;
	
	if (argc==3) add = 0x01;
	else if (argc==2) add = 0x00;
	else {
		printf("USAGE: imet_signer [ text_file ]\n");
		exit(-1);
	}
	
	fp = fopen(argv[1], "rb");
	imet_len = getfilesize(fp);
	imet = (u8 *)malloc(imet_len);
	fread(imet, imet_len, 1, fp);
	fclose(fp);
	memset(imet + 0x0630, 0x00, 0x0010); // Remove MD5 sum
	md5(imet + 0x0040, 0x600, hash);
	printf("Old MD5 sum: ");
	printHashMD5(hash);
	printf("\n");
	memcpy(imet + 0x0630, hash, 0x0010);

	if(add) {
	
		text = (u8 *)malloc(6*0x0054);
		memset(text, 0x00, 6*0x0054); // Remove current channel names
		fp = fopen(argv[2], "rb");
		if (!fp) {
			printf("Cannot read file %s.\n", argv[2]); 
			exit(1);
		}
		banner = (u8 *)malloc(0x20); memset(banner, 0x00, 0x20);
		author = (u8 *)malloc(0x10); memset(author, 0x00, 0x10);
		if (fgets(banner, 0x20, fp)==NULL) {
			printf("Cannot read file %s.\n", argv[2]); 
			exit(1);
		}
		banner[strlen(banner)-1] = 0x00;
		if (fgets(author, 0x10, fp)==NULL) {
			printf("Cannot read file %s.\n", argv[2]); 
			exit(1);
		}
		author[strlen(author)-1] = 0x00;
		for (i=0;i<6;i++) {
			if (fgets(text + 0x0054*i, 0x002A, fp)==NULL) {
				printf("Cannot read file %s.\n", argv[2]); 
				exit(1);
			}
			*(text + 0x0054*i + strlen(text + 0x0054*i) - 0x01) = 0x00;
		}
		fclose(fp);
		// Copy banner info
		memcpy(imet, banner, 0x20);
		// Copy author info
		memcpy(imet + 0x0030, author, 0x10);
		
		memset(imet + 0x00F0, 0x00, 0x0054*6);
		for (i=0;i<6;i++) {
			printf("%s...", text + i*0x0054);
			j=0;
			for (j=0;j<0x0054;j++) {
				if (*(text + i*0x0054 + j)!=0x00) {
					memcpy(imet + 0x00F0 + 0x0054*i + j*2 + 1, text + i*0x0054 + j, 1);
					*(imet + 0x00F0 + 0x0054*i + j*2) = 0x00;
				} else {
					break;
				}
			}
			printf("OK\n");
		}
	}
	printf("Recalculating MD5 sum... ");
	memset(imet + 0x0630, 0x00, 0x0010); // Remove MD5 sum
	md5(imet + 0x0040, 0x600, hash);
	memcpy(imet + 0x0630, hash, 0x0010);
	printf("OK\n");
	printf("New MD5 sum: ");
	printHashMD5(hash);
	printf("\n");
	printf("Writing file... ");
	fp = fopen(argv[1], "wb");
		if (!fp) { printf("Cannot write file %s.\n", argv[1]); exit(-1); }
		fwrite(imet, imet_len, 1, fp);
	fclose(fp);
	printf("OK\n");
	
	return 0;
}
