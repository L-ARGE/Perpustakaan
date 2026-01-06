import pandas as pd
import csv
import random
from datetime import timedelta, datetime

def menu_user(username):
    while True:
            print('==================================')
            print('=========== MAIN MENU ============')
            print('= 1. Lihat Daftar Buku           =')
            print('= 2. Lihat Status Buku           =')
            print('= 3. Cari Buku                   =')
            print('= 4. Pinjam Buku                 =')
            print('= 5. Jadwal Pengembalian         =')
            print('= 6. Pengembalian Buku           =')
            print('= 7. keluar                      =')
            print('==================================')    
            try:
                user_anggota = int(input("pilih menu = "))
                if user_anggota == 1 :
                    lihat_daftar_buku()
                    input("Tekan ENTER untuk kembali ke menu...")
                    
                elif user_anggota == 2:
                    lihat_status_buku()
                    input("\nTekan ENTER untuk kembali ke menu...")
                    
                elif user_anggota == 3:
                    cari_buku()
                    input("\nTekan ENTER untuk kembali ke menu...")
                    
                elif user_anggota == 4:
                    pinjam_buku(username)
                    input("\nTekan ENTER untuk kembali ke menu...")
                    
                elif user_anggota == 5:
                    jadwal_pengembalian(username)
                    input("\nTekan ENTER untuk kembali ke menu...")
                    
                elif user_anggota == 6:
                    kembali_buku(username)
                    input("\nTekan ENTER untuk kembali ke menu...")
                    
                elif user_anggota == 7:
                    print('logout')
                    break
            
                else:
                    print('Menu tidak tersedia')
            except ValueError:
                print("Input harus berupa angka")
                
def lihat_daftar_buku():
    daftar = pd.read_csv("Data_Buku.csv")
        
    if len(daftar) == 0:
        print("Data buku belum tersedia")
    else:
        print("====== DAFTAR BUKU ======")
        print(daftar.to_string(index=True))
        
def lihat_status_buku():
    lihat = pd.read_csv("Data_Buku.csv")
    
    if "status" not in lihat.columns:
        print("Data buku belum tersedia")
        return
    elif lihat.empty:
        print("Data buku belum tersedia")
    else:
        print("====== STATUS BUKU ======")
        print(lihat.iloc[:, [0, 4]].to_string(index=True))
    
        
    
def membuat_id_transaksi():
    while True:
        PMJBK_id = f"PMJBK-{random.randint(100000, 999999)}"

        buat_id = pd.read_csv("Riwayat_Peminjaman.csv")
        if PMJBK_id not in buat_id["id_transaksi"].values:
            return PMJBK_id

def pinjam_buku(username):
    df_buku = pd.read_csv("Data_Buku.csv")

    if df_buku.empty:
        print("Buku belum tersedia")
        return
    
    print(df_buku.to_string(index=True))
    
    pilihan_buku = input("Pilih nomer buku yang ingin dipinjam = ")
    
    if not pilihan_buku.isdigit():
        print("Input harus berupa angka")
        return
    
    index = int(pilihan_buku)
    
    if index < 0 or index >= len(df_buku):
        print("nomer buku tidak valid")
        return
    
    status = df_buku.loc[index, "Status"].lower()
    
    if status != "tersedia":
        print("Buku sedang tidak tersedia atau dipinjam")
        return    
    
    id_transaksi = membuat_id_transaksi()
    tanggal_pinjam = datetime.now()
    tanggal_kembali = tanggal_pinjam + timedelta(days=7)
    judul_buku = df_buku.loc[index, "Judul"]

    with open("Riwayat_Peminjaman.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            id_transaksi,
            username,
            judul_buku,
            tanggal_pinjam.strftime("%Y-%m-%d"),
            tanggal_kembali.strftime("%Y-%m-%d"),
            "dipinjam"
        ])

    df_buku.loc[index, "Status"] = "tidak tersedia"
    df_buku.to_csv("Data_Buku.csv", index=False)

    print("\n=== PEMINJAMAN BERHASIL ===")
    print(f"ID Transaksi : {id_transaksi}")
    print(f"Judul Buku   : {judul_buku}")
    print(f"Jatuh Tempo  : {tanggal_kembali.strftime('%Y-%m-%d')}")

def jadwal_pengembalian(username):
    data_peminjaman = pd.read_csv("Riwayat_Peminjaman.csv")
    
    if data_peminjaman.empty:
        print("Belum ada data peminjaman")
        return
    
    data_peminjam = data_peminjaman[
        (data_peminjaman['nama'] == username) &
        (data_peminjaman['status'] == 'dipinjam' )
    ]
    
    if data_peminjam.empty:
        print("Anda tidak memiliki jadwal pengembalian buku.")
        return
    
    print("=== JADWAL PENGEMBALIAN BUKU ANDA ===") 
    print(data_peminjam[['id_transaksi', 'judul_buku', 'tanggal_kembali']].to_string(index=False)) 
    
def kembali_buku(username):
    data_riwayat = pd.read_csv("Riwayat_Peminjaman.csv")
    
    if data_riwayat.empty:
        print("Belum ada data peminjaman")
        return
    
    data_user = data_riwayat[
        (data_riwayat['nama'] == username) &
        (data_riwayat['status'] == 'dipinjam' )
    ]

    if data_user.empty:
        print("Anda tidak memiliki buku yang dipinjam.")
        return
    
    print("=== DAFTAR BUKU YANG SEDANG ANDA PINJAM ===")
    print(data_user[['id_transaksi', 'judul_buku', 'tanggal_kembali']].to_string(index=False))
    
    id_transaksi = input("Masukkan ID Transaksi buku yang ingin dikembalikan: ").strip()
    if not id_transaksi:
        print("ID Transaksi tidak boleh kosong")
        return
    
    if id_transaksi not in data_user["id_transaksi"].astype(str).values:
        print("ID Transaksi tidak valid atau bukan milik Anda.")
        return
    
    pengembalian = data_riwayat["id_transaksi"].astype(str) == id_transaksi

    judul = data_riwayat.loc[pengembalian, "judul_buku"].values[0]

    data_riwayat.loc[pengembalian, "status"] = "dikembalikan"
    data_riwayat.to_csv("Riwayat_Peminjaman.csv", index=False)

    df_buku = pd.read_csv("Data_Buku.csv")

    buku_pengembalian = df_buku[
        (df_buku["Judul"] == judul) &
        (df_buku["Status"].str.lower() == "tidak tersedia")
    ]

    if buku_pengembalian.empty:
        print("Data buku tidak ditemukan.")
        return

    index_buku = buku_pengembalian.index[0]
    df_buku.loc[index_buku, "Status"] = "tersedia"
    df_buku.to_csv("Data_Buku.csv", index=False)

    print("\n=== PENGEMBALIAN BERHASIL ===")
    print(f"Buku '{judul}' telah berhasil dikembalikan")
    
