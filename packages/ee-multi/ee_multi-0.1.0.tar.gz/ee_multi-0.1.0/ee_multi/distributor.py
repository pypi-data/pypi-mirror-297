import ee
import json

class GEEDistributor:
    def __init__(self, json_files):
        self.json_files = json_files
        self.aoi_index = 0

    def initialize_ee(self, json_file):
        with open(json_file) as f:
            credentials = json.load(f)
            ee.Initialize(ee.ServiceAccountCredentials(credentials['client_email'], credentials['private_key']))

    def process_aoi(self, aoi, processing_function):
        self.initialize_ee(self.json_files[self.aoi_index])
        
        # Process the AOI
        result = aoi.map(processing_function)
        
        # Export results (customize as needed)
        export_desc = f"AOI_{self.aoi_index + 1}_results"
        ee.batch.Export.table.toDrive(collection=result, description=export_desc, fileFormat='CSV').start()
        
        self.aoi_index += 1

    def distribute_processing(self, aois, processing_function):
        for aoi in aois:
            self.process_aoi(aoi, processing_function)
            if self.aoi_index >= len(self.json_files):
                print("All accounts have been utilized. Remaining AOIs will not be processed.")
                break
