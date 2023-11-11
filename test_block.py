import main

def test_block():
    emailResults = []
    testSet = {
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
        emailResult = main.processingEmail.processingEmail(item)
        emailResults.append(emailResult)
    print(emailResults)

