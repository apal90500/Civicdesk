import uuid
def generate_ticket():
    return "CD-" + str(uuid.uuid4())[:8]