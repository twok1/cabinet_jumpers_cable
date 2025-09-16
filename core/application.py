from core.data_parser import DataParser
from core.data_writer import DataWriter
from core.data_merging import DataMerging

class Application:
    def __init__(self, source: str, target: str):
        self.source = source
        self.target = target
        self.parser = DataParser(source)
        self.merger = DataMerging(self.parser.cabinets_connections)
        self.writer = DataWriter(target, self.merger.cabinet_jumpers, self.parser.jumpers_to_lines)
        
    def run(self):
        self.parser.parse_data()
        self.merger.process()
        self.writer.process()
        pass