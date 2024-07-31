from services.facit_api import pull_stat_mapping


def build_mapping_keys():
    resp = pull_stat_mapping()
    mapping = resp.get('mapping', {})

    mapping_keys = {}
    map_info = {}

    for key, value in mapping.items():
        val_name = value.get('label', {}).get('en')
        mapping_keys[key] = val_name
        if val_name == 'Map':
            values = value.get('values', {})
            for v_key, v_value in values.items():
                map_info[v_key] = v_value.get('label', {}).get('en')
    return mapping_keys, map_info
