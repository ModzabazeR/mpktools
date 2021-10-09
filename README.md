# mpktools
Tool for pack/unpack Mages Package files (.mpk)
Currently using for Steins;Gate mpk files. Using unpack will extract the files in the archive, and create TOC file. Using pack will pack the files to `.mpk`, and you'll need a TOC file to pack it.

# โครงสร้าง

## หัวเรื่องของไฟล์
##### ทั้งหมด 8 bytes

ชื่อ | ขนาด | ข้อมูล |
--- | --- | --- 
**IDENT** | 4 bytes | "MPK"\0
Null Bytes | 2 bytes | \0\0
Two | 2 bytes | 0x2

## จำนวนไฟล์
##### ทั้งหมด 56 bytes
ชื่อ | ขนาด |
--- | --- 
File count | 8 bytes
Null Bytes | 6 * 8 bytes

## ข้อมูลแต่ละไฟล์
##### ไฟล์ละ 256 bytes
ทำซ้ำเป็นจำนวนเท่ากับ `จำนวนไฟล์` ทั้งหมด

ชื่อ | ขนาด |
--- | --- 
isCompressed | 4 bytes
Index | 4 bytes
Position | 8 bytes
Size in File | 8 bytes
Uncompressed Size (ถ้าไม่มีการบีบอัดก็จะเท่ากับอันก่อนหน้าเลย) | 8 bytes
Null terminated file name | 224 bytes

## ข้อมูลดิบ
##### ไฟล์ละ n bytes
ทำซ้ำเป็นจำนวนเท่ากับ `จำนวนไฟล์` ทั้งหมด

ชื่อ | ขนาด |
--- | --- 
Raw data | เท่ากับ`ขนาด`ของไฟล์นั้นๆ
