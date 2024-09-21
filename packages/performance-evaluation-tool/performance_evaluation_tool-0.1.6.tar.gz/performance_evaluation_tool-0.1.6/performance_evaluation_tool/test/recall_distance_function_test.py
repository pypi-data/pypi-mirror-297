import unittest
import numpy as np
from performance_evaluation_tool import *

class TestAnnularEvaluation(unittest.TestCase):
    def setUp(self):
        self.height = 200
        self.width = 200
        self.center = (self.width // 2, self.height // 2)
        self.R1 = 20
        self.R2 = 40
        self.R3 = 60
        
        # Colors
        self.IGNORE_COLOR = [255, 255, 255]
        self.C1 = [100, 100, 100]
        self.C2 = [200, 200, 200]
        self.C3 = [150, 150, 150]
        
        # Create fake images
        self.reference_image = np.full((self.height, self.width, 3), self.IGNORE_COLOR, dtype=np.uint8)
        self.query_image = np.full((self.height, self.width, 3), self.IGNORE_COLOR, dtype=np.uint8)
        
        # Set pixels P1, P2, and P3
        self.P1 = (self.center[0] + self.R1, self.center[1])
        self.P2 = (self.center[0] + self.R2, self.center[1])
        self.P3 = (self.center[0] + self.R3, self.center[1])
        
        self.reference_image[self.P1[1], self.P1[0]] = self.C1
        self.reference_image[self.P2[1], self.P2[0]] = self.C2
        self.reference_image[self.P3[1], self.P3[0]] = self.C3
        
        self.query_image[self.P1[1], self.P1[0]] = self.C1
        self.query_image[self.P2[1], self.P2[0]] = self.C2
        self.query_image[self.P3[1], self.P3[0]] = self.C3
        
        # Create ImageInstances
        self.reference_instance = self.create_image_instance(self.reference_image, "reference")
        self.query_instance = self.create_image_instance(self.query_image, "query")
        
        # Create calculator
        self.calculator = SemanticSegmentationMatchCalculator(to_ignore=True, ignore_pixels=self.IGNORE_COLOR)

    def create_image_instance(self, image, name):
        class FakeImageInstance(ImageInstance):
            def __init__(self, image):
                self.image = image
                self._image_fpath = f"/fake/path/{name}.png"
            def load(self):
                return self.image
        
        return FakeImageInstance(image)

    def test_annular_evaluation(self):
        # Case 1: Empty annulus (0 < R < R1)
        try:
            matches, confusion_matrix = self.calculator.match(self.query_instance, self.reference_instance, 0, self.R1 - 1)
            self.fail("Expected ValueError was not raised")
        except ValueError as e:
            self.assertEqual(str(e), "'labels' should contains at least one label.")
        
        # Case 2: Annulus including P1 (0 < R < R2)
        matches, _ = self.calculator.match(self.query_instance, self.reference_instance, 0, self.R2 - 1)
        self.assertEqual(matches['min_radius'], 0)
        self.assertEqual(matches['max_radius'], self.R2 - 1)
        self.assertIn('overall', matches)
        self.assertEqual(matches['overall']['num_matches'], 1)
        self.assertEqual(matches['overall']['num_unmatched_queries'], 0)
        self.assertEqual(matches['overall']['num_unmatched_references'], 0)
        self.assertEqual(matches['overall']['num_query_pixels'], 1)
        self.assertEqual(matches['overall']['num_reference_pixels'], 1)
        
        # Case 3: Annulus including P1 and P2 (0 < R < R3)
        matches, _ = self.calculator.match(self.query_instance, self.reference_instance, 0, self.R3 - 1)
        self.assertEqual(matches['min_radius'], 0)
        self.assertEqual(matches['max_radius'], self.R3 - 1)
        self.assertIn('overall', matches)
        self.assertEqual(matches['overall']['num_matches'], 2)
        self.assertEqual(matches['overall']['num_unmatched_queries'], 0)
        self.assertEqual(matches['overall']['num_unmatched_references'], 0)
        self.assertEqual(matches['overall']['num_query_pixels'], 2)
        self.assertEqual(matches['overall']['num_reference_pixels'], 2)
        
        # Case 4: Annulus including only P2 (R1 < R < R3)
        matches, _ = self.calculator.match(self.query_instance, self.reference_instance, self.R1 + 1, self.R3 - 1)
        self.assertEqual(matches['min_radius'], self.R1 + 1)
        self.assertEqual(matches['max_radius'], self.R3 - 1)
        self.assertIn('overall', matches)
        self.assertEqual(matches['overall']['num_matches'], 1)
        self.assertEqual(matches['overall']['num_unmatched_queries'], 0)
        self.assertEqual(matches['overall']['num_unmatched_references'], 0)
        self.assertEqual(matches['overall']['num_query_pixels'], 1)
        self.assertEqual(matches['overall']['num_reference_pixels'], 1)
        
        # Case 5: Full image evaluation (0 < R < inf)
        matches, _ = self.calculator.match(self.query_instance, self.reference_instance, 0, float('inf'))
        self.assertEqual(matches['min_radius'], 0)
        self.assertEqual(matches['max_radius'], float('inf'))
        self.assertIn('overall', matches)
        self.assertEqual(matches['overall']['num_matches'], 3)
        self.assertEqual(matches['overall']['num_unmatched_queries'], 0)
        self.assertEqual(matches['overall']['num_unmatched_references'], 0)
        self.assertEqual(matches['overall']['num_query_pixels'], 3)
        self.assertEqual(matches['overall']['num_reference_pixels'], 3)

if __name__ == '__main__':
    unittest.main()