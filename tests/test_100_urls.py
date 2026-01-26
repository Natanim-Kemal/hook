import requests
import time

API_URL = 'http://127.0.0.1:5000/predict'

PHISHING_URLS = [
    "http://www.crazy4games-flash.s3.eu-west-1.amazonaws.com",
    "https://www.amaczon-co-jp.amazccn.baicfp.top/ap/signin",
    "https://opmklw.com/",
    "http://www.cg02425-wordpress-1.tw1.ru",
    "http://www.porno.a2zgstcenter.com",
    "http://www.andraaw.ga",
    "https://sitebuilder178857.dynadot.com/",
    "https://accounts-mail.ru/attach/filefolder/gttsaf4gsf/?",
    "https://docs.google.com/presentation/d/e/2pacx-1vs4t3os",
    "https://s3.amazonaws.com/appforest_uf/f1679663058485x32",
    "http://www.massimozanchi.it",
    "http://www.hermannl.ga",
    "http://cq21479.tw1.ru/credit-agricole",
    "http://www.saisaocard.co.jp.nlytoc.top/ai/sign.php",
    "http://www.xn--t8jaf9b0bk3g4fpepd8427bh3wau3m2vinysjzz7",
    "http://www.aouynopt.cf",
    "https://myattverification-333-101.weeblysite.com/",
    "https://infura-ipfs.io/ipfs/qmsaaie24rx19fkzxdwjpuptjut",
    "http://www.72888.com",
    "https://aol-mail-102092.weeblysite.com/",
    "http://www.inpower.xyz",
    "http://www.ricosdulcesmexicanos.com",
    "http://www.info-com.de",
    "https://bafybeifcrcv2qxgk6ejxfzphvmh3fsabnfvmbbcahfqoaw",
    "http://365666n.cc/",
    "http://www.mrbonus.com",
    "http://lugin-upphoold.godaddysites.com/",
    "https://gezidunyasi.com.tr/view/phpmailler/examples/sty",
    "https://ms365-0utl00k-eu-docdrive.firebaseapp.com/",
    "http://www.cdn.217wo.com",
    "https://www.ekli-nat.ekinrt.lnedxt.top",
    "http://www.uk-shaparak.cf",
    "https://shorturl.at/fiknr",
    "http://elsewedy-td.com/",
    "https://www.aruba-fattura-paga.com/n9k06252e5108238h381",
    "http://www.italianrealestateagents.com",
    "http://ialert-support.com/",
    "https://documentation004-service012.web.app/",
    "http://www.bubbleset.com",
    "https://www.sbkp.info/",
    "https://moncar.com.mx/package/bibaztgkmv4944",
    "http://www.blackgirlmagicschool.com",
    "http://www.rampbay.com",
    "http://www.oop.urlfb.co",
    "http://u1951394.plsk.regruhosting.ru/mass-sk-checker-ma",
    "https://microsoft75.yolasite.com/",
    "http://www.dgbet3.roimaster.site",
    "https://monirshouvo.github.io/fb_responsive",
    "http://www.snappertalk.com",
    "https://dreumondrese.web.app/"
]

LEGIT_URLS = [
    "https://www.hellabrunn.de",
    "https://www.ourladyofpurgatory.org",
    "https://www.lisbonlux.com",
    "https://www.usitc.gov",
    "https://www.welshcountry.co.uk",
    "https://www.semarangkota.go.id",
    "https://www.rifleshootermag.com",
    "https://www.clickbaitdefamation.org",
    "https://www.theblaze.com",
    "https://www.unca.edu.ar",
    "https://www.flaps2approach.com",
    "https://www.chemanager-online.com",
    "https://www.creditone.com.au",
    "https://www.dbmuseum.de",
    "https://www.texasoldtown.com",
    "https://www.congreso.es",
    "https://www.famouspictures.org",
    "https://www.chpa.org",
    "https://www.george-smart.co.uk",
    "https://www.minutodigital.com",
    "https://www.euroman.dk",
    "https://www.asamblea.gob.sv",
    "https://www.waldfleisch.de",
    "https://www.futebolinterior.com.br",
    "https://www.mitzvahmarket.com",
    "https://www.slavrada.gov.ua",
    "https://www.pickndazzle.com",
    "https://www.carolinahomedecorandwreaths.com",
    "https://www.socresonline.org.uk",
    "https://www.firstamendment.com",
    "https://www.ccme.org.br",
    "https://www.shapeshiftproductions.com",
    "https://www.lamb-of-god.com",
    "https://www.harpercollins.ca",
    "https://www.hopkintontownlibrary.org",
    "https://www.cnap.fr",
    "https://www.music.iastate.edu",
    "https://www.luriya.com",
    "https://www.ccsd15.net",
    "https://www.vivid.ro",
    "https://www.lizziefortunato.com",
    "https://www.chicagobooth.edu",
    "https://www.hacksontap.com",
    "https://www.lincolnpl.org",
    "https://www.hartwell.co.uk",
    "https://www.ugandainvest.go.ug",
    "https://www.ece.ucf.edu",
    "https://www.healthpills24x7.com",
    "https://www.scott.senate.gov",
    "https://www.euttaranchal.com"
]

print(f"Testing {len(PHISHING_URLS)} phishing + {len(LEGIT_URLS)} legitimate URLs (Fixed List)")
print()
print("=" * 80)
print("TESTING 50 PHISHING URLs (Expected: PHISHING)")
print("=" * 80)

phishing_correct = 0
phishing_wrong = []
for i, url in enumerate(PHISHING_URLS, 1):
    try:
        r = requests.post(API_URL, json={'url': url}, timeout=10)
        data = r.json()
        result = data.get('result', 'ERROR')
        conf = data.get('confidence', 0)
        if result == 'PHISHING':
            phishing_correct += 1
            status = "OK"
        else:
            status = "WRONG"
            phishing_wrong.append(url[:50])
        print(f"[{i:02d}] {status:<5} {result:<12} {conf:.1%}  {url[:55]}")
    except Exception as e:
        print(f"[{i:02d}] ERROR: {e}")

print()
print("=" * 80)
print("TESTING 50 LEGITIMATE URLs (Expected: LEGITIMATE)")
print("=" * 80)

legit_correct = 0
legit_wrong = []
for i, url in enumerate(LEGIT_URLS, 1):
    try:
        r = requests.post(API_URL, json={'url': url}, timeout=10)
        data = r.json()
        result = data.get('result', 'ERROR')
        conf = data.get('confidence', 0)
        if result == 'LEGITIMATE':
            legit_correct += 1
            status = "OK"
        else:
            status = "WRONG"
            legit_wrong.append(url[:50])
        print(f"[{i:02d}] {status:<5} {result:<12} {conf:.1%}  {url[:55]}")
    except Exception as e:
        print(f"[{i:02d}] ERROR: {e}")

print()
print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Phishing URLs correctly identified:   {phishing_correct}/50 ({phishing_correct*2}%)")
print(f"Legitimate URLs correctly identified: {legit_correct}/50 ({legit_correct*2}%)")
total = phishing_correct + legit_correct
print(f"Overall Accuracy:                     {total}/100 ({total}%)")
print()
print(f"False Negatives (Phishing marked Legit): {50 - phishing_correct}")
print(f"False Positives (Legit marked Phishing): {50 - legit_correct}")
print("=" * 80)
