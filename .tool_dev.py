import json
import random
import app.osint.tools as tools
from datetime import datetime
from app.osint import tagging_handler, links_handler, enrichments_handler
from app.osint.utils import (
    get_type,
    remove_missingapikey_results,
    sort_results,
    refang,
)


class TestIndicator:
    def __init__(self, indicator):
        """
        Initialize the TestIndicator object with an indicator to search for
        """
        self.id = random.randint(1, 999)
        self.time_created = datetime.now()
        self.time_updated = None
        self.processing_time = None
        self.creator = "test_user"
        self.username = "test_user"
        self.indicator = refang(indicator).strip()
        self.indicator_type = get_type(self.indicator)
        self.results = []
        self.external_links = []
        self.tags = []
        self.notes = None
        self.enrichments = []
        self.complete = False
        self.ioc_id = None
        self.ioc = None

    def run_tools(self):
        """
        Run all tools on the indicator
        """
        self.results = tools.run_tools(self)
        self.results = sorted(self.results, key=sort_results)
        self.results = remove_missingapikey_results(self.results)
        return self.results

    def run_tagging(self):
        """
        Tag the indicator
        """
        self.run_tools()
        self.tags = tagging_handler(self)
        return self.tags

    def get_links(self):
        """
        Add external links to the indicator
        """
        self.external_links = links_handler(self)
        return self.external_links

    def get_enrichments(self):
        """
        Add enrichments to the indicator
        """
        self.run_tools()
        self.enrichments = enrichments_handler(self)
        return self.enrichments


def print_and_write_output(data):
    print(json.dumps(data, indent=4))
    with open("./.tool_dev.json", "w") as outfile:
        json.dump(data, outfile, indent=4)


indicator = TestIndicator(
    indicator="6f0fac3b955e63f25bd199ec373c677152212fceda20d8bc6672cf62e68482e8"
)

# Run a specific tool
print_and_write_output(tools.malware_bazzar(indicator))

# Run all tools
# print_and_write_output(indicator.run_tools())

# Run tagging
# print_and_write_output(indicator.run_tagging())

# Get external links
# print_and_write_output(indicator.get_links())

# Get enrichments
# print_and_write_output(indicator.get_enrichments())
