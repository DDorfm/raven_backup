#!/usr/bin/python3
import datetime
import tkinter
from tkinter import Tk, Button, filedialog, \
     Label, Listbox, messagebox, StringVar, \
     Scrollbar, Text, Checkbutton, Menu, font, \
     LabelFrame, Entry, Radiobutton, PhotoImage, ttk
from tkinter.messagebox import askyesno
import os.path
import subprocess
import ast
import gettext
import shutil
import glob
import threading
from calendar import month_name, day_name
from cryptography.fernet import Fernet
from pathlib import Path


class RavenBackup:

    def __init__(self):

        self.nombre_aplicacion = 'Raven Backup'
        self.version = '1.4.9'
        self.appname = 'raven_backup'
        self.localedir = './locales'
        self.idioma_seleccionado = ''
        self.color_negro = '#000'
        self.color_rojo = '#f00'
        self.cron_ventana = None
        self.nombre_fichero_configuracion_actual = ""
        self.item_seleccionado = None
        self.modificacion_de_items = False
        self.items_eliminados_lst = []
        self.origen_lst = []
        self.destino = ''
        self.comandos_para_cron_lst = []
        self.opcion_comprimir_inicial_str = ''
        self.opcion_delete_inicial_str = ''
        self.opcion_enlaces_simbolicos_inicial_str = ''
        self.opcion_incremental_inicial_str = ''
        self.directorio_destino_inicial_str = ''
        self.puerto_remoto_inicial_str = ''
        self.password_var_inicial_str = ''
        self.tipo_acceso_var_inicial_str = ''
        self.idioma_seleccionado_inicial_str = ''
        self.modificacion_checkboxes = False
        self.modificacion_radiobotones_ficheros_con_enlaces = False
        self.hilo_copia = None
        self.log_txtbox = None
        self.password = ''
        self.puerto_remoto = None
        self.destino_ip = None
        self.root = None
        self.ancho_pantalla = None
        self.alto_pantalla = None
        self.ancho_ventana = None
        self.medida_ancho_ajustada = None
        self.alto_ventana = None
        self.medida_alto_ajustada = None
        self.texto_etiqueta_mensaje_de_estado = None
        self.txt_lbl_stat_crom = None
        self.opcion_delete_var = None
        self.opcion_comprimir_var = None
        self.opcion_incremental_var = None
        self.opcion_enlaces_simbolicos_var = None
        self.password_var = None
        self.tipo_acceso_var = None
        self.cron_minuto_var = None
        self.cron_hora_var = None
        self.cron_dia_mes_var = None
        self.cron_mes_var = None
        self.cron_dia_semana_var = None
        self.cron_arroba_var = None
        self.option_delete_chkbtn = None
        self.directorio_destino_txtbox = None
        self.option_incremental_chkbtn = None
        self.option_comprimir_chkbtn = None
        self.password_entrybox = None
        self.puerto_remoto_txtbox = None
        self.directorios_seleccionados_lstbox = None
        self.clave_publica_radiobtn = None
        self.password_radiobtn = None
        self.enlaces_simbolicos_copiar_fichero_radiobtn = None
        self.enlaces_simbolicos_mantener_enlace_radiobtn = None
        self.left_buttons_frame = None
        self.dir_selected_lstbox_frame = None
        self.log_txtbox_frame = None
        self.parametros_tiempo_cron = None
        self.parametros_tiempo_cron = None
        self.option_incremental_chkbtn = None
        self.password_radiobtn = None
        self.clave_publica_radiobtn = None
        self.password_entrybox = None
        self.enlaces_simbolicos_mantener_enlace_radiobtn = None
        self.directorios_seleccionados_lstbox = None

        self.i18n = gettext.translation(
            self.appname,
            self.localedir,
            languages=["en"],
            fallback=True
        )
        self._ = self.i18n.gettext
        if os.path.isfile('.raven_backup.conf'):
            self.existe_fichero_configuracion = True
        else:
            self.existe_fichero_configuracion = False

        fichero_de_clave = ".secret.key"
        key = None
        if not os.path.exists(fichero_de_clave):
            key = Fernet.generate_key()
            with open(fichero_de_clave, "wb") as f:
                f.write(key)
                result = subprocess.run(
                    ['chmod', '600', '.secret.key'],
                    capture_output=True, text=True, shell=False)
                if result.returncode != 0:
                    messagebox.showinfo(
                        title=f"{self.nombre_aplicacion} v.  {self.version}",
                        message=self._('Error creando fichero .secret.key'))
        else:
            with open(fichero_de_clave, "rb") as f:
                key = f.read()
        self.cipher = Fernet(key)

    @property
    def titulo_app(self):
        return f"{self.nombre_aplicacion} v. {self.version}"

    def compilar_po_a_mo(self):

        fichero_po_locales_en = Path("locales/en/LC_MESSAGES/raven_backup.po")
        fichero_mo_locales_en = Path("locales/en/LC_MESSAGES/raven_backup.mo")
        if not os.path.exists(fichero_po_locales_en):
            messagebox.showinfo(
                title=f"{self.titulo_app}",
                message=self._('No se encuentra el archivo de idioma'))
            quit()
        else:
            if (not os.path.exists(fichero_mo_locales_en) or
                    Path(fichero_po_locales_en).stat().st_mtime
                    > Path(fichero_mo_locales_en).stat().st_mtime):
                try:
                    subprocess.run(
                        [
                            "pybabel", "compile", "-i",
                            fichero_po_locales_en, "-o",
                            fichero_mo_locales_en
                        ],
                        check=True,
                        capture_output=True,
                        text=True)
                except subprocess.CalledProcessError as e:
                    messagebox.showinfo(
                        title=f"{self.titulo_app}",
                        message=f"{self._('Error al compilar el '
                                          'archivo de idioma')}"
                                f"{e.stderr.strip()}")
                    quit()
                except FileNotFoundError:
                    messagebox.showinfo(
                        title=f"{self.nombre_aplicacion} v.{self.version}",
                        message=self._("pybabel no encontrado. "
                                       "Instale Babel: pip install babel"))
                    quit()
            else:
                pass


    def crea_ventana_root(self):

        self.root = Tk()
        self.ancho_pantalla = self.root.winfo_screenwidth()
        self.alto_pantalla = self.root.winfo_screenheight()
        self.ancho_ventana = 1217
        self.alto_ventana = 570
        self.medida_ancho_ajustada = (
            round(self.ancho_pantalla / 2 - self.ancho_ventana / 2)
        )
        self.medida_alto_ajustada = (
            round(self.alto_pantalla / 2 - self.alto_ventana / 2)
        )
        self.root.geometry(str(self.ancho_ventana)
                           + "x" + str(self.alto_ventana)
                           + "+" + str(self.medida_ancho_ajustada)
                           + "+" + str(self.medida_alto_ajustada))
        self.root.resizable(False, False)

        self.root.iconphoto(
            True,
            PhotoImage(file="assets/raven_backup.png")
                            )  
        self.root.title(f"{self.titulo_app}"
                        f"{15 * ' '}{self._('Configuración actual: ')}"
                        f"{self.chequea_fichero_conf_actual().upper()}"
                        )

        self.texto_etiqueta_mensaje_de_estado = StringVar()
        self.txt_lbl_stat_crom = StringVar()
        self.opcion_delete_var = StringVar()
        self.opcion_comprimir_var = StringVar()
        self.opcion_incremental_var = StringVar()
        self.opcion_enlaces_simbolicos_var = StringVar()
        self.password_var = StringVar()
        self.tipo_acceso_var = StringVar()
        self.cron_minuto_var = StringVar()
        self.cron_hora_var = StringVar()
        self.cron_dia_mes_var = StringVar()
        self.cron_mes_var = StringVar()
        self.cron_dia_semana_var = StringVar()
        self.cron_arroba_var = StringVar()
        self.option_delete_chkbtn = Checkbutton()
        self.directorio_destino_txtbox = Text()
        self.directorios_seleccionados_lstbox = Listbox()
        self.enlaces_simbolicos_mantener_enlace_radiobtn = Radiobutton()
        self.password_entrybox = Entry()
        self.clave_publica_radiobtn = Radiobutton()
        self.password_radiobtn = Radiobutton()
        self.option_delete_chkbtn = Checkbutton()
        self.option_incremental_chkbtn = Checkbutton()

    def lanzar_hilo_copia(self):

        if self.hilo_copia is None or not self.hilo_copia.is_alive():
            self.hilo_copia = threading.Thread(
                target=self.procesa_datos_origen,
                args=(False,)
            )
            self.hilo_copia.start()
        elif self.hilo_copia.is_alive():
            messagebox.showinfo(
                title=f"{self.nombre_aplicacion} v.{self.version}",
                message=self._('Ya se está ejecutando un proceso de copia')
            )
            return None

    def reinicia_gui(self):

        self.elimina_contenido_elementos_graficos()
        self.lee_fichero_configuracion()
        self.rellena_datos()
        self.root.title(f"{self.titulo_app}"
                        f"{15 * ' '}{self._('Configuración actual: ')}"
                        f" {self.chequea_fichero_conf_actual().upper()}")
        self.root.focus()

    def chequea_fichero_conf_actual(self):

        if not os.path.isfile(".raven_backup.conf"):
            return 'tmp'
        for fichero in glob.glob("*.conf"):
            comando_diff = ['diff', '.raven_backup.conf', fichero]
            sp = subprocess.run(comando_diff, capture_output=True, text=True)
            if len(sp.stdout) == 0:
                self.nombre_fichero_configuracion_actual = (
                    fichero.split(".")
                )[0]
                return self.nombre_fichero_configuracion_actual

    def establece_idioma(self, idioma):

        self.idioma_seleccionado = idioma
        self.i18n = gettext.translation(
            self.appname,
            self.localedir,
            fallback=True,
            languages=[self.idioma_seleccionado]
        )
        self._ = self.i18n.gettext

    def selecciona_idioma(self, idioma):

        self.idioma_seleccionado = idioma
        messagebox.showinfo(
            title=f"{self.titulo_app}",
            message=self._('Necesita guardar y reiniciar')
        )
        self.modificacion_de_items = True

    def acerca_de(self):

        tiempo_espera_destruir = 6000
        acerca_de_win = Tk()
        acerca_de_win.resizable(False, False)

        acerca_de_win.title(
            f"{self.titulo_app}")

        lbl_acerca_de_win = Label(master=acerca_de_win)
        lbl_acerca_de_win.configure(
            text=(
                f"{self._('Raven Backup es un script en python'
                          ' 3.12.3 y Tkinter para guardar\n y '
                          'restaurar directorios y ficheros usando rsync.')}"
                f"{self._('\nPuede enviar comentarios, bugs '
                          'y sugerencias para mejorarlo a\n\n')}"
                "Danieldorfman@proto.me"
            )
        )
        lbl_acerca_de_win.configure(font=("TkDefaultFont", 12))
        lbl_acerca_de_win.pack(padx=35, pady=20)
        acerca_de_win.after(
            tiempo_espera_destruir,
            lambda: acerca_de_win.destroy()
        )
        acerca_de_win.mainloop()

    def recoge_valores_cron(self):

        self.txt_lbl_stat_crom.set('')
        self.comandos_para_cron_lst.clear()
        if not self.cron_arroba_var.get() == '' and \
                (not self.cron_minuto_var.get() == ''
                 or not self.cron_hora_var.get() == ''
                 or not self.cron_dia_semana_var.get() == ''
                 or not self.cron_mes_var.get() == ''
                 or not self.cron_dia_mes_var.get() == ''):

            self.cron_ventana.wm_attributes('-topmost', False)
            messagebox.showinfo(
                title=f"{self.titulo_app}",
                message=self._('Seleccione sólo un'
                               ' tipo de parámetro temporal')
            )
            self.cron_ventana.wm_attributes('-topmost', True)
            return None
        self.parametros_tiempo_cron = ''
        if self.cron_arroba_var.get() == '':
            if not self.cron_minuto_var.get() == '':
                self.parametros_tiempo_cron += self.cron_minuto_var.get()
            else:
                self.parametros_tiempo_cron += '*'
            self.parametros_tiempo_cron += ' '
            if not self.cron_hora_var.get() == '':
                self.parametros_tiempo_cron += self.cron_hora_var.get()
            else:
                self.parametros_tiempo_cron += '*'
            self.parametros_tiempo_cron += ' '
            if not self.cron_dia_mes_var.get() == '':
                self.parametros_tiempo_cron += self.cron_dia_mes_var.get()
            else:
                self.parametros_tiempo_cron += '*'
            self.parametros_tiempo_cron += ' '
            if not self.cron_mes_var.get() == '':
                self.parametros_tiempo_cron += self.cron_mes_var.get()
            else:
                self.parametros_tiempo_cron += '*'
            self.parametros_tiempo_cron += ' '
            if not self.cron_dia_semana_var.get() == '':
                self.parametros_tiempo_cron += self.cron_dia_semana_var.get()
            else:
                self.parametros_tiempo_cron += '*'
            self.parametros_tiempo_cron += ' '
        else:
            self.parametros_tiempo_cron += self.cron_arroba_var.get()
        self.parametros_tiempo_cron = self.parametros_tiempo_cron.strip()
        if self.parametros_tiempo_cron == '* * * * *':
            self.cron_ventana.wm_attributes('-topmost', False)
            messagebox.showinfo(
                title=f"{self.titulo_app}",
                message=self._('Debe especificar algún valor temporal')
            )
            self.cron_ventana.wm_attributes('-topmost', True)
            return None
        self.txt_lbl_stat_crom.set(
            self._('Construyendo instrucciones para cron...')
        )
        self.procesa_datos_origen(True)
        err = False
        order_sent = False
        for elemento in self.comandos_para_cron_lst:
            elemento_lst = elemento.split(' ')
            if "ssh" in elemento_lst:
                pos = elemento_lst.index('ssh')
                cadena_ssh = "ssh -p " + elemento_lst[pos + 2]
                cadena_ssh_comas = "'" + cadena_ssh + "'"
                elemento = elemento.replace(cadena_ssh, cadena_ssh_comas)
            item_cron = elemento
            item_cron = self.parametros_tiempo_cron + ' ' + item_cron
            item_cron = '"' + item_cron + '"'
            comando = (
                f"(crontab -l 2>/dev/null; echo {item_cron}) | crontab -"
            )
            chequea_cmd = "crontab -l | grep " + item_cron
            chequea_cmd = chequea_cmd.replace('*', '\\\\*')
            result = subprocess.Popen(
                chequea_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True)
            err_decode = result.stderr.read().decode()
            if err_decode == '':
                err = False
            else:
                self.txt_lbl_stat_crom.set(err_decode)
                err = True
            chequea_resultado = result.stdout.read().decode().strip()
            chequea_resultado_lst = chequea_resultado.split('\n')
            cont = False
            order_sent = False
            for elemento_lista_chequeo in chequea_resultado_lst:
                if elemento_lista_chequeo == item_cron.replace('"', ""):
                    item_origen = item_cron.split(" ")
                    signos_temporales = item_cron.split('rsync')[0]
                    self.txt_lbl_stat_crom.set('')
                    self.cron_ventana.wm_attributes('-topmost', False)
                    messagebox.showinfo(
                        title=f"{self.titulo_app}",
                        message=f"{self._('Ya existe en cron el elemento:')} "
                                f"{signos_temporales} {item_origen[-2]}\""
                                f"{self._('\nSe omite')}")
                    self.cron_ventana.wm_attributes('-topmost', True)
                    cont = True
                else:
                    result = subprocess.Popen(
                        comando,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        shell=True)
                    err_decode = result.stderr.read().decode()
                    if err_decode == '':
                        err = False
                    else:
                        self.txt_lbl_stat_crom.set(
                            err_decode)
                        err = True

                    order_sent = True
            if cont:
                continue

        if not err and order_sent:
            msg_err = self._('órdenes enviadas a cron correctamente')
            self.txt_lbl_stat_crom.set(msg_err)

    def selec_idioma_para_config(self, ancho=350, alto=140):

        selec_idioma_ventana = Tk()
        selec_idioma_ventana.wm_attributes('-topmost', True)
        ancho_ventana = ancho
        alto_ventana = alto
        tamano_ventana = str(ancho_ventana) + "x" + str(alto_ventana)
        selec_idioma_ventana.wm_geometry(tamano_ventana)
        selec_idioma_ventana.resizable(False, False)
        selec_idioma_ventana.title(
            f"{self.titulo_app}"
        )
        Label(
            selec_idioma_ventana,
            text=self._('Select language'),
            font=("TkDefaultFont", 12)
        ).place(x=35, y=30)

        combo = ttk.Combobox(
            selec_idioma_ventana,
            state="readonly",
            values=["Spanish|es", "English|en"],
            width=10
        )
        combo.place(x=200, y=30)

        combo.current(1)  
        aceptar_ventana_msg_btn = Button(
            selec_idioma_ventana,
            text=self._('Aceptar'),
            command=lambda:
            [self.establece_idioma(combo.get().split("|")[1]),
             selec_idioma_ventana.destroy()],
            font=("TkDefaultFont", 12))
        aceptar_ventana_msg_btn.place(x=160, y=80)
        selec_idioma_ventana.mainloop()

    def programador_cron(self):

        self.cron_ventana = tkinter.Toplevel(self.root)
        self.cron_ventana.wm_attributes('-topmost', True)
        parametros_temporales_cron_lf = LabelFrame(
            self.cron_ventana,
            text=self._('Parámetros de tiempo'),
            width=530,
            height=90,
            font=("TkDefaultFont", 12))
        parametros_temporales_cron_lf.place(x=25, y=15)
        if self.idioma_seleccionado == 'en':
            self.cron_ventana.geometry('520x245')
        else:
            self.cron_ventana.geometry('545x255')
        self.cron_ventana.resizable(False, False)
        self.cron_ventana.title(
            f"{self.nombre_aplicacion} v.{self.version}")
        cron_minuto_lbl = Label(
            parametros_temporales_cron_lf,
            text=self._('Minuto'),
            font=("TkDefaultFont", 12))
        cron_minuto_lbl.grid(row=0, column=0)

        cron_minuto_combobox = ttk.Combobox(
            parametros_temporales_cron_lf,
            textvariable=self.cron_minuto_var,
            width=5)

        cron_minuto_combobox['values'] = [m for m in range(0, 60)]
        cron_minuto_combobox.grid(row=1, column=0, padx=10, pady=10)

        cron_hora_lbl = Label(
            parametros_temporales_cron_lf,
            text=self._('Hora'),
            font=("TkDefaultFont", 12))
        cron_hora_lbl.grid(row=0, column=1)

        cron_hora_combobox = ttk.Combobox(
            parametros_temporales_cron_lf,
            textvariable=self.cron_hora_var,
            width=5)

        cron_hora_combobox['values'] = [m for m in range(0, 24)]
        cron_hora_combobox.grid(row=1, column=1, padx=0, pady=0)

        cron_dia_mes_lbl = Label(
            parametros_temporales_cron_lf,
            text=self._('Día del mes'),
            font=("TkDefaultFont", 12))

        cron_dia_mes_lbl.grid(row=0, column=2, padx=10, pady=0)

        cron_hora_combobox = ttk.Combobox(
            parametros_temporales_cron_lf,
            textvariable=self.cron_dia_mes_var,
            width=5)

        cron_hora_combobox['values'] = [m for m in range(1, 32)]
        cron_hora_combobox.grid(row=1, column=2, padx=10, pady=0)

        cron_mes_lbl = Label(
            parametros_temporales_cron_lf,
            text=self._('Mes'),
            font=("TkDefaultFont", 12))

        cron_mes_lbl.grid(row=0, column=3, padx=10, pady=0)

        cron_mes_combobox = ttk.Combobox(
            parametros_temporales_cron_lf,
            textvariable=self.cron_mes_var,
            width=5)

        cron_mes_combobox['values'] = \
            [month_name[m][0:3] for m in range(1, 13)]

        cron_mes_combobox.grid(row=1, column=3, padx=10, pady=0)

        cron_dia_semana_lbl = Label(
            parametros_temporales_cron_lf,
            text=self._('Día de la semana'),
            font=("TkDefaultFont", 12))

        cron_dia_semana_lbl.grid(row=0, column=4, padx=10, pady=0)

        cron_dia_semana_combobox = ttk.Combobox(
            parametros_temporales_cron_lf,
            textvariable=self.cron_dia_semana_var,
            width=5)

        cron_dia_semana_combobox['values'] = (
            [day_name[m][0:3] for m in range(0, 7)]
        )

        cron_dia_semana_combobox.grid(row=1, column=4, padx=10, pady=0)

        cron_arroba_lbl = Label(
            self.cron_ventana,
            text=self._('Cadenas de texto reservadas'),
            font=("TkDefaultFont", 12))

        cron_arroba_lbl.place(x=25, y=129)

        cron_arroba_combobox = ttk.Combobox(
            self.cron_ventana,
            textvariable=self.cron_arroba_var, width=9)

        cron_arroba_combobox['values'] = [
            '@reboot', '@yearly', '@monthly',
            '@weekly', '@daily', '@midnight', '@hourly']

        if self.idioma_seleccionado == 'es':
            cron_arroba_combobox.place(x=275, y=135)
        else:
            cron_arroba_combobox.place(x=210, y=135)
        Label(self.cron_ventana,
              text=self._('Línea de mensajes:'),
              font=("TkDefaultFont", 12)
              ).place(x=25, y=210)
        if self.idioma_seleccionado == 'es':
            x_pos = 250
        else:
            x_pos = 326
        Label(self.cron_ventana,
              text=self._('Puede editar los desplegables manualmente'),
              font=("TkDefaultFont", 9)
              ).place(x=x_pos, y=102)

        aceptar_cron_btn = Button(
            self.cron_ventana,
            text=self._('Aceptar'),
            command=self.recoge_valores_cron,
            font=("TkDefaultFont", 12))
        aceptar_cron_btn.place(x=170, y=172)

        cerrar_cron_btn = Button(
            self.cron_ventana,
            text=self._('Cerrar'),
            command=lambda: [
                self.cron_ventana.destroy(),
                self.root.focus()],
            font=("TkDefaultFont", 12))

        cerrar_cron_btn.place(x=295, y=172)

        mensaje_de_estado_lbl_cron = Label(
            self.cron_ventana,
            textvariable=self.txt_lbl_stat_crom,
            font=(font.Font(None, size=11, weight="bold")))
        self.txt_lbl_stat_crom.set('')
        if self.idioma_seleccionado == 'es':
            x_pos = 185
        else:
            x_pos = 140
        mensaje_de_estado_lbl_cron.place(x=x_pos, y=210)

    def crea_menus(self):

        menubar = Menu(self.root)
        menu_opciones_idiomas = Menu(menubar, tearoff=0)
        menu_opciones_idiomas.add_command(
            label=self._('Español'),
            command=lambda: self.selecciona_idioma('es'))

        menu_opciones_idiomas.add_command(
            label=self._('Inglés'),
            command=lambda: self.selecciona_idioma('en'))

        menubar.add_cascade(
            label=self._('Opciones de idioma'),
            menu=menu_opciones_idiomas)

        menubar.add_command(
            label=self._('Programador'),
            command=lambda: self.programador_cron())

        menubar.add_command(
            label=self._('Configuraciones'),
            command=lambda: self.cambiar_configuracion())

        menubar.add_command(
            label=self._('Acerca de'),
            command=lambda: self.acerca_de())

        self.root.config(menu=menubar)

    def lee_fichero_configuracion(self):

        if os.path.isfile('.raven_backup.conf'):

            fichero_configuracion = open('.raven_backup.conf', 'r')
            items_fichero_configuracion = fichero_configuracion.readlines()
            fichero_configuracion.close()

            self.origen_lst = items_fichero_configuracion[0].split(',')

            self.destino = items_fichero_configuracion[1].strip()

            if not self.destino.find(':') == -1:

                opciones_dict = ast.literal_eval(self.destino)

                self.destino_ip = opciones_dict.get('destino')
                self.directorio_destino_inicial_str = self.destino_ip

                self.puerto_remoto = opciones_dict.get('puerto_remoto')

                self.puerto_remoto_inicial_str = self.puerto_remoto

                self.tipo_acceso_var.set(opciones_dict.get('tipo_acceso'))

                self.tipo_acceso_var_inicial_str = self.tipo_acceso_var.get()

                password_encriptada = opciones_dict.get('password')
                if password_encriptada:
                    try:
                        self.password = (
                            self.cipher.decrypt(
                                password_encriptada.encode()).decode()
                        )
                    except Exception:
                        self.password = password_encriptada
                else:
                    self.password = ''

                self.password_var_inicial_str = self.password
            else:
                self.directorio_destino_inicial_str = self.destino


            opciones_dict = ast.literal_eval(items_fichero_configuracion[2])

            self.opcion_delete_var.set(opciones_dict.get('delete'))

            self.opcion_delete_inicial_str = self.opcion_delete_var.get()

            opciones_dict = ast.literal_eval(items_fichero_configuracion[3])

            self.opcion_comprimir_var.set(
                opciones_dict.get('comprimir_durante_copia'))

            self.opcion_comprimir_inicial_str = (
                self.opcion_comprimir_var.get()
            )

            opciones_dict = ast.literal_eval(items_fichero_configuracion[4])

            self.opcion_enlaces_simbolicos_var.set(
                opciones_dict.get('tratamiento_archivos_enlazados'))

            self.opcion_enlaces_simbolicos_inicial_str = (
                self.opcion_enlaces_simbolicos_var.get()
            )

            opciones_dict = ast.literal_eval(items_fichero_configuracion[5])

            self.opcion_incremental_var.set(
                opciones_dict.get('copia_incremental'))

            self.opcion_incremental_inicial_str = (
                self.opcion_incremental_var.get()
            )

            idioma_seleccionado = items_fichero_configuracion[6]

            self.idioma_seleccionado_inicial_str = idioma_seleccionado
            self.establece_idioma(idioma_seleccionado)
        else:
            self.selec_idioma_para_config()

    def cuenta_atras(self, contador):

        if contador < 8:
            self.root.after(1000, self.cuenta_atras, contador + 1)

        if contador == 3:
            if (not self.texto_etiqueta_mensaje_de_estado.get()
                    == 'Copia finalizada'
                    or not self.texto_etiqueta_mensaje_de_estado.get()
                    == 'Backup done'):
                self.texto_etiqueta_mensaje_de_estado.set('')

    def procesa_datos_origen(self, dry=False):


        if self.directorios_seleccionados_lstbox.size() == 0:
            if dry:
                self.cron_ventana.wm_attributes('-topmost', False)

            messagebox.showinfo(
                title=f"{self.titulo_app}",
                message=self._('No hay ficheros y/o directorios'
                               ' seleccionados para copiar'))

            if dry:
                self.cron_ventana.wm_attributes('-topmost', True)
                self.txt_lbl_stat_crom.set('')
            return None

        if self.directorio_destino_txtbox.get('1.0', 'end').strip() == '':
            if dry:
                self.cron_ventana.wm_attributes('-topmost', False)

            messagebox.showinfo(
                title=f"{self.titulo_app}",
                message=self._('No hay directorio de destino'))
            if dry:
                self.cron_ventana.wm_attributes('-topmost', True)
                self.txt_lbl_stat_crom.set('')
            return None

        self.comprueba_existencia_en_origen()

        if not dry:  
            self.log_txtbox.delete('1.0', tkinter.END)

        if len(self.directorios_seleccionados_lstbox.curselection()) != 0:
            items_seleccionados = tuple()

            tmp_ra = len(self.directorios_seleccionados_lstbox.curselection())
            for i in range(tmp_ra):
                indice = self.directorios_seleccionados_lstbox.curselection()
                [i]
                items_seleccionados += (
                    self.directorios_seleccionados_lstbox.get(indice, indice)
                )

            directorios_seleccionados_tupla = items_seleccionados
        else:
            directorios_seleccionados_tupla = (
                self.directorios_seleccionados_lstbox.get('0', 'end')
            )

        directorio_destino = (
            self.directorio_destino_txtbox.get('1.0', 'end').strip()
        )


        if not directorio_destino.find(':') == -1:
            if self.puerto_remoto_txtbox.get('1.0', 'end').strip() == '':
                if dry:
                    self.cron_ventana.wm_attributes('-topmost', False)

                messagebox.showinfo(
                    title=f"{self.titulo_app}",
                    message=self._('Debe asignar un valor de '
                                   'puerto remoto para un destino remoto'))

                if dry:
                    self.cron_ventana.wm_attributes('-topmost', True)
                    self.txt_lbl_stat_crom.set('')

                return None
            if (self.tipo_acceso_var.get() == 'password'
                    and self.password_var.get() == ''):
                messagebox.showinfo(
                    title=f"{self.titulo_app}",
                    message=self._('Debe asignar un valor de'
                                   ' password para acceso con password'))
                return None

        if directorio_destino.find(':') == -1:
            if not os.path.exists(directorio_destino):
                if dry:
                    self.cron_ventana.wm_attributes('-topmost', False)
                messagebox.showinfo(
                    title=f"{self.titulo_app}",
                    message=self._('No existe directorio de destino'))
                if dry:
                    self.cron_ventana.wm_attributes('-topmost', True)
                    self.txt_lbl_stat_crom.set('')
                return None

        if not dry:
            self.texto_etiqueta_mensaje_de_estado.set(
                self._('Chequeando algunas cosas...'))

        indice = 0
        for item_a_copiar in directorios_seleccionados_tupla:
            if self.directorios_seleccionados_lstbox.size() > indice:
                if not dry:
                    self.directorios_seleccionados_lstbox.itemconfig(
                        indice,
                        bg="lightgrey"
                    )
                self.directorios_seleccionados_lstbox.update()
                indice = indice + 1

            if directorio_destino.find(':') == -1:
                if os.path.isdir(item_a_copiar):

                    directorio_destino_ruta_completa = ''


                    item_a_copiar += '/'
                    item_a_copiar_cadena_final = item_a_copiar.split('/')[-2]
                    directorio_destino_ruta_completa = (
                            directorio_destino + '/' +
                            item_a_copiar_cadena_final + '/'
                    )
                    if self.opcion_incremental_var.get() == 'True':
                        if dry:
                            self.log_txtbox.insert(tkinter.INSERT, '\n')
                            self.log_txtbox.insert(
                                tkinter.INSERT,
                                self._('Se crean enlaces '
                                       'simbólicos para cron: ' + '\n')
                            )
                            self.log_txtbox.update()

                        fichero_simbolico_a_chequear = (
                                item_a_copiar_cadena_final +
                                '_latest'
                        )
                        ruta_fichero_simbolico_a_chequear = (
                                directorio_destino +
                                '/' +
                                fichero_simbolico_a_chequear
                        )

                        chequea_enlace_simbolico_cmd = [
                            'if [ -L  ' +
                            ruta_fichero_simbolico_a_chequear +
                            ' ]; then echo Existe enlace  ; fi'
                        ]

                        result = subprocess.run(
                            chequea_enlace_simbolico_cmd,
                            capture_output=True,
                            text=True,
                            shell=True
                        )

                        if not result.stderr == '':
                            if dry:
                                self.cron_ventana.wm_attributes(
                                    '-topmost',
                                    False
                                )
                                tmp_msg = (
                                    'Error verificando '
                                    'enlaces simbólicos en destino')
                                messagebox.showerror(
                                    title=f"{self.titulo_app}",
                                    message=self._(tmp_msg)
                                )
                                self.cron_ventana.wm_attributes(
                                    '-topmost',
                                    True
                                )
                                self.txt_lbl_stat_crom.set('')

                        else:
                            self.log_txtbox.insert(tkinter.INSERT, '\n')
                            self.log_txtbox.insert(
                                tkinter.INSERT,
                                self._('Chequeando enlace ') +
                                item_a_copiar +
                                ' ---> ' +
                                ruta_fichero_simbolico_a_chequear +
                                '\n'
                            )
                            self.log_txtbox.update()

                        if "Existe enlace" in result.stdout:
                            self.log_txtbox.insert(tkinter.INSERT, '\n')
                            self.log_txtbox.insert(
                                tkinter.INSERT,
                                self._('Existe enlace ') +
                                item_a_copiar +
                                ' ---> ' +
                                ruta_fichero_simbolico_a_chequear +
                                '\n'
                            )
                            self.log_txtbox.update()

                        else:
                            ruta_directorio_origen = (
                                    directorio_destino +
                                    '/' +
                                    item_a_copiar_cadena_final
                            )

                            if not os.path.isdir(
                                    directorio_destino_ruta_completa
                            ):
                                result = subprocess.run(
                                    [
                                        'mkdir -p ' +
                                        directorio_destino_ruta_completa
                                    ],
                                    text=True,
                                    capture_output=True,
                                    shell=True
                                )
                                if not result.stderr == '':
                                    if dry:
                                        self.cron_ventana.wm_attributes(
                                            '-topmost',
                                            False
                                        )
                                    messagebox.showerror(
                                        title=self.titulo_app,
                                        message=self._('Error creando'
                                                       ' directorio destino')
                                    )

                                    if dry:
                                        self.cron_ventana.wm_attributes(
                                            '-topmost',
                                            True
                                        )
                                        self.txt_lbl_stat_crom.set('')


                            crea_enlace_simbolico_cmd = [
                                'ln -s ' + ruta_directorio_origen +
                                ' ' +
                                ruta_fichero_simbolico_a_chequear
                            ]

                            result = subprocess.run(
                                crea_enlace_simbolico_cmd,
                                capture_output=True,
                                text=True, shell=True
                            )
                            if not result.stderr == '':
                                if dry:
                                    self.cron_ventana.wm_attributes(
                                        '-topmost',
                                        False
                                    )
                                tmp_msg = ('Error creando '
                                           'enlace al directorio de destino')
                                messagebox.showerror(
                                    title=self.titulo_app,
                                    message=self._(tmp_msg)
                                )
                                if dry:
                                    self.cron_ventana.wm_attributes(
                                        '-topmost',
                                        True
                                    )
                                    self.txt_lbl_stat_crom.set('')
                            else:
                                self.log_txtbox.insert(tkinter.INSERT, '\n')
                                self.log_txtbox.insert(
                                    tkinter.INSERT,
                                    self._('Creando enlace ') +
                                    item_a_copiar +
                                    ' ---> ' +
                                    ruta_fichero_simbolico_a_chequear +
                                    '\n'
                                )
                                self.log_txtbox.insert(tkinter.INSERT, '\n')
                                self.log_txtbox.update()

                        comando_lst = [
                            'rsync', '-avP', '--link-dest=' +
                            ruta_fichero_simbolico_a_chequear,
                            item_a_copiar,
                            directorio_destino_ruta_completa
                        ]
                    else:
                        comando_lst = [
                            'rsync', '-avP', item_a_copiar,
                            directorio_destino_ruta_completa
                        ]
                else:
                    directorio_destino_ruta_completa = directorio_destino
                    comando_lst = [
                        'rsync', '-avP', item_a_copiar,
                        directorio_destino_ruta_completa
                    ]

            else:
                if self.tipo_acceso_var.get() == 'password':
                    passw = self.password_var.get()
                    pto_remoto = (
                        self.puerto_remoto_txtbox.get('1.0', 'end').strip()
                    )

                    if os.path.isdir(item_a_copiar):

                        directorio_destino_ruta_completa = ''
                        item_a_copiar += '/'
                        item_a_copiar_cadena_final = (
                            item_a_copiar.split('/'))[-2]
                        directorio_destino_ruta_completa = (
                                directorio_destino + '/' +
                                item_a_copiar_cadena_final + '/'
                        )

                        buffer_enlace = (
                            directorio_destino_ruta_completa.split(":"))[-1]

                        enlace_a_chequear = (
                                "~/" +
                                buffer_enlace[:len(buffer_enlace) - 1] +
                                "_latest"
                        )
                        usuario_ip = (
                            directorio_destino_ruta_completa.split(":"))[0]
                        fichero_simbolico = enlace_a_chequear.split("/")[-1]
                        if self.opcion_incremental_var.get() == 'True':

                            self.log_txtbox.insert(tkinter.INSERT, '\n')
                            self.log_txtbox.insert(
                                tkinter.INSERT,
                                self._('Chequeando enlace remoto ') +
                                enlace_a_chequear +
                                ' ---> ' +
                                directorio_destino_ruta_completa +
                                '\n'
                            )
                            self.log_txtbox.insert(tkinter.INSERT, '\n')
                            self.log_txtbox.update()

                            chequea_enlace_simbolico_cmd = [
                                'sshpass', '-p',  passw,
                                'ssh', '-p', pto_remoto, usuario_ip,
                                "if [ -L " + enlace_a_chequear + " ]; "
                                "then  echo Existe  enlace " +
                                fichero_simbolico + " ; fi"]
                            result = subprocess.run(
                                chequea_enlace_simbolico_cmd,
                                capture_output=True,
                                text=True
                            )
                            if not result.stderr == '':
                                if dry:
                                    self.cron_ventana.wm_attributes(
                                        '-topmost',
                                        False
                                    )
                                tmp_msg = ('Error verificando enlaces'
                                           ' simbólicos en el servidor')
                                messagebox.showerror(
                                    title=self.titulo_app,
                                    message=self._(tmp_msg))
                                if dry:
                                    self.cron_ventana.wm_attributes(
                                        '-topmost',
                                        True)
                                    self.txt_lbl_stat_crom.set('')

                            if "Existe enlace" in result.stdout:
                                self.log_txtbox.insert(tkinter.INSERT, '\n')
                                self.log_txtbox.insert(
                                    tkinter.INSERT,
                                    self._('Existe enlace remoto ') +
                                    enlace_a_chequear +
                                    ' ---> ' +
                                    directorio_destino_ruta_completa +
                                    '\n'
                                )
                                self.log_txtbox.insert(tkinter.INSERT, '\n')
                                self.log_txtbox.update()
                            else:
                                enlace_a_crear = enlace_a_chequear

                                self.log_txtbox.insert(tkinter.INSERT, '\n')
                                self.log_txtbox.insert(
                                    tkinter.INSERT,
                                    self._('Creando enlace remoto ') +
                                    enlace_a_chequear +
                                    ' ---> ' +
                                    directorio_destino_ruta_completa +
                                    '\n'
                                )
                                self.log_txtbox.insert(tkinter.INSERT, '\n')
                                self.log_txtbox.update()

                                origen_enlace_simbolico = (
                                    enlace_a_chequear.replace('_latest', '/')
                                )
                                crea_enlace_simbolico_cmd = [
                                    'sshpass', '-p', passw,
                                    'ssh', '-p', pto_remoto,
                                    usuario_ip, 'ln -s ' +
                                    origen_enlace_simbolico,
                                    enlace_a_crear
                                ]

                                result = subprocess.run(
                                    crea_enlace_simbolico_cmd,
                                    capture_output=True,
                                    text=True
                                )
                                if not result.stderr == '':
                                    if dry:
                                        self.cron_ventana.wm_attributes(
                                            '-topmost',
                                            False
                                        )
                                    tmp_msg = ('Error creando enlaces '
                                               'simbólicos en el servidor')
                                    messagebox.showerror(
                                        title=self.titulo_app,
                                        message=self._(tmp_msg))
                                    if dry:
                                        self.cron_ventana.wm_attributes(
                                            '-topmost',
                                            True
                                        )
                                        self.txt_lbl_stat_crom.set('')

                            comando_lst = [
                                'rsync', '-avP', '-e',
                                'sshpass -p ' + passw +
                                ' ssh -p ' + pto_remoto,
                                '--link-dest=' + enlace_a_chequear,
                                item_a_copiar,
                                directorio_destino_ruta_completa
                            ]
                        else:
                            comando_lst = [
                                'rsync', '-avP', '-e',
                                'sshpass -p ' + passw +
                                ' ssh -p ' + pto_remoto,
                                item_a_copiar,
                                directorio_destino_ruta_completa
                                        ]
                    else:
                        directorio_destino_ruta_completa = directorio_destino
                        comando_lst = ['rsync', '-avP', '-e',
                                       'sshpass -p ' + passw +
                                       ' ssh -p ' + pto_remoto, item_a_copiar,
                                       directorio_destino_ruta_completa
                        ]

                else:
                    pto_remoto = (
                        self.puerto_remoto_txtbox.get('1.0', 'end').strip()
                    )

                    if os.path.isdir(item_a_copiar):
                        directorio_destino_ruta_completa = ''
                        item_a_copiar += '/'
                        item_a_copiar_cadena_final = (
                            item_a_copiar.split('/'))[-2]
                        directorio_destino_ruta_completa = (
                                directorio_destino + '/'
                                + item_a_copiar_cadena_final + '/'
                        )
                        buffer_enlace = (
                            directorio_destino_ruta_completa.split(":"))[-1]
                        enlace_a_chequear = (
                                "~/" +
                                buffer_enlace[:len(buffer_enlace) - 1] +
                                "_latest"
                        )

                        fichero_simbolico = enlace_a_chequear.split("/")[-1]
                        if self.opcion_incremental_var.get() == 'True':

                            self.log_txtbox.insert(tkinter.INSERT, '\n')
                            self.log_txtbox.insert(
                                tkinter.INSERT,
                                self._('Chequeando enlace remoto ') +
                                enlace_a_chequear +
                                ' ---> ' +
                                directorio_destino_ruta_completa +
                                '\n'
                            )
                            self.log_txtbox.insert(tkinter.INSERT, '\n')
                            self.log_txtbox.update()

                            usuario_ip = (
                                directorio_destino_ruta_completa.split(":"))[0]
                            chequea_enlace_simbolico_cmd = [
                                'ssh', '-p', pto_remoto,
                                usuario_ip,
                                "if [ -L " + enlace_a_chequear + " ]; "
                                        "then  echo Existe  enlace " +
                                        fichero_simbolico + " ; fi"]

                            result = subprocess.run(
                                chequea_enlace_simbolico_cmd,
                                capture_output=True,
                                text=True)

                            if not result.stderr == '':
                                if dry:
                                    self.cron_ventana.wm_attributes(
                                        '-topmost',
                                        False
                                    )
                                tmp_msg = ('Error verificando enlaces'
                                           ' simbólicos en destino')
                                messagebox.showerror(
                                    title=self.titulo_app,
                                    message=self._(tmp_msg)
                                )
                                if dry:
                                    self.cron_ventana.wm_attributes(
                                        '-topmost',
                                        True
                                    )
                                    self.txt_lbl_stat_crom.set('')

                            if "Existe enlace" in result.stdout:
                                self.log_txtbox.insert(tkinter.INSERT, '\n')
                                self.log_txtbox.insert(
                                    tkinter.INSERT,
                                    self._('Existe enlace remoto ') +
                                    enlace_a_chequear +
                                    ' ---> ' +
                                    directorio_destino_ruta_completa +
                                    ':' +
                                    enlace_a_chequear +
                                    '\n')
                                self.log_txtbox.insert(tkinter.INSERT, '\n')
                                self.log_txtbox.update()
                            else:

                                enlace_a_crear = enlace_a_chequear
                                origen_enlace_simbolico = (
                                    enlace_a_chequear.replace('_latest', '/')
                                )

                                self.log_txtbox.insert(tkinter.INSERT, '\n')
                                self.log_txtbox.insert(
                                    tkinter.INSERT,
                                    self._('Creando enlace remoto ') +
                                    enlace_a_crear +
                                    ' ---> ' +
                                    directorio_destino_ruta_completa +
                                    '\n'
                                )
                                self.log_txtbox.insert(tkinter.INSERT, '\n')
                                self.log_txtbox.update()

                                crea_enlace_simbolico_cmd = [
                                    'ssh', '-p', pto_remoto, usuario_ip,
                                    'ln -s ' + origen_enlace_simbolico,
                                    enlace_a_crear
                                ]
                                result = subprocess.run(
                                    crea_enlace_simbolico_cmd,
                                    capture_output=True,
                                    text=True
                                )

                                if not result.stderr == '':
                                    if dry:
                                        self.cron_ventana.wm_attributes(
                                            '-topmost',
                                            False
                                        )
                                    msg_tmp = ('Error creando enlaces'
                                               ' simbólicos en el servidor')
                                    messagebox.showerror(
                                        title=self.titulo_app,
                                        message=self._(msg_tmp))
                                    if dry:
                                        self.cron_ventana.wm_attributes(
                                            '-topmost',
                                            True
                                        )
                                        self.txt_lbl_stat_crom.set('')

                            comando_lst = [
                                'rsync', '-avP', '-e',
                                ' ssh -p ' + pto_remoto,
                                '--link-dest=' +  enlace_a_chequear,
                                item_a_copiar,
                                directorio_destino_ruta_completa
                            ]
                        else:
                            comando_lst = [
                                'rsync', '-avP', '-e',
                                ' ssh -p ' + pto_remoto,
                                item_a_copiar,
                                directorio_destino_ruta_completa
                            ]
                    else:
                        directorio_destino_ruta_completa = directorio_destino
                        comando_lst = ['rsync', '-avP',
                                       '-e', ' ssh -p ' +
                                       pto_remoto, item_a_copiar,
                                       directorio_destino_ruta_completa
                        ]

            indice_lista = 1
            if self.opcion_delete_var.get() == 'True':
                indice_lista += 1
                tmp = comando_lst[:]
                tmp.insert(indice_lista, '--delete')
                comando_lst = tmp.copy()

            if self.opcion_comprimir_var.get() == 'True':
                tmp = comando_lst[:]
                tmp[1] = tmp[1] + 'z'
                comando_lst = tmp.copy()

            if (self.opcion_enlaces_simbolicos_var.get() ==
                    'mantener_enlaces_simbolicos'):
                tmp = comando_lst[:]
                tmp.insert(3, '--links')
                comando_lst = tmp.copy()

            if (self.opcion_enlaces_simbolicos_var.get() ==
                    'copiar_archivos_enlazados'):
                indice_lista += 1
                tmp = comando_lst[:]
                tmp.insert(indice_lista, '--copy-links')
                comando_lst = tmp.copy()

            comando_lst_str = ''
            for items_seleccionados in comando_lst:
                comando_lst_str += items_seleccionados.strip() + ' '

            if dry:
                self.comandos_para_cron_lst.append(comando_lst_str.strip())
                continue

            if not len(self.log_txtbox.get('1.0', tkinter.END)) > 0:
                self.log_txtbox.insert(tkinter.INSERT, '\n')

            self.texto_etiqueta_mensaje_de_estado.set(
                self._("Ejecutando la copia de ") +
                item_a_copiar
            )

            self.log_txtbox.insert(tkinter.INSERT, '\n')

            if not self.password == '' and self.password in comando_lst_str:
                comando_lst_str=comando_lst_str.replace(
                    self.password, '*********'
                )

            self.log_txtbox.insert(
                tkinter.INSERT,
                self._("Ejecutando ") + comando_lst_str
            )

            self.log_txtbox.insert(tkinter.INSERT, '\n')
            self.log_txtbox.update()

            result = subprocess.run(
                comando_lst,
                capture_output=True,
                text=True
            )
            if result.stderr != '':
                self.log_txtbox.insert(
                    tkinter.INSERT,
                    '\n' + 37 * '*' +
                    ' ERROR ' + 38 * '*'
                )
                self.log_txtbox.insert(tkinter.INSERT, result.stderr)
                self.log_txtbox.update()

                if 'Connection refused' in result.stderr:
                    self.texto_etiqueta_mensaje_de_estado.set(
                        self._('Conexión rehusada')
                    )
                    if dry:
                        self.cron_ventana.wm_attributes('-topmost', False)
                    tmp_msg = 'Conexión rehusada Abandonando la copia'
                    messagebox.showerror(
                        title=self.titulo_app,
                        message=self._(tmp_msg))
                    if dry:
                        self.cron_ventana.wm_attributes('-topmost', True)
                        self.txt_lbl_stat_crom.set('')
                    return None

                if 'No route to host' in result.stderr:
                    self.texto_etiqueta_mensaje_de_estado.set(
                        self._('No hay acceso al host')
                    )
                    if dry:
                        self.cron_ventana.wm_attributes('-topmost', False)
                    tmp_msg = 'No hay acceso al host Abandonando la copia'
                    messagebox.showerror(
                        title=self.titulo_app,
                        message=self._(tmp_msg)
                    )
                    if dry:
                        self.cron_ventana.wm_attributes('-topmost', True)
                        self.txt_lbl_stat_crom.set('')
                    return None

                if 'Permission denied' in result.stderr:
                    self.texto_etiqueta_mensaje_de_estado.set(
                        self._('Permiso denegado')
                    )
                    if dry:
                        self.cron_ventana.wm_attributes('-topmost', False)
                    tmp_msg = 'Permiso denegado Abandonando la copia'
                    messagebox.showerror(
                        title=self.titulo_app,
                        message=self._(tmp_msg))
                    if dry:
                        self.cron_ventana.wm_attributes('-topmost', True)
                        self.txt_lbl_stat_crom.set('')

                    return None

                if 'Connection reset' in result.stderr:
                    self.texto_etiqueta_mensaje_de_estado.set(
                        self._('Reset en la conexión')
                    )
                    messagebox.showerror(
                        title=self.titulo_app,
                        message=self._('Reset en la conexión '
                                       'Abandonando la copia'))
                    return None

                self.texto_etiqueta_mensaje_de_estado.set(
                    self._('Error en el proceso')
                )
                if dry:
                    self.cron_ventana.wm_attributes('-topmost', False)
                messagebox.showerror(
                    title=f"{self.titulo_app}",
                    message=self._('Error en el proceso'
                                   ' Abandonando la copia'))
                if dry:
                    self.cron_ventana.wm_attributes('-topmost', True)
                    self.txt_lbl_stat_crom.set('')
                return None
            else:
                self.log_txtbox.insert(tkinter.INSERT, '\n')
                self.log_txtbox.insert(
                    tkinter.INSERT,
                    self._('Sincronizando ') +
                    ' ' +
                    item_a_copiar +
                    ' --> ' +
                    directorio_destino +
                    '\n'
                )
                self.log_txtbox.insert(tkinter.INSERT, result.stdout)
                self.log_txtbox.insert(tkinter.INSERT, '\n')
                self.log_txtbox.insert(tkinter.INSERT, 111*'-')
                self.log_txtbox.update()

                fichero_log = open("raven_backup.log", "a")
                cadena_a_escribir = (
                        item_a_copiar +
                        " --> " +
                        directorio_destino +
                        " date-time: " +
                        datetime.datetime.now().strftime(
                            "%d/%m/%Y %H:%M:%S"
                        ) +
                        " Ok!"
                )

                fichero_log.write(cadena_a_escribir)
                fichero_log.write('\n')
                fichero_log.write(70 * '=')
                fichero_log.write(2 * '\n')
                fichero_log.close()

            self.directorios_seleccionados_lstbox.itemconfig(
                indice-1,
                bg="white"
            )

        if dry:  
            return self.comandos_para_cron_lst
        else:
            self.texto_etiqueta_mensaje_de_estado.set(
                self._('Copia finalizada')
            )

    def guarda_lista_items_seleccionados(self):

        tmp_var = self.directorio_destino_txtbox.get('1.0', 'end')
        if not (tmp_var.strip().find(':') == -1):
            if self.puerto_remoto_txtbox.get('1.0', 'end').strip() == '':
                messagebox.showinfo(
                    title=f"{self.titulo_app}",
                    message=self._('Debe asignar un valor de puerto remoto'
                                   ' para un destino remoto'))
                return None

            if (self.tipo_acceso_var.get() == 'password' and
                    self.password_var.get() == ''):

                messagebox.showinfo(
                    title=self.titulo_app,
                    message=self._('Debe asignar un valor de '
                                   'password para acceso con password'))

                return None


        opcion_delete_cambio = (
                self.opcion_delete_inicial_str !=
                self.opcion_delete_var.get()
        )
        opcion_comprimir_cambio = (
                self.opcion_comprimir_inicial_str !=
                self.opcion_comprimir_var.get()
        )
        opcion_enlaces_cambio = (
                self.opcion_enlaces_simbolicos_inicial_str !=
                self.opcion_enlaces_simbolicos_var.get()
        )
        opcion_incremental_cambio = (
                self.opcion_incremental_inicial_str !=
                self.opcion_incremental_var.get()
        )
        hay_cambios = (
                self.modificacion_de_items
                or opcion_delete_cambio
                or opcion_comprimir_cambio
                or opcion_enlaces_cambio
                or opcion_incremental_cambio
        )
        if not hay_cambios:
            self.texto_etiqueta_mensaje_de_estado.set(
                self._('No hay cambios que guardar')
            )
            self.cuenta_atras(0)
            return None

        self.comprueba_existencia_en_origen()
        directorios_seleccionados_tupla = (
            self.directorios_seleccionados_lstbox.get('0', 'end')
        )
        directorio_destino = (
            self.directorio_destino_txtbox.get('1.0', 'end').strip()
        )

        if (len(directorios_seleccionados_tupla) == 0
                or len(directorio_destino) == 0):
            if len(directorios_seleccionados_tupla) == 0:
                messagebox.showinfo(
                    title=f"{self.titulo_app}",
                    message=self._('No existen ficheros o directorios '
                                   'de origen para guardar'))
            if len(directorio_destino) == 0:
                messagebox.showinfo(
                    title=f"{self.titulo_app}",
                    message=self._('No existe directorio de '
                                   'destino para guardar'))
            return None

        file = filedialog.asksaveasfile(
            filetypes=(
                ("Configuration files", "*.conf"),
                ("Configuration files", "*.conf")),
            defaultextension='.conf',
            confirmoverwrite=True)

        if file is None:
            return None
        fichero_configuracion = open(file.name.split("/")[-1], 'w')
        for f in range(len(directorios_seleccionados_tupla)):
            fichero_configuracion.write(directorios_seleccionados_tupla[f])
            if f < len(directorios_seleccionados_tupla)-1:
                fichero_configuracion.write(',')
        fichero_configuracion.write('\n')



        if directorio_destino.find(':') == -1:
            fichero_configuracion.write(directorio_destino)
            fichero_configuracion.write('\n')
        else:
            puerto_remoto = self.puerto_remoto_txtbox.get('1.0', 'end').strip()
            password = self.password_entrybox.get().strip()
            tipo_acceso = self.tipo_acceso_var.get()
            if password:
                password_encriptada = (
                    self.cipher.encrypt(password.encode()).decode()
                )
            else:
                password_encriptada = ''

            _dict = ("{'destino':" + "'" + directorio_destino + "'"
                     + ',' + "'puerto_remoto':" + "'" + puerto_remoto + "'"
                     + ',' + "'tipo_acceso':" + "'" + tipo_acceso + "'"
                     + ',' + "'password':" + "'" + password_encriptada + "'"
                     + "}")

            fichero_configuracion.write(_dict)
            fichero_configuracion.write('\n')

        if self.opcion_delete_var.get() == '':
            self.opcion_delete_var.set('False')
        _dict = "{'delete':" + "'" + self.opcion_delete_var.get() + "'" + "}"
        fichero_configuracion.write(_dict)
        fichero_configuracion.write('\n')
        if self.opcion_comprimir_var.get() == '':
            self.opcion_comprimir_var.set('False')
        _dict = ("{'comprimir_durante_copia':" +
                 "'" +
                 self.opcion_comprimir_var.get() +
                 "'" +
                 "}")
        fichero_configuracion.write(_dict)
        fichero_configuracion.write('\n')

        if self.opcion_enlaces_simbolicos_var.get() == '':
            self.opcion_enlaces_simbolicos_var.set(
                'copiar_archivos_enlazados')
        _dict = ("{'tratamiento_archivos_enlazados':" +
                 "'" +
                 self.opcion_enlaces_simbolicos_var.get() +
                 "'" +
                 "}")

        fichero_configuracion.write(_dict)
        fichero_configuracion.write('\n')

        if self.opcion_incremental_var.get() == '':
            self.opcion_incremental_var.set('False')
        _dict = ("{'copia_incremental':" +
                 "'" +
                 self.opcion_incremental_var.get()
                 + "'"
                 + "}")
        fichero_configuracion.write(_dict)
        fichero_configuracion.write('\n')

        if not self.idioma_seleccionado == '':
            fichero_configuracion.write(self.idioma_seleccionado)
        else:
            fichero_configuracion.write(self.idioma_defecto)

        fichero_configuracion.close()
        self.texto_etiqueta_mensaje_de_estado.set(
            self._('La selección ha sido guardada')
        )
        self.cuenta_atras(0)

        self.modificacion_de_items = False
        self.opcion_comprimir_inicial_str = self.opcion_comprimir_var.get()
        self.opcion_delete_inicial_str = self.opcion_delete_var.get()

        self.opcion_enlaces_simbolicos_inicial_str = (
            self.opcion_enlaces_simbolicos_var.get()
        )

        self.opcion_incremental_inicial_str = (
            self.opcion_incremental_var.get()
        )

        self.directorio_destino_inicial_str = (
            self.directorio_destino_txtbox.get('1.0', 'end').strip()
        )
        self.puerto_remoto_inicial_str = (
            self.puerto_remoto_txtbox.get('1.0', 'end').strip()
        )
        self.password_var_inicial_str = self.password_var.get()
        self.tipo_acceso_var_inicial_str = self.tipo_acceso_var.get()

        shutil.copy(file.name.split("/")[-1], '.raven_backup.conf')

    def cambiar_configuracion(self):

        fichero_temporal = (
            (filedialog.askopenfilename(
                filetypes=[("Configuration files", "*.conf")],
                title=self._("Seleccione un fichero de configuración")))
        )
        if len(fichero_temporal) == 0:
            return
        fichero_temporal = fichero_temporal.split("/")[-1]
        f_a_comparar = fichero_temporal.split(".")[0].strip()
        if f_a_comparar == self.nombre_fichero_configuracion_actual.strip():
            messagebox.showinfo(
                title=self._('Información'),
                message=self._('Su elección ya es la configuración actual')
            )
            return
        respuesta = askyesno(
            title=self._('Confirmación'),
            message=self._('¿Confirma que los parámetros del fichero ') +
                            fichero_temporal +
                            self._(' sean aplicados como actuales?')
        )
        if respuesta:
            shutil.copy(fichero_temporal, '.raven_backup.conf')
            self.texto_etiqueta_mensaje_de_estado.set(
                self._('El fichero ') +
                fichero_temporal +
                self._(' es ahora el fichero de parámetros'))
            self.cuenta_atras(0)
            self.reinicia_gui()

    def comprueba_existencia_en_origen(self):


        directorios_seleccionados_tupla = \
            self.directorios_seleccionados_lstbox.get('0', 'end')
        for item_ in directorios_seleccionados_tupla:
            item_ = item_.strip()
            if not os.path.exists(item_):
                if (self.cron_ventana is not None
                        and self.cron_ventana.winfo_exists() == 1):
                    self.cron_ventana.wm_attributes('-topmost', False)
                messagebox.showinfo(
                    title=self._('Confirmación'),
                    message=(
                            self._('El item de origen ') +
                            item_ +
                            self._(' no existe\n') +
                            self._('Se eliminará de la lista'))
                )

                if self.cron_ventana is not None and \
                        self.cron_ventana.winfo_exists() == 1:
                    self.cron_ventana.wm_attributes('-topmost', True)
                indice_item = \
                    (
                     self.directorios_seleccionados_lstbox.
                     get(0, 'end').
                     index(item_)
                    )
                self.directorios_seleccionados_lstbox.delete(indice_item)

                self.modificacion_de_items = True
                directorio_destino = \
                    self.directorio_destino_txtbox.get('1.0', 'end').strip()

                item_ = item_[item_.rfind('/') + 1:]
                if os.path.exists(directorio_destino + '/' + item_):
                    respuesta = askyesno(
                        title=f"{self._('Confirmación')}",
                        message=f"{self._('El item de origen ')}"
                                f"{item_} {self._(' existe en destino\n')}"
                                f"{self._('¿Desea eliminar en destino?')}"
                    )
                    if respuesta:
                        if os.path.isfile(directorio_destino + '/' + item_):
                            os.remove(directorio_destino + '/' + item_)
                        if os.path.isdir(directorio_destino + '/' + item_):
                            shutil.rmtree(directorio_destino + '/' + item_)

    def selecciona_directorios_origen(self):

        directorio_origen = filedialog.askdirectory()
        directorio_en_listbox_bool = False

        for tmp in range(self.directorios_seleccionados_lstbox.size()):
            tmp_d_s = self.directorios_seleccionados_lstbox.get(tmp)
            if directorio_origen == tmp_d_s:
                directorio_en_listbox_bool = True
                messagebox.showinfo(
                    title=f"{self.titulo_app}",
                    message=self._('El directorio ya existe en la selección')
                )
                break
        if not len(directorio_origen) == 0 and not directorio_en_listbox_bool:
            (
                self.directorios_seleccionados_lstbox.insert
                ('end', directorio_origen)
            )
            self.modificacion_de_items = True

    def selecciona_ficheros_origen(self):

        fichero_origen = filedialog.askopenfilename()
        fichero_en_listbox_bool = False

        for tmp in range(self.directorios_seleccionados_lstbox.size()):
            tmp_d_s = self.directorios_seleccionados_lstbox.get(tmp)
            if fichero_origen == tmp_d_s:
                fichero_en_listbox_bool = True
                messagebox.showinfo(
                    title=f"{self.titulo_app}",
                    message=self._('El fichero ya existe en la selección')
                )
            break

        if not len(fichero_origen) == 0 and not fichero_en_listbox_bool:
            self.directorios_seleccionados_lstbox.insert(
                'end', fichero_origen
            )
            self.modificacion_de_items = True

    def selecciona_destino(self):

        directorio_destino = filedialog.askdirectory()
        if not len(directorio_destino) == 0:
            self.directorio_destino_txtbox.delete('1.0', 'end')
            self.directorio_destino_txtbox.insert('end', directorio_destino)
            self.modificacion_de_items = True

    def elimina_items_seleccionados(self):

        if self.item_seleccionado is not None:
            for i in self.directorios_seleccionados_lstbox.curselection():
                self.items_eliminados_lst.append(
                    self.directorios_seleccionados_lstbox.get(i)
                )

            self.directorios_seleccionados_lstbox.delete(
                self.item_seleccionado[0]
            )
            self.modificacion_de_items = True
        else:
            messagebox.showinfo(
                title=f"{self.titulo_app}",
                message=self._('No hay items seleccionados para eliminar')
            )

    def comprueba_cambios_y_salir(self):

        if self.hilo_copia is not None:
            if self.hilo_copia.is_alive():
                messagebox.showinfo(
                    title=f"{self.titulo_app}",
                    message=self._('Se está ejecutando un proceso de copia.\n'
                                   'No se detiene el proceso')
                )
                return None

        if (self.modificacion_de_items or self.modificacion_checkboxes
                or self.modificacion_radiobotones_ficheros_con_enlaces):
            respuesta = askyesno(
                title=self._('Confirmación'),
                message=self._('¿Guardar los cambios antes de salir?')
            )
            if respuesta:
                self.guarda_lista_items_seleccionados()
                return

        respuesta = askyesno(
            title=self._('Confirmación'),
            message=self._('¿Desea salir de Raven Backup?')
        )

        if respuesta:
            quit(0)

    def cambia_color_label_delete(self):

        if self.opcion_delete_var.get() == 'True':
            self.option_delete_chkbtn.config(fg=self.color_rojo)
        else:
            self.option_delete_chkbtn.config(fg=self.color_negro)

    def chequea_seleccion_previa_item(self, event):

        if len(self.directorios_seleccionados_lstbox.curselection()) != 0:
            tmp_item_sel = self.item_seleccionado
            tmp_dir_sel = self.directorios_seleccionados_lstbox.curselection()
            if tmp_item_sel == tmp_dir_sel:
                self.directorios_seleccionados_lstbox.selection_clear(0, 'end')

        self.item_seleccionado = (
            self.directorios_seleccionados_lstbox.curselection())

    def limpia_log(self):

        self.log_txtbox.delete('1.0', tkinter.END)

    def chequea_modificacion_destino(self, event):

        tmp_dest_ini = self.directorio_destino_inicial_str
        tmp_dest_text = (
            self.directorio_destino_txtbox.get('1.0', 'end').strip()
        )
        if tmp_dest_ini == tmp_dest_text:
            self.modificacion_de_items = False
        else:
            self.modificacion_de_items = True

    def chequea_comprimir_durante_copia(self):

        tmp_comp_var = self.opcion_comprimir_var.get()
        tmp_comp_ini = self.opcion_comprimir_inicial_str
        if tmp_comp_var == tmp_comp_ini:
            self.modificacion_checkboxes = False
        else:
            self.modificacion_checkboxes = True

    def chequea_modificacion_copia_incremental(self, event):

        if self.opcion_incremental_var.get() == \
                self.opcion_incremental_inicial_str:
            self.modificacion_checkboxes = False
        else:
            self.modificacion_checkboxes = True

        if self.opcion_incremental_var.get() == 'True':
            messagebox.showinfo(
                title=f"{self.titulo_app}",
                message=f"{self._('Advertencia: rsync no admite copia'
                                  ' incremental para ficheros')}  \n"
                        f"{self._('Si lo desea cree una carpeta e'
                                  ' introduzca los ficheros')}  \n"
                        f"{self._('en ella, después seleccione esta'
                                  ' carpeta para copiar')}"
            )

    def chequea_modificacion_puerto_remoto(self, event):

        if self.directorio_destino_txtbox.get('1.0', 'end').find(':') == -1:
            messagebox.showinfo(
                title=f"{self.titulo_app}",
                message=self._('No se guardarán parámetros'
                               ' remotos para copia local'))
            self.puerto_remoto_txtbox.delete('1.0', tkinter.END)
            self.root.focus()
            return None

        if self.puerto_remoto_inicial_str == \
                self.puerto_remoto_txtbox.get('1.0', 'end').strip():
            self.modificacion_de_items = False
        else:
            self.modificacion_de_items = True

    def chequea_modificacion_password(self, event):

        if self.directorio_destino_txtbox.get('1.0', 'end').find(':') == -1:
            messagebox.showinfo(
                title=f"{self.titulo_app}",
                message=self._('No se guardarán parámetros '
                               'remotos para copia local')
            )
            self.puerto_remoto_txtbox.delete('1.0', tkinter.END)
            self.password_var.set('')
            self.root.focus()
            return None

        if self.tipo_acceso_var.get() == 'clave_publica':
            messagebox.showinfo(
                title=f"{self.titulo_app}",
                message=f"{self._('Clave pública: no se guarda contraseña')}"
            )
            self.password_var.set('')
            self.root.focus()
            return None

        if self.password_var_inicial_str == self.password_var.get():
            self.modificacion_de_items = False
        else:
            self.modificacion_de_items = True

    def chequea_modificacion_tipo_acceso(self, event=None):

        if self.directorio_destino_txtbox.get('1.0', 'end').find(':') == -1:
            messagebox.showinfo(
                title=f"{self.titulo_app}",
                message=self._('No se guardarán parámetros'
                               ' remotos para copia local')
            )
            self.puerto_remoto_txtbox.delete('1.0', tkinter.END)
            self.tipo_acceso_var.set(self.tipo_acceso_var_inicial_str)
            self.root.focus()
            return None

        usa_clave = self.tipo_acceso_var.get() == 'clave_publica'
        passwd_llena = self.password_var.get() != ''

        if usa_clave and passwd_llena:
            messagebox.showinfo(
                title=f"{self.titulo_app}",
                message=self._('Clave pública: no se guarda contraseña')
            )
            self.password_var.set('')
            self.modificacion_de_items = True
            self.root.focus()
            return None

        if self.tipo_acceso_var_inicial_str == self.tipo_acceso_var.get():
            self.modificacion_de_items = False
        else:
            self.modificacion_de_items = True

    def rellena_datos(self):

        if not self.destino.find(':') == -1:
            self.puerto_remoto_txtbox.insert(
                tkinter.INSERT,
                self.puerto_remoto
            )
            self.password_entrybox.insert(0, self.password)

        if not len(self.origen_lst) == 0:
            for item in range(len(self.origen_lst)):
                self.directorios_seleccionados_lstbox.insert(
                    'end',
                    self.origen_lst[item].strip()
                )

        if not len(self.destino) == 0:
            if self.destino.find(':') == -1:
                self.directorio_destino_txtbox.insert(
                    tkinter.INSERT,
                    self.destino
                )
            else:
                self.directorio_destino_txtbox.insert(
                    tkinter.INSERT,
                    self.destino_ip
                )

        self.enlaces_simbolicos_mantener_enlace_radiobtn.configure(
            variable=self.opcion_enlaces_simbolicos_var, )

        self.enlaces_simbolicos_copiar_fichero_radiobtn.configure(
            variable=self.opcion_enlaces_simbolicos_var, )

        self.clave_publica_radiobtn.configure(
            variable=self.tipo_acceso_var,)

        self.password_radiobtn.configure(
            variable=self.tipo_acceso_var,)

        self.option_comprimir_chkbtn.configure(
            variable=self.opcion_comprimir_var,)

        self.option_incremental_chkbtn.configure(
            variable=self.opcion_incremental_var,)

        self.option_delete_chkbtn.configure(
            variable=self.opcion_delete_var,)

    def chequea_modificacion_enlaces_simbolicos(self):

        if (self.opcion_enlaces_simbolicos_var.get() ==
                self.opcion_enlaces_simbolicos_inicial_str):
            self.modificacion_radiobotones_ficheros_con_enlaces = False
        else:
            self.modificacion_radiobotones_ficheros_con_enlaces = True

    def chequea_eliminar_en_destino(self):

        if self.opcion_delete_inicial_str == self.opcion_delete_var.get():
            self.modificacion_checkboxes = False
        else:
            self.modificacion_checkboxes = True

    def crea_elementos_graficos(self):

        self.log_txtbox_frame = tkinter.Frame(self.root)

        self.dir_selected_lstbox_frame = tkinter.Frame(self.root)

        self.left_buttons_frame = tkinter.Frame(self.root)


        self.log_txtbox_frame.place(x=490, y=205, height=450, width=690)
        self.dir_selected_lstbox_frame.place(x=35, y=55, height=160, width=430)
        self.left_buttons_frame.place(x=28, y=418, height=100, width=430)

        opciones_remoto_lf = LabelFrame(
            self.root,
            text=self._('Opciones Remoto'),
            width=370,
            height=75,
            font=("TkDefaultFont", 12)
        )
        opciones_remoto_lf.place(x=810, y=95)

        tipo_acceso_lf = LabelFrame(
            self.root,
            text=self._('Tipo de Acceso Remoto'),
            width=288,
            height=60,
            font=("TkDefaultFont", 12)
        )
        tipo_acceso_lf.place(x=490, y=100)

        opciones_ficheros_enlazados_lf = LabelFrame(
            self.root,
            text=self._('Opciones para ficheros enlazados'),
            width=350,
            height=90,
            font=("TkDefaultFont", 12)
        )
        opciones_ficheros_enlazados_lf.place(x=35, y=230)

        self.enlaces_simbolicos_mantener_enlace_radiobtn = Radiobutton(
            opciones_ficheros_enlazados_lf,
            text=self._('Rsync enlaces simbólicos'),
            value='mantener_enlaces_simbolicos',
            command=self.chequea_modificacion_enlaces_simbolicos,
            font=("TkDefaultFont", 12))
        self.enlaces_simbolicos_mantener_enlace_radiobtn.place(x=6, y=4)

        self.enlaces_simbolicos_copiar_fichero_radiobtn = Radiobutton(
            opciones_ficheros_enlazados_lf,
            text=self._('Rsync archivos enlazados'),
            value='copiar_archivos_enlazados',
            command=self.chequea_modificacion_enlaces_simbolicos,
            font=("TkDefaultFont", 12))
        self.enlaces_simbolicos_copiar_fichero_radiobtn.place(x=6, y=30)

        self.password_radiobtn = Radiobutton(
            tipo_acceso_lf,
            text='Password',
            value='password',
            font=("TkDefaultFont", 12))
        self.password_radiobtn.place(x=2, y=4)
        self.password_radiobtn.bind(
            '<ButtonRelease>',
            self.chequea_modificacion_tipo_acceso
        )

        self.clave_publica_radiobtn = Radiobutton(
            tipo_acceso_lf,
            text=self._('Clave pública'),
            value='clave_publica',
            command=self.chequea_modificacion_tipo_acceso,
            font=("TkDefaultFont", 12))
        self.clave_publica_radiobtn.place(x=125, y=4)

        Label(
            self.root,
            text=self._('Directorios y ficheros de origen seleccionados'),
            font=("TkDefaultFont", 12)
        ).place(x=35, y=25)

        Label(
            self.root,
            text=self._('Destino seleccionado (Local/Remoto)'),
            font=("TkDefaultFont", 12)
        ).place(x=490, y=25)

        Label(
            self.root,
            text=self._('Log del proceso'),
            font=("TkDefaultFont", 12)
        ).place(x=490, y=180)

        Label(
            self.root,
            text=self._('Línea de mensajes:'),
            font=("TkDefaultFont", 12)
        ).place(x=37, y=515)

        Label(
            opciones_remoto_lf,
            text=self._('Puerto Remoto'),
            font=("TkDefaultFont", 11)
        ).place(x=10, y=10)

        Label(
            opciones_remoto_lf,
            text=self._('Password'),
            font=("TkDefaultFont", 11)
        ).place(x=192, y=10)

        mensaje_de_estado_lbl = Label(
            self.root,
            textvariable=self.texto_etiqueta_mensaje_de_estado,
            font=(font.Font(None, size=11, weight="bold"))
        )

        if self.idioma_seleccionado == 'es':
            x_pos = 195
        else:
            x_pos = 155
        mensaje_de_estado_lbl.place(x=x_pos, y=515)

        self.directorios_seleccionados_lstbox = Listbox(
            self.dir_selected_lstbox_frame,
            width=40,
            height=6,
            font=("TkDefaultFont", 12),
            selectmode='multiple')
        self.directorios_seleccionados_lstbox.grid(
            row=0,
            column=0,
            sticky=tkinter.EW
        )
        self.directorios_seleccionados_lstbox.bind(
            '<<ListboxSelect>>',
            self.chequea_seleccion_previa_item
        )

        self.directorio_destino_txtbox = Text(
            self.root,
            height=1,
            width=39,
            font=("TkDefaultFont", 12)
        )
        self.directorio_destino_txtbox.place(x=490, y=50)
        self.directorio_destino_txtbox.bind(
            '<KeyRelease>',
            self.chequea_modificacion_destino
        )

        self.puerto_remoto_txtbox = Text(
            opciones_remoto_lf,
            height=1,
            width=5,
            font=("TkDefaultFont", 11)
        )

        self.puerto_remoto_txtbox.place(x=128, y=8)
        self.puerto_remoto_txtbox.bind(
            '<KeyRelease>',
            self.chequea_modificacion_puerto_remoto
        )

        self.password_entrybox = Entry(
            opciones_remoto_lf,
            width=8,
            show='*',
            textvariable=self.password_var,
            font=("TkDefaultFont", 11)
        )

        self.password_entrybox.place(x=273, y=8)

        self.password_entrybox.bind(
            '<KeyRelease>',
            self.chequea_modificacion_password
        )

        self.log_txtbox = Text(
            self.log_txtbox_frame,
            height=11,
            width=73,
            font=("TkDefaultFont", 12)
        )
        self.log_txtbox.grid(row=0, column=0, sticky=tkinter.EW)

        scrollbar_0 = Scrollbar(
            self.dir_selected_lstbox_frame,
            orient='vertical',
            command=self.directorios_seleccionados_lstbox.yview)

        scrollbar_0.grid(row=0, column=1, sticky=tkinter.NS)
        self.directorios_seleccionados_lstbox[
            'yscrollcommand'] = scrollbar_0.set

        scrollbar = Scrollbar(
            self.log_txtbox_frame,
            orient='vertical',
            width=16,
            command=self.log_txtbox.yview
        )

        scrollbar.grid(row=0, column=1, sticky=tkinter.NS)
        self.log_txtbox['yscrollcommand'] = scrollbar.set
        self.option_delete_chkbtn = Checkbutton(
            self.root,
            text=self._(' Eliminar en destino si ha sido borrado en origen'),
            font=("TkDefaultFont", 12),
            onvalue='True',
            offvalue='False',
            command=lambda: [
                self.chequea_eliminar_en_destino(),
                self.cambia_color_label_delete()
            ]
        )

        self.option_delete_chkbtn.place(x=30, y=332)

        self.option_comprimir_chkbtn = Checkbutton(
            self.root,
            text=self._(' Comprimir durante la copia'),
            font=("TkDefaultFont", 12),
            command=self.chequea_comprimir_durante_copia,
            onvalue='True',
            offvalue='False')
        self.option_comprimir_chkbtn.place(x=30, y=357)

        self.option_incremental_chkbtn = Checkbutton(
            self.root,
            text=self._('Copia incremental'),
            font=("TkDefaultFont", 12),
            onvalue='True',
            offvalue='False')
        self.option_incremental_chkbtn.place(x=30, y=383)
        self.option_incremental_chkbtn.bind(
            '<ButtonRelease>',
            self.chequea_modificacion_copia_incremental
        )

        self.cambia_color_label_delete()

        Button(
            self.left_buttons_frame,
            text=self._('Elegir ficheros'),
            command=self.selecciona_ficheros_origen,
            font=("TkDefaultFont", 12)
        ).grid(row=0, column=0, padx=3, pady=3)

        Button(
            self.left_buttons_frame,
            text=self._('Elegir directorios'),
            command=self.selecciona_directorios_origen,
            font=("TkDefaultFont", 12)
        ).grid(row=0, column=1, padx=3, pady=3)

        Button(
            self.left_buttons_frame,
            text=self._('Eliminar'),
            command=self.elimina_items_seleccionados,
            font=("TkDefaultFont", 12)
        ).grid(row=0, column=3, padx=3, pady=3)

        Button(
            self.root,
            text=self._('Elegir destino local'),
            command=self.selecciona_destino,
            font=("TkDefaultFont", 12)
        ).place(x=910, y=45)

        Button(
            self.left_buttons_frame,
            text=self._('Guardar'),
            width=11,
            command=self.guarda_lista_items_seleccionados,
            font=("TkDefaultFont", 12)
        ).grid(row=1, column=0, padx=3, pady=3)

        Button(
            self.left_buttons_frame,
            text=self._(' Iniciar copia '),
            width=14, command=self.lanzar_hilo_copia,
            font=("TkDefaultFont", 12)
        ).grid(row=1, column=1, padx=3, pady=3)

        Button(
            self.left_buttons_frame,
            text=self._('Salir'),
            width=6,
            command=self.comprueba_cambios_y_salir,
            font=("TkDefaultFont", 12)
        ).grid(row=1, column=3, padx=3, pady=3)

        Button(
            self.log_txtbox_frame,
            text=self._('Limpia Log'),
            width=8,
            command=self.limpia_log,
            font=("TkDefaultFont", 12)
        ).grid(row=1, column=0, padx=3, pady=20)

    def elimina_contenido_elementos_graficos(self):

        self.opcion_enlaces_simbolicos_var.set('')
        self.tipo_acceso_var.set('')
        self.password_var.set('')
        self.opcion_delete_var.set('')
        self.opcion_comprimir_var.set('')
        self.opcion_incremental_var.set('')
        self.origen_lst.clear()
        self.puerto_remoto = ''
        self.puerto_remoto_txtbox.delete("1.0", tkinter.END)
        self.directorios_seleccionados_lstbox.delete(0, tkinter.END)
        self.destino = ''
        self.directorio_destino_txtbox.delete("1.0", tkinter.END)


def main():

    rb: RavenBackup = RavenBackup()
    rb.compilar_po_a_mo()
    if rb.existe_fichero_configuracion:
        rb.crea_ventana_root()
        rb.lee_fichero_configuracion()
    else:
        rb.lee_fichero_configuracion()
        rb.crea_ventana_root()
    rb.crea_elementos_graficos()
    rb.rellena_datos()
    rb.crea_menus()
    rb.root.mainloop()


if __name__ == "__main__":
    main()
