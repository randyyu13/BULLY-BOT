from scrape_utils import *
from misc_utils import *
import datetime
import pytz
from dotenv import load_dotenv

load_dotenv()
current_datetime = datetime.datetime.now(pytz.UTC)
timestamp_string = current_datetime.strftime("%m_%d_%H")
output_file_name = f"output_{timestamp_string}.txt"

timestamp_string = current_datetime.strftime("%m_%d_%H")
output_file_name = f"output_{timestamp_string}.txt"

payload = get_prize_picks_payload()
parsed_payload = parse_payload(payload)
good_lines = find_good_lines(parsed_payload)
write_array_to_file(good_lines, output_file_name)