import customtkinter
from PIL import Image
from CTkSpinbox import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import numpy as np

#----------------------------------####-------------------------------------------------
#----------------------------------####-------------------------------------------------

# Oynaning boshlangich qiymati oq
# bosh oynani o'lchamlarini berib icon qoshib olamiz.
app = customtkinter.CTk()
app.geometry("1024x768")
app.title("LWR Model")
app.iconbitmap("./images/icon.ico")
app.resizable(False, False)
#---------------------------------------------------------------------------------------



#----------------------------------####-------------------------------------------------
#----------------------------------####-------------------------------------------------

# Transport oqimining zichligini hisoblash

def density(L = 7000, step_l = 100, T = 400, step_t = 1000, p_0 = 0.05, p_max=0.25, v_max = 10):

    dl = L/step_l
    dt = T/step_t

    # Kerakli o'lchamdagi massivni numpy kutubxonasi yordamida x va t uchun yaratib,
    # boshlangich chegara shartlari bilan toldirib olamiz

    l = np.array([dl * i for i in range(step_l + 1)])
    t = np.array([dt * i for i in range(step_t + 1)])
    p = np.zeros((step_l + 1, step_t + 1))
    print("test")
    # zichlikning boshlangich chegarasini qiymati 100 metrga 5 deb olingan
    p[0] = 0
    p[1:, 0] = p_0
    p[-1] = p_0
    for j in range(step_t):
        for i in range(1, step_l):
            # bu yerga yuqoridagi keltirilgan 5 formulani yozamiz.
            p[i, j + 1] = (1 / 2) * (p[i + 1, j] + p[i - 1, j]) - (dt / (2 * dl)) \
             * (v_max - 2 * (v_max / p_max) * ((1 / 2) * (p[i + 1, j] + p[i - 1, j]))) * (p[i + 1, j] - p[i - 1, j])
    return l, t, p

#---------------------------------------------------------------------------------------
def reset_window():
    app.update()

def update():
    global l, t, p, L, step_l, T, step_t, p_0, p_max, v_max

    L = l_input.get()
    step_l = stepl_input.get()
    T = t_input.get()
    step_t = stept_input.get()
    p_0 = p0_input.get() / 1000
    p_max = pmax_input.get() / 1000
    v_max = vmax_input.get() / 3.6

    dl_input.configure(text = round(L/step_l, 1))
    dt_input.configure(text = round(T/step_t, 1))
    l, t, p = density(L=L, step_l=step_l, T=T, step_t=step_t, p_0=p_0, p_max=p_max, v_max=v_max)

    update_graph(l, t, p)


def update_graph(l, t, p):
    # ---------------------------------------------------------------------------------------
    ax1.clear()
    ax1.set_title('LWR model')
    ax1.set_xlabel('Time (sec)')
    ax1.set_ylabel('distance (m)')
    ax1.set_zlabel('Density p')
    X, Y = np.meshgrid(t, l)
    ax1.plot_surface(X, Y, p, cmap='plasma')
    main_canvas.draw()

    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # Ikkinchi 2d chizma
    ax2.clear()
    ax2.set_xlabel('distance (m)')
    ax2.set_ylabel('density (avt/m)')
    ax2.grid(True)
    ax2.plot(l[:], p[:, step_t // 6])
    ax2.plot(l[:], p[:, step_t // 6 * 2])
    ax2.plot(l[:], p[:, step_t // 6 * 3])
    ax2.plot(l[:], p[:, step_t // 6 * 4])
    ax2.plot(l[:], p[:, step_t // 6 * 5])
    ax2.plot(l[:], p[:, step_t // 6 * 6])
    main_canvas2.draw()

    # ---------------------------------------------------------------------------------------

    # Uchinchi 2d chizma
    ax3.clear()
    ax3.set_xlabel('Time (sec)')
    ax3.set_ylabel('density (avt/m)')
    ax3.grid(True)
    ax3.plot(t[:], p[step_l // 6, :])
    ax3.plot(t[:], p[step_l // 6 * 2, :])
    ax3.plot(t[:], p[step_l // 6 * 3, :])
    ax3.plot(t[:], p[step_l // 6 * 4, :])
    ax3.plot(t[:], p[step_l // 6 * 5, :])
    ax3.plot(t[:], p[step_l // 6 * 6, :])
    main_canvas3.draw()

    # ---------------------------------------------------------------------------------------




#---------------------------------------------------------------------------------------
# main frame yaratib olamiz
main_frame = customtkinter.CTkFrame(app, fg_color="#FFFFFF")
main_frame.pack(fill='both', expand=True)
#---------------------------------------------------------------------------------------

#----------------------------------####-------------------------------------------------
#----------------------------------####-------------------------------------------------

# Birinchi qator row = 1 Frame
row1_frame = customtkinter.CTkFrame(main_frame, fg_color="#FFFFFF")
row1_frame.pack(fill='x', expand=False, pady=(20, 0), padx=20)

# Logotip va uning textini joylab olaimz.
logo_img = Image.open("./images/logo.png")
logo_img = customtkinter.CTkImage(light_image=logo_img, dark_image=logo_img, size=(78.39, 72.1))
logo_img = customtkinter.CTkLabel(row1_frame, text="", image=logo_img)
logo_img.grid(row=0, column=0)
logo_text = customtkinter.CTkLabel(row1_frame, text="LWR MODEL", font=("Tahoma", 32, "bold"), text_color="#15078A")
logo_text.grid(row=0, column=1)
#---------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------
# Ikkinchi qator row = 2 Frame
row2_frame = customtkinter.CTkFrame(main_frame, fg_color="#FFFFFF")
row2_frame.pack(fill='x', expand=False, pady=(20, 0), padx=20)
#---------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------
# Uchta ustun frame yaratib olamiz
row2_col1_frame = customtkinter.CTkFrame(row2_frame, fg_color="#7703A7")
row2_col1_frame.pack(side='left', fill='x', expand=True, anchor='center')
row2_col1_frame.columnconfigure(0, weight=1)


row2_col2_frame = customtkinter.CTkFrame(row2_frame, fg_color="#7703A7")
row2_col2_frame.pack(side='left', fill='x', expand=True, padx=10)
row2_col2_frame.columnconfigure(0, weight=1)

row2_col3_frame = customtkinter.CTkFrame(row2_frame, fg_color="#7703A7")
row2_col3_frame.pack(side='left', fill='x', expand=True)
row2_col3_frame.columnconfigure(0, weight=1)
#---------------------------------------------------------------------------------------

#----------------------------------####-------------------------------------------------
#----------------------------------####-------------------------------------------------

# Birinchi ustun frame elementlari
# logotip va matn
path_img = Image.open("./images/Path.png")
path_img = customtkinter.CTkImage(light_image=path_img, dark_image=path_img, size=(53,53))
path_img = customtkinter.CTkLabel(row2_col1_frame, text="", image=path_img)
path_img.grid(row=0, column=0, padx=(20, 0), pady=(20, 0))
path_text = customtkinter.CTkLabel(row2_col1_frame, text="L-masofa", font=("Tahoma", 32, "bold"), text_color="#FFFFFF")
path_text.grid(row=0, column=1, padx=(0, 20), pady=(20, 0))
#---------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------
# Birinchi parametrni kiritish maydoni
l_label = customtkinter.CTkLabel(row2_col1_frame, text= "L(m)", font=("Tahoma", 20, "bold"), text_color="#FFFFFF")
l_label.grid(row=1, column=0, padx=(20, 5), pady=(10,0))

# --- l_input - Yo'lning uzunligi
l_input = CTkSpinbox(row2_col1_frame,  start_value = 7000, min_value = 0, fg_color='#FFFFFF',
                    button_color="#FCCD25", button_hover_color="#F99E39",button_border_color="",
                    max_value = 20000, step_value = 1000, width = 180)
l_input.grid(row=1, column=1, padx=(0, 20), pady=(10,0))
#---------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------

# Ikkinchi parametrni kiritish maydoni
stepl_label = customtkinter.CTkLabel(row2_col1_frame, text= "stepL", font=("Tahoma", 20, "bold"), text_color="#FFFFFF")
stepl_label.grid(row=2, column=0,  padx=(20, 5), pady=(10,0))

# --- stepl_input  - Yo'lning uzunligini qadamga bo'lishi uchun kerak bo'ladigan o'zgaruvchi
stepl_input = CTkSpinbox(row2_col1_frame,  start_value = 100, min_value = 0, fg_color='#FFFFFF',
                    button_color="#FCCD25", button_hover_color="#F99E39",button_border_color="",
                    max_value = 20000, step_value = 100, width = 180)

stepl_input.grid(row=2, column=1,padx=(0, 20), pady=(10,0))

#---------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------
# Uchinchi parametri yuqoridagilarni nisbatini chiqarish maydoni
dl_label = customtkinter.CTkLabel(row2_col1_frame, text= "dL", font=("Tahoma", 20, "bold"), text_color="#FFFFFF")
dl_label.grid(row=3, column=0, padx=(20, 5), pady=(10,20))

# --- L/step_l - nisbatini chiqarish
dl_input = customtkinter.CTkLabel(row2_col1_frame, width=180, height=40, fg_color="#FCCD25",
                                   text = l_input.get() / stepl_input.get(), bg_color='#444',
                                   text_color="#000000", corner_radius=5, font=("Tahoma", 20))
dl_input.grid(row=3, column=1, padx=(0, 20), pady=(10,20))
#---------------------------------------------------------------------------------------


#----------------------------------####-------------------------------------------------
#----------------------------------####-------------------------------------------------

# Ikkinchi ustun frame elementlari
# logotip va matn

path_img = Image.open("./images/TrafficJam.png")
path_img = customtkinter.CTkImage(light_image=path_img, dark_image=path_img, size=(53,53))
path_img = customtkinter.CTkLabel(row2_col2_frame, text="", image=path_img)
path_img.grid(row=0, column=0, padx=(20, 0), pady=(20, 0))
path_text = customtkinter.CTkLabel(row2_col2_frame, text="Dinamic", font=("Tahoma", 32, "bold"), text_color="#FFFFFF")
path_text.grid(row=0, column=1, padx=(0, 20), pady=(20, 0))
#---------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------
# Birinchi parametrni kiritish maydoni

p0_input = customtkinter.CTkLabel(row2_col2_frame, text= "p0 (avto/km)", font=("Tahoma", 20, "bold"), text_color="#FFFFFF")
p0_input.grid(row=1, column=0, padx=(20, 5), pady=(10,0))

# --- p0_input - Yo'lda joylashgan mashinalarning boshlang'ich zichligi
p0_input = CTkSpinbox(row2_col2_frame,  start_value = 50, min_value = 0, fg_color='#FFFFFF',
                    button_color="#FCCD25", button_hover_color="#F99E39",button_border_color="",
                    max_value = 300, step_value = 1, width = 180)
p0_input.grid(row=1, column=1, padx=(0, 20), pady=(10,0))
#---------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------
# Ikkinchi parametrni kiritish maydoni
pmax_input_label = customtkinter.CTkLabel(row2_col2_frame, text= "pmax(avt/km)", font=("Tahoma", 20, "bold"), text_color="#FFFFFF")
pmax_input_label.grid(row=2, column=0,  padx=(20, 5), pady=(10,0))

# --- pmax_input - Yo'lda joylashgan mashinalarning boshlang'ich zichligi kilometrda
pmax_input = CTkSpinbox(row2_col2_frame,  start_value = 250, min_value = 0, fg_color='#FFFFFF',
                    button_color="#FCCD25", button_hover_color="#F99E39",button_border_color="",
                    max_value = 300, step_value = 1, width = 180)

pmax_input.grid(row=2, column=1,padx=(0, 20), pady=(10,0))
#---------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------
#Uchinchi parametrni kiritish maydoni
vmax_label = customtkinter.CTkLabel(row2_col2_frame, text= "vmax(km/soat)", font=("Tahoma", 20, "bold"), text_color="#FFFFFF")
vmax_label.grid(row=3, column=0,  padx=(20, 5), pady=(10,20))

# --- vmax_input - Maksimal ruhsat etilgan tezlik km/soat
vmax_input = CTkSpinbox(row2_col2_frame,  start_value = 36, min_value = 0, fg_color='#FFFFFF',
                    button_color="#FCCD25", button_hover_color="#F99E39",button_border_color="",
                    max_value = 100, step_value = 1, width = 180)

vmax_input.grid(row=3, column=1,padx=(0, 20), pady=(10,20))
#---------------------------------------------------------------------------------------

#----------------------------------####-------------------------------------------------
#----------------------------------####-------------------------------------------------

# Uchinchi ustun frame elementlari
# logotip va matn
path_img = Image.open("./images/Timezone.png")
path_img = customtkinter.CTkImage(light_image=path_img, dark_image=path_img, size=(53,53))
path_img = customtkinter.CTkLabel(row2_col3_frame, text="", image=path_img)
path_img.grid(row=0, column=0, padx=(20, 0), pady=(20, 0))
path_text = customtkinter.CTkLabel(row2_col3_frame, text="T-vaqt", font=("Tahoma", 32, "bold"), text_color="#FFFFFF")
path_text.grid(row=0, column=1, padx=(0, 20), pady=(20, 0))
#---------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------
# Birinchi parametrni kiritish maydoni
t_label = customtkinter.CTkLabel(row2_col3_frame, text= "T(sek)", font=("Tahoma", 20, "bold"), text_color="#FFFFFF")
t_label.grid(row=1, column=0, padx=(20, 5), pady=(10,0))

#---t_input mashinani yo'lni bosib o'tishi uchun ketgan vaqti
t_input = CTkSpinbox(row2_col3_frame,  start_value = 400, min_value = 0, fg_color='#FFFFFF',
                    button_color="#FCCD25", button_hover_color="#F99E39",button_border_color="",
                    max_value = 20000, step_value = 100, width = 180)
t_input.grid(row=1, column=1, padx=(0, 20), pady=(10,0))
#---------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------
# Ikkinchi parametrni kiritish maydoni
stept_label = customtkinter.CTkLabel(row2_col3_frame, text= "stepT", font=("Tahoma", 20, "bold"), text_color="#FFFFFF")
stept_label.grid(row=2, column=0,  padx=(20, 5), pady=(10,0))

#---stept_input mashinani yo'lni bosib o'tishi uchun ketgan vaqtini bo'lish uchun yaratilgan o'zgaruvchi
stept_input = CTkSpinbox(row2_col3_frame,  start_value = 1000, min_value = 0, fg_color='#FFFFFF',
                    button_color="#FCCD25", button_hover_color="#F99E39",button_border_color="",
                    max_value = 20000, step_value = 100, width = 180)

stept_input.grid(row=2, column=1,padx=(0, 20), pady=(10,0))
#---------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------
#Uchinchi parametrni kiritish maydoni

dt_label = customtkinter.CTkLabel(row2_col3_frame, text= "dt", font=("Tahoma", 20, "bold"), text_color="#FFFFFF")
dt_label.grid(row=3, column=0, padx=(20, 5), pady=(10,20))

dt_input = customtkinter.CTkLabel(row2_col3_frame, width=180, height=40, fg_color="#FCCD25",
                                   text = t_input.get() / stept_input.get(), bg_color='#444',
                                   text_color="#000000", corner_radius=5, font=("Tahoma", 20))
dt_input.grid(row=3, column=1, padx=(0, 20), pady=(10,20))
#---------------------------------------------------------------------------------------

#----------------------------------####-------------------------------------------------
#----------------------------------####-------------------------------------------------
#matplotlib chizmasini chiqaramiz.
#Uchinchi qator row3 Frame

row3_frame = customtkinter.CTkFrame(main_frame, fg_color="#FFFFFF", border_color="#7703A7", border_width=2)
row3_frame.pack(fill='both', expand=True,  pady=(20, 20), padx=20)

row3_col1_frame = customtkinter.CTkFrame(row3_frame)
row3_col1_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
row3_col1_frame.columnconfigure(0, weight=1)

row3_col2_frame = customtkinter.CTkFrame(row3_frame)
row3_col2_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5, anchor='n')
row3_col2_frame.columnconfigure(0, weight=1)

row3_col3_frame = customtkinter.CTkFrame(row3_frame, fg_color='transparent')
row3_col3_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
row3_col2_frame.columnconfigure(0, weight=1)
#---------------------------------------------------------------------------------------


L = l_input.get()
step_l = stepl_input.get()
T = t_input.get()
step_t = stept_input.get()
p_0 = p0_input.get() / 1000
p_max = pmax_input.get() / 1000
v_max = vmax_input.get() / 3.6
#funksiyani ishga tushirib ma'lumotlarni undan qaytaramiz.

l, t, p = density(L=L, step_l=step_l , T=T, step_t=step_t, p_0=p_0, p_max=p_max, v_max=v_max)



#----------------------------------####-------------------------------------------------
#----------------------------------####-------------------------------------------------
# Barcha grafiklarni chiqarish
# Birinchi 3d chizma
fig1 = plt.Figure(figsize=(4, 3.6), dpi=100)
main_canvas = FigureCanvasTkAgg(fig1, master=row3_col1_frame)
main_canvas.draw()
ax1 = fig1.add_subplot(111, projection='3d')
ax1.set_title('LWR model')
ax1.set_xlabel('Time (sec)')
ax1.set_ylabel('distance (m)')
ax1.set_zlabel('Density p')
ax1.azim = 40
ax1.dist = 10
ax1.elev = 30
X, Y = np.meshgrid(t, l)
surf = ax1.plot_surface(X, Y, p, cmap='plasma')
main_canvas._tkcanvas.pack(fill='both', expand='True')
#---------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------
# Ikkinchi 2d chizma
fig2 = plt.Figure(figsize=(4, 1.8), dpi=50)
main_canvas2 = FigureCanvasTkAgg(fig2, master=row3_col2_frame)
main_canvas2.draw()
ax2 = fig2.add_subplot(111)
ax2.set_xlabel('distance (m)')
ax2.set_ylabel('density (avt/m)')
ax2.grid(True)
ax2.plot(l[:], p[:, step_t // 6])
ax2.plot(l[:], p[:, step_t // 6 * 2])
ax2.plot(l[:], p[:, step_t // 6 * 3])
ax2.plot(l[:], p[:, step_t // 6 * 4])
ax2.plot(l[:], p[:, step_t // 6 * 5])
ax2.plot(l[:], p[:, step_t // 6 * 6])
main_canvas2._tkcanvas.pack(fill='both', expand='True')
#---------------------------------------------------------------------------------------

# Uchinchi 2d chizma
fig3 = plt.Figure(figsize=(4, 1.8), dpi=50)
main_canvas3 = FigureCanvasTkAgg(fig3, master=row3_col2_frame)
main_canvas3.draw()
ax3 = fig3.add_subplot(111)
ax3.set_xlabel('Time (sec)')
ax3.set_ylabel('density (avt/m)')
ax3.grid(True)
ax3.plot(t[:], p[step_l // 6, :])
ax3.plot(t[:], p[step_l // 6 * 2, :])
ax3.plot(t[:], p[step_l // 6 * 3, :])
ax3.plot(t[:], p[step_l // 6 * 4, :])
ax3.plot(t[:], p[step_l // 6 * 5, :])
ax3.plot(t[:], p[step_l // 6 * 6, :])
main_canvas3._tkcanvas.pack(fill='both', expand='True')
#---------------------------------------------------------------------------------------

#----------------------------------####-------------------------------------------------
#----------------------------------####-------------------------------------------------
# Tugmalarni yaratish

calculate_btn = customtkinter.CTkButton(row3_col3_frame, text="Hisoblash", text_color="#FFFFFF",
                                        font=("Tahoma", 20, 'bold'), height=50, command=update,
                                        fg_color="#7703A7", hover_color="#15078A")
calculate_btn.pack(fill = 'both', expand=True, padx=5, pady=(5,0))
cancle_btn = customtkinter.CTkButton(row3_col3_frame, text="Bekor qilish", text_color="#FFFFFF",
                                     font=("Tahoma", 20, 'bold'),  height=50, command=reset_window,
                                     fg_color="#7703A7", hover_color="#15078A")
cancle_btn.pack(fill = 'both', expand=True, padx=5, pady=5)


app.mainloop()