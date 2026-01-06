import csv
from datetime import datetime
import pandas as pd

def catat_login(nama, role, status):
    with open("Riwayat_Login.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            nama,
            role,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status
        ])

def menu_admin():
    while True:
        print('==================================')
        print('=========== MAIN MENU ============')
        print('= 1. Lihat data buku             =')
        print('= 2. Tambah data buku            =')
        print('= 3. Ubah data buku              =')
        print('= 4. Status buku                 =')
        print('= 5. Tambah anggota perpustakaan =')
        print('= 6. lihat anggota perpustakaan  =')
        print('= 7. Logout                      =')
        print('==================================')
        try:
            user_admin = int(input("pilih menu = "))
            if user_admin == 1 :
                lihatData()
                (input('klik enter untuk melanjutkan ke main menu = '))
            elif user_admin == 2:
                tambahData()
                (input('klik enter untuk melanjutkan ke main menu = '))
            elif user_admin == 3:
                editData()
                (input('klik enter untuk melanjutkan ke main menu = '))
            elif user_admin == 4:
                print('status buku')
            elif user_admin == 5:
                tambah_anggota("admin")
            elif user_admin == 6:
                lihat_data_anggota("admin")
            elif user_admin == 7:
                print('logout')
                break
            else: 
                print('erorr')
                
        except ValueError:
            print("Input harus berupa angka")
        

def tambahData():
    while True:
        judul = str(input("masukkan judul buku = ")).upper()
        k = pd.read_csv('katalogBuku.csv')
        ds = k.to_dict(orient='dict')
        for i in range(99):
            print(i,ds['no'][i],ds['kategori'][i])
        k = pd.read_csv('katalogBuku.csv')
        ds = k.to_dict(orient='list')
        while True:
            f = int(input('masukkan no notasi buku dan klasifikasinya = '))
            ano = str(ds['no'][f])
            aka = str(ds['kategori'][f])
            if f >= 99:
                print('notasi tidak terdaftar')
            elif f < 0 :
                print('notasi tidak ditemukan')
            else: break
        Rak = str(input("masukkan Rak buku = "))
        status = str(input("masukkan status buku (tersedia/tidak tersedia) = "))
        penerbit = input('penerbit buku = ').upper()
        tterbit = input('tahun terbit = ')
        penulis = input('penulis buku = ')
        instok = int(input("masukkan stok buku = "))
        while True:
            print([judul, f'{ano} - {aka}',penerbit,tterbit,penulis , Rak, status, f"stok ke -  {i+1}"])
            p = str(input('apakah data sudah benar? (y/n)').upper())
            if p == 'Y' :
                for i in range(instok):
                    with open('dataBuku.csv','a',newline='') as file:
                        write = csv.writer(file)
                        n = [f'{judul}     ||', f'{ano} - {aka}     ||',f'{penerbit}     ||',f'{tterbit}     ||',f'{penulis}     ||' , f'{Rak}     ||', f'{status}     ||', f"stok ke -  {i+1}     ||"]
                        write.writerow(n)
                break
            else:
                break
        a = input('apakh ingin menambahkan buku lagi ? (y/n)').upper()
        if a == 'N':
            break

def lihatData():
    df = pd.read_csv('dataBuku.csv')
    print(df)

def editData():
    while True:
        r = pd.read_csv('dataBuku.csv')
        u = input('hapus/edit data? (h/e) = ').lower()
        if u == 'h':
            print(r)
            while True:
                print('klik b jika ingin hapus beberapa')
                j = input('pilih urutan buku yang ingin di hapus = ')
                if j.isdigit():
                    j = int(j)
                    r = r.drop(index=j)
                elif type(j) == str and j == 'b':
                        a = int(input('hapus dari index berapa? '))
                        b = int(input('sampai index ke? '))
                        r = r.drop(index=range(a, b+1))
                else: 
                    print('input tidak diketahui') 
                    break
                print(r)
                k = input('konfirmasi (y/n) = ')
                if k == 'y':
                    r.to_csv("dataBuku.csv", index=False)
                    break
        elif u == 'e':
            print(r)
            index = int(input('masukkan index yang ingin di edit = '))
            print('kelik s jika ingin mengubah semua kategori')
            kolom = str(input('edit salah saatu kolom (y) = ').lower())
            k = pd.read_csv('katalogBuku.csv')
            ds = k.to_dict(orient='dict')
            if kolom == 's':
                print(r)
                judul = str(input("masukkan judul buku yang baru = ").upper())
                for i in range(99):
                    print(i,ds['no'][i],ds['kategori'][i])
                    k = pd.read_csv('katalogBuku.csv')
                    ds = k.to_dict(orient='list')
                while True:
                    f = int(input('masukkan no notasi buku dan klasifikasinya = '))
                    ano = str(ds['no'][f])
                    aka = str(ds['kategori'][f])
                    if f >= 99:
                        print('notasi tidak terdaftar')
                    elif f < 0 :
                        print('notasi tidak ditemukan')
                    else: break
                Rak = str(input("masukkan Rak buku yang baru = "))
                status = str(input("masukkan status buku yang baru (tersedia/tidak tersedia) = "))
                penerbit = input('penerbit buku yang baru = ').upper()
                tterbit = input('tahun terbit yang baru = ')
                penulis = input('penulis buku yang baru = ')
                stok = input('stok buku = ')
                n = [f'{judul}     ||', f'{ano} - {aka}     ||',f'{penerbit}     ||',f'{tterbit}     ||',f'{penulis}     ||' , f'{Rak}     ||', f'{status}     ||', f"stok ke - {stok}    ||"]
                print(n)
                r.loc[index] = n
            elif kolom == 'y':
                col = list(r.columns)
                for i in range(len(col)):
                    op = col[i]
                    gg = ' ketik = '
                    print(op,gg,i)
                m = int(input('masukkan kolom yang ingin di ganti = '))
                pil = col[m]
                r.loc[index, pil] = ind
                if m == 0:
                    jud = input('masukkan judul yang baru').upper()
                    ind = f'{jud}     ||'
                elif m == 1:
                    for i in range(99):
                        print(i,ds['no'][i],ds['kategori'][i])
                    k = pd.read_csv('katalogBuku.csv')
                    ds = k.to_dict(orient='list')
                    while True:
                        f = int(input('masukkan no notasi buku yang baru = '))
                        ano = str(ds['no'][f])
                        aka = str(ds['kategori'][f])
                        if f >= 99:
                            print('notasi tidak terdaftar')
                        elif f < 0 :
                            print('notasi tidak ditemukan')
                        else: break
                    ind = f'{ano} - {aka}     ||'
                elif m == 2:
                    penerbit = input('penerbit buku yang baru = ').upper()
                    ind = f'{penerbit}    ||'
                elif m == 3:
                    tterbit = input('tahun terbit yang baru = ')
                    ind = f'{tterbit}     ||'
                elif m == 4:
                    penulis = input('penulis buku yang baru = ')
                    ind = f'{penulis}     ||'
                elif m == 5:
                    Rak = str(input("masukkan Rak buku yang baru = "))
                    ind = f'{Rak}     ||'
                elif m == 6:
                    status = str(input("masukkan status buku yang baru (tersedia/tidak tersedia) = "))
                    ind = f'{status}     ||'
                else: print('tidak ditemukan')
                print(ind)
            l = input('konfirmasi perubahan? (y/n) ').lower()
            if l == 'y' :
                r.to_csv("dataBuku.csv", index=False)
                break
        else:
            break

def tambah_anggota(role):
    
    if role != "admin":
        print("Hanya admin yang dapat menambahkan anggota perpustakaan.")
        return
    
    print("======MENAMBAHKAN ANGGOTA======")
    
    username = str(input("Masukkan nama lengkap Anggota Baru Perpustakaan: "))
    password = str(input("Masukkan Password dari Anggota baru (Diawali dengan angka 2 dan bejumlah 5 digit): "))
    
    if not (password.isdigit() and len(password) == 5 and password[0] == "2"):
        print("Password tidak valid, harus berjumlah 5 digit dan diawali angka 2")
        return
    
    alamat = str(input("Masukkan Alamat tempat tinggal Anggota baru: "))
    nomer_hp = int(input("Masukkan nomer handphone yang bisa dihubungi: "))
    
    with open("dataAnggotaPerpus.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            username,
            password,
            alamat,
            nomer_hp,
        ])
    
    print(f"Anggota baru sudah ditambahkan, dengan nama {username}")
    
    tambah_lagi = str(input("Apakah ingin menambahkan Anggota Perpustakaan lainnya?(yes/no): " ))
    if tambah_lagi == "yes":
        tambah_anggota()
    else:
        menu_admin()
    return

def lihat_data_anggota(role):
    if role != "admin":
        print("Hanya admin yang dapat menambahkan anggota perpustakaan.")
        return
    
    print("====== DATA ANGGOTA PERPUSTAKAAN ======")
    try:
        data_anggota = pd.read_csv("dataAnggotaPerpus.csv")

        if data_anggota.empty:
            print("Belum ada data anggota.")
            return
    
        print(data_anggota.to_string(index=False))
    except FileNotFoundError:
            print("File data anggota belum tersedia.")


def pinjam_buku(role):
    if role != "Anggota":
        print("Hanya Anggota Perpustakaan yang dapat mengakses")
        return
    
    print("====== PEMINJAMAN BUKU ======")
    
    

