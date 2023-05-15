import requests


class ZoomaClient:
    def __init__(self):
        pass
    
    def get_json(self, url):
        resp = requests.get(url)
        if resp.status_code == 200:
            return(resp.json())
        return None
        

class FieldMatchingService:
    
    field_dict = {
        'propertyValue': None,
        'semanticTags': None,
        'confidence': None
    }
    
    def __init__(self):
        pass
    
    def get_match(self, url):    
        z_cl = ZoomaClient()
        resp_json = z_cl.get_json(url=url)
        
        outp_dict = dict()
        
        if resp_json is not None:
            outp_dict = dict()
            for i in range(len(resp_json)):
                el = resp_json[i]
                try:
                    self.field_dict['propertyValue'] = el['annotatedProperty']['propertyValue']
                    self.field_dict['semanticTags'] = el['semanticTags']
                    self.field_dict['confidence'] = el['confidence']
                except Exception as e:
                    print(e)

        return self.field_dict
    
    
labels = list()
with open('../../Projects/cohort-atlas_scripts/tests/sample_labels_to_anntate.csv', 'r') as f:
    file = f.readlines()
    for i in range(1, len(file)):
        labels.append(file[i].replace('\n', ''))
        
for label in labels:
    print(label)
    
    fm_cl = FieldMatchingService()
    field_dict = fm_cl.get_match(url=f'http://www.ebi.ac.uk/spot/zooma/v2/api/services/annotate?propertyValue={label}')
    print(field_dict)
    print('-----')
