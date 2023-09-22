# This code is based on CoZ's mpkpack.py at https://github.com/CommitteeOfZero/sghd-patch/blob/master/mpkpack.py

import os
import os.path
import io
import argparse
from PyQt5.QtWidgets import QApplication, QFileDialog
import math

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return f"{s} {size_name[i]}"

parser = argparse.ArgumentParser()
parser.add_argument("-G", type=bool, default=True, help="Enable GUI mode")
parser.add_argument("--mpkfile", "--mpk", type=str, help="MPK file to be list")
args = parser.parse_args()

mpkfile = args.mpkfile
output_path = mpkfile[0:-4] if mpkfile else None
enable_gui = args.G

if enable_gui:
    app = QApplication([])
    mpkfile , check = QFileDialog.getOpenFileName(None, "Select MPK file", os.getenv("HOME"), 
                                                  "MPK Files (*.mpk);;All Files (*)")

if mpkfile:
    print("                       M P K  L I S T")
    print("\"Thailand will get to play Steins;Gate.\" --Phachara Chirapakachote")

with io.open(mpkfile, "rb") as f:
    # ตรวจดูว่าใช่ไฟล์ MPK จริงไหม
    f.seek(os.SEEK_SET)
    if f.read(3) != b'MPK':
        raise Exception("Not a MPK file")

    # นับจำนวนไฟล์ที่อยู่ใน archive
    f.seek(8)
    count = int.from_bytes(f.read(8), byteorder="little", signed=False)
    print("======================")
    print(f"File count: {str(count)}")
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
        print(f"Id: {id}")
        print(f"Offset (int): {offset}")
        print(f"File Size: {convert_size(filesize_uncompressed)} ({filesize_uncompressed:,} bytes)")
        print(f"File Name: {filename}")
        print()
        i += 1
