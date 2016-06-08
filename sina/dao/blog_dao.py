import json


class BlogDao(object):
    # blog = {
    #     'post_from': '',
    #     'post_content': '',
    #     'forward': {
    #         "forward_reference": '',
    #         "forward_content": '',
    #         "forward_from": '',
    #         "forward_count": 0,
    #         "repeat_count": 0,
    #         "praise_count": 0
    #     },
    #     'forward_count': 0,
    #     'repeat_count': 0,
    #     'praise_count': 0,
    # }
    def __init__(self):
        self.user_id=0;
        self.post_from=''
        self.post_content=''
        self.forward={}
        self.forward['forward_reference']=''
        self.forward['forward_content'] = ''
        self.forward['forward_from'] = ''
        self.forward['forward_count'] = 0
        self.forward['repeat_count'] = 0
        self.forward['praise_count'] = 0
        self.forward_count=0
        self.repeat_count = 0
        self.praise_count = 0
        return

    def objTojson(self):
        return json.dumps(BlogDao(), default=lambda object: object.__dict__)

