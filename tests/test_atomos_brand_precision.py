import unittest
from src.brand_scope import is_atomos_equipment
from src.schema import Finding,ResearchReport

class TestAtomosBrandPrecision(unittest.TestCase):
    def test_excludes_homonyms(self):
        for title in ('【FF14】#4 暁月からまいります ※ネタバレ注意【Atomos】',
                      'The End - Alkheadz & DJ Atomos Feat. Mischimaschine',
                      'atomos y ruinas rap','The Seeds of Atomic Theory Democritus Leucippus Atomos'):
            with self.subTest(title=title):
                self.assertFalse(is_atomos_equipment(title))
    def test_real_video_equipment(self):
        for title in ('I Finally Got the LUT Output on the Atomos Ninja RAW to Work',
                      'AtomOS 12.7.3 LUT Output for HDMI recording',
                      'Atomos Shogun Ultra monitoring HDMI 4K',
                      'Atomos Shinobi II field monitor'):
            with self.subTest(title=title):
                self.assertTrue(is_atomos_equipment(title))
    def test_guard_excludes_games_from_daily_kpis(self):
        video=Finding(url='https://www.youtube.com/watch?v=UuNaTGJgofM',
              title='【FF14】Game stream【Atomos】',source_excerpt='Final Fantasy XIV Atomos game play',
              status='verified',published_date='2026-10-30',date_evidence='YouTube API publishedAt 2026-10-30 PKT')
        real=Finding(url='https://www.youtube.com/watch?v=roEMkfDDC0Y',
              title='Atomos Ninja RAW LUT Output fixed',source_excerpt='Atomos Ninja RAW camera LUT Output HDMI settings',
              status='verified',published_date='2026-10-30',date_evidence='YouTube API publishedAt 2026-10-30 PKT')
        report=ResearchReport(report_date='2026-10-30',today_findings=[video,real]).enforce_date_guardrails()
        self.assertEqual([x.url for x in report.today_findings],[real.url])
if __name__=='__main__':unittest.main()
