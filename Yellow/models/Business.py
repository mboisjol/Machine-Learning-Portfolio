class Business:
    def __init__(self, name, phone=None, address=None, province=None, email=None, contact=None):
        self.name = name

        if phone is None:
            self.phone = "N/A"
        else:
            self.phone = phone

        if address is None:
            self.address = "N/A"
        else:
            self.address = address

        if province is None:
            self.province = "N/A"
        else:
            self.province = province

        if email is None:
            self.email = "N/A"
        else:
            self.email = email

        if contact is None:
            self.contact = "N/A"
        else:
            self.contact = contact

    @staticmethod
    def from_dict(json):
        name = json["name"]
        phone = json["phone"]
        address = json["address"]
        province = json["province"]
        email = json["email"]
        contact = json["contact"]

        return Business(name=name, phone=phone, address=address, province=province, email=email, contact=contact)
