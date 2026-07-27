import unittest
import os
import pandas as pd
from src.formatter import ResultFormatter

class TestResumeScreeningAgent(unittest.TestCase):
    
    def test_export_to_csv(self):
        """Test if the formatter correctly converts data to a DataFrame and saves it."""
        # 1. Create fake dummy data
        dummy_data = [
            {
                "filename": "mock_resume.pdf", 
                "nlp_similarity_score": 95.0,
                "qualitative_grade": "Strong Fit",
                "matched_skills": "Python",
                "missing_skills": "None",
                "rationale": "Great fit."
            }
        ]
        test_output_path = "test_ranked_candidates.csv"
        
        # 2. Run the function
        df = ResultFormatter.export_to_csv(dummy_data, test_output_path)
        
        # 3. Assert (Check) if the results are what we expect
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["filename"], "mock_resume.pdf")
        self.assertTrue(os.path.exists(test_output_path))
        
        # 4. Cleanup the test file so it doesn't clutter your folder
        if os.path.exists(test_output_path):
            os.remove(test_output_path)

if __name__ == "__main__":
    unittest.main()