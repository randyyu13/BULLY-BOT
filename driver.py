from dotenv import load_dotenv
from scrape_utils import *
from misc_utils import *

def main():
    load_dotenv()
    payload = get_prize_picks_payload()
    parsed_payload = parse_payload(payload)
    good_lines = find_good_lines(parsed_payload)
    write_array_to_file(good_lines, "good_lines.txt")


if __name__ == "__main__":
    main()