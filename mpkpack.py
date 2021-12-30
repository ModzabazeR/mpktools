# This code is modified from CoZ's mpkpack.py at https://github.com/CommitteeOfZero/sghd-patch/blob/master/mpkpack.py

import csv
import os
import struct
import io
import argparse
import tkinter
from tkinter import filedialog

def round_to_2kb(par):
    return int(((par / 2048) + (0 if (par % 2048) == 0 else 1)) * 2048)

parser = argparse.ArgumentParser()
parser.add_argument("-G", type=bool, default=True, help="Enable GUI mode")
parser.add_argument("--tocfile", "--toc", type=str, help="TOC file to be referenced")
args = parser.parse_args()

tocfile = args.tocfile
output_path = f"{tocfile[0:-4]}.mpk" if tocfile else None
enable_gui = args.G

if enable_gui:
    root = tkinter.Tk()
    root.withdraw()
    tocfile = filedialog.askopenfilename(title="Select TOC file", filetypes=[("TOC file", "*.csv")])
    output_path = f"{tocfile[0:-4]}.mpk"
    root.destroy()

if tocfile:
    print("                M P K P A C K")
    print("\"Couldn't have done it better myself.\" --Phil Katz")
    print()
    print("Please don't touch any inputs while I work, or feed me invalid ones")
    print(" or I *will* break horribly")
    print()

entries = []

# อ่านข้อมูลในไฟล์ csv
print("Reading TOC...")
with io.open(tocfile, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0].startswith('#'): # ถ้าแถวไหนเริ่มด้วย # ให้ข้ามไปเลย
            continue
        entry = {
            'id': int(row[0]),
            'filename_on_disk': row[1],
            'filename_in_archive': row[2]
        }
        entries.append(entry) # output จะออกมาเป็น list ของ dictionary
    print("Total entries found: {0}".format(len(entries)))
    print()

# เขียนข้อมูลในไฟล์ mpk
with io.open(output_path, 'wb') as f:
    print("Writing header...")
    magic = b'MPK\0'
    ver = b'\x00\x00\x02\x00'
    f.write(magic)
    f.write(ver)
    count = struct.pack("<Q", len(entries)) # little endian interger 8 bytes (C: unsigned long long)
    f.write(count)
    print("Count in byte: {0}".format(count))
    print()
    
    pos = round_to_2kb(0x40 + len(entries) * 0x100)
    print("Writing files...")
    print("pos = " + str(pos))
    for entry in entries:
        print("[{0}] '{1}' => '{2}' ...".format(entry["id"], entry["filename_on_disk"], entry["filename_in_archive"]))
        f.seek(pos, os.SEEK_SET)
        entry["offset"] = pos
        with io.open(entry["filename_on_disk"], 'rb') as infile: # เปิดไฟล์แต่ละตัว
            while True:
                buf = infile.read(io.DEFAULT_BUFFER_SIZE)
                if buf == b'':
                    break
                f.write(buf)
            entry["filesize"] = infile.tell()
        pos = round_to_2kb(pos + entry["filesize"])
    
    i = 0
    print()
    print("Writing TOC...")
    for entry in entries:
        f.seek(0x40 + (i * 0x100), os.SEEK_SET)
        # skip compression field (always 0 for us)
        f.seek(0x4, os.SEEK_CUR)
        id = struct.pack("<L", entry["id"]) # little endian interger 4 bytes (C: unsigned long)
        f.write(id)
        offset = struct.pack("<Q", entry["offset"]) # little endian interger 8 bytes (C: unsigned long long)
        f.write(offset)
        filesize = struct.pack("<Q", entry["filesize"]) # little endian interger 8 bytes (C: unsigned long long)
        # compressed and uncompressed
        f.write(filesize)
        f.write(filesize)
        # I'm not sure whether the null terminator is necessary
        # so let's just ensure there always is one
        filename = entry["filename_in_archive"].encode('ascii')[:(0xE0 - 1)]
        f.write(filename)
        i += 1

print()
print("Done!")
print("Output file: {0}".format(output_path))
input("Press Enter to exit...")