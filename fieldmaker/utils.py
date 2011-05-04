
def prep_for_kwargs(dictionary):
    result = dict()
    for key, value in dictionary.iteritems():
        result[str(key)] = value
    return result
