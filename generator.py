import os
from jinja2 import Environment, PackageLoader, select_autoescape
from jinja2 import FileSystemLoader

# Przygotowywuję folder na generowane pliki
if not os.path.exists("generated_files"):
    os.makedirs("generated_files")

path = os.path.dirname(os.path.abspath(__file__))
env = Environment(
    # loader=PackageLoader('generator', 'templates'),
    # autoescape=select_autoescape(['html', 'xml'])
    autoescape=False,
    loader=FileSystemLoader(os.path.join(path, 'templates'))
)
template = env.get_template('my_template.html')

# # testGeneratora
# for x in range(10):
#     outputName = "output" + str(x) + ".html"
#     with open("generated_files/" + outputName, 'w') as f:
#         html = env.get_template('my_template.html').render({'x': x})
#         f.write(html)


# PARSOWANIE XML'a
from xml.etree import ElementTree
xml_tree = ElementTree.parse(path+"/data/TERC_Urzedowy_2018-03-02.xml")
xml_teryt = xml_tree.getroot()
print(xml_teryt.tag)
print("-----------------")

# musiałem to doinstalować
import xlrd
xls_file = xlrd.open_workbook(path+"/data/gm-kraj-posortowane.xls")
# xls_data = xls_file.sheet_by_name("gl")
xls_data = xls_file.sheet_by_index(0)

wszystkie_obwody = 0
 # Polska, wojewodztwo, okręg, powiat, gmina

# print(str(xls_data.cell(2495, 4).value))
ile_wierszy = 0
for x in xls_data.get_rows():
    ile_wierszy += 1

kandydaci = [xls_data.cell(0, 10 + x).value for x in range(12)]

print("start")

Polska = {}
wojewodztwa = {}
okregi = {}
gminy = {}

def oblicz_Polska():
    obwody = uprawnieni = karty_wydane = glosy_oddane = glosy_niewazne = glosy_wazne = 0
    zebrane_glosy = [0 for i in range(12)]
    wyniki = {
        "obwody": obwody,
        "uprawnieni": uprawnieni,
        "karty_wydane": karty_wydane,
        "glosy_oddane": glosy_oddane,
        "glosy_niewazne": glosy_niewazne,
        "glosy_wazne": glosy_wazne,
        "zebrane_glosy": zebrane_glosy
    }
    Polska["id_nazwa"] = "Polska"
    Polska["wyniki"] = wyniki
    Polska["wojewodztwa"] = []

def oblicz_wojewodztwa():
    for catalog in xml_teryt:
        print(catalog.tag)
        for row in catalog:
            if row[1].text is None and row[2].text is None:
                obwody = uprawnieni = karty_wydane = glosy_oddane = glosy_niewazne = glosy_wazne = 0
                zebrane_glosy = [0 for i in range(12)]
                wyniki = {
                    "obwody": obwody,
                    "uprawnieni": uprawnieni,
                    "karty_wydane": karty_wydane,
                    "glosy_oddane": glosy_oddane,
                    "glosy_niewazne": glosy_niewazne,
                    "glosy_wazne": glosy_wazne,
                    "zebrane_glosy": zebrane_glosy
                }
                nazwa = {
                    "wojewodztwo": row[4].text,
                    "okreg": "",
                    "gmina": ""
                }
                wojewodztwa[str(row[0].text)] = {
                    "id_nazwa": row[4].text,
                    "nazwa": nazwa,
                    "wyniki": wyniki,
                    "okregi": []
                }
                print(len(Polska["wojewodztwa"]))
                Polska["wojewodztwa"].append(wojewodztwa[str(row[0].text)])
    print("Stworzylem wojewodztwa")

def oblicz_okregi():
    nr_wiersza = 1
    while nr_wiersza < ile_wierszy:
        num = str(xls_data.cell(nr_wiersza, 1).value[:2])
        # print("num1 ok - " + num)
        okreg = ""
        if int(xls_data.cell(nr_wiersza, 0).value) < 10:
            okreg += "0"
        okreg += str(int(xls_data.cell(nr_wiersza, 0).value))
        num += okreg

        if num not in okregi.keys():
            obwody = uprawnieni = karty_wydane = glosy_oddane = glosy_niewazne = glosy_wazne = 0
            zebrane_glosy = [0 for i in range(12)]
            wyniki = {
                "obwody": obwody,
                "uprawnieni": uprawnieni,
                "karty_wydane": karty_wydane,
                "glosy_oddane": glosy_oddane,
                "glosy_niewazne": glosy_niewazne,
                "glosy_wazne": glosy_wazne,
                "zebrane_glosy": zebrane_glosy
            }
            nazwa = {
                "wojewodztwo": wojewodztwa[str(xls_data.cell(nr_wiersza, 1).value[:2])]['nazwa']['wojewodztwo'],
                "okreg": okreg,
                "gmina": ""
            }
            okregi[num] = {
                "id_nazwa": okreg,
                "nazwa": nazwa,
                "wyniki": wyniki,
                "gminy": []
            }
            wojewodztwa[num[:2]]["okregi"].append(okregi[num])
        nr_wiersza += 1
    print("Stworzylem okręgi")


def oblicz_gminy():
    nr_wiersza = 1
    while nr_wiersza < ile_wierszy:
        num = str(xls_data.cell(nr_wiersza, 1).value[:2])
        # print("num1 - " + num)
        okreg = ""
        if int(xls_data.cell(nr_wiersza, 0).value) < 10:
            okreg += "0"
        okreg += str(int(xls_data.cell(nr_wiersza, 0).value))
        # print("ok - " + okreg)
        num += okreg
        num += str(xls_data.cell(nr_wiersza, 1).value[4:6])
        print("num gminy = " + num)

        obwody = int(xls_data.cell(nr_wiersza, 4).value)
        uprawnieni = int(xls_data.cell(nr_wiersza, 5).value)
        karty_wydane = int(xls_data.cell(nr_wiersza, 6).value)
        glosy_oddane = int(xls_data.cell(nr_wiersza, 7).value)
        glosy_niewazne = int(xls_data.cell(nr_wiersza, 8).value)
        glosy_wazne = int(xls_data.cell(nr_wiersza, 9).value)
        zebrane_glosy = [int(xls_data.cell(nr_wiersza, 10 + x).value) for x in range(12)]
        # print("zebrane glosy : " + str(int(xls_data.cell(nr_wiersza, 10).value)))
        # print("zebrane glosy : " + zebrane_glosy[0])

        wyniki = {
            "obwody": obwody,
            "uprawnieni": uprawnieni,
            "karty_wydane": karty_wydane,
            "glosy_oddane": glosy_oddane,
            "glosy_niewazne": glosy_niewazne,
            "glosy_wazne": glosy_wazne,
            "zebrane_glosy": zebrane_glosy
        }
        nazwa = {
            "wojewodztwo": wojewodztwa[num[:2]]['nazwa']['wojewodztwo'],
            "okreg": okreg,
            "gmina": xls_data.cell(nr_wiersza, 2).value
        }
        gminy[num] = {
            "id_nazwa": xls_data.cell(nr_wiersza, 2).value,
            "nazwa": nazwa,
            "wyniki": wyniki,
        }

        okregi[num[:4]]["gminy"].append(gminy[num])

        nr_wiersza += 1

        Polska["wyniki"]["obwody"] += wyniki["obwody"]
        Polska["wyniki"]["uprawnieni"] += wyniki["uprawnieni"]
        Polska["wyniki"]["karty_wydane"] += wyniki["karty_wydane"]
        Polska["wyniki"]["glosy_oddane"] += wyniki["glosy_oddane"]
        Polska["wyniki"]["glosy_niewazne"] += wyniki["glosy_niewazne"]
        Polska["wyniki"]["glosy_wazne"] += wyniki["glosy_wazne"]
        for x in range(12):
            Polska["wyniki"]["zebrane_glosy"][x] += wyniki["zebrane_glosy"][x]

        wojewodztwa[num[:2]]["wyniki"]["obwody"] += wyniki["obwody"]
        wojewodztwa[num[:2]]["wyniki"]["uprawnieni"] += wyniki["uprawnieni"]
        wojewodztwa[num[:2]]["wyniki"]["karty_wydane"] += wyniki["karty_wydane"]
        wojewodztwa[num[:2]]["wyniki"]["glosy_oddane"] += wyniki["glosy_oddane"]
        wojewodztwa[num[:2]]["wyniki"]["glosy_niewazne"] += wyniki["glosy_niewazne"]
        wojewodztwa[num[:2]]["wyniki"]["glosy_wazne"] += wyniki["glosy_wazne"]
        for x in range(12):
            # print("uhuhuu : " + str(int(wyniki["zebrane_glosy"][0])))
            wojewodztwa[num[:2]]["wyniki"]["zebrane_glosy"][x] += wyniki["zebrane_glosy"][x]

        okregi[num[:4]]["wyniki"]["obwody"] += wyniki["obwody"]
        okregi[num[:4]]["wyniki"]["uprawnieni"] += wyniki["uprawnieni"]
        okregi[num[:4]]["wyniki"]["karty_wydane"] += wyniki["karty_wydane"]
        okregi[num[:4]]["wyniki"]["glosy_oddane"] += wyniki["glosy_oddane"]
        okregi[num[:4]]["wyniki"]["glosy_niewazne"] += wyniki["glosy_niewazne"]
        okregi[num[:4]]["wyniki"]["glosy_wazne"] += wyniki["glosy_wazne"]
        for x in range(12):
            okregi[num[:4]]["wyniki"]["zebrane_glosy"][x] += wyniki["zebrane_glosy"][x]

    print("Stworzylem gminy")


def generuj():

    filename = "Polska.html"
    with open("generated_files/" + filename, 'w') as f:
        html = env.get_template('my_template.html').render({
            "typ_obszaru": "",
            "dane": Polska,
            "kandydaci": kandydaci,
            "linki": Polska["wojewodztwa"],
            "typ_linku": "wojewodztwo",
            "poczatek_linku": "Polska_wojewodztwo"
        })
        f.write(html)

    ile_wygenerowanych_wojewodztw = 0
    print("Wygenerowanych wojewodztw : " + str(ile_wygenerowanych_wojewodztw))
    for woj in Polska["wojewodztwa"]:
        filename = "Polska_wojewodztwo" + woj["id_nazwa"] + ".html"
        with open("generated_files/" + filename, 'w') as f:
            html = env.get_template('my_template.html').render({
                "poczatek_typu_obszaru": "",
                "typ_obszaru": "wojewodztwo ",
                "dane": woj,
                "kandydaci": kandydaci,
                "linki": sorted(woj["okregi"], key=lambda params: params["id_nazwa"]),
                "typ_linku": "okreg",
                "poczatek_linku": "Polska_wojewodztwo" + woj["id_nazwa"] + "_okreg"
            })
            f.write(html)

        for ok in woj["okregi"]:
            filename2 = "Polska" + \
                        "_wojewodztwo" + woj["id_nazwa"] + \
                        "_okreg" + ok["id_nazwa"] + ".html"
            with open("generated_files/" + filename2, 'w') as f2:
                html = env.get_template('my_template.html').render({
                    "poczatek_typu_obszaru": "wojewodztwo " + woj["id_nazwa"] + " --> ",
                    "typ_obszaru": "okręg ",
                    "dane": ok,
                    "kandydaci": kandydaci,
                    "linki": sorted(ok["gminy"], key=lambda params: params["id_nazwa"]),
                    "typ_linku": "gmina",
                    "poczatek_linku": "Polska_wojewodztwo" + woj["id_nazwa"] + "_okreg" + ok["id_nazwa"] + "_gmina"
                })
                f2.write(html)

            for gm in ok["gminy"]:
                filename3 = "Polska" + \
                            "_wojewodztwo" + woj["id_nazwa"] + \
                            "_okreg" + ok["id_nazwa"] + \
                            "_gmina" + gm["id_nazwa"] + ".html"
                with open("generated_files/" + filename3, 'w') as f3:
                    html = env.get_template('my_template.html').render({
                        "poczatek_typu_obszaru": "wojewodztwo " + woj["id_nazwa"] + " --> " +
                                                 "okręg " + ok["id_nazwa"] + " --> ",
                        "typ_obszaru": "gmina ",
                        "dane": gm,
                        "kandydaci": kandydaci,
                    })
                    f3.write(html)

        ile_wygenerowanych_wojewodztw += 1
        print("Wygenerowanych wojewodztw : " + str(ile_wygenerowanych_wojewodztw))

def generuj_test():

    filename = "Polska.html"
    with open("generated_files/" + filename, 'w') as f:
        html = env.get_template('my_template.html').render({
            "typ_obszaru": "",
            "dane": Polska,
            "kandydaci": kandydaci,
            "linki": Polska["wojewodztwa"],
            "typ_linku": "wojewodztwo",
            "poczatek_linku": "Polska_wojewodztwo"
        })
        f.write(html)

oblicz_Polska()
oblicz_wojewodztwa()
oblicz_okregi()
oblicz_gminy()

generuj()
# generuj_test()
