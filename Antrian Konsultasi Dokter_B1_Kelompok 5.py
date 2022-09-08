import json
from mimetypes import init
import os.path
from platform import node
import prettytable
import pwinput
import time
from prettytable import PrettyTable

data_pasien = PrettyTable()
data_pasien.field_names = ["List","nama","umur","keluhan"]
global urut
urut = []
antrian = []
data_login = [{
    "username":  "admin",
    "password": "admin",
    "permission": True
}]
nama = ""
umur = 1
keluhan = ""

def red(skk): 
    print("\033[91m {}\033[00m" .format(skk))
def green(skk): 
    print("\033[92m {}\033[00m" .format(skk))
def yellow(skk): 
    print("\033[93m {}\033[00m" .format(skk))
def lightpurple(skk): 
    print("\033[94m {}\033[00m" .format(skk))
def purple(skk): 
    print("\033[95m {}\033[00m" .format(skk))

def isExist(file):
    return os.path.isfile(file)
    
if isExist('antrian.json'):
    with open("antrian.json", "r") as json_antrian:
        antrian = json.load(json_antrian)
if isExist('data_login.json'):
    with open("data_login.json", "r") as json_login:
        data_login = json.load(json_login)

# FIFO Queue implementation using a linked list 
# as its underlying storage
class LinkedListQueue:
  # ----------------------Nested Node Class ----------------------
    # This Node class stores a piece of data (element) and
    # a reference to the Next node in the Linked List
    class Node:
        def __init__(self, e):
            self.element = e    
            self.next = None   # reference to the next Node
 
# ---------------------- queue methods -------------------------
    # create an empty queue
    def __init__(self):
        self._size = 0
        self.head = None
        self.tail = None
 
    # Add element e to the back of the queue.
    def enqueue(self, e):
        newest = self.Node(e)
 
        if self.is_empty():
            self.head = newest
        else:
            self.tail.next = newest
        self.tail = newest
        self._size += 1
        #print('antrian tambah')
        #self.printenqueue()
 
    # Remove and return the first element from the queue
    # (i.e., FIFO). Raise exception if the queue is empty.
    def dequeue(self):
        if self.is_empty():
           return 'Antrian Kosong'
 
        elementToReturn = self.head.element
        self.head = self.head.next
        self._size -= 1
        if self.is_empty():
            self.tail = None
 
        return elementToReturn
 
    # Return (but do not remove) the element at the front of
    # the queue. Raise exception if the queue is empty.

    def front(self):
        if self.is_empty():
           return 'Kosong'
        return self.head.element
 
    # Return True if the queue is empty.
    def is_empty(self):
        return self._size == 0
 
    # Return the number of elements in the queue.
    def size(self):
        return self._size
        
    def printenqueue(self):
        print("Antrian saat ini :") 
        temp=self.head 
        while temp is not None: 
            print(temp.element,end="->") 
            temp=temp.next

    def resetqueue(self):
        self.head = self.tail= None;
        print('antrian clear')
    
 
 
q = LinkedListQueue()

def shellSortasc(array, n):
    tengah = n // 2
    while tengah > 0:
        for i in range(tengah, n):
            temp = array[i]
            j = i
            while j >= tengah and array[j - tengah] > temp:
                array[j] = array[j - tengah]
                j -= tengah
            array[j] = temp
        tengah //= 2

def shellSortdesc(array, n):
    tengah = n // 2
    while tengah > 0:
        for i in range(tengah, n):
            temp = array[i]
            j = i
            while j >= tengah and array[j - tengah] < temp:
                array[j] = array[j - tengah]
                j -= tengah
            array[j] = temp
        tengah //= 2

def perbarui_tabel(antrian):
    with open('antrian.json', 'w') as file:
        json.dump(antrian, file, indent=4)

    antri = antrian
    data_pasien.clear_rows()
    for i in range(len(antrian)):
        data_pasien.add_row([i + 1, antri[i].get('nama'),
                           antri[i].get('umur'),antri[i].get('keluhan')])

def masukdata():
    red("Silahkan masukkan data diri dan keluhan anda terlebih dahulu")
    try:
        while True:
                nama = input("nama : ")
                nama.isalpha()
                if nama.isalpha() == False:
                    print("nama harus berisi huruf dan tidak boleh kosong")
                    return masukdata()
                #else:
                #    q.enqueue(nama)

                umur = int(input("umur : "))
                if umur < 1:
                    print("umur tidak boleh kosong atau kurang dari 1")
                    return masukdata()
    
                keluhan = input("keluhan :")
                keluhan.isalpha()
                if keluhan.isalpha() == False:
                    print("keluhan harus berisi huruf dan tidak boleh kosong")
                    return masukdata()

                for pasien in antrian:
                    if pasien.get('nama') == nama:
                        print("nama sudah ada")
                        return masukdata() 

                data = {
                    "nama": nama, 
                    "umur": umur,
                    "keluhan": keluhan
                }
                print(data.get('nama'))
                q.enqueue(data.get('nama'))
                print(q.printenqueue())
                antrian.append(data)
                with open("antrian.json", "w") as json_antrian:
                    json.dump(antrian, json_antrian, indent=4)
                    print("mohon tunggu sebentar...")
                    time.sleep(1)
                    print("antrian berhasil ditambahkan")
                perbarui_tabel(antrian)
                break
    except ValueError:
        print("inputan salah mohon periksa kembali inputan anda")
        masukdata()
            
        #data = {
        #    "nama": nama,
        #    "umur": umur,
        #    "keluhan": keluhan
        #}
        #antrian.append(data)
        #for i in range(len(antrian)):
        #    if nama == antrian[i]:
        #        q.enqueue(antrian[i])
        #    else:
        #        i = antrian[i].get('nama')
        #        q.enqueue(i)
        #with open("antrian.json", "w") as json_antrian:
        #    json.dump(antrian, json_antrian)
        #print("data berhasil dimasukan")
        #perbarui_tabel(antrian)


#def perbarui_tabel(antrian):
#    with open('antrian.json', 'w') as file:
#        json.dump(antrian, file, indent=4)
#
#    antri = antrian
#    data_pasien.clear_rows()
#    for i in range(len(antrian)):
#        data_pasien.add_row([i + 1, antri[i].get('nama'),
#                           antri[i].get('umur'),antri[i].get('keluhan')])

#def binarySearch(arr, l, r, x):
#    while l <= r:
#        mid = l + (r - l) // 2
#        if arr[mid] == x:
#            return mid
#        elif arr[mid] < x:
#            l = mid + 1
#        else:
#            r = mid - 1
#    return -1
#
#def binary_search(arr, x):
#    low = 0
#    high = len(arr) - 1
#    mid = 0
# 
#    while low <= high:
# 
#        mid = (high + low) // 2
# 
#        # If x is greater, ignore left half
#        if arr[mid] < x:
#            low = mid + 1
# 
#        # If x is smaller, ignore right half
#        elif arr[mid] > x:
#            high = mid - 1
# 
#        # means x is present at mid
#        else:
#            return mid
# 
#    # If we reach here, then the element was not present
#    return -1

def binarySearch(arr, l, r, x):
 
    while l <= r:
 
        mid = l + (r - l) // 2
 
        # Check if x is present at mid
        if arr[mid] == x:
            return mid
 
        # If x is greater, ignore left half
        elif arr[mid] < x:
            l = mid + 1
 
        # If x is smaller, ignore right half
        else:
            r = mid - 1
 
    # If we reach here, then the element
    # was not present
    return -1

def menu(user):
    if user == 'admin':
            red('>>>>>>>>>>> Menu <<<<<<<<<<<<')  
                    
            lightpurple('-> 1. Lihat database')
            lightpurple('-> 2. Searching database ')
            lightpurple('-> 3. Input antrian ')
            lightpurple('-> 4. Lihat antrian ')
            lightpurple('-> 5. Hapus antrian ')
            lightpurple('-> 6. Reset antrian')
            lightpurple('-> 7. Hapus database ')
            lightpurple('-> 8. Exit')

    elif user == 'user':
        red('>>>>>>>>>> Menu <<<<<<<<')
        yellow('-> 1. Ambil antrian')
        yellow('-> 2. Lihat antrian ')
        yellow('-> 3. Exit ')
    return input("Ada yang bisa dibantu? : ")
    
    
def lihatdata():
    print("lihat database pasien")
    for i in range(len(antrian)):
        if antrian[i].get('nama'): 
            urut.append(antrian[i].get('nama'))
    print('1. Tanpa sorting')
    print('2. Ascending')
    print('3. Descending')
    print('4. Kembali')
    #print(urut)
    pilih = int(input('Pilih : '))
    if pilih == 1:
        print("mohon tunggu sebentar...")
        os.system('cls')
        time.sleep(1)
        perbarui_tabel(antrian)
        os.system('cls')
        green("Berikut database pasien Klinik 7B")
        
        print(data_pasien) 
    elif pilih == 2:
        print("mohon tunggu sebentar...")
        os.system('cls')
        time.sleep(1)
        urut.clear()
        for i in range(len(antrian)):
            if antrian[i].get('nama'): 
                urut.append(antrian[i].get('nama'))
        size = len(urut)
        shellSortasc(urut, size)
        os.system('cls')
        green("Berikut database pasien Klinik 7B secara Ascending")
        print(urut)
    elif pilih == 3:
        print("mohon tunggu sebentar...")
        os.system('cls')
        time.sleep(1)
        urut.clear()
        for i in range(len(antrian)):
            if antrian[i].get('nama'): 
                urut.append(antrian[i].get('nama'))
        size = len(urut)
        shellSortdesc(urut,size)
        os.system('cls')
        green("Berikut database pasien Klinik 7B secara Descending")
        print(urut)
    #elif pilih == 4:
    #   menu('admin')
    else:
        print('====== keluar ======')

def hapusdata():
    print("hapus data")
    q.dequeue()
    with open("antrian.json", "w") as json_antrian:
        json.dump(antrian, json_antrian)
    print("antrian berhasil dihapus")

def lihatantrian():
    #for i in range(len(antrian)):
    #        #if nama = antrian[i].get('nama'):
    #        #    q.enqueue(nama, i+1)
    #        name = antrian[i].get('nama')
    #        q.enqueue(name)
    #print(antrian)
    if q.is_empty():
        print('Antrian kosong')
    else:
        green("Berikut antrian yang sedang berjalan:")
        print(q.printenqueue())

def sizeantrian():
    print("size antrian")
    print(q.size())

def antriandepan():
    print("Antrian Saat ini sedang diproses", q.front())

def hapusisijson():
    print("hapus data")
    antrian.clear()
    with open("antrian.json", "w") as json_antrian:
        json.dump(antrian, json_antrian)
    print("data berhasil dihapus")

def login(name, password):
    time.sleep(1)
    os.system('cls')
    global loginAs
    for akun in data_login:
        if name == akun.get('username') and password == akun.get('password'):
            print("loading.")
            time.sleep(0.5)
            os.system('cls')
            print("loading..")
            time.sleep(0.5)
            os.system('cls')
            print("loading...")
            time.sleep(0.5)
            os.system('cls')
            yellow('Login berhasil, Silahkan lihat menu'.center(32))

            loginAs = akun
            return True

    print("Username atau Password yang Anda Input Salah, Silahkan login Ulang")
    return begin()

def register(username, password):
    for akun in data_login:
        if username == akun.get("username"):
            print('Akun Sudah ada ')
            return begin()
    data_login.append({
        "username": username,
        "password": password,
        "permission": False
    })

    with open('data_login.json', 'w') as file:
        json.dump(data_login, file, indent=3)

def akses(option):
    if(option == "login"):
        username = input("Username : ")
        password = pwinput.pwinput("Password : ")
        isLogin = login(username, password)
        if isLogin == True:
            return isLogin
        else:
            return akses('login')
    else:
        print("Input Username dan Password akun baru anda")
        username = input("Masukkan Username : ")
        username.isalpha()
        if username == "":
            print("Username tidak boleh kosong")
            return akses('register')
        if username.isalpha()==False:
            print("Username hanya boleh huruf")
            return akses('register')
        else:
            password = pwinput.pwinput("Masukkan Password : ")
            if password == "":
                print("Password tidak boleh kosong")
                return akses('register')
            else:
                register(username, password)
                print("Akun anda berhasil dibuat")
                return akses('login')
        #password = pwinput.pwinput("Masukkan password anda: ")
        #register(username, password)
        #print("Register anda berhasil, Silahkan Masuk")
        #return False

def begin():
    purple("""
+==========================================+
|            SELAMAT DATANG                |
+==========================================+
|     Silahkan input 'login' untuk login   |
|    Silahkan input 'reg' untuk registrasi |
+==========================================+
          """)
    option = input("Silahkan Input Pilihan [login/reg]: ")
    if(option != "login" and option != "reg"):
        return begin()

    if akses(option):
        main()
    else:
        return begin()

def cekPermission(akun):
    if akun.get('permission') == True:
        return True
    else:
        return False

def main():
    isAdmin = cekPermission(loginAs)
    while True:
        if isAdmin == True:
            pilihan = menu('admin')
            if pilihan == "1":
                lihatdata()
            elif pilihan == '2': #ini masih ada bug nya, dah kelar bug nya
                nyari = []
                for i in range(len(antrian)):
                    nama = antrian[i].get('nama')
                    nyari.append(nama)
               #         urut.append(antrian[i].get('nama'))
                #print(nyari)
                print(len(nyari))
                size = len(nyari)
                shellSortasc(nyari, size)
                print(nyari)
                cari = input('Masukan Nama : ')
                print("mohon tunggu sebentar...")
                time.sleep(1)
                result = binarySearch(nyari, 0, len(nyari)-1, cari)
                if result != -1:
                    print(cari, 'berada diurutan ke-', result+1)
                else:
                    print(cari, 'tidak ditemukan')
                print('') 
               
            elif pilihan == '4':
                print("mohon tunggu sebentar...")
                time.sleep(1)
                #lihatantrian()
                q.printenqueue()
                
            elif pilihan == '5':
                print("mohon tunggu sebentar...")
                time.sleep(1)
                hapusdata()
                
            elif pilihan == '6':
                print("mohon tunggu sebentar...")
                time.sleep(1)
                q.resetqueue()
                green("antrian berhasil dikosongkan")
                
            elif pilihan == '7':
                print("mohon tunggu sebentar...")
                hapusisijson()        
                q.resetqueue()
            
            elif pilihan == '8':
                break
            
            elif pilihan == '3':
                masukdata()
                #q.dequeue()
            else:
                print("salah input")
                
        else:
            pilihan = menu('user')
            antriandepan()
            if pilihan == "1":
                print("mohon tunggu sebentar...")
                time.sleep(1)
                masukdata()
            elif pilihan == '2':
                print("mohon tunggu sebentar...")
                time.sleep(1)
                q.printenqueue()
                #lihatantrian()
            elif pilihan == '3':
                break
            else:
                print("[Salah Input]")
        print()
    green("[-------------------- Terimakasih & Semoga Cepat Pulih :) -------------------------]")
    return begin()
begin()
