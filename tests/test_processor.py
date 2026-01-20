import unittest
from bs4 import BeautifulSoup
from src.processor import extract_section, clean_text
from src.config import NAVBAR_TAGS, NAVBAR_CLASSES, FOOTER_TAGS, FOOTER_CLASSES

class TestProcessor(unittest.TestCase):
    def test_clean_text(self):
        raw = "  Hello   World  \n "
        cleaned = clean_text(raw)
        self.assertEqual(cleaned, "Hello World")

    def test_extract_navbar_by_tag(self):
        html = "<html><nav>Home | About</nav><body>Body</body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        result = extract_section(soup, NAVBAR_TAGS, NAVBAR_CLASSES)
        self.assertEqual(result, "Home | About")

    def test_extract_navbar_by_class(self):
        html = "<html><div class='my-navbar'>Home | About</div><body>Body</body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        result = extract_section(soup, [], ['navbar'])
        self.assertEqual(result, "Home | About")

    def test_extract_footer_by_tag(self):
        html = "<html><body>Body</body><footer>Copyright 2026</footer></html>"
        soup = BeautifulSoup(html, 'html.parser')
        result = extract_section(soup, FOOTER_TAGS, FOOTER_CLASSES)
        self.assertEqual(result, "Copyright 2026")

    def test_extract_missing_section(self):
        html = "<html><body>No nav here</body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        result = extract_section(soup, NAVBAR_TAGS, NAVBAR_CLASSES)
        self.assertEqual(result, "")

if __name__ == '__main__':
    unittest.main()
