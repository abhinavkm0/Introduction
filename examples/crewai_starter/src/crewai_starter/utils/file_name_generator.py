import datetime
import uuid

def generate_filename(extension: str = "md"):
    # Get current date and time
    now = datetime.datetime.now()
    
    # Format date and time as dd_mm_yy-mm_hh
    date_time_part = now.strftime("%d_%m_%y-%M_%H")
    
    # Generate a UUID4 and get its hex representation
    uuid_part = uuid.uuid4().hex
    
    # Combine all parts
    filename = f"{date_time_part}-{uuid_part}"
    
    return f"{filename}.{extension}"
