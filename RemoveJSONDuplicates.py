import json

# Opening JSON file
f = open('PortainerTemplate.json')

# returns JSON object as 
# a dictionary
data = json.load(f)


def remove_duplicate_items(_api_data, _key):
    print("Initial items in list: {}".format(len(_api_data)))
    unique_elements = []
    cleaned_data = []
    keys = []
    for i, j in enumerate(_api_data):
        print("Element i in j i={}, j={}".format(i, j["title"]))
        print("Items in child: {}".format(len(j)))

        print("Child content: {}".format(j))
        print("------------------")

        if _key not in unique_elements:
            unique_elements.append(j)
            keys.append(j[_key])
            print("Found key")

        # print("------------------")

        # print("Search content: {}".format([j][_key]))

        # print("------------------")

        # if _api_data[i][j][_key] not in unique_elements:
        #     unique_elements.append(_api_data[i][j][_key])
        #     keys.append(i)
    # print("Available keys: {}".format(keys))

    for i, j in enumerate(keys):
        cleaned_data.append(_api_data[i])

    print(
        "Total duplicates removed: {}, Total items: {}, Final items:{}".format(
            (len(_api_data) - len(unique_elements)),
            len(_api_data), len(unique_elements)))
    print("Final items in list: {}".format(len(cleaned_data)))

    return cleaned_data


unique_data = remove_duplicate_items(data['templates'], "title")

# Writing to sample.json
with open("unique_data.json", "w") as outfile:
    outfile.write(unique_data)
