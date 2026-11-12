"""Aplicación de Escritorio Nativa (Estilo Apple macOS Pro con Modo Claro y Modo Oscuro)
para BidFactory AI — Fábrica de Licitaciones.
Desarrollado por Tecknologia · Diseñado por Geologgia Ltda.
"""
from __future__ import annotations

import email
import json
import os
import shutil
import sys
import threading
import tkinter as tk
import webbrowser
from email import policy
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
    if not (BASE_DIR / "licitaciones").exists() and (BASE_DIR.parent / "licitaciones").exists():
        BASE_DIR = BASE_DIR.parent
else:
    BASE_DIR = Path(__file__).resolve().parent

SCRIPTS_DIR = BASE_DIR / "scripts"
LIC_DIR = BASE_DIR / "licitaciones"
sys.path.insert(0, str(SCRIPTS_DIR))

import armar_propuesta  # noqa: E402
import cartera  # noqa: E402
import extraer_texto  # noqa: E402
import informe_aprobacion  # noqa: E402
import leer_correos  # noqa: E402
import matriz_cumplimiento  # noqa: E402
import nueva_licitacion  # noqa: E402
import plantilla_costos  # noqa: E402

THEMES = {
    "light": {
        "bg_primary": "#F5F5F7",
        "bg_secondary": "#FFFFFF",
        "bg_tertiary": "#EFEFF4",
        "fg_primary": "#1D1D1F",
        "fg_secondary": "#515154",
        "fg_muted": "#86868B",
        "border": "#D2D2D7",
        "accent": "#0066CC",
        "accent_fg": "#FFFFFF",
        "btn_neutral_bg": "#E8E8ED",
        "btn_neutral_fg": "#1D1D1F",
        "console_bg": "#FAFAFC",
        "console_fg": "#1D1D1F",
    },
    "dark": {
        "bg_primary": "#000000",
        "bg_secondary": "#141416",
        "bg_tertiary": "#1C1C1E",
        "fg_primary": "#F5F5F7",
        "fg_secondary": "#A1A1A6",
        "fg_muted": "#6E6E73",
        "border": "#2C2C2E",
        "accent": "#0A84FF",
        "accent_fg": "#FFFFFF",
        "btn_neutral_bg": "#242426",
        "btn_neutral_fg": "#F5F5F7",
        "console_bg": "#0D0D0F",
        "console_fg": "#E5E5EA",
    },
}


class FabricaLicitacionesApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("BidFactory AI — Equipo de Licitaciones | Desarrollado por Tecknologia · Diseñado por Geologgia Ltda.")
        self.geometry("1160x760")
        self.minsize(1000, 680)

        ico_path = BASE_DIR / "geologgia_licitaciones.ico"
        if ico_path.exists():
            try:
                self.iconbitmap(str(ico_path))
            except Exception:
                pass

        self.theme_mode = "light"
        self.codigo_actual = tk.StringVar()
        self._img_refs: list[ImageTk.PhotoImage] = []
        self._build_ui()
        self.refrescar_lista_licitaciones()

    def _load_logo(self, filename: str, height: int = 26, pad_white: bool = False) -> ImageTk.PhotoImage | None:
        for folder in [BASE_DIR, BASE_DIR / "assets", BASE_DIR / "web"]:
            p = folder / filename
            if p.exists():
                try:
                    im = Image.open(p).convert("RGBA")
                    ratio = height / im.height
                    new_w = max(1, int(im.width * ratio))
                    im = im.resize((new_w, height), Image.Resampling.LANCZOS)
                    if pad_white:
                        bg = Image.new("RGBA", (new_w + 14, height + 8), (255, 255, 255, 255))
                        bg.paste(im, (7, 4), im)
                        im = bg
                    photo = ImageTk.PhotoImage(im)
                    self._img_refs.append(photo)
                    return photo
                except Exception:
                    return None
        return None

    def _build_ui(self) -> None:
        for w in self.winfo_children():
            w.destroy()
        self._img_refs.clear()

        t = THEMES[self.theme_mode]
        self.configure(bg=t["bg_primary"])

        # ---------------- BARRA SUPERIOR ESTILO APPLE HIG ----------------
        top = tk.Frame(self, bg=t["bg_secondary"], height=66, highlightbackground=t["border"], highlightthickness=1)
        top.pack(fill="x", side="top")

        brand_frame = tk.Frame(top, bg=t["bg_secondary"])
        brand_frame.pack(side="left", padx=20, pady=10)

        tk.Label(brand_frame, text="Desarrollado por", font=("Segoe UI", 8), fg=t["fg_muted"], bg=t["bg_secondary"]).pack(side="left", padx=(0, 6))
        logo_teck = self._load_logo("logo-tecknologia.png", height=24, pad_white=(self.theme_mode == "light"))
        if logo_teck:
            tk.Label(brand_frame, image=logo_teck, bg=t["bg_secondary"]).pack(side="left", padx=(0, 14))
        else:
            tk.Label(brand_frame, text="TECKNOLOGIA", font=("Segoe UI", 10, "bold"), fg=t["fg_primary"], bg=t["bg_secondary"]).pack(side="left", padx=(0, 14))

        tk.Label(brand_frame, text="|", font=("Segoe UI", 11), fg=t["border"], bg=t["bg_secondary"]).pack(side="left", padx=6)

        tk.Label(brand_frame, text="Diseñado por", font=("Segoe UI", 8), fg=t["fg_muted"], bg=t["bg_secondary"]).pack(side="left", padx=(6, 6))
        logo_geo = self._load_logo("logo-geologgia.png", height=24, pad_white=True)
        if logo_geo:
            tk.Label(brand_frame, image=logo_geo, bg=t["bg_secondary"]).pack(side="left", padx=(0, 16))
        else:
            tk.Label(brand_frame, text="GEOLOGGIA LTDA.", font=("Segoe UI", 10, "bold"), fg=t["fg_primary"], bg=t["bg_secondary"]).pack(side="left", padx=(0, 16))

        title_box = tk.Frame(top, bg=t["bg_secondary"])
        title_box.pack(side="left", padx=10)
        tk.Label(title_box, text="BidFactory AI — Equipo de Licitaciones", font=("Segoe UI", 13, "bold"), fg=t["fg_primary"], bg=t["bg_secondary"]).pack(anchor="w")
        tk.Label(title_box, text="50 Habilidades · Revisor Final y Aprobador: Cristian Ávila", font=("Segoe UI", 8), fg=t["fg_secondary"], bg=t["bg_secondary"]).pack(anchor="w")

        right_top = tk.Frame(top, bg=t["bg_secondary"])
        right_top.pack(side="right", padx=18)

        theme_txt = "🌙 Modo Oscuro" if self.theme_mode == "light" else "☀️ Modo Claro"
        self._btn(right_top, theme_txt, self.toggle_theme, primary=False).pack(side="left", padx=4)
        self._btn(right_top, "Mapa 50 Habilidades (Web)", self.abrir_panel_web, primary=False).pack(side="left", padx=4)
        self._btn(right_top, "Cartera General (Excel)", self.abrir_cartera_excel, primary=True).pack(side="left", padx=4)

        # ---------------- CUERPO PRINCIPAL ----------------
        body = tk.Frame(self, bg=t["bg_primary"])
        body.pack(fill="both", expand=True, padx=20, pady=16)

        # Columna Izquierda (Sidebar estilo macOS)
        left = tk.Frame(body, bg=t["bg_secondary"], width=340, highlightbackground=t["border"], highlightthickness=1)
        left.pack(side="left", fill="y", padx=(0, 16))
        left.pack_propagate(False)

        tk.Label(left, text="CARTERA DE LICITACIONES", font=("Segoe UI", 9, "bold"), fg=t["fg_muted"], bg=t["bg_secondary"]).pack(anchor="w", padx=16, pady=(14, 6))

        self.listbox = tk.Listbox(
            left,
            bg=t["bg_tertiary"],
            fg=t["fg_primary"],
            selectbackground=t["accent"],
            selectforeground="#FFFFFF",
            font=("Consolas", 10),
            bd=0,
            highlightthickness=1,
            highlightbackground=t["border"],
            height=9,
        )
        self.listbox.pack(fill="x", padx=16, pady=4)
        self.listbox.bind("<<ListboxSelect>>", self.on_select_licitacion)

        btn_left = tk.Frame(left, bg=t["bg_secondary"])
        btn_left.pack(fill="x", padx=16, pady=8)

        self._btn(btn_left, "Importar Correo (.eml) + Ejecutar Todo", self.importar_correo_eml, primary=True).pack(fill="x", pady=3)
        self._btn(btn_left, "Agregar Antecedentes / Bases (PDF, ZIP, DOCX)", self.agregar_archivos_bases, primary=False).pack(fill="x", pady=3)
        self._btn(btn_left, "Nueva Licitación Manual", self.dialogo_nueva_licitacion, primary=False).pack(fill="x", pady=3)
        self._btn(btn_left, "Formatos de Propuesta Tipo (Biblioteca)", self.gestionar_modelos_propuesta, primary=False).pack(fill="x", pady=3)
        self._btn(btn_left, "Abrir Carpeta en Windows Explorer", self.abrir_carpeta_licitacion, primary=False).pack(fill="x", pady=3)

        tk.Label(left, text="RESUMEN DEL PROCESO SELECCIONADO", font=("Segoe UI", 9, "bold"), fg=t["fg_muted"], bg=t["bg_secondary"]).pack(anchor="w", padx=16, pady=(10, 4))

        self.info_label = tk.Label(
            left,
            text="Seleccione una licitación...",
            font=("Segoe UI", 9),
            fg=t["fg_primary"],
            bg=t["bg_tertiary"],
            justify="left",
            anchor="nw",
            padx=12,
            pady=10,
            wraplength=295,
        )
        self.info_label.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        # Columna Derecha
        right = tk.Frame(body, bg=t["bg_primary"])
        right.pack(side="left", fill="both", expand=True)

        card_steps = tk.Frame(right, bg=t["bg_secondary"], highlightbackground=t["border"], highlightthickness=1)
        card_steps.pack(fill="x", pady=(0, 14))

        tk.Label(
            card_steps,
            text="FLUJO DE EJECUCIÓN (DE LA RECEPCIÓN AL REVISOR FINAL Y APROBADOR)",
            font=("Segoe UI", 9, "bold"),
            fg=t["fg_muted"],
            bg=t["bg_secondary"],
        ).pack(anchor="w", padx=18, pady=(14, 8))

        grid_b = tk.Frame(card_steps, bg=t["bg_secondary"])
        grid_b.pack(fill="x", padx=18, pady=(0, 10))
        grid_b.columnconfigure(0, weight=1)
        grid_b.columnconfigure(1, weight=1)

        pasos = [
            ("01 · Extraer Texto de Bases y ZIP (Hab. 02)", self.run_extraer_texto),
            ("02 · Generar Matriz de Cumplimiento Excel (Hab. 09–10)", self.run_matriz),
            ("03 · Crear Borrador Consultas al Mandante (Hab. 15–16)", self.run_consultas),
            ("04 · Generar Presupuesto y Escenarios Excel (Hab. 29–34)", self.run_costos),
            ("05 · Compilar Propuesta Técnica Word + QA (Hab. 20–28, 46)", self.run_propuesta_word),
            ("06 · Generar Informe Revisor Final Word (Hab. 47)", self.run_informe_revisor),
        ]
        for idx, (label_p, cmd_p) in enumerate(pasos):
            r, c = divmod(idx, 2)
            self._btn(grid_b, label_p, cmd_p, primary=False).grid(row=r, column=c, sticky="ew", padx=5, pady=4)

        exec_row = tk.Frame(card_steps, bg=t["bg_secondary"])
        exec_row.pack(fill="x", padx=18, pady=(2, 12))
        exec_row.columnconfigure(0, weight=1)
        exec_row.columnconfigure(1, weight=1)

        self._btn(exec_row, "07 · Aprobar Envío y Emitir Acta (Revisor Final · Hab. 48)", self.dialogo_aprobar_envio, primary=True).grid(
            row=0, column=0, sticky="ew", padx=5, pady=4
        )
        self._btn(exec_row, "Ejecutar Ciclo Completo (Pasos 01 al 06 + Cartera)", self.run_pipeline_completo, primary=True).grid(
            row=0, column=1, sticky="ew", padx=5, pady=4
        )

        # Barra de documentos generados
        docs_bar = tk.Frame(card_steps, bg=t["bg_tertiary"], highlightbackground=t["border"], highlightthickness=1)
        docs_bar.pack(fill="x", padx=18, pady=(0, 14))
        tk.Label(docs_bar, text="Entregables:", font=("Segoe UI", 9, "bold"), fg=t["fg_secondary"], bg=t["bg_tertiary"]).pack(side="left", padx=10, pady=7)

        self._btn(docs_bar, "Matriz Excel", lambda: self._abrir_rel("analisis/matriz_cumplimiento.xlsx"), primary=False).pack(side="left", padx=4, pady=5)
        self._btn(docs_bar, "Costos Excel", lambda: self._abrir_rel("propuesta/economica/costos.xlsx"), primary=False).pack(side="left", padx=4, pady=5)
        self._btn(docs_bar, "Propuesta Word", self._abrir_propuesta_docx, primary=False).pack(side="left", padx=4, pady=5)
        self._btn(docs_bar, "Informe Revisor Final", lambda: self._abrir_rel("revision/informe_revisor_final.docx"), primary=False).pack(side="left", padx=4, pady=5)
        self._btn(docs_bar, "Acta Aprobación", lambda: self._abrir_rel("revision/acta_aprobacion.md"), primary=False).pack(side="left", padx=4, pady=5)

        # Bitácora
        log_card = tk.Frame(right, bg=t["bg_secondary"], highlightbackground=t["border"], highlightthickness=1)
        log_card.pack(fill="both", expand=True)
        tk.Label(log_card, text="BITÁCORA DE EJECUCIÓN", font=("Segoe UI", 9, "bold"), fg=t["fg_muted"], bg=t["bg_secondary"]).pack(anchor="w", padx=18, pady=(12, 4))

        self.log_text = tk.Text(
            log_card,
            bg=t["console_bg"],
            fg=t["console_fg"],
            font=("Consolas", 9),
            bd=0,
            padx=12,
            pady=10,
            wrap="word",
            highlightthickness=1,
            highlightbackground=t["border"],
        )
        self.log_text.pack(fill="both", expand=True, padx=18, pady=(0, 16))
        self.log("BidFactory AI listo. Desarrollado por Tecknologia · Diseñado por Geologgia Ltda.")

    def _btn(self, parent: tk.Widget, text: str, cmd, primary: bool = False) -> tk.Button:
        t = THEMES[self.theme_mode]
        bg = t["accent"] if primary else t["btn_neutral_bg"]
        fg = t["accent_fg"] if primary else t["btn_neutral_fg"]
        return tk.Button(
            parent,
            text=text,
            command=cmd,
            bg=bg,
            fg=fg,
            activebackground=t["accent"],
            activeforeground="#FFFFFF",
            font=("Segoe UI", 9, "bold" if primary else "normal"),
            bd=0,
            padx=12,
            pady=7,
            cursor="hand2",
        )

    def toggle_theme(self) -> None:
        sel = self.codigo_actual.get()
        self.theme_mode = "dark" if self.theme_mode == "light" else "light"
        self._build_ui()
        self.refrescar_lista_licitaciones(seleccionar=sel)

    def log(self, msg: str) -> None:
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.update_idletasks()

    def refrescar_lista_licitaciones(self, seleccionar: str | None = None) -> None:
        self.listbox.delete(0, "end")
        LIC_DIR.mkdir(parents=True, exist_ok=True)
        codigos = sorted([d.name for d in LIC_DIR.iterdir() if d.is_dir() and (d / "ficha.json").exists()])
        for c in codigos:
            self.listbox.insert("end", c)
        if codigos:
            target = seleccionar if seleccionar in codigos else codigos[0]
            idx = codigos.index(target)
            self.listbox.selection_set(idx)
            self.codigo_actual.set(target)
            self.actualizar_ficha_ui(target)

    def on_select_licitacion(self, _event=None) -> None:
        sel = self.listbox.curselection()
        if not sel:
            return
        cod = self.listbox.get(sel[0])
        self.codigo_actual.set(cod)
        self.actualizar_ficha_ui(cod)

    def actualizar_ficha_ui(self, codigo: str) -> None:
        dest = LIC_DIR / codigo
        if not (dest / "ficha.json").exists():
            return
        ficha = json.loads((dest / "ficha.json").read_text(encoding="utf-8"))
        estado = json.loads((dest / "estado.json").read_text(encoding="utf-8")) if (dest / "estado.json").exists() else {}
        aprob = estado.get("aprobacion", {})
        rev = estado.get("revision_final", {})
        txt = (
            f"Código: {codigo}\n"
            f"Nombre: {ficha.get('nombre', '')}\n"
            f"Mandante: {ficha.get('mandante', '')}\n"
            f"Canal: {ficha.get('portal', '')}\n"
            f"Cierre: {ficha.get('hitos', {}).get('cierre_ofertas', '')}\n\n"
            f"Estado: {estado.get('estado_global', 'RECIBIDA')}\n"
            f"Puntaje Simulado: {rev.get('puntaje_tecnico_simulado') or 'Pendiente'} pts\n"
            f"Precio Autorizado: {aprob.get('precio_aprobado') or 'Por definir'} {aprob.get('moneda', 'UF')}"
        )
        self.info_label.configure(text=txt)

    def _get_codigo_or_warn(self) -> str | None:
        cod = self.codigo_actual.get().strip()
        if not cod:
            messagebox.showwarning("Sin licitación", "Selecciona o crea primero una licitación.")
            return None
        return cod

    def _run_bg(self, titulo: str, fn) -> None:
        def wrapper() -> None:
            try:
                self.log(f"▶ {titulo}...")
                fn()
                self.after(0, lambda: self.actualizar_ficha_ui(self.codigo_actual.get()))
            except Exception as e:
                self.log(f"Error en {titulo}: {e}")
                messagebox.showerror("Error", str(e))

        threading.Thread(target=wrapper, daemon=True).start()

    def dialogo_nueva_licitacion(self) -> None:
        codigo = simpledialog.askstring("Nueva Licitación", "Código único (ej. LIC-2026-002):", parent=self)
        if not codigo:
            return
        nombre = simpledialog.askstring("Nueva Licitación", "Nombre oficial de la licitación:", parent=self) or f"Licitación {codigo}"
        mandante = simpledialog.askstring("Nueva Licitación", "Mandante / Cliente:", parent=self) or "Mandante"
        portal = simpledialog.askstring("Nueva Licitación", "Portal (Mercado Público / SAP Ariba / Correo):", initialvalue="Mercado Público", parent=self) or "Mercado Público"

        nueva_licitacion.crear_licitacion(codigo.strip(), nombre.strip(), mandante.strip(), portal.strip())
        cartera.actualizar_cartera()
        self.refrescar_lista_licitaciones(seleccionar=codigo.strip())
        self.log(f"✔ Licitación {codigo} creada.")

    def importar_correo_eml(self) -> None:
        fpath = filedialog.askopenfilename(
            title="Seleccionar correo de invitación (.eml)",
            filetypes=[("Correo EML", "*.eml"), ("Todos los archivos", "*.*")],
        )
        if not fpath:
            return
        codigo_sugerido = simpledialog.askstring(
            "Código de Licitación (Opcional)",
            "Ingresa un código corto (ej. LIC-CACHAPOAL-2026) o deja vacío para autodetectar:",
            parent=self,
        )
        raw = Path(fpath).read_bytes()
        msg = email.message_from_bytes(raw, policy=policy.default)
        dest = leer_correos.procesar_mensaje_email(
            msg, codigo_forzado=codigo_sugerido.strip() if codigo_sugerido and codigo_sugerido.strip() else None
        )
        cod = dest.name
        self.refrescar_lista_licitaciones(seleccionar=cod)
        self.log(f"✔ Correo importado en {cod}. Ejecutando ciclo completo...")
        self.run_pipeline_completo()

    def agregar_archivos_bases(self) -> None:
        cod = self._get_codigo_or_warn()
        if not cod:
            return
        fpaths = filedialog.askopenfilenames(
            title=f"Seleccionar antecedentes/bases para {cod} (PDF, DOCX, XLSX, ZIP, TXT)",
            filetypes=[("Antecedentes y Bases", "*.pdf *.docx *.doc *.xlsx *.zip *.txt *.md"), ("Todos los archivos", "*.*")],
        )
        if not fpaths:
            return
        bases_dir = LIC_DIR / cod / "bases"
        bases_dir.mkdir(parents=True, exist_ok=True)
        for fp in fpaths:
            src = Path(fp)
            shutil.copy2(src, bases_dir / src.name)
            self.log(f"Copiado a bases/: {src.name}")
        self.run_pipeline_completo()

    def run_extraer_texto(self) -> None:
        cod = self._get_codigo_or_warn()
        if cod:
            self._run_bg(f"Extracción de texto de bases ({cod})", lambda: (extraer_texto.procesar_bases(cod), self.log("✔ Texto extraído e inventario generado.")))

    def run_matriz(self) -> None:
        cod = self._get_codigo_or_warn()
        if cod:
            self._run_bg(f"Matriz de Cumplimiento Excel ({cod})", lambda: (matriz_cumplimiento.generar_matriz_excel(cod), self.log("✔ matriz_cumplimiento.xlsx actualizada.")))

    def run_consultas(self) -> None:
        cod = self._get_codigo_or_warn()
        if cod:
            self._run_bg(f"Borrador de consultas ({cod})", lambda: (leer_correos.generar_borrador_consultas(cod, 1), self.log("✔ Borrador .eml creado en consultas/.")))

    def run_costos(self) -> None:
        cod = self._get_codigo_or_warn()
        if cod:
            self._run_bg(f"Planilla de Costos y Escenarios ({cod})", lambda: (plantilla_costos.generar_costos_excel(cod), self.log("✔ costos.xlsx generado.")))

    def run_propuesta_word(self) -> None:
        cod = self._get_codigo_or_warn()
        if cod:
            def _work():
                armar_propuesta.compilar_propuesta(cod)
                hallazgos = armar_propuesta.verificar_propuesta(cod)
                self.log(f"✔ Propuesta Técnica Word generada (marcadores pendientes: {len(hallazgos['marcadores_pendientes'])}).")
            self._run_bg(f"Propuesta Técnica Word + QA ({cod})", _work)

    def run_informe_revisor(self) -> None:
        cod = self._get_codigo_or_warn()
        if cod:
            self._run_bg(f"Informe Ejecutivo Revisor Final ({cod})", lambda: (informe_aprobacion.generar_informe_revisor_final(cod), self.log("✔ informe_revisor_final.docx listo.")))

    def dialogo_aprobar_envio(self) -> None:
        cod = self._get_codigo_or_warn()
        if not cod:
            return
        precios = informe_aprobacion.leer_escenarios_costos(LIC_DIR / cod)
        sugerido = precios.get("objetivo") or 853.73
        precio_str = simpledialog.askstring(
            "Aprobación de Envío — Revisor Final (Hab. 48)",
            f"Escenarios calculados:\n"
            f"  • Agresivo (12%): {precios.get('agresivo', 0):,.2f} UF\n"
            f"  • Objetivo (18%): {precios.get('objetivo', 0):,.2f} UF\n"
            f"  • Conservador (25%): {precios.get('conservador', 0):,.2f} UF\n\n"
            f"Ingrese el Precio Neto Final Autorizado (UF):",
            initialvalue=str(sugerido),
            parent=self,
        )
        if not precio_str:
            return
        try:
            precio_val = float(precio_str.replace(",", "."))
        except ValueError:
            messagebox.showerror("Valor inválido", "Ingrese un monto numérico válido.")
            return
        obs = simpledialog.askstring(
            "Observaciones del Aprobador",
            "Instrucciones o condiciones de envío:",
            initialvalue="Visto bueno técnico y económico otorgado.",
            parent=self,
        ) or ""

        def _work():
            informe_aprobacion.registrar_aprobacion(cod, precio_val, "UF", "Cristian Ávila", obs)
            cartera.actualizar_cartera()
            self.log(f"✔ Acta de Aprobación emitida para {cod} ({precio_val:,.2f} UF).")

        self._run_bg(f"Aprobación Final ({cod})", _work)

    def run_pipeline_completo(self) -> None:
        cod = self._get_codigo_or_warn()
        if not cod:
            return

        def _work():
            extraer_texto.procesar_bases(cod)
            matriz_cumplimiento.generar_matriz_excel(cod)
            leer_correos.generar_borrador_consultas(cod, 1)
            plantilla_costos.generar_costos_excel(cod)
            armar_propuesta.compilar_propuesta(cod)
            armar_propuesta.verificar_propuesta(cod)
            informe_aprobacion.generar_informe_revisor_final(cod)
            cartera.actualizar_cartera()
            self.log(f"✔ Ciclo completo finalizado para {cod}.")

        self._run_bg(f"Ciclo Completo ({cod})", _work)

    def abrir_panel_web(self) -> None:
        panel = BASE_DIR / "panel_equipo_licitaciones.html"
        if panel.exists():
            webbrowser.open(panel.as_uri())

    def abrir_cartera_excel(self) -> None:
        xlsx = cartera.actualizar_cartera()
        os.startfile(str(xlsx))

    def abrir_carpeta_licitacion(self) -> None:
        cod = self._get_codigo_or_warn()
        if cod:
            os.startfile(str(LIC_DIR / cod))

    def gestionar_modelos_propuesta(self) -> None:
        modelos_dir = BASE_DIR / "plantillas" / "modelos_propuesta"
        modelos_dir.mkdir(parents=True, exist_ok=True)
        resp = messagebox.askyesnocancel(
            "Modelos de Propuesta e Informes Tipo",
            "¿Deseas agregar archivos Word/PDF de propuestas tipo a la biblioteca estándar?\n\n"
            "• SÍ: Seleccionar archivos (.docx / .pdf) desde tu PC.\n"
            "• NO: Abrir la carpeta 'plantillas/modelos_propuesta/'.",
            parent=self,
        )
        if resp is True:
            fpaths = filedialog.askopenfilenames(
                title="Seleccionar Propuestas o Informes Tipo (.docx, .pdf)",
                filetypes=[("Documentos Word / PDF", "*.docx *.pdf"), ("Todos los archivos", "*.*")],
            )
            for fp in fpaths:
                src = Path(fp)
                shutil.copy2(src, modelos_dir / src.name)
                self.log(f"Modelo guardado: {src.name}")
            os.startfile(str(modelos_dir))
        elif resp is False:
            os.startfile(str(modelos_dir))

    def _abrir_rel(self, rel_path: str) -> None:
        cod = self._get_codigo_or_warn()
        if not cod:
            return
        target = LIC_DIR / cod / rel_path
        if target.exists():
            os.startfile(str(target))
        else:
            messagebox.showinfo("Archivo aún no generado", f"Ejecuta primero el paso correspondiente para crear:\n{target}")

    def _abrir_propuesta_docx(self) -> None:
        cod = self._get_codigo_or_warn()
        if cod:
            self._abrir_rel(f"propuesta/propuesta_tecnica_{cod}.docx")


if __name__ == "__main__":
    app = FabricaLicitacionesApp()
    app.mainloop()
