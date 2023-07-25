import logging

from harmonise.zooma import ZoomaClient


class FieldMatchingService:

    def __init__(self, base_url):

        self.base_url = base_url

        self.field_dict = {
            'propertyValue': None,
            'semanticTags': None,
            'confidence': None
        }

        logging.basicConfig(filename='log_file.log', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def get_field_dict(self):
        zooma_client = ZoomaClient(base_url=self.base_url)
        field_label_json = zooma_client.field_label()

        if field_label_json is not None:
            for i, el in enumerate(field_label_json):
                try:
                    self.field_dict['propertyValue'] = el['annotatedProperty']['propertyValue']
                    self.field_dict['semanticTags'] = el['semanticTags']
                    self.field_dict['confidence'] = el['confidence']
                except Exception as e:
                    logging.error(f"An error occurred while processing element {i}: {e}")

        return self.field_dict


def get_match(file_path: str):
    match_dict = dict()

    with open(file_path, 'r') as f:
        labels = list(map(lambda s: s.strip(), f.readlines()))

        for label in labels:
            if len(label) != 0:
                fm_cl = FieldMatchingService(
                    base_url=f'http://www.ebi.ac.uk/spot/zooma/v2/api/services/annotate?propertyValue={label}'
                )
                field_dict = fm_cl.get_field_dict()
                match_dict[label] = field_dict

    return match_dict
