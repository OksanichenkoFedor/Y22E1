import tkinter as tk
import config
import numpy as np
from count_plot_array import count_wave

class ChRB_panel(tk.Frame):
    def __init__(self, master, var, command):
        self.master = master
        super().__init__(master)

        self.ch_lb = tk.Label(self, text="Настройка умного курсора")
        self.ch_lb.grid(row=0, column=0, columnspan=2)
        self.print_U = tk.Radiobutton(self, text="Первый", value=0, variable=var, command=command)
        self.print_U.grid(row=1, column=0, sticky="W")

        self.print_I = tk.Radiobutton(self, text="Второй", value=1, variable=var, command=command)
        self.print_I.grid(row=1, column=1, sticky="W")


class SPC_panel(tk.Frame):
    def __init__(self, master):
        self.master = master
        super().__init__(master)
        self.initFrame()

    def initFrame(self):
        self.main_label = tk.Label(self, text="Настройки спектра")
        self.main_label.grid(row=0, column = 0, columnspan = 3)

        self.pix_label = tk.Label(self, text="Пиксели")
        self.pix_label.grid(row=1, column=1)
        self.wave_label = tk.Label(self, text="Длины волн(нм)")
        self.wave_label.grid(row=1, column=2)

        self.SPECstatus = tk.StringVar()
        self.SPECstatus.set("Корректные параметры.")
        self.SPECstatuscolor = tk.StringVar()

        if config.is_correct_spec_param == 0:
            self.SPECstatuscolor = "r"
        else:
            self.SPECstatuscolor = "g"

        self.status_label = tk.Label(self, textvariable = self.SPECstatus, fg = "green")


        self.pixel_vars = []
        self.wave_vars = []
        self.pixel_entrys = []
        self.wave_entrys = []
        self.labels = []
        self.texts = ["I", "II", "III"]
        for i in range(3):
            self.pixel_vars.append(tk.StringVar())
            self.wave_vars.append(tk.StringVar())
            self.pixel_vars[i].set(config.pixels[i])
            self.wave_vars[i].set(config.wave_lenghts[i])

            self.labels.append(tk.Label(self, text=self.texts[i]))
            self.labels[i].grid(row=i + 2, column=0)

            self.pixel_entrys.append(tk.Entry(self, textvariable=self.pixel_vars[i]))
            self.pixel_entrys[i].grid(row=i + 2, column=1)

            self.wave_entrys.append(tk.Entry(self, textvariable=self.wave_vars[i]))
            self.wave_entrys[i].grid(row=i + 2, column=2)

            self.pixel_vars[i].trace("w", lambda name, index, mode, ind=i:self.change(ind, True))
            self.wave_vars[i].trace("w", lambda name, index, mode, ind=i: self.change(ind, False))

        self.status_label.grid(row=5, column=0, columnspan=3)

        self.param_text_var = tk.StringVar()

        self.param_text_var.set("k="+str(round(config.k, 3)) + ", b="+str(round(config.b, 3)))

        self.type_of_formula_label = tk.Label(self, text="y = kx + b")
        self.type_of_formula_label.grid(column=0, row=6, columnspan = 3)
        self.formula_label = tk.Label(self, textvariable=self.param_text_var)  # , background="#777")
        self.formula_label.grid(row=7, column=0, columnspan=3)
    def change(self, ind,is_pix):
        try:
            for i in range(3):
                config.pixels[i] = int(self.pixel_vars[i].get())
                config.wave_lenghts[i] = int(self.wave_vars[i].get())
            self.SPECstatus.set("Корректные параметры.")
            self.status_label["fg"] = "green"
            config.is_correct_spec_param = 1
            count_wave()
            self.param_text_var.set("k=" + str(round(config.k, 3)) + ", b=" + str(round(config.b, 3)))
            self.update()
            self.master.plot_field.update_plot()
        except:
            self.SPECstatus.set("Недопустимые параметры.")
            self.status_label["fg"] = "red"
            config.is_correct_spec_param = 0







    def SpectrCB(self, name, index, mode, status, colr, start_l, end_l, light_start_l, light_end_l):
        self.print_tint = tk.StringVar()
        try:
            start = np.uint32(int(start_l.get()))
            end = np.uint32(int(end_l.get()))
            light_start = np.uint32(int(light_start_l.get()))
            light_end = np.uint32(int(light_end_l.get()))

            if (start >= 0) and (end <= config.num_pixels) and (start < end) and (light_start > 0) and (
                    light_start < light_end):
                status.set("Корректные параметры.")
                colr.configure(fg="green")
                config.start = start
                config.end = end
                config.light_start = light_start
                config.light_end = light_end
            else:
                status.set("Недопустимые параметры.")
                colr.configure(fg="red")
                self.print_tint.set("invalid")
        except:
            status.set("Недопустимые параметры.")
            colr.configure(fg="red")
            self.print_tint.set("invalid")