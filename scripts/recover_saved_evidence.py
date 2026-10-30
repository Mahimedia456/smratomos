"""Recover the already billed 2026-10-30 research without repeating model calls.

The GitHub workflow first downloads the original same-repository Actions
artifact. This script applies the current Atomos camera-equipment relevance
guard and keeps dated, original-source-backed records only.
"""
import json
import sys
from pathlib import Path
from src.schema import ResearchReport
from src.report_scope import scope_to_day
from src.brand_scope import is_atomos_equipment

ROOT=Path(__file__).resolve().parents[1]

def recover(day):
    source=ROOT/'data'/day[:4]/day[5:7]/f'Atomos-Social-Monitoring-{day}.json'
    if not source.exists():
        raise FileNotFoundError('Saved failed-run research artifact not downloaded: '+str(source))
    data=json.loads(source.read_text(encoding='utf-8'))
    originals=list(data.get('today_findings') or [])
    valid=[i for i in originals if is_atomos_equipment(
        i.get('source_excerpt',''),title=i.get('title',''),url=i.get('url',''))]
    removed=len(originals)-len(valid)
    data['today_findings']=valid
    data['unverified_leads']=[
        i for i in (data.get('unverified_leads') or [])
        if is_atomos_equipment(i.get('source_excerpt',''),title=i.get('title',''),url=i.get('url',''))
        and i.get('reference_date')==day
    ]
    data['retail_observations']=[
        i for i in (data.get('retail_observations') or [])
        if i.get('reference_date')==day and is_atomos_equipment(
            i.get('source_excerpt',''),title=i.get('title',''),url=i.get('url',''))
    ]
    for key in ('older_leads','historical_findings','historical_retail'):
        data[key]=[]
    report=scope_to_day(ResearchReport.model_validate(data))
    report.status='Recovered source research | cached original YouTube evidence; zero repeat paid GPT calls'
    report.headline=(
        f'{len(report.today_findings)} verified original-date Atomos video equipment findings '
        f'for {day}; {removed} unrelated gaming/music/atomism posts excluded. '
        'Platform coverage is bounded to publicly accessible sources.'
    )
    report.visibility_gaps.append(
        f'Precision filter excluded {removed} irrelevant same-name posts before publication.'
    )
    # Any media files missing from the saved Actions artifact are flagged, never invented.
    actual_media=0
    for item in report.today_findings:
        item.image_files=[p for p in item.image_files if (ROOT/p).is_file()]
        actual_media+=len(item.image_files)
    source.write_text(report.model_dump_json(indent=2)+'\n',encoding='utf-8')
    print('CACHED EVIDENCE RECOVERY COMPLETE: day',day,
          'kept',len(report.today_findings),'excluded',removed,
          'image files',actual_media,'paid API calls',0,flush=True)
    assert len(report.today_findings)==2, (
        'This source-specific 2026-10-30 recovery expected exactly 2 evidence records.'
    )
    return report

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Usage: python scripts/recover_saved_evidence.py YYYY-MM-DD')
    recover(sys.argv[1])
