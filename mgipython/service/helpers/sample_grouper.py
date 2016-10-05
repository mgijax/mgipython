
class SampleGrouper:

    def group_samples(self, samples):
        sample_hash = {}
        for row in samples:
            if row.getKey() in sample_hash:
                sample_hash[row.getKey()].mergeRawSample(row)
            else:
                sample_hash[row.getKey()] = row
        keylist = sample_hash.keys()
        keylist.sort()
        retlist = []
        for key in keylist:
            retlist.append(sample_hash[key])
        return retlist
