class Packet:
    """
    def __init__:
        -Funzionamento:
            >Initialize Global Variables
            >Inizialize Dictionary with all LLC and Ethertypes
        
        -Persone:
            >Ushanov
            >Deidda
            >Cantatori
            >Gugoasa
            >Dodon

        -Tempo: +- 1h
    """

    def __init__(self):
        self.packet_frame = []
        self.etherDictionare = {
            #LLC
            0x00f0 : "Netbeui/Netbios",
            0x00e0 : "IPX Novell",
            0x0006 : "IP, Internet Protocol Version 4 (IPv4)",
            0x0042 : "Spanning Tree Protocol (IEEE 802.1D)",
            #EtherTypes
            0x0800 : "IP, Internet Protocol Version 4 (IPv4)",
            0x0806 : "Address Resolution Protocol (ARP)",
            0x8035 : "Reverse Address Resolution Protocol (RARP)",
            0x809b : "AppleTalk (Ethertalk)",
            0x8100 : "VLAN-tagged frame (IEEE 802.1Q)",
            0x814c : "Simple Network Management Protocol (SNMP)",
            0x86dd : "IP, Internet Protocol Version 6 (IPv6)",
            0x8808 : "MAC Control", 
            0x8809 : "LACP",
            0x8847 : "Multi Protocol Label Switch (MPLS)",
            0x0886 : "PPPoE",
            0x8870 : "Jumbo Frames",
        }

    """
    def readMacFromFile(file):
        -Funzionamento:
            >Read the Frame from text File
            >Return an Array with the readed elements in the file Text
        
        -Parametri:
            >file: directory for the file

        -Persone:
            >Cantatori
            >Deidda

        -Tempo: +-30min
    """

    def readPacketFromFile(self, file):
        try:
            cache = open(file, "r").read()
            self.packet_frame = cache.split()
        except Exception:
            return print("Error: No file Found\n")

    """
    def readMacFromtext(MAC_RAW):
        -Funzionamento:
            >Read the MAC from Console
            >Returna an Array with the readed elements in the Console
        
        -Parametri:
            >MAC_RAW: String containing the Frame

        -Persone:
            >Cantatori
            >Deidda

        -Tempo: +-2min
    """

    def readPacketFromText(self, FRAME_RAW):
        self.packet_frame = FRAME_RAW.split()

    """
    def get*():
        -Funzionamento:
            >Get the required data from the Packet
            >Return the required data

        -Persone:
            >Cantatori
            >Dodon

        -Tempo: +- 1h
    """

    def getMAC_D(self):
        try:
            return self.packet_frame[0:6]
        except Exception:
            return print("Error: Failed to take the MAC_D\n")

    def getMAC_M(self):
        try:
            return self.packet_frame[6:12]
        except Exception:
            return print("Error: Failed to take the MAC_M\n")

    def getDSAP(self):
        try:
            return self.packet_frame[14]
        except Exception:
            return print("Error: Failed to take the DSAP\n")

    def getOUI(self):
        try:
            return "-".join(self.packet_frame[17:20])
        except Exception:
            return print("Error: Failed to take the OUI\n")

    def getEther(self):
        try:
            EthLen = "".join(self.packet_frame[12:14])
            try:
                return int(EthLen, 16)
            except Exception:
                return print("Error: Conversion in 16 not possible\n")
        except Exception:
            return print("Error: Failed to take the Ethertype\n")

    """
    def decodeEtherType():
        -Funzionamento:
            >Finds out if a Packet is Ethernet 2 or 802.3
            >Return the corresponding value (Eth. 2/802.3)

        -Persone:
            >Cantatori
            >Ushanov
    """

    def decodeEtherType(self):
        EthLen = self.getEther()

        if EthLen > 0x5dc: #1500
            return "Ethernet 2"
        else: 
            return "802.3"

    """
    def decodeLLC():
        -Funzionamento:
            >Finds out the LLC Ethertype of the Packet
            >Use a Dictionary (Made by the person mentioned below)
            >Return the corresponding value assigned in the Dictionary

        -Persone:
            >Cantatori
            >Ushanov

        -Tempo: +- 1.5h
    """

    def decodeLLC(self):
        EthType = self.decodeEtherType()

        if EthType == "Ethernet 2":
            return self.etherDictionare[self.getEther()]
        else: 
            if int(self.getDSAP(), 16) == 0xaa:
                return "SNAP Protocol"
            else:
                return "{0} Protocol".format(self.etherDictionare[self.getDSAP()])

    """
    def chooseOUIorDSAP():
        -Funzionamento:
            >Based on the LLC, decide to output the OUI or the DSAP
            >Return the OUI/DSAP of the Packet

        -Persone:
            >Cantatori
            >Ushanov

        -Tempo: +-1h
    """
    def chooseOUIorDSAP(self):
        LLC = self.decodeLLC()
        EtherType = self.decodeEtherType()

        if LLC == "SNAP Protocol" and EtherType == "802.3 LLC":
            return str(self.getOUI())    
        elif EtherType == "802.3 LLC":
            return str(self.getDSAP())
        else:
            return "---"

    """

    def checkFrameLenght():
        -Funzionamento:
            >Get the total Length of the Packet's Payload 
            >Return the Lenght

        -Persone:
            >Cantatori
            >Gugoasa

        -Tempo: +- 20min
    """
    def checkFrameLenght(self):
        EthLen = self.getEther()

        if EthLen < 0x5dc:
            return EthLen
        else:
            return int("".join(self.packet_frame[16:18]), 16) + 14

    """

    def checkMadAddress():
        -Funzionamento:
            >Given the MAC Address, decide the type of it.
            >Return the Type of the MAC Address

        -Persone:
            >Cantatori
            >Gugoasa

        -Tempo: +- 20min
    """
    def checkMacAddress(self, MAC):
        MACByte = int(MAC[0], 16)

        if int("".join(MAC), 16) == 0xFFFFFFFFFFFF:
            return "Broadcast"
        elif MACByte % 2 == 0:
            return "Singlecast"
        elif (MACByte >> 1) % 2 == 1:
            return "Multicast Local"
        else:
            return "Multicast Global" 