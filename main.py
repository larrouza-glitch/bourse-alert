import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import yfinance as yf

# --- CONFIGURATION ---
# Remplace par ton adresse mail
EMAIL_EXPEDITEUR = "larrouza@gmail.com" 
EMAIL_DESTINATAIRE = "larrouza@gmail.com"

# Récupère le mot de passe depuis les "Secrets" GitHub (ne le tape pas ici !)
rqyy xgme cijo woju = os.environ.get("EMAIL_PASSWORD")

ACTIONS = ["NVDA", "AIR.PA", "DSY.PA", "STMP.PA"]

def envoyer_email(sujet, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_EXPEDITEUR
        msg['To'] = EMAIL_DESTINATAIRE
        msg['Subject'] = sujet
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_EXPEDITEUR, EMAIL_PASSWORD)
        server.sendmail(EMAIL_EXPEDITEUR, EMAIL_DESTINATAIRE, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Erreur envoi email : {e}")

def verifier_marche():
    for ticker in ACTIONS:
        try:
            donnees = yf.Ticker(ticker)
            hist = donnees.history(period="5d")
            if hist.empty: continue

            prix_actuel = hist['Close'].iloc[-1]
            prix_veille = hist['Close'].iloc[-2]
            variation = ((prix_actuel - prix_veille) / prix_veille) * 100
            
            # Alerte si baisse > 3%
            if variation <= -3.0:
                envoyer_email(f"🚨 ALERTE {ticker}", f"{ticker} chute de {variation:.2f}%. Prix : {prix_actuel:.2f}")

            # Alerte NVDA sous 190
            if ticker == "NVDA" and prix_actuel <= 190.0:
                envoyer_email("🎯 OPPORTUNITÉ NVDA", f"NVDA est à {prix_actuel:.2f} $")
        except Exception as e:
            print(f"Erreur {ticker}: {e}")

if __name__ == "__main__":
    verifier_marche()
