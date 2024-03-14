from datetime import datetime
#client
class Client:
    def __init__(self, nom, date_naissance, numero_telephone):
        self.nom = nom
        self.date_naissance = date_naissance
        self.numero_telephone = numero_telephone
        self.facture = 0
    def getNom(self):
        return self.nom
    def getDateNaissance(self):
        return self.date_naissance
    def getNumeroTelephone(self):
        return self.numero_telephone
    def getFacture(self):
        return self.facture  
#gestionnaire des clients 
class GererClients(Client):
    def __init__(self):
        self.clients = []
    def setNom(self, nNom):
        self.nom = nNom
    def setDateNaissance(self, ndate):
        self.date_naissance = ndate
    def setNumeroTelephone(self, nTel):
        self.numero_telephone = nTel
    def setfacture(self, nFact):
        self.facture = nFact
    def ajouter_client(self, client):
        self.clients.append(client)

#importation fichier cdr et conversion
class ImportCDR:
    def __init__(self, file_path):
        self.cdr_data = []
        with open(file_path, 'r') as file:
            for line in file:
                data = line.strip().split('|')
                cdr_dict = {
                    'Identifiant': int(data[0]),
                    'Type call': int(data[1]),
                    'Date et heure': datetime.strptime(data[2], '%Y%m%d%H%M%S'),
                    'Appelant': data[3],
                    'Appelé': data[4],
                    'Durée': int(data[5]),
                    'Taxe': int(data[6]),
                    'TotalVolume': int(data[7])
                }
                self.cdr_data.append(cdr_dict)

class GenererFacture:
    def __init__(self, client, cdr_data):
        self.client = client
        self.cdr_data = cdr_data

    def generer_facture_client(self):
        for cdr in self.cdr_data:
            if cdr['Type call'] == 0:  # Appel
                if cdr['Appelant'][:3] == cdr['Appelé'][:3]:  # Même réseau
                    myfacture = cdr['Durée'] * 0.025
                    if cdr['Taxe']== 0: #0 : Aucune taxe
                        self.client.facture += myfacture                        
                    elif cdr['Taxe'] == 1: #Appliquer l'ACCISE 10%
                        self.client.facture += (myfacture + (myfacture * 0.1))
                    elif cdr['Taxe'] == 2: #Appliquer la TVA 16%
                        self.client.facture += (myfacture + (myfacture * 0.16))                        
                else:
                    myfacture += cdr['Durée'] * 0.05
                    if cdr['Taxe']== 0: #0 : Aucune taxe
                        self.client.facture += myfacture                        
                    elif cdr['Taxe'] == 1: #Appliquer l'ACCISE 10%
                        self.client.facture += (myfacture + (myfacture * 0.1))
                    elif cdr['Taxe'] == 2: #Appliquer la TVA 16%
                        self.client.facture += (myfacture + (myfacture * 0.16))
            elif cdr['Type call'] == 1:  # SMS
                if cdr['Appelant'][:3] == cdr['Appelé'][:3]:  # Même réseau
                    myfacture = 0.001
                    if cdr['Taxe']== 0: #0 : Aucune taxe
                        self.client.facture += myfacture                        
                    elif cdr['Taxe'] == 1: #Appliquer l'ACCISE 10%
                        self.client.facture += (myfacture + (myfacture * 0.1))
                    elif cdr['Taxe'] == 2: #Appliquer la TVA 16%
                        self.client.facture += (myfacture + (myfacture * 0.16))
                else:
                    myfacture = 0.002
                    if cdr['Taxe']== 0: #0 : Aucune taxe
                        self.client.facture += myfacture                        
                    elif cdr['Taxe'] == 1: #Appliquer l'ACCISE 10%
                        self.client.facture += (myfacture + (myfacture * 0.1))
                    elif cdr['Taxe'] == 2: #Appliquer la TVA 16%
                        self.client.facture += (myfacture + (myfacture * 0.16))                    
            elif cdr['Type call'] == 2:  # Internet
                myfacture = cdr['TotalVolume'] * 0.03
                if cdr['Taxe']== 0: #0 : Aucune taxe
                    self.client.facture += myfacture                        
                elif cdr['Taxe'] == 1: #Appliquer l'ACCISE 10%
                    self.client.facture += (myfacture + (myfacture * 0.1))
                elif cdr['Taxe'] == 2: #Appliquer la TVA 16%
                    self.client.facture += (myfacture + (myfacture * 0.16))

class Statistiques:
    def __init__(self, cdr_data):
        self.cdr_data = cdr_data

    def calculer_statistiques(self, debut_periode, fin_periode):
        debut_periode = datetime.strptime(debut_periode, "%Y%m%d%H%M%S") #prends en charge l'heure du debut
        fin_periode = datetime.strptime(fin_periode, "%Y%m%d%H%M%S") #prends en charge l'heure de la fin
        
        nb_appels = sum(1 for cdr in self.cdr_data if cdr['Type call'] == 0 and debut_periode <= (cdr['Date et heure'])<= fin_periode)
        duree_appels = sum(cdr['Durée'] for cdr in self.cdr_data if cdr['Type call'] == 0 and debut_periode <= (cdr['Date et heure'])<= fin_periode)
        nb_sms = sum(1 for cdr in self.cdr_data if cdr['Type call'] == 1 and debut_periode <= (cdr['Date et heure'])<= fin_periode)
        volume_internet = sum(cdr['TotalVolume'] for cdr in self.cdr_data if cdr['Type call'] == 2 and debut_periode <= (cdr['Date et heure'])<= fin_periode)
        return nb_appels, duree_appels, nb_sms, volume_internet
# Test unitaire
if __name__ =='__main__':
    
    #pour le premier cdr
    client_cdr = Client("POLYTECHNIQUE", "1960-06-30", "243818140560, 243818140120")
    cdr_import = ImportCDR("E:/GC/SEMESTER 1/Algo/pro_1/cdr.txt")
    generer_facture = GenererFacture(client_cdr, cdr_import.cdr_data)
    generer_facture.generer_facture_client()
    
    #pour le deuxieme cdr
    tp_algo = Client("POLYTECHNIQUE", "1960-06-30", "243818140560, 243818140120,")
    cdr_import = ImportCDR("E:/GC/SEMESTER 1/Algo/pro_1/tp_algo.txt")
    generer_facture = GenererFacture(tp_algo, cdr_import.cdr_data)
    generer_facture.generer_facture_client()
    
    #pour la statistique
    #periode
    debut = "20230111125011" #date du debut de la periode
    fin = "20230314125011" #date de la fin de la periode
    #calcul de la statitistique
    statistiques = Statistiques(cdr_import.cdr_data)
    nb_appels, duree_appels, nb_sms, volume_internet = statistiques.calculer_statistiques(debut,fin)
    statistiques = Statistiques(cdr_import.cdr_data)
    nb_appels1, duree_appels1, nb_sms1, volume_internet1 = statistiques.calculer_statistiques(debut,fin)
    
    #calcul des totaux
    factureTotal = client_cdr.facture + tp_algo.facture #facture totale
    nbTotal_appels = nb_appels + nb_appels1
    dureeTotale_appels = duree_appels + duree_appels1
    nbTotal_SMS = nb_sms + nb_sms1
    volumeTotal_internet = volume_internet + volume_internet1
    #affichage résultats
    print("\nSituation du client \n-------------------")
    print(f"Nom du client : {client_cdr.nom}")
    print(f"Date de naissance : {client_cdr.date_naissance}")
    print(f"Numero de téléphone : {client_cdr.numero_telephone}")
    print(f"Facture du client : ${factureTotal}")
    
    print("\nStatistique du client \n-------------------")
    print(f"Période allant du : {debut} au {fin}")
    print(f"Nombre d'appels: {nbTotal_appels} Durée totale des appels: {dureeTotale_appels} secondes")
    print(f"Nombre de SMS: {nbTotal_SMS}")
    print(f"Volume internet utilisé: {volumeTotal_internet} MegaBytes")
