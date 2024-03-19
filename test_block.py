import main
import processingEmail


def test_block():
    emailResults = []
    testSet = {
        "https://good-kvadro.com/"
        # "https://paevskiydesign.ru/"
        # "https://www.houseandflat.net/"
        # "https://www.idaspb.com"
        # "https://lp.laresds.ru/",
        # "https://www.o-mossur.ru",
        # "https://www.kovalchuk-interior.com",
        # "https://krasikovadesign.com",
        # "https://Simmetria.pro",
        # "https://www.nw-interior.com/",

        # "https://designleo.ru",
        # "https://www.starikova-design.ru"
        # "https://pechenyi.com",
        # "https://kutenkovs.com",
        # "https://marinasvetlova.ru",
        # "https://a-e-studio.ru/",
        # "https://NomadForm.ru",
        # "https://artek-studio.ru",
        # "https://gordd.ru",
        # "https://aleksandrainteriors.ru/"
        # "https://scandinavi.ru/",
        # "https://loft-and-home.ru/work/",
        # "https://art-remont.ru",
        # "https://sv-servise.ru/"
        # "https://flatsdesign.com/",
        # "https://admagroup.ru"

        # "https://ukvartira.ru/",
        # "https://moscow-interior.ru/",
        # "https://domeo-design.ru/",
        # "https://vproekte.com",
        # "https://arhint.ru",
        # "https://intek-design.ru",
        # "https://d-sav.ru",
        # "https://rerooms.ru/",
        # "https://linum.group",
        # "https://www.egupova.spb.ru",
        # "https://www.nsdsgn.ru",
        # "https://buro9.ru/",
        # "https://tbdesign.pro/"
    }
    testList = list(testSet)
    for item in testSet:
        print(f"{processingEmail.isIriValid(item)}")
        emailResult = main.processingEmail.processingEmail(item)
        emailResults.append(emailResult)
    print(emailResults)

def test_block2():
    url = "https://www.houzz.ru/professionaly/dizaynery-interyera/arhitekturno-proektnaya-masterskaya-№1-pfvwru-pf~850626898"
    main.fetchSiteSoup(url)