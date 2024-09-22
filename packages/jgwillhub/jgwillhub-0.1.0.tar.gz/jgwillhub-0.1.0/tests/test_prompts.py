import unittest
from jgwillhub.prompts import pull

class TestPrompts(unittest.TestCase):
    def test_pull(self):
        tool_hub_tag = "jgwill/cmpenghelperbeta"
        prompt_template = pull(tool_hub_tag)
        # Add your assertions here

if __name__ == "__main__":
    unittest.main()