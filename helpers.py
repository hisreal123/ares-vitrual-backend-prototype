import random
import string
from models import Meeting

def  generate_meeting_id():
    while True:
        meeting_id = ''.join(str(random.randint(0,9)) for _ in range(13))
        if not Meeting.query.filter_by(meeting_id=meeting_id).first():
            return meeting_id


def generate_passcode(length=18):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))