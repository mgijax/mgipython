
class SampleGrouper:

    def group_samples(self, samples):
        sample_hash = {}
        for row in samples:
            if row.getKey() in sample_hash:
                self.mergeRawSample(sample_hash[row.getKey()], row)
            else:
                sample_hash[row.getKey()] = row
        keylist = sample_hash.keys()
        keylist.sort()
        retlist = []
        for key in keylist:
            retlist.append(sample_hash[key])
        return retlist

    def mergeRawSample(self, target_object, source_object):

        char_hash = {}
        for char in target_object.characteristic:
            if char["category"] not in char_hash:
                char_hash[char["category"]] = char

        for char in source_object.characteristic:
            if char["category"] in char_hash:
                if char_hash[char["category"]]["value"] == None:
                    char_hash[char["category"]]["value"] = ""
                if char["value"] == None:
                    char["value"] = ""
                if char_hash[char["category"]]["value"] != char["value"]:
                    char_hash[char["category"]]["value"] = char_hash[char["category"]]["value"] + char["value"]
            else:
                char_hash[char["category"]] = char

        source_hash = {}
        if "comment" not in target_object.source:
            target_object.source["comment"] = []
        if "comment" not in source_object.source:
            source_object.source["comment"] = []
  
        if type(target_object.source["comment"]) is list:
            for source in target_object.source["comment"]:
                if source["name"] not in source_hash:
                    source_hash[source["name"]] = source
        else:
            source = target_object.source["comment"]
            if source["name"] not in source_hash:
                source_hash[source["name"]] = source

        if type(source_object.source["comment"]) is list:
            for source in source_object.source["comment"]:
                if source["name"] in source_hash:
                    if source_hash[source["name"]]["value"] == None:
                        source_hash[source["name"]]["value"] = ""
                    if source["value"] == None:
                        source["value"] = ""
                    if source_hash[source["name"]]["value"] != source["value"]:
                        source_hash[source["name"]]["value"] = source_hash[source["name"]]["value"] + source["value"]
                else:
                    source_hash[source["name"]] = source
        else:
            source = source_object.source["comment"]
            if source["name"] not in source_hash:
                source_hash[source["name"]] = source

        var_hash = {}
        if target_object.variable:
            for var in target_object.variable:
                if var["name"] not in var_hash:
                    var_hash[var["name"]] = var

        if source_object.variable:
            for var in source_object.variable:
                if var["name"] in var_hash:
                    if var_hash[var["name"]]["value"] == None:
                        var_hash[var["name"]]["value"] = ""
                    if var["value"] == None:
                        var["value"] = ""
                    if var_hash[var["name"]]["value"] != var["value"]:
                        var_hash[var["name"]]["value"] = var_hash[var["name"]]["value"] + var["value"]
                else:
                    var_hash[var["name"]] = var
