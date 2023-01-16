import json
import requests
import joblib
from os.path import exists
import logging
from datetime import datetime

# Creating and Configuring Logger
Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="logfile_" + str(datetime.now()) + ".log",
                    filemode="w",
                    format=Log_Format,
                    level=logging.DEBUG)

logger = logging.getLogger()

# Testing our Logger
logger.info("Begin with logging")


def collect_templates(_data):
    resultlist = []

    if not exists("resultlist.data"):
        for i, j in enumerate(_data):
            print("i: {} - link:{}".format(i, j["link"]))
            if j["link"] != "":
                response = requests.get(j["link"])
            print("response: {}".format(response))

            if response.status_code == 200:
                print("good response")
                tmpstr = response.text

                res = tmpstr.replace("\n", "").replace("  ", "")

                resdict = json.loads(res)

                tmplist = resdict["templates"]
                resultlist.append(tmplist)

        joblib.dump(resultlist, "resultlist.data")


def sortlists(_lists):
    _clearedlist = []
    _dupList = []
    _titles = []
    _postions = []

    i = 0

    for list in _lists:
        for elements in list:
            title = elements["title"]
            if title != "":
                if title not in _titles:
                    _titles.append(elements["title"])
                    _clearedlist.append(elements)
                else:
                    logger.info("Found duplicate entry with title '{}'. Start check deeper differences".format(title))
                    dupPos = _titles.index(title)
                    _existingElement = _clearedlist[dupPos]
                    tmpElement = elements

                    tmpElement["title"] = "dup_" + str(i) + "_" + tmpElement["title"]
                    logger.info("Changed duplicate name with ({}) to {}".format(i, tmpElement["title"]))

                    _dupList.append(tmpElement)

                    for d1, (d2, d3) in enumerate(elements.items()):
                        for e1, (e2, e3) in enumerate(_existingElement.items()):
                            if d2 == e2 and d3 == e3:
                                break
                            elif d1 == e1 and str(d2).lower() == str(e2).lower() and str(d3).lower() != str(e3).lower():
                                if str(d2).lower() == "logo" or str(d2).lower() == "description":
                                    logger.info("    Found difference @ {}".format(d2))
                                    logger.info("        {}".format(d3))
                                    logger.info("        {}".format(e3))
                                else:
                                    logger.warning("    Found difference @ {}".format(d2))
                                    logger.warning("        {}".format(d3))
                                    logger.warning("        {}".format(e3))
            else:
                print("Somethig wrong with dictionary element 'title': {}".format(title))
            i = i + 1

    return _clearedlist, _dupList

def createPortainerJSON(_data):
    tmpdict = {}
    tmpdict["version"] = 2

    # for listitem in _data:
    #     print(listitem)
    #     ...

    tmpdict["templates"] = _data

    return tmpdict


def main():
    # Opening templatelists.json file
    templatefile = open('templatelists.json')
    data = json.load(templatefile)

    collect_templates(data)

    unclearedlist = joblib.load("resultlist.data")

    clearedList, duplicateList = sortlists(unclearedlist)

    clearResult = createPortainerJSON(clearedList)
    duplicateResult = createPortainerJSON(duplicateList)

    with open("clearResult.json", "w") as outfile_clear:
        json.dump(clearResult, outfile_clear)

    with open("duplicateResult.json", "w") as outfile_dup:
        json.dump(duplicateResult, outfile_dup)


    #ToDo: count log files and hold last 5. Delete the rest
    #ToDo: create subfolder and extract from the cleared list each dict entry to a separate portainer file

    print("Generated two lists. \n Cleared List: {} \n Duplicate List: {}".format(len(clearedList), len(duplicateList)))
    logger.info(
        "Generated two lists. A clear list without any duplicates and one list with all filtered duplicates \n "
        "Cleared List has {} elements \n "
        "Duplicate List has {} elements".format(len(clearedList), len(duplicateList)))

if __name__ == "__main__":
    main()
