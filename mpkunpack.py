# This code is based on CoZ's mpkpack.py at https://github.com/CommitteeOfZero/sghd-patch/blob/master/mpkpack.py

import csv
import sys
import os
import os.path
import io

print("                       M P K  U N P A C K")
print("\"Thailand will get to play Steins;Gate.\" --Phachara Chirapakachote")
if len(sys.argv) != 2:
    print("Usage: mpkunpack.py <mpk file>")
    print("Example: mpkunpack.py c0data.mpk")
    print("Output: Folder with extracted files + TOC file")
    sys.exit(0)

mpkfile = sys.argv[1]
csv_file_name = os.path.basename(mpkfile)[0:-4] + "_toc.csv"
output_path = os.path.basename(mpkfile)[0:-4]

if not os.path.exists(output_path):
    os.makedirs(output_path)

with io.open(mpkfile, "rb") as f:
    # ตรวจดูว่าใช่ไฟล์ MPK จริงไหม
    f.seek(os.SEEK_SET)
    if f.read(3) != b'MPK':
        print("Invalid file.")
        sys.exit()

    # สร้างไฟล์ csv
    with io.open(csv_file_name, "w", newline="") as csv_file:
        item = csv.writer(csv_file)
        item.writerow(["# id", "filename_on_disk", "filename_in_archive"])

    # นับจำนวนไฟล์ที่อยู่ใน archive
    f.seek(8)
    count = int.from_bytes(f.read(8), byteorder="little", signed=False)
    print("======================")
    print("File count: " + str(count))
    print("======================")

    i = 0
    for file in range(count):
        f.seek(0x40 + (i * 0x100), os.SEEK_SET)
        # ข้าม compression field (เป็นเลข 0 เสมอ)
        f.seek(0x4, os.SEEK_CUR)
        # อ่านข้อมูล meta ของแต่ละไฟล์
        id = int.from_bytes(f.read(4), byteorder="little", signed=False)
        offset = int.from_bytes(f.read(8), byteorder="little", signed=False)
        filesize = int.from_bytes(f.read(8), byteorder="little", signed=False)
        filesize_uncompressed = int.from_bytes(f.read(8), byteorder="little", signed=False)
        filename = f.read(48).decode('ascii').rstrip('\x00') 

        # แสดงข้อมูลที่ได้
        print("Id: " + str(id))
        print("Offset (int): " + str(offset))
        print("File Size: " + str(filesize_uncompressed) + " bytes")
        print("File Name: " + filename)
        print()

        # สร้างและเขียนข้อมูลแต่ละไฟล์
        with io.open(output_path + "/" + filename, "ab") as file_in_archive:
            f.seek(offset)
            buf = f.read(filesize_uncompressed)
            file_in_archive.write(buf)

        # เขียนไฟล์ csv
        with io.open(csv_file_name, "a", newline="") as csv_file:
            item = csv.writer(csv_file)
            item.writerow([id, output_path + "/" + filename, filename])
        i += 1

    print("Files and TOC extracted successfully.")
    