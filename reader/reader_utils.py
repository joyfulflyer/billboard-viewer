

def convert_to_spaces(input):
    return " ".join(input.split('_'))


def convert_entry_to_dict(entries):
    r = [{'name': e.name, 'artist': e.artist, 'id': e.id} for e in entries]
    return r


def convert_rows_to_dict(rows):
    return [dict(r) for r in rows]
