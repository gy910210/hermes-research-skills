"""Offline packaging checks for the HTML publication skill."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / 'skills' / 'report-html-publisher-zh'

class SkillPackagingTests(unittest.TestCase):
    def test_frontmatter_and_related_skills(self):
        text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        self.assertTrue(text.startswith('---\n'))
        header, body = text[4:].split('\n---\n', 1)
        self.assertTrue(body.strip())
        for field in ['name', 'description', 'version', 'author', 'license', 'platforms', 'metadata']:
            self.assertRegex(header, rf'(?m)^{field}:')
        description_match = re.search(r'^description: "(.*)"$', header, re.M)
        assert description_match is not None, 'Missing quoted description'
        description = description_match.group(1)
        self.assertLessEqual(len(description), 60)
        self.assertTrue(description.endswith('.'))
        related_match = re.search(r'related_skills: \[(.*?)\]', header)
        assert related_match is not None, 'Missing related_skills'
        related = related_match.group(1)
        for name in related.split(','):
            self.assertTrue((ROOT / 'skills' / name.strip() / 'SKILL.md').is_file(), name)

    def test_skill_links_are_portable(self):
        for path in [SKILL / 'SKILL.md', *SKILL.glob('references/*.md')]:
            text = path.read_text(encoding='utf-8')
            self.assertNotRegex(text, r'/Users/|/home/|arxiv-2610\.04862')
            for href in re.findall(r'\]\(([^)]+)\)', text):
                if not href.startswith(('https:', 'http:', '#')):
                    self.assertTrue((path.parent / href.split('#')[0]).is_file(), str(path) + ': ' + href)

    def test_workflow_integration(self):
        name = 'report-html-publisher-zh'
        for path in [ROOT / 'README.md', ROOT / 'CHANGELOG.md', ROOT / 'skills/research-orchestrator-zh/SKILL.md', ROOT / 'skills/report-maintainer-zh/SKILL.md']:
            self.assertIn(name, path.read_text(encoding='utf-8'))
        for ref in ['workflow-state-machine.md', 'artifact-contracts.md', 'report-types.md']:
            self.assertIn('html_', (ROOT / 'skills/research-orchestrator-zh/references' / ref).read_text(encoding='utf-8'))

if __name__ == '__main__':
    unittest.main()
