"""Fitur
-buat unit test dengan ctrl+w isi data dari file unit-test-'namaframe'.txt untuk automate data bind dengan frame untuk insert

"""
#import Tkinter as tk
from Tkinter import *
from PIL import ImageTk, Image
import tkMessageBox
import tkFileDialog
import psycopg2
import sys
import shutil
import os
import time
import datetime
import bz2
import base64
global companyName, copyapp, appname, coder, iconcopy, useicon, graphicAbout, picprofile
global verapp
global fpathname, path
global serverfile
global addstr
global ipget, top, kstr, destinationprofile


appname = 'Sinjar'
companyName = "Fakultas Hukum Universitas Warmadewa"
verapp = 'Alpha 0.10'
copyapp = 'Copyright 2013'
coder = 'wkusnadhi@gmail.com'
iconcopy = 'Icon by (iconspedia.com)'
useicon = 'logo.ico'
graphicAbout = "logo.png"
picprofile = "photos/profile-photo.jpg"
path = 'logo-unwar-yellow.png'
serverfile = 'server.txt'
addstr='QlpoOTFBWSZTW'
kstr='KMXckU4'
destinationprofile = "photos/"


#---------------------------BIODATA-----------------------------------------
def finputbio():
    from PIL import ImageTk, Image
    root.withdraw()
    # create child window
    global curF, bio, bolisdos
    global Toplevel
    curF = "bio"
    bio = Toplevel()
    w, h = bio.winfo_screenwidth(), bio.winfo_screenheight()
    # use the next line if you also want to get rid of the titlebar
    #bio.overrideredirect(1)
    bio.geometry("%dx%d+0+0" % (w, h))
    #bio.minsize(300,300)
    #bio.geometry("880x600")
    bio.wm_iconbitmap(useicon)
    bio.title ('%s - Input Biodata' % appname)
    afields  = ['Nama', 'Tempat/Tgl. Lahir', 'Alamat', 'NIP NIK']
    bfields  = ['Dosen/Pegawai',]
    cfields  = ['SNIDN', 'NOSERDOS', 'Telpon', 'HP', 'Nomer bisa dihubungi','Email']
    

    def utbio():
        size=11
        f = open('unittestbio.txt','r')
        fl = []
        for i in f:
            if not (i.strip('\n')==''):
                fl.append(i.strip('\n'))
        fm=[fl[i:i+size] for i  in range(0, len(fl), size)]
        kl=fm[1] #number in text
        f.close()
        for ent_item in entjentry:
            ent_item.delete(0,END)
        e_list[0].insert(0,kl[0])
        e_list[1].insert(0,kl[1])
        e_list[2].insert(0,kl[2])
        e_list[3].insert(0,kl[3])
        varCombo.set(kl[4])
        e_list[5].insert(0,kl[5])
        e_list[6].insert(0,kl[6])
        e_list[7].insert(0,kl[7])
        e_list[8].insert(0,kl[8])
        e_list[9].insert(0,kl[9])
        e_list[10].insert(0,kl[10])

        
        
    def validatebio():
        ik = -1
        #print e_list
        valK = [(labList[0], e_list[0].get()), (labList[1], e_list[1].get()),
                (labList[2], e_list[2].get()), (labList[3], e_list[3].get()), 
                (labList[4], varCombo.get()), (labList[5], e_list[5].get()),
                (labList[6], e_list[6].get()), (labList[7], e_list[7].get()),
                (labList[8], e_list[8].get()), (labList[9], e_list[9].get()),
                 (labList[10], e_list[10].get())]                
        for itemList in valK :
            field = itemList[0]
            text = itemList[1]
            #print ('%s: --%s--' % (field, text))
        warning = ()    
        for itemvalK in valK :            
            if len(str(itemvalK[1])) == 0:
                #print ('--%s-- has value %s' % (itemvalK[0], itemvalK[1]))
                tkMessageBox.showinfo("Peringatan", "Tolong %s diisi dengan lengkap!" % itemvalK[0])
                warning = warning + (itemvalK[0],)
        #print warning
        #print len(warning)
        if len(warning) == 0:
            insbio()

    def checkNama():
        name = enttuples[0].get()
        #print enttuples
        print name
        #for name in (e0.get()): 
        cursor.execute("SELECT count(*) FROM biodata WHERE namabio = %s", (name,))
        data=cursor.fetchone()[0]
        if data==0:
            print('Tidak ada nama %s'%name)
            #insemp()
            validatebio()
        else:
            tkMessageBox.showinfo("Peringatan", "Sudah ada biodata dengan nama %s!"%name)


    def delNama():
        print myid
        name = e_list[0].get()
        cursor.execute("SELECT count(*) FROM biodata WHERE namabio=%s", (name,))
        data=cursor.fetchone()[0]
        if len(name)==0:
            tkMessageBox.showinfo("Peringatan", "Seleksi dulu nama biodata dari list!")
        else:
            if data==0:
                tkMessageBox.showinfo("Peringatan", "Tidak ada biodata bernama %s!" % (name))
            else:
                print('Data %s akan dihapus, Lanjut?'%(name))
                if tkMessageBox.askokcancel("Peringatan", "Data %s akan dihapus, Lanjut?" %(name)):
                    cursor.execute("DELETE FROM biodata WHERE idbio='%s'" % myid)
                    cursor.execute("COMMIT")
                    evClear()
                    refreshMlb()
                    btnU['state'] = DISABLED
                    btnD['state'] = DISABLED
                    tkMessageBox.showinfo("Konfirmasi", "Data %s sukses dihapus." % (name))
        return
    
    def Updbio():
        nama_update = e_list[0].get()

        if len (e_list[0].get())==0:
            tkMessageBox.showinfo("Peringatan", "Nama biodata mesti diisi!")
        else:
            if (varCombo.get()=='Dosen'):
                bolisdos = 't'
            else:
                bolisdos = 'f'
            biodict = {"namabio":e_list[0].get(),
                    "ttl":e_list[1].get(),
                    "alamat":e_list[2].get(),
                    "nipnik":e_list[3].get(),
                    "isdos":bolisdos,
                    "snidn":e_list[5].get(),
                    "noserdos":e_list[6].get(),
                    "notelp":e_list[7].get(),
                    "hp":e_list[8].get(),
                    "nohub":e_list[9].get(),
                    "email":e_list[10].get(),
                    "ubio":psycopg2.TimestampFromTicks(time.time()),
                    "idbio":myid}
            cursor.execute('UPDATE biodata SET \
                    namabio=%(namabio)s,\
                    ttl=%(ttl)s,\
                    alamat=%(alamat)s,\
                    nipnik=%(nipnik)s,\
                    isdos=%(isdos)s,\
                    snidn=%(snidn)s,\
                    noserdos=%(noserdos)s,\
                    notelp=%(notelp)s,\
                    hp=%(hp)s,\
                    nohub=%(nohub)s,\
                    email=%(email)s,\
                    ubio=%(ubio)s \
                    WHERE idbio =%(idbio)s', biodict)
            cursor.execute("COMMIT") 
            print "Sukses Update"
            evClear()
            refreshMlb()
            btnU['state'] = DISABLED
            tkMessageBox.showinfo("Sukses", "Biodata %s sukses diupdate!" % (nama_update))



    def insbio():
        print entjentry
        print "+++++++++++++++++++++++"
        if (varCombo.get()=='Dosen'):
            bolisdos = 't'
        else:
            bolisdos = 'f'
        #metadata = {"Name": "Guest", "Details": "['One', 'Two', 'Three']"}
        namebio = e_list[0].get()
        biodict = {"namabio":e_list[0].get(),
                    "ttl":e_list[1].get(),
                    "alamat":e_list[2].get(),
                    "nipnik":e_list[3].get(),
                    "isdos":bolisdos,
                    "snidn":e_list[5].get(),
                    "noserdos":e_list[6].get(),
                    "notelp":e_list[7].get(),
                    "hp":e_list[8].get(),
                    "nohub":e_list[9].get(),
                    "email":e_list[10].get()}
        cursor.execute("INSERT INTO biodata (namabio,ttl,alamat,nipnik,isdos,snidn,noserdos,\
                notelp,hp,nohub,email) VALUES (%(namabio)s,%(ttl)s,%(alamat)s,%(nipnik)s,%(isdos)s,\
                %(snidn)s,%(noserdos)s,%(notelp)s,\
                %(hp)s,\
                %(nohub)s,\
                %(email)s)\
                ", biodict)
        #cursor.execute("insert into biodata values %s", biodict)
        cursor.execute("COMMIT")   
        cursor.execute("SELECT * FROM biodata")
        for bioku in cursor.fetchall():
            print "ID %d NAME %s %s" % (bioku[0], bioku[1], bioku[5])
        evClear()
        refreshMlb()
        btnU['state'] = DISABLED
        tkMessageBox.showinfo("Sukses", "Biodata %s sukses tersimpan!" % namebio)

    def evClear():
        global ent_item
        for ent_item in entjentry: #enttuples
            ent_item.delete(0,END)
        varCombo.set("Dosen")
        btnU['state'] = DISABLED
        btnD['state'] = DISABLED
        print 'Clear'

    def print_it(event):
        print varCombo.get()


    def print_it_agama(event):
        print varComboAgama.get()

    def print_it_norek(event):
        print varComboNorek.get()

    def loadMlb():
        global mlb, LForm
        LForm = LabelFrame(pbio, text="List Biodata", padx=10, pady=5, bg = "green", height = 30)
        LForm.pack(side=RIGHT, expand = 0, pady = 2, padx = 10)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM biodata")
        dataKar=cursor.fetchall()
                   
        mlb = MultiListbox(LForm, (('ID', 10), ('Nama', 40), ('Dosen/Pegawai', 20)))
        for i in dataKar:
            if (i[5]==True):
                isdosen='Dosen'
            else:
                isdosen='Pegawai'
            mlb.insert(END, ('%d' % int(i[0]), '%s' % str(i[1].strip()), '%s' % isdosen))

        mlb.pack(side=TOP)

    def refreshMlb():
        global mlb
        mlb.delete(0, END)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM biodata")
        dataKar=cursor.fetchall()
        for i in dataKar:
            if (i[5]==True):
                isdosen='Dosen'
            else:
                isdosen='Pegawai'
            mlb.insert(END, ('%d' % int(i[0]),
                             '%s' % str(i[1].strip()), '%s' %  isdosen))

    def cfile():
        #root.withdraw()
        global photoimg
        filename = tkFileDialog.askopenfilename(title="Open Image Biodata", filetypes=[("image file",".jpg"),])
        if os.path.isfile(filename):
            if filename.endswith(".jpg"):
                shutil.copy(filename,destinationprofile)
                #photoimg.configure(file='photos/sample-profile.jpg')
                
                #im = Image.open("photos/"+os.path.basename(filename))
                Logo_IMG = Image.open("photos/"+os.path.basename(filename))
                photoimg = ImageTk.PhotoImage(Logo_IMG)
                Canv_logo.itemconfigure(item, image=photoimg)
            print filename
        else:
            print 'No file chosen'
        #raw_input('\nReady, push Enter')
        entfoto.delete(0, END)
        entfoto.insert(0, str(filename))
        print filename
        print "OK!"
        
    
    def makeformKaryawan(root, fields):
        global btnN, btnS, btnD, btnR, btnQ, entries, enttuples, labList, e_list, entjentry
        global entfoto, vfoto, photoimg
        labList = ['Nama', 'Tempat/Tgl. Lahir', 'Alamat', 'NIP NIK',
                   'Dosen/Pegawai', 'SNIDN', 'NOSERDOS', 'Telpon',
                   'HP', 'Nomer bisa dihubungi', 'Email']
        entries = []
        enttuples = [] 
        entjentry = []
        
        for afield in afields:
            row = Frame(aForm)
            lab = Label(row, width=20, text=afield, anchor='w')
            ent = Entry(row)
            enttuples.append((ent))
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            entries.append((afield, ent))
            entjentry.append((ent)) #for entry only

        for bfield in bfields:
            row = Frame(aForm)
            lab = Label(row, width=20, text=bfield, anchor='w')
            ent = OptionMenu(row, varCombo, "Dosen","Pegawai", command=print_it)
            enttuples.append((ent))
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            entries.append((bfield, ent))
        
        for cfield in cfields:
            row = Frame(aForm)
            lab = Label(row, width=20, text=cfield, anchor='w')
            ent = Entry(row)
            enttuples.append((ent))
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            entries.append((cfield, ent))
            entjentry.append((ent)) #for entry only

        e_list = list(enttuples)
        fotobio=LabelFrame(aForm, padx=5, pady=2)
        fotobio.pack(padx=5, pady=2)
        

        mfoto = "Pilih gambar format .jpg untuk biodata (225 x 300 pixel)."
        Label(fotobio, text=mfoto).pack()
        btncfoto = Button(fotobio, text='Choose File', anchor='n', command=cfile)
        btncfoto.pack(side=LEFT, padx=5)
        vfoto= StringVar()
        vfoto=''
        entfoto = Entry(fotobio, font=("Arial", "9"))
        entfoto.pack(side=RIGHT, expand=YES, fill=X)
        kbio=LabelFrame(aForm, padx=5, pady=2)
        kbio.pack(padx=5, pady=2)
        kbioa=LabelFrame(kbio, padx=5, pady=2,relief=FLAT)
        kbioa.pack(side=LEFT, padx=5, pady=2)
        kbiob=LabelFrame(kbio, padx=5, pady=2,relief=FLAT)
        kbiob.pack(side=RIGHT, padx=5, pady=2)
        Label(kbio, width=20, text='Kegiatan', anchor='n').pack(side=TOP)
        alla = AutoScrollListBox_demo(kbioa)
        allb = AutoScrollListBox_demo(kbiob)
        a = Button(kbioa, text="Tambah Kegiatan", command=allb.onAdd)
        a.pack()
        b = Button(kbiob, text="Kurangi Kegiatan", command=alla.onAdd)
        b.pack()

        #with unit test
        #utbio()
        return entries

        
        # display message
    

    # quit child window and return to root window
    # the button is optional here, simply use the corner x of the child window
    global varCombo, btnU, btnD
    varCombo = StringVar()
    varCombo.set("Dosen")
    Label(bio, text="").pack()
    pbio=LabelFrame(bio, padx=5, pady=2,relief=FLAT)
    pbio.pack(padx=5, pady=2)

    aForm = LabelFrame(pbio, text="Form Biodata", padx=5, pady=2)
    #aForm.pack(expand = 1, pady = 10, padx = 10)
    aForm.pack(side=LEFT, expand = TRUE, pady = 2, padx = 5)
    ents = makeformKaryawan(aForm, afields)
    
    Label(aForm, text="").pack()
    #data listbox
    bForm = LabelFrame(aForm, text="Action", padx=5, pady=2, bg = "orange", height = 250)
    bForm.pack(side=BOTTOM, expand = 1, pady = 2, padx = 5)
    
    btnN = Button(bForm, text='Add New', command=evClear)
    btnS = Button(bForm, text='Save', command=checkNama)
    btnU = Button(bForm, text='Update', command=Updbio)
    btnD = Button(bForm, text='Delete', command=delNama)
    btnR = Button(bForm, text='Reset', command=evClear)
    btnQ = Button(bForm, text='Quit', command=activaterootfrombio)
    btnN.pack(side=LEFT, padx=5)
    btnS.pack(side=LEFT, padx=5)
    btnU.pack(side=LEFT, padx=5)
    btnD.pack(side=LEFT, padx=5)
    btnR.pack(side=LEFT, padx=5)
    btnQ.pack(side=LEFT, padx=5)

    btnU['state'] = DISABLED
    btnD['state'] = DISABLED
    profilebio=LabelFrame(pbio, text="Foto Profile", padx=5, pady=2)
    profilebio.pack(side=TOP, padx=5, pady=2)

    im = Image.open(picprofile)
    canvas = Canvas(root, height=im.size[1]+20, width=im.size[0]+20)
    canvas.pack(side=LEFT,fill=BOTH,expand=1)

    photo = ImageTk.PhotoImage(im)
    item = canvas.create_image(10,10,anchor=NW, image=photo)


    Logo_IMG = Image.open(picprofile)
    #here you use Photoimage to assign the image to ImageTk
    photoimg = ImageTk.PhotoImage(Logo_IMG)
    Canv_logo = Canvas(profilebio, width=240, height=320,  bd=0)
    #Canv_logo = Canvas(profilebio, height=Logo_IMG.size[1]+20, width=Logo_IMG.size[0]+20,  bd=0)
    #here you show the image in the canvas
    item=Canv_logo.create_image(120, 160, image=photoimg)
    Canv_logo.pack()
    #here you reference at the image again -without this you won't see the image-
    Canv_logo.image = photoimg



    
    loadMlb()
    #Label(bio, text='').pack(side=TOP)
    
#---------------------------ABOUT-------------------------------------------
def about():
    def closeAbo():
        # check if saving
        # if not:
        abo.destroy()
    def callquit(event):
        abo.destroy()

    from PIL import ImageTk, Image
    global curF, abo
    curF = "abo"
    abo = Toplevel()
    abo.minsize(150,150)
    abo.geometry("250x250")
    abo.title ('About %s' % appname)
    abo.protocol('WM_DELETE_WINDOW', closeAbo)
    abo.attributes("-toolwindow", 1)
    abo.resizable(0,0)
    abo.bind("<Button-1>", callquit)
    Logo_IMG = Image.open(graphicAbout)
    #here you use Photoimage to assign the image to ImageTk
    photoimg = ImageTk.PhotoImage(Logo_IMG)
    Canv_logo = Canvas(abo, width=200, height=250,  bd=0)
    #here you show the image in the canvas
    Canv_logo.create_image(105, 60, image=photoimg)
    Label(abo, text='').pack()
    canvas_id = Canv_logo.create_text(10, 120, anchor="nw")
    Canv_logo.itemconfig(canvas_id, text="%s v. %s" % (appname, verapp,))
    Canv_logo.insert(Canv_logo, 15, "new ")

    canvas_id_copy = Canv_logo.create_text(10, 140, anchor="nw")
    Canv_logo.itemconfig(canvas_id_copy, text=copyapp)
    Canv_logo.insert(Canv_logo, 15, "new ")

    canvas_id_des = Canv_logo.create_text(10, 160, anchor="nw")
    Canv_logo.itemconfig(canvas_id_des, text="%s is designed by \n%s" % (appname, coder,))
    Canv_logo.insert(Canv_logo, 15, "new ")

    canvas_id_icon = Canv_logo.create_text(10, 200, anchor="nw")
    Canv_logo.itemconfig(canvas_id_icon, text=iconcopy)
    Canv_logo.insert(Canv_logo, 15, "new ")
  
    Canv_logo.pack()
    #here you reference at the image again -without this you won't see the image-
    Canv_logo.image = photoimg

#----------------------FUNCTION-------------------------------------------
    
class AutoScrollListBox_demo:
    def __init__(self, master):
        frame = Frame(master, width=500, height=400, bd=1)
        frame.pack()

        self.listbox_log = Listbox(frame, height=4)
        self.scrollbar_log = Scrollbar(frame) 

        self.scrollbar_log.pack(side=RIGHT, fill=Y)
        self.listbox_log.pack(side=LEFT,fill=Y) 

        self.listbox_log.configure(yscrollcommand = self.scrollbar_log.set)
        self.scrollbar_log.configure(command = self.listbox_log.yview)

        #Just to show unique items in the list
        self.item_num = 0

    def onAdd(self):
        self.listbox_log.insert(END, "test %s" %(str(self.item_num)))       #Insert a new item at the end of the list

        self.listbox_log.select_clear(self.listbox_log.size() - 2)   #Clear the current selected item     
        self.listbox_log.select_set(END)                             #Select the new item
        self.listbox_log.yview(END)                                  #Set the scrollbar to the end of the listbox

        self.item_num += 1
        
def notdone():  
    showerror('Not implemented', 'Not yet available')

def finputkegiatan():  
    showerror('Not implemented', 'Not yet available')

def fadmin():  
    showerror('Not implemented', 'Not yet available')



def makemenufront():
    
    global front
    front = Toplevel()
    front.minsize(150,150)
    front.geometry("250x250")
    front.title ('front')
    front.resizable(0,0)
    #front.attributes('-fullscreen', True)
    img = ImageTk.PhotoImage(Image.open(path))
    panel = Label(front, image = img)
    panel.pack(side = "bottom", fill = "both", expand = "yes")



class MyDialog:
    def __init__(self, parent):
        
        top = self.top = Toplevel(parent)
        top.geometry('200x90')
        top.title ('Input IP Server')
        Label(top, text="Masukkan IP V4 Server").pack()
        self.e = Entry(top)
        self.e.pack(padx=5)
        b = Button(top, text="Save", command=self.ok)
        b.pack(pady=5)
        root.withdraw()
        
    def ok(self):
        global ipget
        ipget=self.e.get()
        self.top.destroy()
        return [ipget,]#ipget

def frontmenu():
    def closeAbo():
        # check if saving
        # if not:
        abo.destroy()
    def callquit(event):
        abo.destroy()

    #from PIL import ImageTk, Image
    global curF, fmenu
    curF = "abo"
    fmenu = Toplevel()
    fmenu.title ('About ')
    fmenu.attributes('-fullscreen', True)
    fmenu.protocol('WM_DELETE_WINDOW', closeAbo)
    fmenu.attributes("-toolwindow", 1)
    #abo.resizable(0,0)
    fmenu.bind("<Button-1>", callquit)
    img = ImageTk.PhotoImage(Image.open(path))
    panel = Label(fmenu, image = img)
    panel.pack(side = "bottom", fill = "both", expand = "yes")

def isadmin():
    if (stsa==0):
        quit()
    else:
        showadmin()

def showadmin():
    #checkpwd()
    print 'cheat password'
    makemenu(root)
    return

def makemenu(win):
    top = Menu(win)       
    win.config(menu=top)
    win.title('%s' % appname)
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    # use the next line if you also want to get rid of the titlebar
    #root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.wm_iconbitmap(useicon)
    file = Menu(top, tearoff=0)
    file.add_command(label='Input Biodata',  command=finputbio,  underline=0)
    file.add_command(label='Input Kegiatan',  command=finputkegiatan,  underline=7)
    file.add_command(label='Admin Password',  command=fadmin,  underline=0)
    file.add_command(label='Tutup',    command=root.destroy, underline=0)
    top.add_cascade(label='Menu Utama',     menu=file,        underline=0)

    edit = Menu(top, tearoff=0)
    edit.add_command(label='About %s' % appname,     command=about,  underline=0)
    top.add_cascade(label='About', menu=edit,  underline=0)

    finputbio()
    #about()
    
def checkpwd():
    failure_max = 3
    passwords = [('admin', 'hukum'), ('newbie', 'help!')]
    global dlog
    dlog=None

    def make_entry(parent, caption, width=None, **options):
        Label(parent, text=caption).pack(side=TOP)
        entry = Entry(parent, **options)
        if width:
            entry.config(width=width)
        entry.pack(side=TOP, padx=10, fill=BOTH)
        return entry

    def enter(event):
        check_password()

    def check_password():
        """ Collect 1's for every failure and quit program in case of failure_max failures """
        #print(user.get(), password.get())
        if (user.get(), password.get()) in passwords:
            check_password.user = user.get()
            #root.destroy()
            root.deiconify()
            pwdf.destroy()
            dlog = True
            makemenu(root)
            return
        check_password.failures += 1
        if check_password.failures == failure_max:
            root.destroy()
            raise SystemExit('Login tidak diijinkan')
        else:
            pwdf.title('Coba lagi. Kesempatan %i/%i' % (check_password.failures + 1, failure_max))
    check_password.failures = 0

    root.withdraw()
    pwdf = Toplevel()
    pwdf.geometry('300x160')
    pwdf.title('Masukkan informasi anda')
    #frame for window margin
    parent = Frame(pwdf, padx=10, pady=10)
    parent.pack(fill=BOTH, expand=True)
    #entrys with not shown text
    user = make_entry(parent, "Username:", 16, show='*')
    password = make_entry(parent, "Password:", 16, show="*")
    #button to attempt to login
    b = Button(parent, borderwidth=4, text="Login", width=10, pady=8, command=check_password)
    b.pack(side=BOTTOM)
    password.bind('<Return>', enter)

    user.focus_set()
    
def main():
    global db, cursor, dhost, host, ipserv, stsa
    if not os.path.exists(serverfile):
        ips()
    #cadmin()
    stsa=0
    try:
        fileserv = open(serverfile, 'r')
        stserv=addstr+fileserv.read()[7:]
        ipserv= bz2.decompress(base64.b64decode(stserv))
        host = ipserv
        db = psycopg2.connect(
        host = ipserv,
        database = 'fhunwardb',
        user = 'postgres',
        password = 'srigaladomb4'
        )
        cursor = db.cursor()
        stsa=1
        #go to view

        return True
    except Exception: # try to avoid catching Exception unless you have too
        #first use check existing file in server.txt
        try:
            db = psycopg2.connect(
            host = ipserv,
            database = 'fhunwardb',
            user = 'postgres',
            password = 'srigaladomb4'
            )
            cursor = db.cursor()
            print "Successfully connect host: %s" % host
            print "Welcome Admin!"
            stsa=1
            #go to admin
            #showadmin()
            return
        except Exception:
            tkMessageBox.showinfo("Info Cek", "Apakah komputer view (server) sudah dihidupkan?")
            if tkMessageBox.askyesno("Reset IP Server", "Apakah IP Server berubah, tulis konfigurasi IP ulang?"):
                try:
                    os.remove(serverfile)
                except OSError:
                    pass
                ips()
                tkMessageBox.showinfo("Restart Diperlukan", "Konfigurasi IP sukses. Silahkan restart Aplikasi untuk melanjutkan!")
        root.destroy()
        return False


def ips():
    #ask ipserver
    d = MyDialog(root)
    root.wait_window(d.top)
    root.withdraw()
    foo = base64.b64encode(bz2.compress(ipget))
    gfoo = foo[13:]
    wfile=(kstr+gfoo).strip(' ')
    file(serverfile, 'w').close
    text_file = open(serverfile, "w")
    text_file.write(wfile)
    text_file.close()

def activaterootfrombio():
    root.update()
    root.deiconify()
    bio.destroy()

def printSelect(running,tweak):
    print tweak
    global myid
    if (running == "bio"):
        #find staff detail
        thismonth()
        cursor.execute("SELECT * FROM biodata WHERE idbio = %s", (tweak,))
        myid = tweak
        databio=cursor.fetchall()
        for ent_item in entjentry:  #enttuples
            ent_item.delete(0,END)
        for dK in databio:
            if (dK[5]==1):
                isdo='Dosen'
            else:
                isdo='Pegawai'
            e_list[0].insert(0, dK[1])
            e_list[1].insert(0, dK[2])
            e_list[2].insert(0, dK[3])
            e_list[3].insert(0, dK[4])
            varCombo.set(isdo)
            e_list[5].insert(0, dK[6])
            e_list[6].insert(0, dK[7])
            e_list[7].insert(0, dK[8])
            e_list[8].insert(0, dK[9])
            e_list[9].insert(0, dK[10])
            e_list[10].insert(0, dK[11])
        btnU['state'] = NORMAL
        btnD['state'] = NORMAL

def thismonth():
    global month
    month_en = datetime.date.today().strftime("%B")
    lmonth_en = ['January', 'February', 'March', 'April', 'May',
                     'June', 'July', 'August', 'September', 'October', 'November', 'December']
    lmonth_id = ['Januari', 'Februari', 'Maret', 'April', 'Mei',
                     'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'Nopember', 'Desember']
    idm = lmonth_en.index(month_en)
    idmonth = lmonth_id[int(idm)]
    thisyear = datetime.date.today().strftime("%Y")
    month = '%s %s' % (idmonth, str(thisyear),)
    print 'Bulan sekarang adalah %s' % month
    
class MultiListbox(Frame):
    def __init__(self, master, lists):
        Frame.__init__(self, master)
        
        self.lists = []
        for l,w in lists:
            frame = Frame(self); frame.pack(side=LEFT, expand=YES, fill=BOTH)
            Label(frame, text=l, borderwidth=1, relief=RAISED).pack(fill=X)
            lb = Listbox(frame, width=w, borderwidth=0, selectborderwidth=0,
			 relief=FLAT, exportselection=FALSE)
            lb.pack(expand=YES, fill=BOTH)
            self.lists.append(lb)
            lb.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
            lb.bind('<Button-1>', lambda e, s=self: s._select(e.y))
            lb.bind('<Leave>', lambda e: 'break')
            lb.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
            lb.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
        frame = Frame(self); frame.pack(side=LEFT, fill=Y)
        Label(frame, borderwidth=1, relief=RAISED).pack(fill=X)
        sb = Scrollbar(frame, orient=VERTICAL, command=self._scroll)
        sb.pack(expand=YES, fill=Y)
        self.lists[0]['yscrollcommand']=sb.set

    def _select(self, y):
        row = self.lists[0].nearest(y)
        self.selection_clear(0, END)
        self.selection_set(row)
        #begin modify
        listmyrow = ()
        for l in self.lists:
            myrow = l.get(row) #print
            listmyrow = listmyrow + (myrow,)
        printSelect(curF,listmyrow[0])
        #make function to related window call
        return 'break'

    def _button2(self, x, y):
        for l in self.lists: l.scan_mark(x, y)
        return 'break'

    def _b2motion(self, x, y):
        for l in self.lists: l.scan_dragto(x, y)
        return 'break'

    def _scroll(self, *args):
        for l in self.lists:
            apply(l.yview, args)

    def curselection(self):
        return self.lists[0].curselection()

    def delete(self, first, last=None):
        for l in self.lists:
            l.delete(first, last)

    def get(self, first, last=None):
        result = []
        for l in self.lists:
            result.append(l.get(first,last))
        if last: return apply(map, [None] + result)
        return result
	    
    def index(self, index):
        self.lists[0].index(index)

    def insert(self, index, *elements):
        for e in elements:
            i = 0
            for l in self.lists:
                l.insert(index, e[i])
                i = i + 1

    def size(self):
        return self.lists[0].size()

    def see(self, index):
        for l in self.lists:
            l.see(index)

    def selection_anchor(self, index):
        for l in self.lists:
            l.selection_anchor(index)

    def selection_clear(self, first, last=None):
        for l in self.lists:
            l.selection_clear(first, last)

    def selection_includes(self, index):
        return self.lists[0].selection_includes(index)

    def selection_set(self, first, last=None):
        for l in self.lists:
            l.selection_set(first, last)

    def __init__(self, master, lists):
        Frame.__init__(self, master)
        self.lists = []
        self.colmapping={}
        self.origData = None
        for l,w in lists:
            frame = Frame(self); frame.pack(side=LEFT, expand=YES, fill=BOTH)
            b = Button(frame, text=l, borderwidth=1, relief=RAISED)
            b.pack(fill=X)
            b.bind('<Button-1>', self._sort)
            self.colmapping[b]=(len(self.lists),1)
            lb = Listbox(frame, width=w, borderwidth=0, selectborderwidth=0,
                         relief=FLAT, exportselection=FALSE)
            lb.pack(expand=YES, fill=BOTH)
            self.lists.append(lb)
            lb.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
            lb.bind('<Button-1>', lambda e, s=self: s._select(e.y))
            lb.bind('<Leave>', lambda e: 'break')
            lb.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
            lb.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
        frame = Frame(self); frame.pack(side=LEFT, fill=Y)
        Label(frame, borderwidth=1, relief=RAISED).pack(fill=X)
        sb = Scrollbar(frame, orient=VERTICAL, command=self._scroll)
        sb.pack(expand=YES, fill=Y)
        self.lists[0]['yscrollcommand']=sb.set
        
    def _sort(self, e):
        # get the listbox to sort by (mapped by the header button)
        b=e.widget
        col, direction = self.colmapping[b]

        # get the entire table data into mem
        tableData = self.get(0,END)
        if self.origData == None:
            import copy
            self.origData = copy.deepcopy(tableData)
            
        rowcount = len(tableData)
        
        #remove old sort indicators if it exists
        for btn in self.colmapping:
            lab = btn.cget('text')
            if lab[0]=='[': btn.config(text=lab[4:])
                
        btnLabel = b.cget('text')
        #sort data based on direction
        if direction==0:
            tableData = self.origData
        else:
            if direction==1: b.config(text='[+] ' + btnLabel) 
            else: b.config(text='[-] ' + btnLabel)
            # sort by col
            tableData.sort(key=lambda x: x[col], reverse=direction<0)

        #clear widget
        self.delete(0,END)
        
        # refill widget
        for row in range(rowcount):
            self.insert(END, tableData[row])
 
        # toggle direction flag 
        if direction==1: direction=-1
        else: direction += 1
        self.colmapping[b] = (col, direction)
    
if __name__ == '__main__':
    print "For Admin only"
    root = Tk()
    main()
    isadmin()
    root.mainloop()
