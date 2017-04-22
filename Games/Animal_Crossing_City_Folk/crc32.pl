use strict;
use warnings;
use String::CRC32;

open(SOMEFILE, "item.bin");
binmode SOMEFILE;
my $crc = crc32(*SOMEFILE, 4225757159);
my $hex = sprintf("%X", $crc);
print($hex, "\n");
close(SOMEFILE);