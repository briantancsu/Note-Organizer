import tkinter as tk
from tkinter.constants import DISABLED, LEFT, RIGHT
from tkinter.scrolledtext import ScrolledText
from typing import Collection
from tkcalendar import Calendar
import tkinter.font as font
import numpy as np
import os
from tkinter import ttk

def generate_time_intervals():
    intervals = []
    for hour in range(24):
        for minute in range(0, 60, 15):
            time_str = f"{hour:02}:{minute:02}"
            intervals.append(time_str)
    return intervals

global chosen_date, data_dict, lates

lates = []
report_hidden = []
if os.path.exists("report.npy"):
    report_hidden = np.load("report.npy",allow_pickle='TRUE').tolist()

master=tk.Tk()
master.title("Note Organizer")
master.config(bg="gray")

height = 900
width = 1400
x = (master.winfo_screenwidth()//2)-(width//2) 
y = (master.winfo_screenheight()//2)-(height//2) 
master.geometry("{}x{}+{}+{}".format(width, height, x, y)) 
master.iconbitmap('logo.ico')
cal_can = tk.Canvas(master, width=600, height=600, bg="black")


from datetime import datetime
year_cur = datetime.today().strftime('%Y')
month_cur = datetime.today().strftime('%m')
date_cur = datetime.today().strftime('%d')

cal = Calendar(cal_can, selectmode = 'day',
               year = int(year_cur), month =int(month_cur),
               day = int(date_cur),width=200, height=400)

month, day, year = map(int, cal.get_date().split('/'))
chosen_date = "d" + str(day) + "m" + str(month) + "y" + str(year)
#print(day, month, 2000+year)
today_rank = day + 100*month + 1000*(2000 + year)
print(chosen_date)

note_can = tk.Canvas(master, width=700, height=200, bg="white")
text = ScrolledText(note_can, width=100, height=100, bg="white")
text.insert('end', "\n\t")
text.window_create('end', window=tk.Label(text, text=datetime.now().strftime("%A, %B %d"), fg="black", 
        bg='white', font=("Calibri", 70)))
text.config(state=DISABLED)

text.pack()

if os.path.exists("data.npy"):
    data_dict = np.load('data.npy',allow_pickle='TRUE').item()
    for dd in data_dict.keys():
        if len(data_dict[dd]) > 0:
            nums = []
            cur_char = ""
            for c in dd[1:]:
                if str(c).isnumeric() : 
                    cur_char += c
                else:
                    nums.append(int(cur_char))
                    cur_char = ""
            nums.append(int("20" + cur_char))
            date_rank = nums[2]*1000 + nums[1]*100 + nums[0]
            #print(dd, nums, date_rank, today_rank)
            if date_rank < today_rank:
                if len(lates) == 0:
                    lates.append((date_rank, dd))
                else:
                    i_d = 0
                    if date_rank > lates[-1][0]:
                        lates.append((date_rank, dd))
                    else:
                        for (dr, k) in lates:
                            if date_rank < dr:
                                lates.insert(i_d, (date_rank, dd))
                                break
    print("bisa", lates)
    cur_items = None
    try:
        cur_items = data_dict[chosen_date]
        print(cur_items)
    except:
        cur_items = None
    text.pack_forget()
    text = ScrolledText(note_can, width=100, height=100, bg="white", wrap='word')
    text.insert('end', "\n\t")
    text.window_create('end', window=tk.Label(text, text=cal.selection_get().strftime("%A, %B %d"), fg="black", 
        bg='white', font=("Calibri", 70)))
    buttons = []
    if cur_items != None:
        for i in range(len(cur_items)):

            cb = tk.Label(text, text=str(cur_items[i][1][0]), fg="black", 
            bg='white', font=("Calibri", 30))
            text.insert('end', "\n\n\t")
            text.window_create('end', window=cb)

            # dt = ScrolledText(text, width=96, height=20, bg="gray", fg="white", wrap='word')
            # dt.insert("end", str(cur_items[i][1]))
            # dt.config(state=DISABLED)
            dt = tk.Label(text, text="More Detail", fg="black", bg="white", font=('underline'), borderwidth=2, relief="groove")
            def test(event, title, det, ur, tv):
                global text
                new_window2 = tk.Toplevel(master)
                new_window2.title(title)
                new_window2.geometry("700x600")
                new_window2.iconbitmap('logo.ico')
                height = 600
                width = 700
                x = (new_window2.winfo_screenwidth()//2)-(width//2) 
                y = (new_window2.winfo_screenheight()//2)-(height//2) 
                new_window2.geometry("{}x{}+{}+{}".format(width, height, x, y)) 
                tk.Label(new_window2, text=title, font=("Calibri", 45)).pack()
                d_txt = tk.Text(new_window2, height = 15,
                        width = 55,
                        fg="black")
                d_txt.insert(tk.END, det)
                d_txt.config(state=DISABLED)
                d_txt.pack(pady=30)
                #.get_date().split('/'))
                #chosen_date_temp_temp = "d" + str(day) + "m" + str(month) + "y" + str(year)
                def fu():
                    new_window2.destroy()
                    new_window3 = tk.Toplevel(master)
                    new_window3.title(title)
                    new_window3.geometry("1100x450")
                    new_window3.iconbitmap('logo.ico')
                    height = 450
                    width = 1100
                    x = (new_window3.winfo_screenwidth()//2)-(width//2) 
                    y = (new_window3.winfo_screenheight()//2)-(height//2) 
                    new_window3.geometry("{}x{}+{}+{}".format(width, height, x, y)) 
                    year_cur = datetime.today().strftime('%Y')
                    month_cur = datetime.today().strftime('%m')
                    date_cur = datetime.today().strftime('%d')

                    cal_temp = Calendar(new_window3, selectmode = 'day',
                                year = int(year_cur), month =int(month_cur),
                                day = int(date_cur),width=200, height=400)

                    large_font = font.Font(size=20)
                    cal_temp.configure(font=large_font)
                    cal_temp.pack(side=LEFT, padx=30)
                    can_w2 = tk.Canvas(new_window3, width=500, height=300)
                    can_w2.pack_propagate(False)

                    title_in = tk.Text(new_window3, height = 1,
                        width = 60,
                        fg="black")
                    title_in.insert(tk.END, title)
                    title_in.pack(pady=10)

                    com_in = tk.Text(new_window3, height = 5,
                        width = 60,
                        fg="black")
                    com_in.insert(tk.END, "Result : ")
                    com_in.pack(pady=10)

                    det_in = tk.Text(new_window3, height = 5,
                        width = 60,
                        fg="black")
                    det_in.insert(tk.END, "Task : ")
                    det_in.pack(pady=10)
                    but_can = tk.Canvas(can_w2, width=500, height=30)
                    def con_but_fu():
                        global text, data_dict
            

                        top = title_in.get("1.0", "end-1c")
                        bot = det_in.get("1.0", "end-1c")
                        if bot == "":
                            new_window2 = tk.Toplevel(master)
                            new_window2.title("error")
                            new_window2.geometry("150x70")
                            new_window2.iconbitmap('logo.ico')
                            height = 70
                            width = 150
                            x = (new_window2.winfo_screenwidth()//2)-(width//2) 
                            y = (new_window2.winfo_screenheight()//2)-(height//2) 
                            new_window2.geometry("{}x{}+{}+{}".format(width, height, x, y)) 
                            tk.Label(new_window2, text="Error\n\nPlease fill the info").pack()
                        else:
                            month, day, year = map(int, cal_temp.get_date().split('/'))
                            chosen_date_temp = "d" + str(day) + "m" + str(month) + "y" + str(year)
                            urgency = 0
                            time_var = None
                            if str(selected_option.get()) == "Top Urgent":#, time_combobox.get())
                                urgency = 1
                            elif str(selected_option.get()) == "Urgent":
                                urgency = 2
                            else:
                                if radio_var.get():
                                    hour_com, min_com = int(time_combobox.get()[0:2]), int(time_combobox.get()[3:])
                                    time_var = (hour_com, min_com)
                                    #print(hour_com, min_com, 4*hour_com + min_com/15)
                                    urgency = 3 + (4*hour_com + min_com/15)
                                else:
                                    urgency = 100
                            print("urgency", urgency)
                            month_t, day_t, year_t = map(int, cal.get_date().split('/'))
                            bot =   det + "\n"  + com_in.get("1.0", "end-1c") + "\n"  + str(day_t) + "/" + str(month_t) + "/" + str(year_t)+"\n\n\n" + bot
                            res = (urgency, (top, bot), time_var)
                            if chosen_date_temp in data_dict:
                                if len(data_dict[chosen_date_temp]) == 0:
                                    data_dict[chosen_date_temp].append(res)
                                else:
                                    if urgency >= data_dict[chosen_date_temp][-1][0] :
                                        data_dict[chosen_date_temp].append(res)
                                    else:
                                        for u in range(len(data_dict[chosen_date_temp])):
                                            if urgency <= data_dict[chosen_date_temp][u][0]:
                                                data_dict[chosen_date_temp].insert(u, res)
                                                break
                            else:
                                data_dict[chosen_date_temp] = [res]
                            new_window3.destroy()
                            date_rank = (2000+year)*1000 + month*100 + day
                            if date_rank < today_rank:
                                if len(lates) == 0:
                                    lates.append((date_rank, chosen_date_temp))
                                else:
                                    i_d = 0
                                    if date_rank > lates[-1][0]:
                                        lates.append((date_rank, chosen_date_temp))
                                    else:
                                        for (dr, k) in lates:
                                            if date_rank < dr:
                                                lates.insert(i_d, (date_rank, chosen_date_temp))
                                                break
                            print(str(int(np.sum([len(data_dict[x[1]]) for x in lates]))))   
                            late_but.config(text="Overdue (" + str(int(np.sum([len(data_dict[x[1]]) for x in lates]))) + ")")
                            check_off(None, (ur, (title, det), tv), chosen_date)
                    tk.Button(but_can, width=28, text="Confirm", command=con_but_fu).pack(side=LEFT, padx=(0, 30))
                    tk.Button(but_can, width=28, text="Cancel", command= lambda: new_window3.destroy()).pack(side=RIGHT, padx=(10, 10))
                    time_intervals = generate_time_intervals()
                    time_can = tk.Canvas(can_w2, width=550)
                    def update_combobox_state():
                        if radio_var.get():
                            time_combobox.config(state="normal")
                        else:
                            time_combobox.config(state="disabled")

                    radio_var = tk.BooleanVar(value=False)  # Default to enabled

                    # Create the Radiobutton widget
                    radio_toggle = tk.Checkbutton(time_can, text="Time-Dependent", variable=radio_var, command=update_combobox_state)
                    #radio_toggle.select()

                    radio_toggle.pack(side=LEFT, pady=10, padx=50)
                    # Create the dropdown (Combobox) and populate it with time intervals
                    time_combobox = ttk.Combobox(time_can, values=time_intervals)
                    time_combobox.config(state="disabled")
                    time_combobox.pack(side=RIGHT, pady=10, padx=50)

                    # Set a default value (optional)
                    time_combobox.set(time_intervals[0])

                    ur_can = tk.Canvas(can_w2, width=550)

                    selected_option = tk.StringVar(value="Top Urgent")

                    radio1 = tk.Radiobutton(ur_can, text="Top Urgent", variable=selected_option, value="Top Urgent")
                    radio2 = tk.Radiobutton(ur_can, text="Urgent", variable=selected_option, value="Urgent")
                    radio3 = tk.Radiobutton(ur_can, text="Normal", variable=selected_option, value="Normal")

                    radio1.grid(row=0, column=0, padx=50, pady=10)
                    radio2.grid(row=0, column=1, padx=40, pady=10)
                    radio3.grid(row=0, column=2, padx=50, pady=10)

                    ur_can.pack(pady=10)

                    
                    time_can.pack(pady=10)
                    but_can.pack(pady=10)

                    can_w2.pack(side=RIGHT)
                tk.Button(new_window2, text="Follow Up", width=20, height=2, command=fu).pack(pady=0)
                def check_off(event, res, date_var):
                    global text
                    print("CHECK OFF", res, res in data_dict[date_var])
                    nums_temp = []
                    cur_char = ''
                    for c in date_var[1:]:
                        if str(c).isnumeric() : 
                            cur_char += c
                        else:
                            nums_temp.append(int(cur_char))
                            cur_char = ""
                    nums_temp.append(int("20" + cur_char))
                    report_hidden.append((datetime.now(), str(nums_temp[0]) + "/" + str(nums_temp[1]) + "/" + str(nums_temp[2]), res[1][0], res[1][1], res[0]))
                    np.save('report.npy', report_hidden)
                    data_dict[date_var].remove(res)
                    date_rank = nums_temp[2]*1000 + nums_temp[1]*100 + nums_temp[0]
                    if date_var in [d for (u, d) in lates] and len(data_dict[date_var]) == 0:
                        lates.remove((date_rank, date_var))
                    late_but.config(text="Overdue (" + str(int(np.sum([len(data_dict[x[1]]) for x in lates]))) + ")")
                    grad_date()
                    new_window2.destroy()
                    save_command()
                    
                def co_con(event, r_temp, c_temp):
                    new_window2.destroy()
                    new_window8 = tk.Toplevel(master)
                    new_window8.title("error")
                    new_window8.geometry("300x200")
                    new_window8.iconbitmap('logo.ico')
                    height = 200
                    width = 300
                    x = (new_window8.winfo_screenwidth()//2)-(width//2) 
                    y = (new_window8.winfo_screenheight()//2)-(height//2) 
                    new_window8.geometry("{}x{}+{}+{}".format(width, height, x, y)) 
                    def con_and_can(event, r_te, d_te):
                        new_window8.destroy()
                        check_off(None, r_te, d_te)

                    tk.Button(new_window8, text="Confirm", width=20, height=2, command=lambda event=None, res=r_temp, cd=c_temp :con_and_can(event, res, cd)).pack(pady=25)
                    tk.Button(new_window8, text="Cancel", width=20, height=2, command=lambda: new_window8.destroy()).pack(pady=30)
                tk.Button(new_window2, text="Check Off", width=20, height=2, command=lambda event=None, res=(ur, (title, det), tv), cd=chosen_date :co_con(event, res, cd)).pack(pady=30)
                tk.Button(new_window2, text="Exit", width=20, height=2, command=lambda: new_window2.destroy()).pack(pady=0)
            #dt.bind("<Button-1>", lambda event, arg=str(cur_items[i][0]), arg2=str(cur_items[i][1]), arg3 = cur_items[i][0]: test(event, arg, arg2, arg3))
            dt.bind("<Button-1>", lambda event, arg=str(cur_items[i][1][0]), arg2=str(cur_items[i][1][1]), arg3=cur_items[i][0], arg4=cur_items[i][2]: test(event, arg, arg2, arg3, arg4))
            text.insert('end', '\n\t')
            if cur_items[i][0] == 1:
                text.window_create(tk.END, window=tk.Label(text, text="Top Urgent", fg="Red", 
            bg='white', font=("Calibri", 15, 'bold')))
                text.insert('end', '\n\t')
            elif cur_items[i][0] == 2:
                text.window_create(tk.END, window=tk.Label(text, text="Urgent", fg="Blue", 
            bg='white', font=("Calibri", 15, 'bold')))
                text.insert('end', '\n\t')
            
            elif cur_items[i][2] != None:
                text.window_create(tk.END, window=tk.Label(text, text="Scheduled At " + '%02d' % cur_items[i][2][0] + ":" + '%02d' % cur_items[i][2][1], fg="black", 
            bg='white', font=("Calibri", 15)))
                text.insert('end', '\n\t')
            text.insert('end', '\n\t')
            text.window_create(tk.END, window=dt)
            text.insert('end', '\n')
    text.config(state=DISABLED)
    text.pack()
else:
    data_dict = {}

def find_center(x, y, w, h):
    return x + w//2, y + h//2

def find_center_rect(x1, x2, y1, y2):
    return x1 + (x2 - x1) // 2, y1 + (y2 - y1) // 2 + 50



#chosen_date = (int(date_cur), int(month_cur), int(year_cur))



large_font = font.Font(size=14)
cal.configure(font=large_font)
cal.pack(padx=20, pady=20, expand=True, fill=tk.BOTH)
 
cal.pack()

date = tk.Label(cal_can, text = "Selected Date is: " + month_cur 
+ '/' + date_cur + "/" + year_cur , bg="black")
date.pack(pady = 20)

def grad_date():
    global chosen_date, text
    date.config(text = "Selected Date is: " + cal.get_date())
    month, day, year = map(int, cal.get_date().split('/'))
    chosen_date = "d" + str(day) + "m" + str(month) + "y" + str(year)
    try:
        cur_items = data_dict[chosen_date]
        print(cur_items)
        text.pack_forget()
        text = ScrolledText(note_can, width=100, height=100, bg="white", wrap='word')
        text.insert('end', "\n\t")
        text.window_create('end', window=tk.Label(text, text=cal.selection_get().strftime("%A, %B %d"), fg="black", 
            bg='white', font=("Calibri", 70)))
        buttons = []

        for i in range(len(cur_items)):
            print("now", tuple(cur_items[i])[1])
            cb = tk.Label(text, text=str(cur_items[i][1][0]), fg="black", 
            bg='white', font=("Calibri", 30))
            text.insert('end', "\n\n\t")
            text.window_create('end', window=cb)

            # dt = ScrolledText(text, width=96, height=20, bg="gray", fg="white", wrap='word')
            # dt.insert("end", str(cur_items[i][1]))
            # dt.config(state=DISABLED)
            dt = tk.Label(text, text="More Detail", fg="black", bg="white", font=('underline'), borderwidth=2, relief="groove")
            def test(event, title, det, ur, tv):
                global text
                new_window2 = tk.Toplevel(master)
                new_window2.title(title)
                new_window2.geometry("700x600")
                new_window2.iconbitmap('logo.ico')
                height = 600
                width = 700
                x = (new_window2.winfo_screenwidth()//2)-(width//2) 
                y = (new_window2.winfo_screenheight()//2)-(height//2) 
                new_window2.geometry("{}x{}+{}+{}".format(width, height, x, y)) 
                tk.Label(new_window2, text=title, font=("Calibri", 45)).pack()
                d_txt = tk.Text(new_window2, height = 15,
                        width = 55,
                        fg="black")
                d_txt.insert(tk.END, det)
                d_txt.config(state=DISABLED)
                d_txt.pack(pady=30)
                #month, day, year = map(int, cal.get_date().split('/'))
                #chosen_date_temp_temp = "d" + str(day) + "m" + str(month) + "y" + str(year)
                def fu():
                    new_window2.destroy()
                    new_window3 = tk.Toplevel(master)
                    new_window3.title(title)
                    new_window3.geometry("1100x450")
                    new_window3.iconbitmap('logo.ico')
                    height = 450
                    width = 1100
                    x = (new_window3.winfo_screenwidth()//2)-(width//2) 
                    y = (new_window3.winfo_screenheight()//2)-(height//2) 
                    new_window3.geometry("{}x{}+{}+{}".format(width, height, x, y)) 
                    year_cur = datetime.today().strftime('%Y')
                    month_cur = datetime.today().strftime('%m')
                    date_cur = datetime.today().strftime('%d')

                    cal_temp = Calendar(new_window3, selectmode = 'day',
                                year = int(year_cur), month =int(month_cur),
                                day = int(date_cur),width=200, height=400)

                    #month, day, year = map(int, cal_temp.get_date().split('/'))
                    #chosen_date_temp_temp = "d" + str(day) + "m" + str(month) + "y" + str(year)

                    large_font = font.Font(size=20)
                    cal_temp.configure(font=large_font)
                    cal_temp.pack(side=LEFT, padx=30)
                    can_w2 = tk.Canvas(new_window3, width=500, height=300)
                    can_w2.pack_propagate(False)

                    title_in = tk.Text(new_window3, height = 1,
                        width = 60,
                        fg="black")
                    title_in.insert(tk.END, title)
                    title_in.pack(pady=10)

                    com_in = tk.Text(new_window3, height = 5,
                        width = 60,
                        fg="black")
                    com_in.insert(tk.END, "Result : ")
                    com_in.pack(pady=10)

                    det_in = tk.Text(new_window3, height = 5,
                        width = 60,
                        fg="black")
                    det_in.insert(tk.END, "Task : ")
                    det_in.pack(pady=10)
                    but_can = tk.Canvas(can_w2, width=500, height=30)
                    def con_but_fu():
                        global text, data_dict
        

                        top = title_in.get("1.0", "end-1c")
                        bot = det_in.get("1.0", "end-1c")
                        if bot == "":
                            new_window2 = tk.Toplevel(master)
                            new_window2.title("error")
                            new_window2.geometry("150x70")
                            new_window2.iconbitmap('logo.ico')
                            height = 70
                            width = 150
                            x = (new_window2.winfo_screenwidth()//2)-(width//2) 
                            y = (new_window2.winfo_screenheight()//2)-(height//2) 
                            new_window2.geometry("{}x{}+{}+{}".format(width, height, x, y)) 
                            tk.Label(new_window2, text="Error\n\nPlease fill the info").pack()
                        else:
                            month, day, year = map(int, cal_temp.get_date().split('/'))
                            chosen_date_temp = "d" + str(day) + "m" + str(month) + "y" + str(year)
                            urgency = 0
                            time_var = None
                            if str(selected_option.get()) == "Top Urgent":#, time_combobox.get())
                                urgency = 1
                            elif str(selected_option.get()) == "Urgent":
                                urgency = 2
                            else:
                                if radio_var.get():
                                    hour_com, min_com = int(time_combobox.get()[0:2]), int(time_combobox.get()[3:])
                                    time_var = (hour_com, min_com)
                                    #print(hour_com, min_com, 4*hour_com + min_com/15)
                                    urgency = 3 + (4*hour_com + min_com/15)
                                else:
                                    urgency = 100
                            print("urgency", urgency, )
                            month_t, day_t, year_t = map(int, cal.get_date().split('/'))
                            bot =   det + "\n"  + com_in.get("1.0", "end-1c") + "\n"  + str(day_t) + "/" + str(month_t) + "/" + str(year_t)+"\n\n\n" + bot
                            res = (urgency, (top, bot), time_var)
                            if chosen_date_temp in data_dict:
                                if len(data_dict[chosen_date_temp]) == 0:
                                    data_dict[chosen_date_temp].append(res)
                                else:
                                    if urgency >= data_dict[chosen_date_temp][-1][0] :
                                        data_dict[chosen_date_temp].append(res)
                                    else:
                                        for u in range(len(data_dict[chosen_date_temp])):
                                            if urgency <= data_dict[chosen_date_temp][u][0]:
                                                data_dict[chosen_date_temp].insert(u, res)
                                                break
                            else:
                                data_dict[chosen_date_temp] = [res]
                            date_rank = (2000+year)*1000 + month*100 + day
                            if date_rank < today_rank:
                                if len(lates) == 0:
                                    lates.append((date_rank, chosen_date_temp))
                                else:
                                    i_d = 0
                                    if date_rank > lates[-1][0]:
                                        lates.append((date_rank, chosen_date_temp))
                                    else:
                                        for (dr, k) in lates:
                                            if date_rank < dr:
                                                lates.insert(i_d, (date_rank, chosen_date_temp))
                                                break
                            print(str(int(np.sum([len(data_dict[x[1]]) for x in lates]))))   
                            late_but.config(text="Overdue (" + str(int(np.sum([len(data_dict[x[1]]) for x in lates]))) + ")")
                            check_off(None, (ur, (title, det), tv), chosen_date)
                            new_window3.destroy()
                            
                    tk.Button(but_can, width=28, text="Confirm", command=con_but_fu).pack(side=LEFT, padx=(0, 30))
                    tk.Button(but_can, width=28, text="Cancel", command= lambda: new_window3.destroy()).pack(side=RIGHT, padx=10)
                    time_intervals = generate_time_intervals()
                    time_can = tk.Canvas(can_w2, width=550)
                    def update_combobox_state():
                        if radio_var.get():
                            time_combobox.config(state="normal")
                        else:
                            time_combobox.config(state="disabled")

                    radio_var = tk.BooleanVar(value=False)  # Default to enabled

                    # Create the Radiobutton widget
                    radio_toggle = tk.Checkbutton(time_can, text="Time-Dependent", variable=radio_var, command=update_combobox_state)
                    #radio_toggle.select()

                    radio_toggle.pack(side=LEFT, pady=10, padx=50)
                    # Create the dropdown (Combobox) and populate it with time intervals
                    time_combobox = ttk.Combobox(time_can, values=time_intervals)
                    time_combobox.config(state="disabled")
                    time_combobox.pack(side=RIGHT, pady=10, padx=50)

                    # Set a default value (optional)
                    time_combobox.set(time_intervals[0])

                    ur_can = tk.Canvas(can_w2, width=550)

                    selected_option = tk.StringVar(value="Top Urgent")

                    radio1 = tk.Radiobutton(ur_can, text="Top Urgent", variable=selected_option, value="Top Urgent")
                    radio2 = tk.Radiobutton(ur_can, text="Urgent", variable=selected_option, value="Urgent")
                    radio3 = tk.Radiobutton(ur_can, text="Normal", variable=selected_option, value="Normal")

                    radio1.grid(row=0, column=0, padx=50, pady=10)
                    radio2.grid(row=0, column=1, padx=40, pady=10)
                    radio3.grid(row=0, column=2, padx=50, pady=10)

                    ur_can.pack(pady=10)

                    
                    time_can.pack(pady=10)
                    but_can.pack(pady=10)

                    can_w2.pack(side=RIGHT)
                tk.Button(new_window2, text="Follow Up", width=20, height=2, command=fu).pack(pady=0)
                def check_off(event, res, date_var):
                    global text
                    print("CHECK OFF", res, res in data_dict[date_var])
                    nums_temp = []
                    cur_char = ""
                    for c in date_var[1:]:
                        if str(c).isnumeric() : 
                            cur_char += c
                        else:
                            nums_temp.append(int(cur_char))
                            cur_char = ""
                    nums_temp.append(int("20" + cur_char))
                    report_hidden.append((datetime.now(), str(nums_temp[0]) + "/" + str(nums_temp[1]) + "/" + str(nums_temp[2]), res[1][0], res[1][1], res[0]))
                    np.save('report.npy', report_hidden)
                    data_dict[date_var].remove(res)
                    date_rank = nums_temp[2]*1000 + nums_temp[1]*100 + nums_temp[0]
                    if date_var in [d for (u, d) in lates] and len(data_dict[date_var]) == 0:
                        lates.remove((date_rank, date_var))
                    late_but.config(text="Overdue (" + str(int(np.sum([len(data_dict[x[1]]) for x in lates]))) + ")")
                    grad_date()
                    new_window2.destroy()
                    save_command()
                def co_con(event, r_temp, c_temp):
                    new_window2.destroy()
                    new_window8 = tk.Toplevel(master)
                    new_window8.title("Confirm Check Off")
                    new_window8.geometry("300x200")
                    new_window8.iconbitmap('logo.ico')
                    height = 200
                    width = 300
                    x = (new_window8.winfo_screenwidth()//2)-(width//2) 
                    y = (new_window8.winfo_screenheight()//2)-(height//2) 
                    new_window8.geometry("{}x{}+{}+{}".format(width, height, x, y)) 
                    print("SINI", r_temp in data_dict[c_temp], r_temp, data_dict[c_temp])
                    def con_and_can(event, r_te, d_te):
                        new_window8.destroy()
                        check_off(None, r_te, d_te)

                    tk.Button(new_window8, text="Confirm", width=20, height=2, command=lambda event=None, res=r_temp, cd=c_temp :con_and_can(event, res, cd)).pack(pady=25)
                    tk.Button(new_window8, text="Cancel", width=20, height=2, command=lambda: new_window8.destroy()).pack(pady=30)
                tk.Button(new_window2, text="Check Off", width=20, height=2, command=lambda event=None, res=(ur, (title, det), tv), cd=chosen_date :co_con(event, res, cd)).pack(pady=20)
                tk.Button(new_window2, text="Exit", width=20, height=2, command=new_window2.destroy).pack(pady=0)
            dt.bind("<Button-1>", lambda event, arg=str(cur_items[i][1][0]), arg2=str(cur_items[i][1][1]), arg3=cur_items[i][0], arg4=cur_items[i][2]: test(event, arg, arg2, arg3, arg4))

            text.insert('end', '\n\t')
            if cur_items[i][0] == 1:
                text.window_create(tk.END, window=tk.Label(text, text="Top Urgent", fg="Red", 
            bg='white', font=("Calibri", 15, 'bold')))
                text.insert('end', '\n')
            elif cur_items[i][0] == 2:
                text.window_create(tk.END, window=tk.Label(text, text="Urgent", fg="Blue", 
            bg='white', font=("Calibri", 15, 'bold')))
                text.insert('end', '\n')
            if cur_items[i][2] != None:
                text.window_create(tk.END, window=tk.Label(text, text="Scheduled At " + '%02d' % cur_items[i][2][0] + ":" + '%02d' % cur_items[i][2][1], fg="black", 
            bg='white', font=("Calibri", 15)))
                text.insert('end', '\n')
            text.insert('end', '\n\t')
            text.window_create(tk.END, window=dt)
            text.insert('end', '\n')
        text.config(state=DISABLED)   
        text.pack()
    except:
        print("None")

        text.pack_forget()
        text = ScrolledText(note_can, width=100, height=100, bg="white", wrap='word')
        text.insert('end', "\n\t")
        text.window_create('end', window=tk.Label(text, text=cal.selection_get().strftime("%A, %B %d"), fg="black", 
            bg='white', font=("Calibri", 70)))
        text.config(state=DISABLED)
        text.pack()
 
# Add Button and Label
tk.Button(cal_can, text = "Get Date",
       command = grad_date).pack(pady = 20)

center_x = (0 + 650) / 2

cal_can.place(x=0, y=0)

cal_can.update_idletasks()

canvas_width = cal_can.winfo_width()
canvas_height = cal_can.winfo_height()

canvas_x = center_x - (canvas_width / 2)

cal_can.place(x=canvas_x, y=30)

def save_command():
    global data_dict
    np.save('data.npy', data_dict)

def gen_rep():
    import os
    import numpy as np
    import pandas as pd
    if os.path.exists("report.npy"):
        data = {"Time" : [], "Scheduled Date" : [], "Title" : [], "Detail" : [], "Urgency" : []}
        print(np.load("report.npy",allow_pickle='TRUE'))
        for (t1, sd, t2, d, u) in np.load("report.npy",allow_pickle='TRUE'):
            data["Time"].append("At " + str(t1))
            data["Scheduled Date"].append("At " + str(sd))
            data["Title"].append(t2)
            data["Detail"].append(d)
            rank = "None"
            if u == 1:
                rank = "Top Urgent"
            elif u == 2:
                rank = "Urgent"
            elif u == 100:
                rank = "Normal"
            else:
                hour = (u-3) //4
                minutes = ((u - 3) % 4)*15
                rank = "Scheduled At " + '%02d' % hour + ":" + '%02d' % minutes
            data["Urgency"].append(rank)
        pd.DataFrame(data=data).to_csv("Report.csv")

rep_but = tk.Button(master, text="Generate Report", width=35, height=3, command=gen_rep)
rep_but.place(x=325-20, y=500)

rep_but.update_idletasks()

canvas_width = rep_but.winfo_width()
canvas_height = rep_but.winfo_height()

but_x = center_x - (canvas_width / 2)

rep_but.place(x=but_x, y=500-0)



def open_new_window():
    global text, data_dict
    new_window3 = tk.Toplevel(master)
    new_window3.title("Insert")
    new_window3.geometry("1100x400")
    new_window3.iconbitmap('logo.ico')
    height = 450
    width = 1100
    x = (new_window3.winfo_screenwidth()//2)-(width//2) 
    y = (new_window3.winfo_screenheight()//2)-(height//2) 
    new_window3.geometry("{}x{}+{}+{}".format(width, height, x, y)) 
    year_cur = datetime.today().strftime('%Y')
    month_cur = datetime.today().strftime('%m')
    date_cur = datetime.today().strftime('%d')

    cal_temp = Calendar(new_window3, selectmode = 'day',
                year = int(year_cur), month =int(month_cur),
                day = int(date_cur),width=200, height=400)

    large_font = font.Font(size=20)
    cal_temp.configure(font=large_font)
    cal_temp.pack(side=LEFT, padx=30)
    can_w2 = tk.Canvas(new_window3, width=550, height=400)
    can_w2.pack_propagate(False)

    title_in = tk.Text(new_window3, height = 1,
        width = 60,
        fg="black")
    title_in.pack(pady=10)

    det_in = tk.Text(new_window3, height = 10,
        width = 60,
        fg="black")
    det_in.pack(pady=10)
    but_can = tk.Canvas(can_w2, width=500, height=30)
    def con_but_fu():
        global text, data_dict
        

        top = title_in.get("1.0", "end-1c")
        bot = det_in.get("1.0", "end-1c")
        if bot == "":
            new_window2 = tk.Toplevel(master)
            new_window2.title("error")
            new_window2.geometry("150x70")
            new_window2.iconbitmap('logo.ico')
            height = 70
            width = 150
            x = (new_window2.winfo_screenwidth()//2)-(width//2) 
            y = (new_window2.winfo_screenheight()//2)-(height//2) 
            new_window2.geometry("{}x{}+{}+{}".format(width, height, x, y)) 
            tk.Label(new_window2, text="Error\n\nPlease fill the info").pack()
        else:
            month, day, year = map(int, cal_temp.get_date().split('/'))
            chosen_date_temp = "d" + str(day) + "m" + str(month) + "y" + str(year)
            urgency = 0
            time_var = None
            if str(selected_option.get()) == "Top Urgent":#, time_combobox.get())
                urgency = 1
            elif str(selected_option.get()) == "Urgent":
                urgency = 2
            else:
                if radio_var.get():
                    hour_com, min_com = int(time_combobox.get()[0:2]), int(time_combobox.get()[3:])
                    time_var = (hour_com, min_com)
                    #print(hour_com, min_com, 4*hour_com + min_com/15)
                    urgency = 3 + (4*hour_com + min_com/15)
                else:
                    urgency = 100
            print("urgency", urgency)
            res = (urgency, (top, bot), time_var)
            
            if chosen_date_temp in data_dict:
                if len(data_dict[chosen_date_temp]) == 0:
                    data_dict[chosen_date_temp].append(res)
                else:
                    if urgency >= data_dict[chosen_date_temp][-1][0] :
                        data_dict[chosen_date_temp].append(res)
                    else:
                        for u in range(len(data_dict[chosen_date_temp])):
                            if urgency <= data_dict[chosen_date_temp][u][0]:
                                data_dict[chosen_date_temp].insert(u, res)
                                break
            else:
                data_dict[chosen_date_temp] = [res]
            date_rank = (2000+year)*1000 + month*100 + day
            if date_rank < today_rank:
                if len(lates) == 0:
                    lates.append((date_rank, chosen_date_temp))
                else:
                    i_d = 0
                    if date_rank > lates[-1][0]:
                        lates.append((date_rank, chosen_date_temp))
                    else:
                        for (dr, k) in lates:
                            if date_rank < dr:
                                lates.insert(i_d, (date_rank, chosen_date_temp))
                                break
            print(str(int(np.sum([len(data_dict[x[1]]) for x in lates]))))   
            late_but.config(text="Overdue (" + str(int(np.sum([len(data_dict[x[1]]) for x in lates]))) + ")")
            new_window3.destroy()
            print("now", data_dict[chosen_date_temp])
            grad_date()
            save_command()
    tk.Button(but_can, width=28, text="Confirm", command=con_but_fu).pack(side=LEFT, padx=(0,30))
    tk.Button(but_can, width=28, text="Cancel", command= lambda: new_window3.destroy()).pack(side=RIGHT, padx=(30, 0))
    time_intervals = generate_time_intervals()
    time_can = tk.Canvas(can_w2, width=550)
    def update_combobox_state():
        if radio_var.get():
            time_combobox.config(state="normal")
        else:
            time_combobox.config(state="disabled")

    radio_var = tk.BooleanVar(value=False)  # Default to enabled

    # Create the Radiobutton widget
    radio_toggle = tk.Checkbutton(time_can, text="Time-Dependent", variable=radio_var, command=update_combobox_state)
    #radio_toggle.select()

    radio_toggle.pack(side=LEFT, pady=10, padx=50)
    # Create the dropdown (Combobox) and populate it with time intervals
    time_combobox = ttk.Combobox(time_can, values=time_intervals)
    time_combobox.config(state="disabled")
    time_combobox.pack(side=RIGHT, pady=10, padx=50)

    # Set a default value (optional)
    time_combobox.set(time_intervals[0])

    ur_can = tk.Canvas(can_w2, width=550)

    selected_option = tk.StringVar(value="Top Urgent")

    radio1 = tk.Radiobutton(ur_can, text="Top Urgent", variable=selected_option, value="Top Urgent")
    radio2 = tk.Radiobutton(ur_can, text="Urgent", variable=selected_option, value="Urgent")
    radio3 = tk.Radiobutton(ur_can, text="Normal", variable=selected_option, value="Normal")

    radio1.grid(row=0, column=0, padx=50, pady=10)
    radio2.grid(row=0, column=1, padx=40, pady=10)
    radio3.grid(row=0, column=2, padx=50, pady=10)

    ur_can.pack(pady=10)

    
    time_can.pack(pady=10)
    but_can.pack(pady=10)
    can_w2.pack(side=RIGHT)


    
    
    
 

in_but = tk.Button(master, text="New Reminder", width=35, height=3, command=open_new_window)
in_but.place(x=325-20, y=500)

in_but.update_idletasks()

canvas_width = in_but.winfo_width()
canvas_height = in_but.winfo_height()

but_x = center_x - (canvas_width / 2)

in_but.place(x=but_x, y=600-0)

def late_fun():
    if len(lates) > 0:
        new_window5 = tk.Toplevel(master)
        new_window5.title("Overdue")
        new_window5.geometry("700x750")
        new_window5.iconbitmap('logo.ico')
        height = 750
        width = 700
        x = (new_window5.winfo_screenwidth()//2)-(width//2) 
        y = (new_window5.winfo_screenheight()//2)-(height//2) 
        new_window5.geometry("{}x{}+{}+{}".format(width, height, x, y)) 
        tk.Label(new_window5, text="Overdue (" + str(np.sum([len(data_dict[x[1]]) for x in lates])) + ")", font=("Calibri", 50)).pack(pady=10)
        bgcanvas = tk.Canvas(new_window5, bg="white")
        text = ScrolledText(bgcanvas, width=70, height=35, bg="white", wrap=tk.NONE, bd=0, highlightthickness=0)
        text.config(wrap=tk.NONE)
        text.insert('end', "\n\t")
        for (useless, dates) in lates:
            nums = []
            cur_char = ""
            for c in dates[1:]:
                if str(c).isnumeric() : 
                    cur_char += c
                else:
                    nums.append(int(cur_char))
                    cur_char = ""
            nums.append(int("20" + cur_char))
            import datetime
            ans = datetime.date(nums[2], nums[1], nums[0])
            print(ans.strftime("%A, %B %d"), data_dict[dates])
            text.window_create(tk.END, window=tk.Label(text, text=ans.strftime("%A, %B %d"), fg="black", 
            bg='white', font=("Calibri", 25, 'bold')))

            cur_items = data_dict[dates]

            for i in range(len(cur_items)):
                #print("now", tuple(cur_items[i])[1])
                cb = tk.Label(text, text=str(cur_items[i][1][0]), fg="black", 
                bg='white', font=("Calibri", 25))
                text.insert('end', "\n\t")
                text.window_create('end', window=cb)

                # dt = ScrolledText(text, width=96, height=20, bg="gray", fg="white", wrap='word')
                # dt.insert("end", str(cur_items[i][1]))
                # dt.config(state=DISABLED)
                dt = tk.Label(text, text="More Detail", fg="black", bg="white", font=('underline'), borderwidth=2, relief="groove")
                def test(event, title, det, ur, tv, date_temp, date_pure):
                    global text
                    new_window5.destroy()
                    new_window2 = tk.Toplevel(master)
                    new_window2.title(title)
                    new_window2.geometry("700x600")
                    new_window2.iconbitmap('logo.ico')
                    height = 600
                    width = 700
                    x = (new_window2.winfo_screenwidth()//2)-(width//2) 
                    y = (new_window2.winfo_screenheight()//2)-(height//2) 
                    new_window2.geometry("{}x{}+{}+{}".format(width, height, x, y)) 
                    tk.Label(new_window2, text=title, font=("Calibri", 45)).pack()
                    d_txt = tk.Text(new_window2, height = 15,
                            width = 55,
                            fg="black")
                    d_txt.insert(tk.END, det)
                    d_txt.config(state=DISABLED)
                    d_txt.pack(pady=30)
                    #month, day, year = map(int, cal.get_date().split('/'))
                    #chosen_date_temp_temp = "d" + str(day) + "m" + str(month) + "y" + str(year)
                    def fu():
                        new_window2.destroy()
                        new_window3 = tk.Toplevel(master)
                        new_window3.title(title)
                        new_window3.geometry("1100x450")
                        new_window3.iconbitmap('logo.ico')
                        height = 450
                        width = 1100
                        x = (new_window3.winfo_screenwidth()//2)-(width//2) 
                        y = (new_window3.winfo_screenheight()//2)-(height//2) 
                        new_window3.geometry("{}x{}+{}+{}".format(width, height, x, y)) 
                        import datetime
                        year_cur = datetime.date.today().strftime('%Y')
                        month_cur = datetime.date.today().strftime('%m')
                        date_cur = datetime.date.today().strftime('%d')

                        cal_temp = Calendar(new_window3, selectmode = 'day',
                                    year = int(year_cur), month =int(month_cur),
                                    day = int(date_cur),width=200, height=400)

                        #month, day, year = map(int, cal_temp.get_date().split('/'))
                        #chosen_date_temp_temp = "d" + str(day) + "m" + str(month) + "y" + str(year)

                        large_font = font.Font(size=20)
                        cal_temp.configure(font=large_font)
                        cal_temp.pack(side=LEFT, padx=30)
                        can_w2 = tk.Canvas(new_window3, width=500, height=300)
                        can_w2.pack_propagate(False)

                        title_in = tk.Text(new_window3, height = 1,
                            width = 60,
                            fg="black")
                        title_in.insert(tk.END, title)
                        title_in.pack(pady=10)

                        com_in = tk.Text(new_window3, height = 5,
                            width = 60,
                            fg="black")
                        com_in.insert(tk.END, "Result : ")
                        com_in.pack(pady=10)

                        det_in = tk.Text(new_window3, height = 5,
                            width = 60,
                            fg="black")
                        det_in.insert(tk.END, "Task : ")
                        det_in.pack(pady=10)
                        but_can = tk.Canvas(can_w2, width=500, height=30)
                        def con_but_fu():
                            global text, data_dict
            

                            top = title_in.get("1.0", "end-1c")
                            bot = det_in.get("1.0", "end-1c")
                            if bot == "":
                                new_window2 = tk.Toplevel(master)
                                new_window2.title("error")
                                new_window2.geometry("150x70")
                                new_window2.iconbitmap('logo.ico')
                                height = 70
                                width = 150
                                x = (new_window2.winfo_screenwidth()//2)-(width//2) 
                                y = (new_window2.winfo_screenheight()//2)-(height//2) 
                                new_window2.geometry("{}x{}+{}+{}".format(width, height, x, y)) 
                                tk.Label(new_window2, text="Error\n\nPlease fill the info").pack()
                            else:
                                month, day, year = map(int, cal_temp.get_date().split('/'))
                                chosen_date_temp = "d" + str(day) + "m" + str(month) + "y" + str(year)
                                urgency = 0
                                time_var = None
                                if str(selected_option.get()) == "Top Urgent":#, time_combobox.get())
                                    urgency = 1
                                elif str(selected_option.get()) == "Urgent":
                                    urgency = 2
                                else:
                                    if radio_var.get():
                                        hour_com, min_com = int(time_combobox.get()[0:2]), int(time_combobox.get()[3:])
                                        time_var = (hour_com, min_com)
                                        #print(hour_com, min_com, 4*hour_com + min_com/15)
                                        urgency = 3 + (4*hour_com + min_com/15)
                                    else:
                                        urgency = 100
                                print("urgency", urgency, )
                                month_t, day_t, year_t = date_pure[1], date_pure[0], date_pure[2]
                                bot =   det + "\n"  + com_in.get("1.0", "end-1c") + "\n"  + str(day_t) + "/" + str(month_t) + "/" + str(year_t)+"\n\n\n" + bot
                                res = (urgency, (top, bot), time_var)
                                if chosen_date_temp in data_dict:
                                    if len(data_dict[chosen_date_temp]) == 0:
                                        data_dict[chosen_date_temp].append(res)
                                    else:
                                        if urgency >= data_dict[chosen_date_temp][-1][0] :
                                            data_dict[chosen_date_temp].append(res)
                                        else:
                                            for u in range(len(data_dict[chosen_date_temp])):
                                                if urgency <= data_dict[chosen_date_temp][u][0]:
                                                    data_dict[chosen_date_temp].insert(u, res)
                                                    break
                                else:
                                    data_dict[chosen_date_temp] = [res]
                                date_rank = (2000+year)*1000 + month*100 + day
                                if date_rank < today_rank:
                                    if len(lates) == 0:
                                        lates.append((date_rank, chosen_date_temp))
                                    else:
                                        i_d = 0
                                        if date_rank > lates[-1][0]:
                                            lates.append((date_rank, chosen_date_temp))
                                        else:
                                            for (dr, k) in lates:
                                                if date_rank < dr:
                                                    lates.insert(i_d, (date_rank, chosen_date_temp))
                                                    break
                                print(str(int(np.sum([len(data_dict[x[1]]) for x in lates]))))   
                                late_but.config(text="Overdue (" + str(int(np.sum([len(data_dict[x[1]]) for x in lates]))) + ")")
                                check_off(None, (ur, (title, det), tv), date_temp)
                                new_window3.destroy()
                                
                        tk.Button(but_can, width=28, text="Confirm", command=con_but_fu).pack(side=LEFT, padx=(0, 30))
                        tk.Button(but_can, width=28, text="Cancel", command= lambda: new_window3.destroy()).pack(side=RIGHT, padx=(10,10))
                        time_intervals = generate_time_intervals()
                        time_can = tk.Canvas(can_w2, width=550)
                        def update_combobox_state():
                            if radio_var.get():
                                time_combobox.config(state="normal")
                            else:
                                time_combobox.config(state="disabled")

                        radio_var = tk.BooleanVar(value=False)  # Default to enabled

                        # Create the Radiobutton widget
                        radio_toggle = tk.Checkbutton(time_can, text="Time-Dependent", variable=radio_var, command=update_combobox_state)
                        #radio_toggle.select()

                        radio_toggle.pack(side=LEFT, pady=10, padx=50)
                        # Create the dropdown (Combobox) and populate it with time intervals
                        time_combobox = ttk.Combobox(time_can, values=time_intervals)
                        time_combobox.config(state="disabled")
                        time_combobox.pack(side=RIGHT, pady=10, padx=50)

                        # Set a default value (optional)
                        time_combobox.set(time_intervals[0])

                        ur_can = tk.Canvas(can_w2, width=550)

                        selected_option = tk.StringVar(value="Top Urgent")

                        radio1 = tk.Radiobutton(ur_can, text="Top Urgent", variable=selected_option, value="Top Urgent")
                        radio2 = tk.Radiobutton(ur_can, text="Urgent", variable=selected_option, value="Urgent")
                        radio3 = tk.Radiobutton(ur_can, text="Normal", variable=selected_option, value="Normal")

                        radio1.grid(row=0, column=0, padx=50, pady=10)
                        radio2.grid(row=0, column=1, padx=40, pady=10)
                        radio3.grid(row=0, column=2, padx=50, pady=10)

                        ur_can.pack(pady=10)

                        
                        time_can.pack(pady=10)
                        but_can.pack(pady=10)

                        can_w2.pack(side=RIGHT)
                    tk.Button(new_window2, text="Follow Up", width=20, height=2, command=fu).pack(pady=0)
                    def check_off(event, res, date_var):
                        global text
                        new_window5.destroy()
                        print("CHECK OFF", res, date_var , res in data_dict[date_var])
                        report_hidden.append((datetime.datetime.today(), str(date_pure[0]) + "/" + str(date_pure[1]) + "/" + str(date_pure[2]), res[1][0], res[1][1], res[0]))
                        np.save('report.npy', report_hidden)
                        data_dict[date_var].remove(res)
                        if date_var in [d for (u, d) in lates] and len(data_dict[date_var]) == 0:
                            lates.remove((date_pure[0] + date_pure[1]*100 + date_pure[2]*1000, date_var))
                        late_but.config(text="Overdue (" + str(int(np.sum([len(data_dict[x[1]]) for x in lates]))) + ")")
                        new_window2.destroy()
                        grad_date()
                        save_command()
                    def co_con(event, r_temp, c_temp):
                        new_window2.destroy()
                        new_window8 = tk.Toplevel(master)
                        new_window8.title("error")
                        new_window8.geometry("300x200")
                        new_window8.iconbitmap('logo.ico')
                        height = 200
                        width = 300
                        x = (new_window8.winfo_screenwidth()//2)-(width//2) 
                        y = (new_window8.winfo_screenheight()//2)-(height//2) 
                        new_window8.geometry("{}x{}+{}+{}".format(width, height, x, y)) 
                        def con_and_can(event, r_te, d_te):
                            new_window8.destroy()
                            check_off(None, r_te, d_te)

                        tk.Button(new_window8, text="Confirm", width=20, height=2, command=lambda event=None, res=r_temp, cd=c_temp :con_and_can(event, res, cd)).pack(pady=25)
                        tk.Button(new_window8, text="Cancel", width=20, height=2, command=lambda: new_window8.destroy()).pack(pady=30)
                    tk.Button(new_window2, text="Check Off", width=20, height=2, command=lambda event=None, res=(ur, (title, det), tv), cd=date_temp: co_con(event, res, cd)).pack(pady=30)
                    tk.Button(new_window2, text="Exit", width=20, height=2, command=lambda: new_window2.destroy()).pack(pady=0)

                text.insert(tk.END, "\t")
                dt.bind("<Button-1>", lambda event, arg=str(cur_items[i][1][0]), arg2=str(cur_items[i][1][1]), 
                arg3=cur_items[i][0], arg4=cur_items[i][2], arg5=dates, arg6=nums: test(event, arg, arg2, arg3, arg4, arg5, arg6))

                text.insert('end', '\n\t')
                if cur_items[i][0] == 1:
                    text.window_create(tk.END, window=tk.Label(text, text="Top Urgent", fg="Red", 
                bg='white', font=("Calibri", 15, 'bold')))
                    text.insert('end', '\n')
                elif cur_items[i][0] == 2:
                    text.window_create(tk.END, window=tk.Label(text, text="Urgent", fg="Blue", 
                bg='white', font=("Calibri", 15, 'bold')))
                    text.insert('end', '\n')
                if cur_items[i][2] != None:
                    text.window_create(tk.END, window=tk.Label(text, text="Scheduled At " + '%02d' % cur_items[i][2][0] + ":" + '%02d' % cur_items[i][2][1], fg="black", 
                bg='white', font=("Calibri", 15)))
                    text.insert('end', '\n')
                text.insert('end', '\t')
                text.window_create(tk.END, window=dt)
                text.insert('end', '\n\n\t')
        text.config(state=DISABLED)
        text.pack(pady=30, padx=30)
        bgcanvas.pack(pady=20)
        tk.Button(new_window5, text="Exit", width=35, height=3, command= lambda: new_window5.destroy()).pack(pady=20)
        

late_but = tk.Button(master, text="Overdue (" + str(int(np.sum([len(data_dict[x[1]]) for x in lates]))) + ")", width=35, height=3, command=late_fun)
late_but.place(x=325-20, y=500)

late_but.update_idletasks()

canvas_width = late_but.winfo_width()
canvas_height = late_but.winfo_height()

but_x = center_x - (canvas_width / 2)

late_but.place(x=but_x, y=700-0)






note_can.pack(side=RIGHT)
master.configure(background='black')
master.mainloop()