from dataclasses import dataclass
from datetime import datetime, date
import yaml
from typing import Literal
import dataclasses

FILE_NAME = ""

@dataclass
class JSONEntry:
    title: str
    abstract_deadline: datetime | None
    paper_deadline: datetime | None
    review_start: datetime | None
    review_end: datetime | None
    notification_date: datetime | None
    start_date: datetime | None
    end_date: datetime | None
    hindex: int
    sub: str | list[str]
    link: str
    place: str
    core_rating: Literal["A", "A*", "B"] | None
    note: str


if __name__ == "__main__":
    with open(FILE_NAME, "r") as f:
        data = yaml.safe_load(f)

    json_output = []
    for entry in data:
        # Define default values for missing fields
        defaults = {
            "abstract_deadline": None,
            "deadline": None, # Changed from paper_deadline to deadline
            "review_start": None,
            "review_end": None,
            "notification_date": None,
            "start": None, # Changed from start_date to start
            "end": None, # Changed from end_date to end
            "hindex": -1,
            "sub": "UNKNOWN",
            "link": "#",
            "place": "Unknown",
            "core_rating": "B", # Default to "B"
            "note": "",
        }

        # Convert string dates to datetime objects if they are strings, otherwise use directly
        abstract_deadline = entry.get("abstract_deadline")
        if isinstance(abstract_deadline, str):
            try:
                abstract_deadline = datetime.strptime(abstract_deadline, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                abstract_deadline = datetime.strptime(abstract_deadline, '%Y-%m-%d %H:%M')
        elif isinstance(abstract_deadline, date): # Handle already parsed date objects
            abstract_deadline = datetime.combine(abstract_deadline, datetime.min.time())

        paper_deadline = entry.get("deadline") 
        if isinstance(paper_deadline, str):
            try:
                paper_deadline = datetime.strptime(paper_deadline, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                paper_deadline = datetime.strptime(paper_deadline, '%Y-%m-%d %H:%M')
        elif isinstance(paper_deadline, date): # Handle already parsed date objects
            paper_deadline = datetime.combine(paper_deadline, datetime.min.time())

        start_date = entry.get("start")
        if isinstance(start_date, str):
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError: # Handle cases like '2025-2-28' for WACV
                year, month, day = map(int, start_date.split('-'))
                start_date = date(year, month, day)
                start_date = datetime.combine(start_date, datetime.min.time())
        elif isinstance(start_date, date): # Handle already parsed date objects
            start_date = datetime.combine(start_date, datetime.min.time())

        end_date = entry.get("end")
        if isinstance(end_date, str):
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError: # Handle cases like '2025-3-4' for WACV
                year, month, day = map(int, end_date.split('-'))
                end_date = date(year, month, day)
                end_date = datetime.combine(end_date, datetime.min.time())
        elif isinstance(end_date, date): # Handle already parsed date objects
            end_date = datetime.combine(end_date, datetime.min.time())

        json_entry = JSONEntry(
            title=entry["title"],
            abstract_deadline=abstract_deadline if abstract_deadline is not None else defaults["abstract_deadline"],
            paper_deadline=paper_deadline if paper_deadline is not None else defaults["deadline"],
            review_start=defaults["review_start"],
            review_end=defaults["review_end"],
            notification_date=defaults["notification_date"],
            start_date=start_date if start_date is not None else defaults["start"],
            end_date=end_date if end_date is not None else defaults["end"],
            hindex=entry.get("hindex", defaults["hindex"]),
            sub=entry.get("sub", defaults["sub"]),
            link=entry.get("link", defaults["link"]),
            place=entry.get("place", defaults["place"]),
            core_rating=entry.get("core_rating", defaults["core_rating"]),
            note=entry.get("note", defaults["note"])
        )
        json_output.append(dataclasses.asdict(json_entry))

    import json
    with open(FILE_NAME.replace(".yaml", ".json"), "w") as f:
        json.dump(json_output, f, indent=4, default=str)



