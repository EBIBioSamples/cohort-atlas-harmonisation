from harmonise.zooma import ZoomaClient


class FieldMatchingService:

    field_dict = {
        'propertyValue': None,
        'semanticTags': None,
        'confidence': None
    }

    def __init__(self):
        pass

    def get_field_dict(self, url):
        z_cl = ZoomaClient()
        resp_json = z_cl.get_json(url=url)

        if resp_json is not None:
            for i, el in enumerate(resp_json):
                try:
                    self.field_dict['propertyValue'] = el['annotatedProperty']['propertyValue']
                    self.field_dict['semanticTags'] = el['semanticTags']
                    self.field_dict['confidence'] = el['confidence']
                except Exception as e:
                    print(e)

        return self.field_dict


def get_match(file_path: str):
    match_dict = dict()

    with open(file_path, 'r') as f:
        labels = list(map(lambda s: s.strip(), f.readlines()))

        for label in labels:
            if len(label) != 0:
                fm_cl = FieldMatchingService()
                field_dict = fm_cl.get_field_dict(
                    url=f'http://www.ebi.ac.uk/spot/zooma/v2/api/services/annotate?propertyValue={label}'
                )
                match_dict[label] = field_dict

    return match_dict
