import Fungsi_Data_1 as FD1
import Fungsi_Data_2 as FD2
import csv
from datetime import datetime
import pandas as pd
    
nama = (input("Masukkan Nama Anda: "))
pin = (input("Masukkan PIN (5 digit angka): "))

if not (pin.isdigit() and len(pin) == 5):
    print("PIN harus 5 digit angka")
    FD1.catat_login(nama, "Telah GAGAL melakukan Login")

if pin[0] == '1':
    role = "admin"
    file_data = "Data_Admin_Perpustakaan.csv"
elif pin[0] == '2':
    role = "Anggota"
    file_data = "Data_Anggota_Perpustakaan.csv"
else:
    file_data = ""
    FD1.catat_login(nama, "Tidak Diketahui", "Telah  GAGAL Melakukan Login")
    

try:
    with open(file_data, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == nama and row['password'] == pin:
                print(f"\nLogin berhasil sebagai {role.upper()} Perpustakaan")
                FD1.catat_login(nama, role, "BERHASIL")

                if role == "admin":
                    FD1.menu_admin()
                else:
                    FD2.menu_user(nama)
except FileNotFoundError:
    print("Data akun tidak ditemukan.")
    FD1.catat_login(nama, "Tidak Diketahui ", "Telah Gagal Melakukan Login")



