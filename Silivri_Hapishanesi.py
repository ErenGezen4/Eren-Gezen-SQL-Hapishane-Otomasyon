import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import bcrypt
import hashlib

connection = sqlite3.connect("databasenin path'i")
cursor = connection.cursor()

yasakli_karakterler = ["'", "=", "*", "/", ";", "--", "#", "%", "$", "!", "&", "|"]

cursor.execute("""
CREATE TABLE IF NOT EXISTS Login (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Kullanici_adi TEXT NOT NULL,
    sifre TEXT NOT NULL,
    rol TEXT NOT NULL
);
""")
connection.commit()


def kontrol_giris():
    global kullanici_adi
    kullanici_adi = kullanici_adi_entry.get()
    sifre = sifre_entry.get()

    if not kullanici_adi:
        messagebox.showerror("Hata", "Bu alan boş bırakılamaz")
        return
    
    if not sifre:
        messagebox.showerror("Hata", "Bu alan boş bırakılamaz")
        return

    if any(char in kullanici_adi for char in yasakli_karakterler):
        messagebox.showerror("Hata", "SQL KORUMASI")
        return

    sifre_hash = hashlib.sha256(sifre.encode('utf-8')).hexdigest()

    cursor.execute("SELECT Kullanici_adi, sifre, rol FROM Login WHERE Kullanici_adi = ? AND sifre = ?", (kullanici_adi, sifre_hash))
    sonuc = cursor.fetchone()

    if sonuc:
        messagebox.showinfo("Başarılı", "Giriş başarılı!")
        ana_pencere.withdraw()
        yeni_pencere(kullanici_adi, sonuc[2])  
    else:
        messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış!")



def yeni_pencere(kullanici_adi, rol):
    yeni = tk.Toplevel()
    yeni.title("Hapishane Otomasyonu")
    yeni.geometry("1200x800")

    sol_panel = tk.Frame(yeni, bg="#2b3e50", width=250)
    sol_panel.pack(side="left", fill="y")

    title_label = tk.Label(sol_panel, text="Silivri Cezaevi", fg="white", bg="#2b3e50", font=("Arial", 16, "bold"))
    title_label.pack(pady=20)

    bilgi_frame = tk.Frame(yeni, bg="#f7f7f7", bd=2, relief="groove")
    bilgi_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    role_label = tk.Label(
        sol_panel,
        text=f"Rol: {rol.capitalize()}",
        bg="#2b3e50",
        fg="white",
        font=("Arial", 12, "italic")
    )
    role_label.pack(side="bottom", pady=10)

    def ana_sayfa():
        for widget in bilgi_frame.winfo_children():
            widget.destroy()

        # Başlık kısmı
        header_frame = tk.Frame(bilgi_frame, bg="#1f6aa5")
        header_frame.pack(fill="x")

        tk.Label(
            header_frame,
            text="Hapishane Otomasyonu",
            bg="#1f6aa5",
            fg="white",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

 
        content_frame = tk.Frame(bilgi_frame, bg="#ffffff")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    
        hapishane_emoji = "🏢🔒"  
        tk.Label(
            content_frame,
            text=hapishane_emoji,
            font=("Arial", 100),
            bg="#ffffff",
            fg="#2b3e50"
        ).pack(pady=20)

   
        metin = (
            "Silivri Cezaevi, modern altyapısı ve yüksek güvenlik önlemleriyle Türkiye'nin en büyük hapishanelerindendir. "
            "Mahkumların rehabilitasyonu için çeşitli eğitim ve sosyal programlar sunar. "
            "Gelişmiş güvenlik sistemleri sayesinde mahkumların ve çalışanların güvenliği sağlanır. "
            "Bu otomasyon sistemi, tüm süreçleri kolaylaştırmayı amaçlamaktadır."

        )
        tk.Label(
            content_frame,
            text=metin,
            bg="#ffffff",
            font=("Arial", 14),
            wraplength=600,
            justify="left"
        ).pack(pady=20)
        
        footer_frame = tk.Frame(bilgi_frame, bg="#2b3e50")  
        footer_frame.pack(fill="x", side="bottom")  

        tk.Label(
            footer_frame,
            text="|  Eren Gezen   |",
            bg="#2b3e50", 
            fg="white",
            font=("Arial", 10, "italic")
        ).pack(pady=5)
    tk.Button(
        sol_panel,
        text="Ana Sayfa",
        command=ana_sayfa,
        bg="#2b3e50",
        fg="white",
        font=("Arial", 12)
    ).pack(pady=10, fill="x")

    ana_sayfa()

    
    def mahkumlari_goruntule():
        for widget in bilgi_frame.winfo_children():
            widget.destroy()

        header_frame = tk.Frame(bilgi_frame, bg="#1f6aa5")
        header_frame.pack(fill="x")

        tk.Label(header_frame, text="Mahkumlar", bg="#1f6aa5", fg="white", font=("Arial", 18, "bold")).pack(pady=10)

        content_frame = tk.Frame(bilgi_frame, bg="#ffffff")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        cursor.execute("""
        SELECT Mahkum.isim, Mahkum.adres, Mahkum.tel_no, Mahkum.yas, Suc.suc, Mahkum.giris
        FROM Mahkum
        JOIN Suc ON Mahkum.suc_id = Suc.ID
        JOIN Kogus ON Mahkum.kogus_id = Kogus.ID;
        """)
        mahkumlar = cursor.fetchall()

        columns = ["İsim", "Adres", "Telefon", "Yaş", "Suç", "Giriş Tarihi"]
        tree = ttk.Treeview(content_frame, columns=columns, show="headings", height=15)
        tree.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#FFA500", foreground="black")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        for mahkum in mahkumlar:
            tree.insert("", "end", values=mahkum)

    def mahkum_sorgu():
        for widget in bilgi_frame.winfo_children():
            widget.destroy()

        header_frame = tk.Frame(bilgi_frame, bg="#1f6aa5")
        header_frame.pack(fill="x")

        tk.Label(header_frame, text="Mahkum Sorgu", bg="#1f6aa5", fg="white", font=("Arial", 18, "bold")).pack(pady=10)

        content_frame = tk.Frame(bilgi_frame, bg="#ffffff")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        search_frame = tk.Frame(content_frame, bg="#ffffff")
        search_frame.pack(fill="x", padx=4, pady=10)

        tk.Label(search_frame, text="Mahkum Adı:", bg="#ffffff", font=("Arial", 12)).pack(side="left", padx=5)
        search_entry = tk.Entry(search_frame, font=("Arial", 12))
        search_entry.pack(side="left", fill="x", expand=True, padx=5)

        def search():
            for widget in content_frame.winfo_children():
                if widget != search_frame:
                    widget.destroy()

            mahkum_adi = search_entry.get()
            
            if not mahkum_adi:
                messagebox.showerror("Hata", "Bu alan boş bırakılamaz")
                return
            
            if any(char in mahkum_adi for char in yasakli_karakterler):
                messagebox.showerror("Hata", "SQL KORUMASI")
                return
            
            cursor.execute("""
            SELECT Mahkum.isim, Mahkum.adres, Mahkum.tel_no, Mahkum.yas, Suc.suc, Suc.ceza_suresi, Mahkum.giris, Kogus.kogus_ismi, Mahkum.foto_url
            FROM Mahkum
            JOIN Suc ON Mahkum.suc_id = Suc.ID
            JOIN Kogus ON Mahkum.kogus_id = Kogus.ID
            WHERE Mahkum.isim LIKE ?;
            """, (f"%{mahkum_adi}%",))
            sonuc = cursor.fetchall()

            if not sonuc:
                tk.Label(content_frame, text="Sonuç bulunamadı.", bg="#ffffff", font=("Arial", 12)).pack(pady=10)
                return

            columns = ["İsim", "Adres", "Telefon", "Yaş", "Suç","Ceza Süresi", "Giriş Tarihi", "Koğuş"]
            tree = ttk.Treeview(content_frame, columns=columns, show="headings", height=10)
            tree.pack(fill="both", expand=True, padx=5, pady=5)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center")

            for row in sonuc:
                tree.insert("", "end", values=row[:-1])

            if sonuc[0][-1]:
                try:
                    img = Image.open(sonuc[0][-1])
                    img = img.resize((700, 400))
                    photo = ImageTk.PhotoImage(img)
                    img_label = tk.Label(content_frame, image=photo, bg="#ffffff")
                    img_label.image = photo
                    img_label.pack(pady=10)
                except Exception as e:
                    tk.Label(content_frame, text="Fotoğraf yüklenemedi.", bg="#ffffff", fg="red", font=("Arial", 12)).pack(pady=10)

        tk.Button(search_frame, text="Ara", command=search, bg="#2b3e50", fg="white", font=("Arial", 12)).pack(side="left", padx=5)

    tk.Button(sol_panel, text="Mahkumları Görüntüle", command=mahkumlari_goruntule, bg="#2b3e50", fg="white", font=("Arial", 12)).pack(pady=10, fill="x")
    tk.Button(sol_panel, text="Mahkum Sorgu", command=mahkum_sorgu, bg="#2b3e50", fg="white", font=("Arial", 12)).pack(pady=10, fill="x")
    def yonetim_paneli(rol):
        for widget in bilgi_frame.winfo_children():
            widget.destroy()

        header_frame = tk.Frame(bilgi_frame, bg="#1f6aa5")
        header_frame.pack(fill="x")

        tk.Label(header_frame, text="Yönetim Paneli", bg="#1f6aa5", fg="white", font=("Arial", 18, "bold")).pack(pady=10)

        content_frame = tk.Frame(bilgi_frame, bg="#ffffff")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        if rol != "müdür":
            tk.Label(content_frame, text="Bu panele sadece müdürler erişebilir!", bg="#ffffff", fg="red", font=("Arial", 14, "bold")).pack(pady=20)
            return

        def hesap_ekle():
            ekle_pencere = tk.Toplevel()
            ekle_pencere.title("Hesap Ekle")

        
            tk.Label(ekle_pencere, text="Kullanıcı Adı:").grid(row=0, column=0)
            kullanici_adi_entry = tk.Entry(ekle_pencere)
            kullanici_adi_entry.grid(row=0, column=1)

            tk.Label(ekle_pencere, text="Şifre:").grid(row=1, column=0)
            sifre_entry = tk.Entry(ekle_pencere, show="*")
            sifre_entry.grid(row=1, column=1)

        
            rol_secenekleri = ["kullanıcı", "müdür"]
            rol_variable = tk.StringVar(ekle_pencere)
            rol_variable.set(rol_secenekleri[0])  
            rol_combobox = ttk.Combobox(ekle_pencere, textvariable=rol_variable, values=rol_secenekleri)
            rol_combobox.grid(row=2, column=0, columnspan=2)

            def kaydet():
                kullanici_adi = kullanici_adi_entry.get()
                sifre = sifre_entry.get()
                rol = rol_variable.get()
                
                if not kullanici_adi:
                    messagebox.showerror("Hata", "Bu alan boş bırakılamaz")
                    return
                
                if not sifre:
                    messagebox.showerror("Hata", "Bu alan boş bırakılamaz")
                    return
                
                if not rol:
                    messagebox.showerror("Hata", "Bu alan boş bırakılamaz")
                    return
                
                if any(char in kullanici_adi or sifre or rol for char in yasakli_karakterler):
                    messagebox.showerror("Hata", "SQL KORUMASI")
                    return
                sifre_hash = hashlib.sha256(sifre.encode('utf-8')).hexdigest()

                # Veritabanına yeni kullanıcı ekleme
                cursor.execute("INSERT INTO Login (Kullanici_adi, sifre, rol) VALUES (?, ?, ?)", (kullanici_adi, sifre_hash, rol))
                connection.commit()

                messagebox.showinfo("Başarılı", "Hesap başarıyla eklendi!")
                ekle_pencere.destroy()

            tk.Button(ekle_pencere, text="Kaydet", command=kaydet).grid(row=3, column=0, columnspan=2)
        
        def hesap_sil():
            sil_pencere = tk.Toplevel()
            sil_pencere.title("Hesap Sil")

            tk.Label(sil_pencere, text="Kullanıcı Adı:").grid(row=0, column=0)
            silinecek_kullanici_entry = tk.Entry(sil_pencere)
            silinecek_kullanici_entry.grid(row=0, column=1)

            def sil():
                kullanici_adi = silinecek_kullanici_entry.get()

                if not kullanici_adi:
                    messagebox.showerror("Hata", "Bu alan boş bırakılamaz")
                    return
                
                if any(char in kullanici_adi for char in yasakli_karakterler):
                    messagebox.showerror("Hata", "SQL KORUMASI")
                    return

                # Veritabanından kullanıcı silme
                cursor.execute("DELETE FROM Login WHERE Kullanici_adi = ?", (kullanici_adi,))
                connection.commit()

                messagebox.showinfo("Başarılı", "Hesap başarıyla silindi!")
                sil_pencere.destroy()

            tk.Button(sil_pencere, text="Sil", command=sil).grid(row=1, column=0, columnspan=2)
        
        
        def mahkum_ekle():
            ekle_pencere = tk.Toplevel()
            ekle_pencere.title("Mahkum Ekle")

            fields = ["İsim", "Adres", "Telefon", "Yaş", "Suç ID", "Ceza Süresi ID", "Giriş Tarihi", "Koğuş ID","Gorev ID", "Fotoğraf URL"]
            entries = {}

            for idx, field in enumerate(fields):
                tk.Label(ekle_pencere, text=f"{field}:").grid(row=idx, column=0)
                entry = tk.Entry(ekle_pencere)
                entry.grid(row=idx, column=1)
                entries[field] = entry

            def kaydet():
                data = {field: entry.get() for field, entry in entries.items()}
                
                cursor.execute("""
                INSERT INTO Mahkum (isim, adres, tel_no, yas, suc_id, ceza_suresi_id, giris, kogus_id, gorev_id, foto_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, tuple(data.values()))
                connection.commit()
                messagebox.showinfo("Başarılı", "Mahkum eklendi!")
                ekle_pencere.destroy()

            tk.Button(ekle_pencere, text="Kaydet", command=kaydet, bg="#2b3e50", fg="white", font=("Arial", 12)).grid(row=len(fields), columnspan=2)

        def mahkum_sil():
            sil_pencere = tk.Toplevel()
            sil_pencere.title("Mahkum Sil")

            tk.Label(sil_pencere, text="Mahkum Adı:").grid(row=0, column=0)
            isim_entry = tk.Entry(sil_pencere)
            isim_entry.grid(row=0, column=1)

            def sil():
                mahkum_adi = isim_entry.get()
                
                if not mahkum_adi:
                    messagebox.showerror("Hata", "Bu alan boş bırakılamaz")
                    return
                
                if any(char in mahkum_adi for char in yasakli_karakterler):
                    messagebox.showerror("Hata", "SQL KORUMASI")
                    return
                cursor.execute("DELETE FROM Mahkum WHERE isim = ?", (mahkum_adi,))
                connection.commit()
                messagebox.showinfo("Başarılı", "Mahkum silindi!")
                sil_pencere.destroy()

            tk.Button(sil_pencere, text="Sil", command=sil, bg="#2b3e50", fg="white", font=("Arial", 12)).grid(row=1, columnspan=2)

        def mahkum_guncelle():
            guncelle_pencere = tk.Toplevel()
            guncelle_pencere.title("Mahkum Güncelle")

            fields = ["ID", "İsim", "Adres", "Telefon", "Yaş", "Suç ID", "Ceza Süresi ID", "Giriş Tarihi", "Koğuş ID","Gorev ID", "Fotoğraf URL"]
            entries = {}

            for idx, field in enumerate(fields):
                tk.Label(guncelle_pencere, text=f"{field}:").grid(row=idx, column=0)
                entry = tk.Entry(guncelle_pencere)
                entry.grid(row=idx, column=1)
                entries[field] = entry

            def guncelle():
                    # Kullanıcıdan girilen verileri al
                data = {field: entry.get() for field, entry in entries.items()}
                cursor.execute("""
                UPDATE Mahkum 
                SET isim = ?, adres = ?, tel_no = ?, yas = ?, suc_id = ?, ceza_suresi_id = ?, giris = ?, kogus_id = ?, gorev_id = ?, foto_url = ?
                WHERE ID = ?
                """, (*list(data.values())[1:], data["ID"]))
    

                connection.commit()
                messagebox.showinfo("Başarılı", "Mahkum bilgileri güncellendi!")
    

                guncelle_pencere.destroy()

            tk.Button(guncelle_pencere, text="Güncelle", command=guncelle, bg="#2b3e50", fg="white", font=("Arial", 12)).grid(row=len(fields), columnspan=2)

        tk.Button(content_frame, text="Mahkum Ekle", command=mahkum_ekle, bg="#2b3e50", fg="white", font=("Arial", 12)).pack(pady=10, fill="x")
        tk.Button(content_frame, text="Mahkum Sil", command=mahkum_sil, bg="#2b3e50", fg="white", font=("Arial", 12)).pack(pady=10, fill="x")
        tk.Button(content_frame, text="Mahkum Güncelle", command=mahkum_guncelle, bg="#2b3e50", fg="white", font=("Arial", 12)).pack(pady=10, fill="x")
        tk.Button(content_frame, text="Hesap Ekle", command=hesap_ekle, bg="#2b3e50", fg="white", font=("Arial", 12)).pack(pady=10, fill="x")
        tk.Button(content_frame, text="Hesap Sil", command=hesap_sil, bg="#2b3e50", fg="white", font=("Arial", 12)).pack(pady=10, fill="x")

    def sifre_degistir():
        sifre_pencere = tk.Toplevel()
        sifre_pencere.title("Şifre Değiştir")
        sifre_pencere.geometry("400x200")

        tk.Label(sifre_pencere, text="Eski Şifre:", font=("Arial", 12)).grid(row=0, column=0, pady=10, padx=10)
        eski_sifre_entry = tk.Entry(sifre_pencere, show="*", font=("Arial", 12))
        eski_sifre_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(sifre_pencere, text="Yeni Şifre:", font=("Arial", 12)).grid(row=1, column=0, pady=10, padx=10)
        yeni_sifre_entry = tk.Entry(sifre_pencere, show="*", font=("Arial", 12))
        yeni_sifre_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(sifre_pencere, text="Yeni Şifre (Tekrar):", font=("Arial", 12)).grid(row=2, column=0, pady=10, padx=10)
        yeni_sifre_tekrar_entry = tk.Entry(sifre_pencere, show="*", font=("Arial", 12))
        yeni_sifre_tekrar_entry.grid(row=2, column=1, pady=10, padx=10)

        def sifre_guncelle():
            eski_sifre = eski_sifre_entry.get()
            yeni_sifre = yeni_sifre_entry.get()
            yeni_sifre_tekrar = yeni_sifre_tekrar_entry.get()

            if not eski_sifre:
                    messagebox.showerror("Hata", "Bu alan boş bırakılamaz")
                    return
            
            if not yeni_sifre:
                    messagebox.showerror("Hata", "Bu alan boş bırakılamaz")
                    return

            if not yeni_sifre_tekrar:
                    messagebox.showerror("Hata", "Bu alan boş bırakılamaz")
                    return

            if any(char in eski_sifre or yeni_sifre or yeni_sifre_tekrar for char in yasakli_karakterler):
                messagebox.showerror("Hata", "SQL KORUMASI: Yasaklı karakter kullanılamaz!")
                return

            cursor.execute("SELECT sifre FROM Login WHERE Kullanici_adi = ?", (kullanici_adi,))
            mevcut_sifre = cursor.fetchone()

            if mevcut_sifre and mevcut_sifre[0] == eski_sifre:
                if yeni_sifre == yeni_sifre_tekrar:
                    cursor.execute("UPDATE Login SET sifre = ? WHERE Kullanici_adi = ?", (yeni_sifre, kullanici_adi))
                    connection.commit()
                    messagebox.showinfo("Başarılı", "Şifre başarıyla değiştirildi!")
                    sifre_pencere.destroy()
                else:
                    messagebox.showerror("Hata", "Yeni şifreler eşleşmiyor!")
            else:
                messagebox.showerror("Hata", "Eski şifre yanlış!")

        tk.Button(sifre_pencere, text="Güncelle", command=sifre_guncelle, bg="#2b3e50", fg="white", font=("Arial", 12)).grid(row=3, columnspan=2, pady=10)

    tk.Button(sol_panel, text="Yönetim Paneli", command=lambda: yonetim_paneli(rol), bg="#2b3e50", fg="white", font=("Arial", 12)).pack(pady=10, fill="x")
    tk.Button(sol_panel, text="Şifre Değiştir", command=sifre_degistir, bg="#2b3e50", fg="white", font=("Arial", 12)).pack(pady=10, fill="x")
    def kogus_bilgisi():
        for widget in bilgi_frame.winfo_children():
            widget.destroy()

        header_frame = tk.Frame(bilgi_frame, bg="#1f6aa5")
        header_frame.pack(fill="x")

        tk.Label(header_frame, text="Koğuş Bilgisi", bg="#1f6aa5", fg="white", font=("Arial", 18, "bold")).pack(pady=10)

        content_frame = tk.Frame(bilgi_frame, bg="#ffffff")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        cursor.execute("SELECT ID, kogus_ismi FROM Kogus;")
        koguslar = cursor.fetchall()

        for kogus in koguslar:
            def show_kogus_mahkumlar(kogus_id):
                for widget in content_frame.winfo_children():
                    widget.destroy()

                tk.Label(content_frame, text=f"Koğuş {kogus_id} Mahkumları", bg="#ffffff", font=("Arial", 14, "bold")).pack(pady=10)

                cursor.execute("""
                SELECT Mahkum.isim, Mahkum.adres, Mahkum.tel_no, Mahkum.yas, Suc.suc, Suc.ceza_suresi, Gorev.gorev, Mahkum.giris
                FROM Mahkum
                JOIN Suc ON Mahkum.suc_id = Suc.ID
                JOIN Gorev ON Mahkum.gorev_id = Gorev.ID
                WHERE kogus_id = ?;
                """, (kogus_id,))
                mahkumlar = cursor.fetchall()

                columns = ["İsim", "Adres", "Telefon", "Yaş", "Suç", "Ceza Süresi", "Gorevi", "Giriş Tarihi"]
                tree = ttk.Treeview(content_frame, columns=columns, show="headings", height=10)
                tree.pack(fill="both", expand=True, padx=5, pady=5)

                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, anchor="center")

                for mahkum in mahkumlar:
                    tree.insert("", "end", values=mahkum)

            tk.Button(content_frame, text=f"{kogus[1]}", command=lambda k_id=kogus[0]: show_kogus_mahkumlar(k_id), 
                      bg="#2b3e50", fg="white", font=("Arial", 12)).pack(pady=5, fill="x")

    tk.Button(sol_panel, text="Koğuş Bilgisi", command=kogus_bilgisi, bg="#2b3e50", fg="white", font=("Arial", 12)).pack(pady=10, fill="x")


ana_pencere = tk.Tk()
ana_pencere.title("Silivri Hapishanesi - Giriş")
ana_pencere.geometry("500x400")


bg_image = Image.open("hapishane_resiminin path'i")
bg_image = bg_image.resize((500, 400), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)
arka_plan = tk.Label(ana_pencere, image=bg_photo)
arka_plan.place(relwidth=1, relheight=1)


tk.Label(ana_pencere, text="Silivri Hapishanesi", bg="#2c3e50", fg="white", font=("Arial", 16, "bold"), pady=10).pack(fill="x")


tk.Label(ana_pencere, text="Kullanıcı Adı:", bg="#34495e", fg="white", font=("Arial", 12)).pack(pady=10)
kullanici_adi_entry = tk.Entry(ana_pencere, font=("Arial", 12), justify="center", bg="#ecf0f1", relief="flat")
kullanici_adi_entry.pack(pady=5, padx=50, fill="x")

tk.Label(ana_pencere, text="Şifre:", bg="#34495e", fg="white", font=("Arial", 12)).pack(pady=10)
sifre_entry = tk.Entry(ana_pencere, show="*", font=("Arial", 12), justify="center", bg="#ecf0f1", relief="flat")
sifre_entry.pack(pady=5, padx=50, fill="x")

giris_butonu = tk.Button(
    ana_pencere,
    text="Giriş Yap",
    command=kontrol_giris,
    bg="#2980b9",
    fg="white",
    font=("Arial", 12, "bold"),
    activebackground="#3498db",
    activeforeground="white",
    relief="flat",
    cursor="hand2"
)
giris_butonu.pack(pady=20, padx=50, fill="x")

tk.Label(ana_pencere, text="| Eren Gezen |", bg="#2c3e50", fg="white", font=("Arial", 10), pady=10).pack(side="bottom", fill="x")

ana_pencere.mainloop()

conn.close()