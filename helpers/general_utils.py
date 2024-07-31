def parse_event(match_jsn):
    event =  match_jsn.get('entity', {})
    return {
        'event_id': event.get('id'),
        'event_name': event.get('name')
    }