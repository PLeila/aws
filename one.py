import boto3
import pickle
import csv

AWS_ACCESS_KEY = "AKIAQOIUAEI3OLRJGHEK"
AWS_SECRET_KEY = "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"
BUCKET_NAME = 'projetleilateste'
OBJECT_KEY = 'path/in/bucket/done_aplikan.pkl'
CSV_FILE_NAME = 'donnees_aplikan.csv'

def anrejistre_done(done, fichier):
    with open(fichier, 'wb') as file:
        pickle.dump(done, file)

def li_done(fichier):
    with open(fichier, 'rb') as file:
        done = pickle.load(file)
    return done

def anrejistre_done_aws_s3(done, bucket, key, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY):
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    done_serialize = pickle.dumps(done)
    s3.put_object(Body=done_serialize, Bucket=bucket, Key=key)

def li_done_aws_s3(bucket, key, aws_access_key_id, aws_secret_access_key):
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    response = s3.get_object(Bucket=bucket, Key=key)
    done_serialize = response['Body'].read()
    done = pickle.loads(done_serialize)
    return done

def enregistrer_donnees_csv(done, fichier_csv):
    with open(fichier_csv, 'w', newline='') as csvfile:
        fieldnames = done.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow(done)

# Fonksyon pou jwenn repons aplikan yo
def jwenn_repons_aplikan():
    done = {
        'Intentions_quitter_pays': input("Avez-vous l'intention de quitter le pays après avoir terminé vos études universitaires? (Oui/Non/Incertain): "),
        'Tranche_age': input("Quel est votre âge actuel? (Moins de 20 ans/20-24 ans/25-29 ans/30-34 ans/35 ans et plus): "),
        'Niveau_etudes': input("À quel niveau d'études êtes-vous actuellement? (Licence 1/Licence 2/Licence 3/Licence 4/DUT 1/DUT 2): "),
        'Pays_vise': input("Vers quel(s) pays envisagez-vous de vous rendre? (Sélectionnez tous ceux qui s'appliquent, séparés par des virgules)\nÉtats-Unis, Canada, Royaume-Uni, Australie, France, Autre: "),
        'Raison_depart': input("Pourquoi envisagez-vous de quitter le pays? (Sélectionnez toutes celles qui s'appliquent, séparées par des virgules)\nOpportunités professionnelles, Recherche académique, Qualité de vie, Autre: "),
        'Objectif_depart': input("Envisagez-vous de quitter le pays pour des études supplémentaires ou d'autres raisons? (Sélectionnez tous ceux qui s'appliquent, séparés par des virgules)\nÉtudes supplémentaires, Raisons professionnelles, Raisons personnelles: "),
        'Duree_prevue_etranger': input("Si vous envisagez un départ temporaire, quelle est la durée prévue de votre séjour? (Moins d'un an/1-2 ans/3-5 ans/Plus de 5 ans): "),
        'Intention_retour_pays_origine': input("Avez-vous l'intention de retourner dans votre pays d'origine après votre séjour à l'étranger? (Oui/Non/Incertain): ")
    }
    return done

# Exemple itilizasyon
done_aplikan = jwenn_repons_aplikan()
print("Done aplikan yo:", done_aplikan)

# Anrejistre done lokal
anrejistre_done(done_aplikan, 'done_aplikan.pkl')

# Anrejistre done nan AWS S3
anrejistre_done_aws_s3(done_aplikan, BUCKET_NAME, OBJECT_KEY, AWS_ACCESS_KEY, AWS_SECRET_KEY)

# Enregistre les données dans un fichier CSV
enregistrer_donnees_csv(done_aplikan, CSV_FILE_NAME)

# Li done lokal
done_local_li = li_done('done_aplikan.pkl')
print("Done lokal li:", done_local_li)

# Li done nan AWS S3
done_s3_li = li_done_aws_s3(BUCKET_NAME, OBJECT_KEY, AWS_ACCESS_KEY, AWS_SECRET_KEY)
print("Done nan AWS S3 li:", done_s3_li)
