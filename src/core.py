from pathlib import Path
from .widgets import SettingsFrame, FileFrame, File
from . import utils
import json
import customtkinter as ctk


BASE_DIR = Path(__file__).resolve().parent
ASSET_DIR=BASE_DIR.parent / "assets"
NOTES_DIR=ASSET_DIR / "notes"
FILE_DATA=ASSET_DIR / "file_data.json"
SETTINGS=ASSET_DIR / "settings.json"

class App(ctk.CTk):
    def __init__(self):
        global core_settings
        super().__init__()
        self.load_widgets()
        core_settings=read_settings()
        
    def load_widgets(self):

        for widget in self.children.values():
            widget.destroy()
        self.geometry("800x600")
        self.title("Notebook")
        self.iconbitmap(r"assets\icon.ico")
        self.resizable(False,False)
        ctk.set_default_color_theme(core_settings["color-scheme"])
        ctk.set_appearance_mode(core_settings["theme"])
        self.colormap={
            "blue":"#007BB8",
            "green":"#00A651",
            "dark-blue":"#0057A3",
        }
        self.header_font=ctk.CTkFont(size=core_settings["heading-font-size"],family=core_settings["font-family"])
        self.body_font=ctk.CTkFont(size=core_settings["body-font-size"],family=core_settings["font-family"])


        self.side_bar=ctk.CTkFrame(self,width=70,height=580)
        self.side_bar.place(x=10,y=10)

        self.home=ctk.CTkButton(self.side_bar,text="\u2302",width=50,height=50,font=ctk.CTkFont(size=29),command=self.to_home)
        self.home.place(x=10,y=10)
        self.home.configure(state="disabled")

        self.new=ctk.CTkButton(self.side_bar,text="+",width=50,height=50,command=self.new_note,font=ctk.CTkFont(size=29))
        self.new.place(x=10,y=70)

        self.setting=ctk.CTkButton(self.side_bar,text="\u2261",width=50,height=50,font=ctk.CTkFont(size=29),command=self.open_settings)
        self.setting.place(x=10,y=520)

        self.note=ctk.CTkFrame(self,width=700,height=580)
        self.note.place(x=90,y=10)

        self.note_title=ctk.CTkLabel(self.note,text="Notes",font=self.header_font)
        self.note_title.place(x=10,y=10)

        self.scrollframe=ctk.CTkScrollableFrame(self.note,width=690,height=580,bg_color="transparent",fg_color="transparent",
                                                border_width=0)
        self.scrollframe.place(x=0,y=90)
        self.scrollframe._scrollbar.configure(width=0)

        self.noteframe=FileFrame(self,width=700,height=580,heading_font=self.header_font,body_font=self.body_font)
        self.noteframe.place(x=90,y=10)
        self.noteframe.save_button.configure(command=lambda:self.save_note(current_noteid))
        self.noteframe.delete_button.configure(command=lambda:self.noteframe.delete_note(current_noteid) or self.to_home())

        self.settings=SettingsFrame(self,width=700,height=580,header_font=self.header_font,body_font=self.body_font)
        self.settings.place(x=90,y=10)
        self.settings.theme.set(core_settings["theme"]) if core_settings["theme"] else self.settings.theme.set("dark")
        self.settings.theme.configure(command=self.check_settings_state)
        self.settings.color.set(core_settings["color-scheme"])
        self.settings.color.configure(command=self.check_settings_state)
        self.settings.font_family.set(core_settings["font-family"])
        self.settings.font_family.configure(command=self.check_settings_state)
        self.settings.heading_font_size.set(core_settings["heading-font-size"])
        self.settings.heading_font_size.configure(command=lambda value:self.settings.update_heading_font_label(value)
                                                or self.check_settings_state())
        self.settings.body_font_size.set(core_settings["body-font-size"])
        self.settings.body_font_size.configure(command=lambda value:self.settings.update_body_font_label(value)
                                               or self.check_settings_state())
        self.settings.heading_font_label.configure(text=f"{core_settings['heading-font-size']} pt")
        self.settings.body_font_label.configure(text=f"{core_settings['body-font-size']} pt")
        self.settings.save.configure(command=self.save_settings,state="disabled")
        self.load_notes()
        self.to_home()

    def load_notes(self):
        for widget in self.scrollframe.winfo_children():
            widget.destroy()
        color=self.colormap[core_settings["color-scheme"]]
        for note in get_file_data():
            noteid=note["id"]
            title=note["title"]
            timestamp=note["timestamp"]
            file_widget=File(title,timestamp,self.scrollframe,height=80,fg_color=color,corner_radius=10,)
            file_widget.pack(padx=10,pady=5,fill="x",)
            file_widget.bind("<Button-1>",lambda event, nid=noteid: self.open_note(nid))

    def add_note(self,event=None):
        global current_noteid
        current_noteid=utils.generate_id()
        write_note(current_noteid, "", "Untitled")

    def open_note(self,noteid):
        global current_noteid
        current_noteid=noteid
        self.noteframe.tkraise()
        self.noteframe.set_up(current_noteid)
        self.setting.configure(state="disabled")
        self.home.configure(state="normal")
    def new_note(self):
        global current_noteid
        self.add_note()
        self.open_note(current_noteid)
        self.home.configure(state="disabled")
        self.new.configure(state="disabled")
        self.setting.configure(state="disabled")

    def save_note(self,noteid):
        self.noteframe.save_note(noteid)
        self.home.configure(state="normal")
        self.new.configure(state="normal")
        self.setting.configure(state="normal")

    def to_home(self):
        self.load_notes()
        self.note.tkraise()
        self.home.configure(state="disabled")
        self.new.configure(state="normal")    
        self.setting.configure(state="normal")

    def open_settings(self):
        self.settings.tkraise()
        self.home.configure(state="normal")
        self.new.configure(state="normal")

    def kill_children(self):
        for child in self.winfo_children():
            child.destroy()

    def save_settings(self):
        global core_settings
        new_settings={
            "theme":self.settings.theme.get(),
            "color-scheme":self.settings.color.get(),
            "heading-font-size":int(self.settings.heading_font_size.get()),
            "body-font-size":int(self.settings.body_font_size.get()),
            "font-family":self.settings.font_family.get()
        }
        update_settings(new_settings)
        core_settings=new_settings
        self.kill_children()
        ctk.set_default_color_theme(new_settings["color-scheme"])
        ctk.set_appearance_mode(new_settings["theme"])
        self.load_widgets()
        self.settings.tkraise()
        self.home.configure(state="normal")
        self.settings.save.configure(state="disabled")

    def check_settings_state(self,event=None):
        state=[
            self.settings.theme.get() == core_settings["theme"],
            self.settings.color.get() == core_settings["color-scheme"],
            self.settings.font_family.get() == core_settings["font-family"],
            int(self.settings.heading_font_size.get()) == core_settings["heading-font-size"],
            int(self.settings.body_font_size.get()) == core_settings["body-font-size"],
        ]
        if all(state):
            self.settings.save.configure(state="disabled")
            self.home.configure(state="disabled")
            self.new.configure(state="disabled")
        else:
            self.settings.save.configure(state="normal")
            self.home.configure(state="normal")
            self.new.configure(state="normal")

def write_default_settings():
    default_settings={
        "theme": "dark",
        "color-scheme": "green",
        "heading-font-size": 40,
        "body-font-size": 18,
        "font-family": "Arial"
        }
    with open(SETTINGS, "w") as file:
        json.dump(default_settings, file, indent=4)

def read_settings():
    with open(SETTINGS, "r") as file:
        settings = json.load(file)
        return settings

def update_settings(new_settings):
    with open(SETTINGS, "w") as file:
        json.dump(new_settings, file, indent=4)

def get_file_data():
    with open(FILE_DATA, "r") as file:
        data = json.load(file)
        return data

def update_file_data(new_data):
    with open(FILE_DATA, "w") as file:
        json.dump(new_data, file, indent=4)

def add_file_entry(file_id: str, title: str):
    file_data = get_file_data()
    file_data.append({
        "id": file_id,
        "title": title,
        "timestamp": utils.get_timestamp()
    })
    update_file_data(file_data)

def read_notes(note_id: str) -> str:
    note_path = NOTES_DIR / f"{note_id}.txt"
    if note_path.exists():
        with open(note_path, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    return ""

def write_note(note_id: str, content: str, title: str|None = None):
    note_path = NOTES_DIR / f"{note_id}.txt"
    with open(note_path, "w", encoding="utf-8") as file:
        file.write(content)
    
    
    
    existing = utils.get_file_data(file_id=note_id)
    if not existing:
        if title and title.strip() != "":
            add_file_entry(note_id, title)
        else:
            add_file_entry(note_id, "Untitled")
    
    all_files = get_file_data()
    for f in all_files:
        if f["id"] == note_id:
            f["timestamp"] = utils.get_timestamp()
            if title and title.strip() != "":
                f["title"] = title
            break
    update_file_data(all_files)

def delete_note(note_id: str):
    note_path = NOTES_DIR / f"{note_id}.txt"
    if note_path.exists():
        note_path.unlink()
    file_data = get_file_data()
    file_data = [file for file in file_data if file["id"] != note_id]
    update_file_data(file_data)

def rename_note(note_id: str, new_title: str):
    file_data = get_file_data()
    for file in file_data:
        if file["id"] == note_id:
            file["title"] = new_title
            break
    update_file_data(file_data)

current_noteid=None
core_settings=read_settings()