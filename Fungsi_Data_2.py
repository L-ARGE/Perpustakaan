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
                    input("\nTekan ENTER untuk kembali ke menu...")
                    
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
                    print('Anda telah keluar dari sistem perpustakaan')
                    break
            
                else:
                    print('Menu tidak tersedia')
            except ValueError:
                print("Input harus berupa angka")
                
def lihat_daftar_buku():
    daftar = pd.read_csv("Data_Buku.csv")

    if daftar.empty:
        print("Data buku belum tersedia")
        return

    daftar["Status"] = daftar["Status"].str.strip().str.lower()

    katalog = (
        daftar
        .groupby(["Judul", "Kategori", "Rak_Buku"])
        .agg(
            Total_Stok=("stok", "count"),
            Tersedia=("Status", lambda x: (x == "tersedia").sum())
        )
        .reset_index()
    )

    print("\n====== DAFTAR KATALOG BUKU ======")
    print(katalog.to_string(index=False))

        
def lihat_status_buku():
    lihat = pd.read_csv("Data_Buku.csv")
    
    if "Status" not in lihat.columns:
        print("Data buku belum tersedia")
        return
    elif lihat.empty:
        print("Data buku belum tersedia")
    else:
        print("====== STATUS BUKU ======")
        print(lihat.iloc[:, [0, 4]].to_string(index=True))
    
def cari_buku():
    while True:
        print('=== CARI BUKU ===')
        keyword = input("Masukkan judul buku: ").lower()
        ditemukan = False

        with open("Data_Buku.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if keyword in row['Judul'].lower():
                    print("Rak_Buku     :", row['Rak_Buku'])
                    print("Judul        :", row['Judul'])
                    print("Status       :", row['Status'])
                    print("-" * 25)
                    ditemukan = True

        if not ditemukan:
            print("Buku tidak ditemukan")    
        lanjut = input("Ingin mencari buku lain? (y/n): ").strip().lower()
        if lanjut != 'y':
            break
    
def membuat_id_transaksi():
    while True:
        PMJBK_id = f"PMJBK-{random.randint(100000, 999999)}"
 
        buat_id = pd.read_csv("Riwayat_Peminjaman.csv")
        if PMJBK_id not in buat_id["id_transaksi"].values:
            return PMJBK_id

def pinjam_buku(username):
    while True:
        lihat_daftar_buku()
        
        nama_buku = input("Masukkan judul buku yang ingin dipinjam: ").strip().upper()

        df = pd.read_csv("Data_Buku.csv")
        df["Status"] = df["Status"].str.strip().str.lower()
        df["Judul"] = df["Judul"].str.upper()
        
        buku_tersedia = df[
           (df["Judul"] == nama_buku) &
           (df["Status"] == "tersedia")
        ]
        
        if  buku_tersedia.empty:
            print(f"Buku '{nama_buku}' tidak tersedia atau tidak ditemukan")
            if input("Ingin mencari buku lain? (y/n): ").strip().lower() != 'y':
                break
            continue
        
        posisi_asli = buku_tersedia.index[0]
        judul_buku = df.loc[posisi_asli, "Judul"]
        
        id_transaksi = membuat_id_transaksi()
        tanggal_pinjam = datetime.now()
        tanggal_kembali = tanggal_pinjam + timedelta(days=7)

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

        df.loc[posisi_asli, "Status"] = "tidak tersedia"
        df.to_csv("Data_Buku.csv", index=False)

        print("\n=== PEMINJAMAN BERHASIL ===")
        print(f"ID Transaksi : {id_transaksi}")
        print(f"Judul Buku   : {judul_buku}")
        print(f"Jatuh Tempo  : {tanggal_kembali.strftime('%Y-%m-%d')}")
        lanjut = input("Ingin meminjam buku lagi? (y/n): ").strip().lower()
        if lanjut != 'y':
            break

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
    while True:
        
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
            else:
                index_buku = buku_pengembalian.index[0]
                df_buku.loc[index_buku, "Status"] = "tersedia"
                df_buku.to_csv("Data_Buku.csv", index=False)

            print("\n=== PENGEMBALIAN BERHASIL ===")
            print(f"Buku '{judul}' telah berhasil dikembalikan")
            lanjut = input("Ingin mengembalikan buku lain? (y/n): ").strip().lower()
            if lanjut != 'y':
                break
