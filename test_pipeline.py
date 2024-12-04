import unittest
from PipelineRecord import FormattedPipelineRecord, load_data_from_file, PipelineRecord

class TestPipeline(unittest.TestCase):
    """
    Unit tests for the pipeline program.
    """
    print("Test by Pavel Boukine")

    def test_load_data_from_file(self):
        """
        Test that the load_data_from_file function correctly loads records.
        """
        file_name = 'keystone-throughput-and-capacity.csv'
        records = load_data_from_file(file_name)

        # Assert that the records list is not empty
        self.assertGreater(len(records), 0, "No records were loaded from the file.")
        
        # Assert that the correct number of records are loaded (or fewer if file contains fewer)
        self.assertLessEqual(len(records), 100, "More than 100 records were loaded.")
        
        # Assert that the records are instances of PipelineRecord
        for record in records:
            self.assertIsInstance(record, PipelineRecord, "Record is not of type PipelineRecord.")

class TestPipelineRecord(unittest.TestCase):
    def test_pipeline_record_str(self):
        """
        Test the string representation of PipelineRecord.
        """
        record = PipelineRecord("500", "200")
        expected_output = "Throughput: 500 (1000 m3/d), Available Capacity: 200 (1000 m3/d)"
        self.assertEqual(str(record), expected_output)

    def test_formatted_pipeline_record_str(self):
        """
        Test the custom string representation of FormattedPipelineRecord.
        """
        record = FormattedPipelineRecord("600", "300")
        expected_output = (
            "\n********** Formatted Pipeline Record **********\n"
            "🚀 Throughput       : 600 (1000 m3/d)\n"
            "💧 Available Capacity: 300 (1000 m3/d)\n"
            "***********************************************"
        )

if __name__ == "__main__":
    unittest.main()
