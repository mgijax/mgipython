from natsort import natsorted, ns

class SampleGrouper:

    def group_raw_samples(self, samples):
        sample_hash = {}
        for row in samples:
            self.mergeDupColumns(row.raw_sample)
        for row in samples:
            if row.getKey() in sample_hash:
                self.mergeRawSample(sample_hash[row.getKey()].raw_sample, row.raw_sample)
            else:
                sample_hash[row.getKey()] = row
        keylist = natsorted(sample_hash.keys(), key=lambda y: str(y).lower())
        retlist = []
        for key in keylist:
            retlist.append(sample_hash[key])
        return retlist


    def mergeDupColumns(self, source_object):

        char_hash = {}
        char_ret_hash = []
        for char in source_object.characteristic:
            if "unit" in char:
                char["value"] = str(char["value"]) + " " + str(char["unit"])
             
            if char["category"] not in char_hash:
                char_hash[char["category"]] = char
                oldval = char["value"]
                char_hash[char["category"]]["value"] = []
                char_hash[char["category"]]["value"].append(str(oldval))
                char_ret_hash.append(char)
            else:
                if char["value"] not in char_hash[char["category"]]["value"]:
                    char_hash[char["category"]]["value"].append(char["value"])
        source_object.characteristic = char_ret_hash

        if source_object.variable:
            var_hash = {}
            var_ret_hash = []
            for var in source_object.variable:
                if var["name"] not in var_hash:
                    var_hash[var["name"]] = var
                    oldval = var["value"]
                    var_hash[var["name"]]["value"] = []
                    var_hash[var["name"]]["value"].append(str(oldval))
                    var_ret_hash.append(var)
                else:
                    if var["value"] not in var_hash[var["name"]]["value"]:
                        var_hash[var["name"]]["value"].append(var["value"])
            source_object.variable = var_ret_hash

        source_hash = {}
        source_ret_hash = []
        if "comment" not in source_object.source:
            source_object.source["comment"] = []
  
        if type(source_object.source["comment"]) is list:
            for source in source_object.source["comment"]:
                if source["name"] not in source_hash:
                    source_hash[source["name"]] = source
                    oldval = source["value"]
                    source_hash[source["name"]]["value"] = []
                    source_hash[source["name"]]["value"].append(str(oldval))
                    source_ret_hash.append(source)
                else:
                    if source["value"] not in source_hash[source["name"]]["value"]:
                        source_hash[source["name"]]["value"].append(source["value"])
        else:
            source = source_object.source["comment"]
            if source["name"] not in source_hash:
                source_hash[source["name"]] = source
                oldval = source["value"]
                source_hash[source["name"]]["value"] = []
                source_hash[source["name"]]["value"].append(str(oldval))
                source_ret_hash.append(source)
            else:
                if source["value"] not in source_hash[source["name"]]["value"]:
                    source_hash[source["name"]]["value"].append(source["value"])
        source_object.source["comment"] = source_ret_hash

    def mergeRawSample(self, target_object, source_object):
        self.filterOutDups(target_object.characteristic, source_object.characteristic, "category", "value")
        self.filterOutDups(target_object.variable, source_object.variable, "name", "value")
        self.filterOutDups(target_object.source["comment"], source_object.source["comment"], "name", "value")

    def filterOutDups(self, target_object_list, source_object_list, prime_field_name, sub_field_name):
        if target_object_list != None and source_object_list != None:
            item_hash = {}
            for item in target_object_list:
                if item[prime_field_name] not in item_hash:
                    item_hash[item[prime_field_name]] = item

            for item in source_object_list:
                if item[prime_field_name] in item_hash:
                    for value in item[sub_field_name]:
                        if value not in item_hash[item[prime_field_name]][sub_field_name]:
                            item_hash[item[prime_field_name]][sub_field_name].append(value)
                else:
                    item_hash[item[prime_field_name]] = item
