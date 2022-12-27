import json


class Product:
    def __init__(self, name: str, reference: str, price: str, availability: str, img: str, link: str):
        self.name = name
        self.reference = reference
        self.price = price
        self.availability = availability
        self.img = img
        self.link = link

    def __str__(self):
        return "name : " + self.name + " reference : " + self.reference + " price : " + self.price + " availability : " + self.availability + " img : " + self.img + " link : " + self.link

    def toJSON(self):
        # return json.dumps(self, default=lambda o: o.__dict__,
        #                   sort_keys=True, indent=4)

        encodedUnicode = json.dumps(self.__dict__, ensure_ascii=False)  # use dump() method to write it in file
        return json.loads(encodedUnicode)
