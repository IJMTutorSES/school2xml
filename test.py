from datetime import date
from tkinter import Tk, Label, Entry, Button, messagebox, END
from tkinter.ttk import Combobox
from export import export


def main():
    def create_xml():
        # e_vals = {}
        # for key, val in etrs.items():
        #     e_vals[key] = val.get()

        # success = export(e_vals)

        # if success:
        #     messagebox.showinfo("Info", message="XML-Dateien wurde erstellt.")
        #     for etr in [etrs["school"], etrs["sch_email"], etrs["te_ct"], etrs["st_ct"], etrs["course"]]:
        #         etr.delete(0, END)
        # else:
        #     messagebox.showerror(
        #         "Fehler",
        #         message="XML-Dateien konnten nicht erstellt werden. Bitte überprüfen Sie Ihre Eingaben.\n\n"
        #         + "Anzahl der Lehrer- und Schülerkonten: muss eine Zahl sein\n"
        #         + "Daten: im Format YYYY-MM-DD\n\n"
        #         + "Bitte überprüfen Sie auch, ob sie in einem Feld ungewollte Leerzeichen eingegeben haben.",
        #     )
        pass

    root = Tk()
    root.title("school2xml")
    root.geometry("320x190")

    # Labels
    lbls = {}
    lbls["school"] = Label(root, text="Kürzel der Schule:", anchor="w")
    lbls["sch_email"] = Label(root, text="E-Mail der Schule:", anchor="w")
    lbls["course"] = Label(root, text="Kursauswahl:", anchor="w")
    lbls["te_ct"] = Label(root, text="Anzahl Lehrer:", anchor="w")
    lbls["st_ct"] = Label(root, text="Anzahl Schüler:", anchor="w")
    lbls["vld_fr"] = Label(root, text="Konten aktiv ab:", anchor="w")
    lbls["vld_utl"] = Label(root, text="Konten aktiv bis:", anchor="w")

    # Entry fields
    etrs = {}
    etrs["school"] = Entry(root, width=12)
    etrs["sch_email"] = Entry(root, width=35)
    etrs["course"] = Combobox(
        root,
        values=["Mathematik", "Sprachen", "Beide"],
        width=11,
    )
    etrs["te_ct"] = Entry(root, width=7)
    etrs["st_ct"] = Entry(root, width=7)
    etrs["vld_fr"] = Entry(root, width=11)
    etrs["vld_utl"] = Entry(root, width=11)

    etrs["vld_fr"].insert(0, str(date.today()))
    etrs["course"].current(0)
    # Button
    btn = Button(root, text="XML-Dateien erstellen", command=create_xml)

    # Positions of labels, entry fields, button (grid)
    i = 0
    for _, val in lbls.items():
        val.grid(row=i, column=0, sticky="w")
        i += 1

    i = 0
    for _, val in etrs.items():
        val.grid(row=i, column=1, sticky="w")
        i += 1

    btn.place(x=101, y=155)

    # Main loop
    root.mainloop()


if __name__ == "__main__":
    main()
