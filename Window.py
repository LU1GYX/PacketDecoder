from Packet import Packet
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as mbox
import os

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.packet = Packet()
        self.initUI()

    def initUI(self):
        #Menu Bar
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        #Help Menu
        helpMenu = Menu(menubar, tearoff=0)
        helpMenu.add_command(label="?", command=self.documentationButton)

        #Adding the menus to the Bar
        menubar.add_cascade(label="Open Frame from File", command=self.openExternalFile)
        menubar.add_cascade(label="Help", menu=helpMenu)

        #Frame Label + textBox1
        self.label1 = Label(self.master, text="Insert the frame to decode, or\n take it from an External File")
        self.label1.place(x = 435, y = 5)
        self.textBox1 = Text(self.master)
        self.textBox1.place(x = 5, y = 5, width = 430, height=100)

        #Decode Button
        self.decodeButton = Button(self.master, text="Get Decoding Informations", command=self.decode)
        self.decodeButton.place(x = 440, y = 45, height = 60)

        #Divisor Label
        self.divisor = Label(self.master, text="_____________________________________________________________________________________________________________________")
        self.divisor.place(x = 5, y = 105)

        #Listbox 
        self.listBox = Listbox(self.master)
        self.listBox.place(x = 5, y = 135, width = 100, height =   180)
        self.listBox.insert(1, "MAC Dest. Info")
        self.listBox.insert(2, "MAC Mitt. Info")
        self.listBox.insert(3, "Packet Info")

        #Packet preview Label2 + textBox2
        self.label2 = Label(self.master, text="Packet Given:")
        self.label2.place(x = 110, y = 140)
        self.textBox2 = Text(self.master)
        self.textBox2.place(x = 110, y = 160, width = 480, height = 80)
        
        #MAC preview Label3 + textBox3
        self.label3 = Label(self.master, text="MAC ---:")
        self.label3.place(x = 110, y = 250)
        self.textBox3 = Text(self.master)
        self.textBox3.place(x = 180, y = 250, width = 410, height = 20)
        
        #MAC Type / Protocol Preview Label4 + textBox4
        self.label4 = Label(self.master, text="MAC Type:")
        self.label4.place(x = 110, y = 280)
        self.textBox4 = Text(self.master)
        self.textBox4.place(x = 180, y = 280, width = 410, height = 20)

        #Length Preview Label5 + textBox5
        self.label5 = Label(self.master, text="Length:")
        self.textBox5 = Text(self.master)

        #OUI/DSAP Preview Label6 + textBox6
        self.label6 = Label(self.master, text="")
        self.textBox6 = Text(self.master)

        #Error textBox7
        self.textBox7 = Text(self.master)
        self.textBox7.place(x = 5, y = 320, width = 585, height = 20)

        self.listBox.bind("<<ListboxSelect>>", self.listSelection)

    def clearTextBoxes(self):
        #Clear the textBoxes (A E S T H E T I C)
        self.textBox1.delete("1.0", END)
        self.textBox3.delete("1.0", END)
        self.textBox4.delete("1.0", END)
        self.textBox5.delete("1.0", END)
        self.textBox6.delete("1.0", END)
        self.textBox7.delete("1.0", END)

    def noFileArgsWindow(self): 
        mbox.showerror("Error", "You must select a file or insert any arguments in the filed.")

    def documentationButton(self):
        os.system("start ./Documentation/index.html")

    def openExternalFile(self):
        self.clearTextBoxes()
        try:
            #Preparing the "Open" windowDialog
            filename = askopenfilename()

            #Saving the Packet read in the file
            self.packet.readPacketFromFile(filename)

            #Insert it in the textBox1 for de decoing function
            self.textBox1.delete("1.0", END)
            self.textBox1.insert("1.0", self.packet.packet_frame)

            #Error handler in case no file is selected
            if not filename:
                self.textBox7.insert("1.0", "Error: No file has been selected")
                return self.noFileArgsWindow()
            else:
                self.decode()
        except Exception:
            self.textBox7.insert("1.0", "Error: Can't open the File")

    def decode(self):
        #Get the Packet in the textBox
        self.getText = self.textBox1.get("1.0", END)

        #Setting up the various elements in the window
        self.master.geometry("600x350")

        #Insiance the Packet in the Object
        self.packet.readPacketFromText(self.getText)

        self.textBox2.insert("1.0", self.getText)
    
    def listSelection(self, event):
        selection = event.widget.curselection()

        self.clearTextBoxes()

        if selection:
            index = selection[0]
            if index == 0:
                self.clearTextBoxes()

                #Hide certain textBoxes
                self.label5.place_forget()
                self.textBox5.place_forget()
                
                self.label6.place_forget()
                self.textBox6.place_forget()

                self.textBox3.place(width = 410, height = 20)
                self.label3.config(text = "MAC Dest:")
                self.label4.config(text = "MAC Type:")

                #Insert the Results
                try:
                    self.textBox3.insert("1.0", self.packet.getMAC_D())
                    self.textBox4.insert("1.0", self.packet.checkMacAddress(self.packet.getMAC_D()))
                except Exception:
                    self.textBox7.insert("1.0", "Error: Can't take the MAC information")
                    return 
            elif index == 1:
                self.clearTextBoxes()

                #Hide certain textBoxes
                self.label5.place_forget()
                self.textBox5.place_forget()

                self.label6.place_forget()
                self.textBox6.place_forget()

                self.textBox3.place(width = 410, height = 20)
                self.label3.config(text = "MAC Mitt:")
                self.label4.config(text = "MAC Type:")

                #Insert the Results
                try:
                    self.textBox3.insert("1.0", self.packet.getMAC_M())
                    self.textBox4.insert("1.0", self.packet.checkMacAddress(self.packet.getMAC_M()))
                except Exception:
                    self.textBox7.insert("1.0", "Error: Can't take the MAC information") 
                    return
            else:               
                self.clearTextBoxes()

                #Modify the textBoxes for more A E S T H E T I C
                self.label3.config(text = "EtherType:")
                self.label4.config(text = "Protocol:")
                self.label5.place(x = 285, y = 250)
                self.label6.place(x = 445, y = 250)

                #Finally, show up the textBox + label we hide earlier
                self.textBox3.place(width = 100, height = 20)
                self.textBox5.place(x = 335, y = 250, width = 100, height = 20)
                self.textBox6.place(x = 490, y = 250, width = 100, height = 20)

                try: 
                    self.textBox3.insert("1.0", self.packet.decodeEtherType())
                    self.textBox4.insert("1.0", self.packet.decodeLLC())
                    self.textBox5.insert("1.0", self.packet.checkFrameLenght())
                    self.textBox6.insert("1.0", self.packet.chooseOUIorDSAP())

                    #Condition for SNAP protocol label text Change
                    if self.packet.decodeLLC() == "SNAP Protocol" and self.packet.decodeEtherType() == "802.3 LLC":
                        self.label6.config(text="OUI:")
                    elif self.packet.decodeEtherType() == "802.3 LLC":
                        self.label6.config(text="DSAP:")
                    else:
                        self.label6.config(text="---")
                except Exception:
                    self.textBox7.insert("1.0", "Error: Can't take the Packet information") 
                    return 
