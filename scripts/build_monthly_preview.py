"""One-time October monthly diagnostic PDF from saved Atomos evidence. No cron."""
import json
from pathlib import Path
from datetime import date, timedelta
from collections import Counter
from reportlab.platypus import SimpleDocTemplate, Spacer, KeepTogether
from reportlab.lib.pagesizes import A4
from src.schema import ResearchReport
from src import pdf_report_v2 as pdf
from src.platform_analytics import PLATFORMS, platform_summary
from src.social_content import content_type

ROOT=Path(__file__).resolve().parents[1]
END=date(2026,10,30)
START=date(2026,10,1)
BRAND='Atomos' if 'atomos' in str(ROOT).lower() else 'Angelbird'
# Repo-name independent: schema and source header agree on the brand.
if (ROOT/'src'/'brand_scope.py').exists():
    import inspect
    source=(ROOT/'src'/'pdf_report_v2.py').read_text(encoding='utf-8')
    BRAND='ATOMOS' if 'ATOMOS | DAILY' in source else 'ANGELBIRD'

def inside(d):
    try:return START<=date.fromisoformat(d)<=END
    except (ValueError,TypeError):return False


def continuous_card(item,number):
    """Split-safe monthly evidence record: NEVER place an entire long item in one table cell."""
    from xml.sax.saxutils import escape
    parts=[pdf.band(f'{number} | {item.platform} | {content_type(item).upper()}'),
           Spacer(1,7),pdf.P(item.title,'item'),Spacer(1,6),
           pdf.P(f'Author: {item.author or "Not recorded"} | Published: {item.published_date or "Unverified"} | Sentiment: {item.sentiment} | Priority: {item.priority}','meta'),
           Spacer(1,5),pdf.link(item.url,'OPEN ORIGINAL SOURCE'),
           pdf.source_url_line(item.url),Spacer(1,7)]
    images=pdf.evidence_thumbnail(item,max_width=pdf.W-42)
    if images:parts.extend(images)
    else:parts.append(pdf.P('Source image not cached or accessible. Do not substitute a fabricated preview.','micro'))
    for label,value in [('Source excerpt',item.source_excerpt),('Finding',item.summary),('Details',item.details),
                         ('Impact',item.impact),('Suggested response',item.response_action),
                         ('Date evidence',item.date_evidence),('Verification',item.verification_note)]:
        if value:parts.extend([Spacer(1,5),pdf.P(f'<b>{escape(label)}:</b> {escape(str(value))}','small',raw=True)])
    if item.engagement:
        parts.extend([Spacer(1,6),pdf.P('Public source metrics: '+', '.join(f'{k}: {v}' for k,v in item.engagement.items()),'small')])
    for i,comment in enumerate(item.comments or [],1):
        parts.extend([Spacer(1,7),pdf.P(f'COMMENT {i} | '+str(comment.get('author','Public user')),'caption'),
                      pdf.P(str(comment.get('text','')),'small')])
        if comment.get('url'):parts.append(pdf.link(comment['url'],'OPEN COMMENT'))
    parts.append(Spacer(1,14))
    return parts

def main():
    findings,offers,leads=[],[],[]
    reference_findings=[]
    undated_leads=[]
    seen=set()
    saved_dates=[]
    for day_offset in range((END-START).days+1):
        d=START+timedelta(days=day_offset)
        p=ROOT/'data'/d.strftime('%Y')/d.strftime('%m')/(f'{BRAND.title()}-Social-Monitoring-{d.isoformat()}.json')
        if not p.exists():continue
        saved_dates.append(d.isoformat())
        report=ResearchReport.model_validate(json.loads(p.read_text(encoding='utf-8')))
        for field,target in [('today_findings',findings),('historical_findings',findings),
                             ('retail_observations',offers),('historical_retail',offers),
                             ('unverified_leads',leads)]:
            for item in getattr(report,field):
                period_date=(item.reference_date or item.published_date) if field in ('retail_observations','historical_retail') else item.published_date
                if field=='unverified_leads':
                    if not inside(period_date):continue
                elif not inside(period_date):continue
                if field in ('today_findings','historical_findings') and (item.status!='verified' or not item.date_evidence):continue
                key=(('retail' if target is offers else 'lead' if target is leads else 'finding'),item.url.rstrip('/').lower())
                if key in seen:continue
                seen.add(key);target.append(item)
    # Import auxiliary GPT evidence as leads only. These files are not authoritative
    # date proof, so never promote them to the verified monthly KPI.
    for p in sorted((ROOT/'data').glob('2026/10/*-gpt-*-evidence.json')):
        try:aux=json.loads(p.read_text(encoding='utf-8'))
        except (OSError,ValueError):continue
        if not isinstance(aux,dict):continue
        for bucket in ('today_findings','historical_findings','unverified_leads','older_leads'):
            for obj in aux.get(bucket,[]):
                if not isinstance(obj,dict) or not str(obj.get('url','')).startswith(('https://','http://')):continue
                from src.schema import Finding
                try:item=Finding.model_validate(dict(obj,status='unverified'))
                except Exception:continue
                key=('lead',item.url.rstrip('/').lower())
                if key in seen or ('finding',item.url.rstrip('/').lower()) in seen:continue
                seen.add(key)
                if inside(item.published_date) and item.date_evidence:
                    leads.append(item)
                else:
                    undated_leads.append(item)
    # Historical public evidence archive, separate from direct collector's verified bucket.
    history=ROOT/'data'/'reference_history_2026_10_30.json'
    if history.exists():
        from src.schema import Finding
        archive=json.loads(history.read_text(encoding='utf-8'))
        for obj in archive.get('findings',[]):
            if not inside(obj.get('published_date')):continue
            try:item=Finding.model_validate(dict(obj,status='older'))
            except Exception:continue
            key=('finding',item.url.rstrip('/').lower())
            if key not in seen:
                seen.add(key);reference_findings.append(item)
    editorial=ROOT/'data'/'reference_editorial_2026_10.json'
    if editorial.exists():
        from src.schema import Finding
        archive=json.loads(editorial.read_text(encoding='utf-8'))
        for obj in archive.get('findings',[]):
            if not inside(obj.get('published_date')):continue
            try:item=Finding.model_validate(dict(obj,status='older'))
            except Exception:continue
            key=('finding',item.url.rstrip('/').lower())
            if key not in seen:
                seen.add(key);reference_findings.append(item)
    support_archive=ROOT/'data'/'reference_support_2026_10.json'
    if support_archive.exists():
        from src.schema import Finding
        support=json.loads(support_archive.read_text(encoding='utf-8'))
        for obj in support.get('findings',[]):
            if not inside(obj.get('published_date')):continue
            try:item=Finding.model_validate(dict(obj,status='older'))
            except Exception:continue
            key=('finding',item.url.rstrip('/').lower())
            if key not in seen:
                seen.add(key);reference_findings.append(item)
    cross_audit=ROOT/'data'/'cross_platform_oct_2026_audit.json'
    social_coverage=[]
    if cross_audit.exists():
        from src.schema import Finding
        supplement=json.loads(cross_audit.read_text(encoding='utf-8'))
        social_coverage=supplement.get('coverage',[])
        for obj in supplement.get('leads',[]):
            try:item=Finding.model_validate(dict(obj,status='unverified'))
            except Exception:continue
            key=('lead',item.url.rstrip('/').lower(),item.title.lower())
            if key not in seen:
                seen.add(key);undated_leads.append(item)
    findings.sort(key=lambda x:(x.published_date,x.platform,x.url),reverse=True)
    all_findings=findings+reference_findings
    dest=ROOT/'reports'/'2026'/'10'/f'{BRAND.title()}-Social-Monitoring-Monthly-2026-10-01_to_2026-10-30.pdf'
    dest.parent.mkdir(parents=True,exist_ok=True)
    doc=SimpleDocTemplate(str(dest),pagesize=A4,topMargin=34,bottomMargin=60,leftMargin=pdf.MARGIN,rightMargin=pdf.MARGIN,
        title=f'{BRAND.title()} Monthly Social Monitoring | 01-30 October 2026')
    story=[pdf.band(f'{BRAND.upper()} | MONTHLY SOCIAL MONITORING','01 - 30 OCTOBER 2026'),
           Spacer(1,12),pdf.P('30-DAY OBSERVED ENGAGEMENT & SOURCE EVIDENCE','item'),Spacer(1,7),
           pdf.P('Monthly preview: 01-30 October 2026 (Pakistan time). Evidence compiled from saved repository records only; no new research performed.','small'),
           Spacer(1,8),pdf.P(f'Daily source files available: {len(saved_dates)} of 30 ({", ".join(saved_dates) or "none"}). Missing days are incomplete coverage, NOT zero brand mentions.','small'),Spacer(1,12)]
    story.extend([pdf.P('KPI interpretation: counts describe source records captured, not total platform activity. Reddit cross-posts cover one issue cluster. Blank engagement means not measured.','small'),Spacer(1,8)])
    story.extend(pdf.engagement_overview(all_findings))
    story.extend([pdf.P('IMPORTANT: A platform row showing 0 sourced posts means zero items in this incomplete archive, NOT zero posts on the platform. Report coverage is only 1 daily collector snapshot out of 30 days.','small'),Spacer(1,9)])
    counts=Counter(x.sentiment for x in all_findings)
    story.extend([pdf.P(f'Direct verified: {len(findings)} | Dated archival source posts: {len(reference_findings)}  |  Retail snapshots: {len(offers)}  |  Positive: {counts["Positive"]}  |  Neutral: {counts["Neutral"]}  |  Negative: {counts["Negative"]}  |  Questions: {counts["Question"]}','small'),Spacer(1,10),
                  pdf.band('MONTHLY PLATFORM KPIS AND INDIVIDUAL EVIDENCE','POST / COMMENT / STORY / VIDEO / ARTICLE')])
    grouped=platform_summary(all_findings)
    represented=sum(bool(records) for records in grouped.values())
    story.extend([Spacer(1,7),pdf.P(f'Platforms with dated source records: {represented} of {len(PLATFORMS)} | Reddit issue clusters: 1 (3 source posts) | Research coverage: incomplete, 29 days without daily snapshot files.','small'),Spacer(1,7)])
    uncertain=platform_summary(leads+undated_leads)
    for platform in PLATFORMS:
        records=grouped[platform]
        story.append(Spacer(1,13))
        story.extend(pdf.platform_scorecard(platform,records,'01-30 OCTOBER 2026'))
        if platform=='Reddit' and records:
            story.extend([pdf.P('CONVERSATION CLUSTERS: Three linked Reddit posts concern one Shinobi 7 II 4K60/4K30 complaint. Comment summaries follow their parent thread and are not extra post counts.','small'),Spacer(1,8)])
        if records:
            for i,item in enumerate(records,1):
                story.extend([pdf.P('PUBLISHED '+str(item.published_date)+'  |  '+('ARCHIVED ORIGINAL SOURCE | ' if item in reference_findings else 'VERIFIED | ')+content_type(item).upper(),'caption'),Spacer(1,5)])
                story.extend(continuous_card(item,'W'+str(i)))
        else:
            story.extend([pdf.P('NOT VERIFIED IN SAVED SOURCES. Platform activity and engagement were not measured for the full month; zero activity is NOT established.','small'),Spacer(1,7)])
        if uncertain.get(platform):
            story.append(pdf.P('UNVERIFIED / UNDATED SOURCE LEADS (EXCLUDED FROM KPI COUNTS)','caption'))
            for i,item in enumerate(uncertain[platform],1):story.extend(continuous_card(item,'U'+str(i)))
        if platform=='Retailers':
            story.extend([pdf.P(f'{len(offers)} dated retailer snapshots; excluded from social post KPIs.','small'),Spacer(1,7)])
            for i,item in enumerate(offers,1):story.extend(continuous_card(item,'R'+str(i)))
    story.extend([Spacer(1,9),pdf.P(f'Auxiliary source leads surfaced: {len(undated_leads)} undated and {len(leads)} date-attributed; all excluded from verified post KPIs. An unobserved public metric is N/A, not a confirmed zero.','small')])
    story.extend([Spacer(1,10),pdf.band('CROSS-PLATFORM RESEARCH AUDIT'),Spacer(1,8)])
    for check in social_coverage:
        story.extend([pdf.P(str(check.get('platform',''))+' | '+str(check.get('status','')),'caption'),
                      pdf.P(str(check.get('note','')),'small'),Spacer(1,7)])
    story.extend([Spacer(1,10),pdf.band('MONTHLY COVERAGE AND VERIFICATION NOTES'),Spacer(1,9),
                  pdf.P('This is a one-time manual monthly compilation. The 30-day window is not a claim that thirty daily scans were completed. Missing metrics are unavailable, not zero. The saved evidence may contain inaccessible Instagram Stories or other platforms; URLs alone are never proof of content, media or publication date.','small'),
                  Spacer(1,8),pdf.P('No monthly schedule, cron trigger, research API call or modifications to daily reports are introduced.','small')])
    doc.build(story,onFirstPage=pdf.footer,onLaterPages=pdf.footer)
    # Publication QA audit is persisted and verified by GitHub Actions.
    from pypdf import PdfReader
    from src.platform_analytics import category
    reader=PdfReader(str(dest),strict=True)
    full_text='\\n'.join(page.extract_text() or '' for page in reader.pages)
    import re
    normalized_pdf=re.sub(r'\\s+',' ',full_text).casefold()
    def is_present(title):
        words=re.findall(r'[a-z0-9]+',title.casefold())
        extracted=set(re.findall(r'[a-z0-9]+',normalized_pdf))
        return bool(words) and sum(w in extracted for w in words)/len(words)>=0.85
    missing_titles=[x.title for x in all_findings if not is_present(x.title)]
    if missing_titles:
        raise RuntimeError('PDF omitted source titles: '+repr(missing_titles))
    if len(reader.pages)<1:raise RuntimeError('Monthly PDF missing pages')
    audit={'report_start':START.isoformat(),'report_end':END.isoformat(),
           'pdf_pages':len(reader.pages),'pdf_bytes':dest.stat().st_size,
           'source_record_count':len(all_findings),'unique_urls':len({x.url for x in all_findings}),
           'verified_direct':len(findings),'archived':len(reference_findings),
           'platform_counts':{platform:len(grouped[platform]) for platform in PLATFORMS},
           'source_titles_missing_from_pdf':missing_titles,
           'daily_snapshots':saved_dates,'cross_platform_leads':len([x for x in undated_leads if x.platform=='LinkedIn']),'cross_platform_audit':social_coverage,
           'warning':'Platform 0 means no saved dated entries, not zero real-world activity.'}
    (ROOT/'monthly-report-audit.json').write_text(json.dumps(audit,indent=2)+chr(10))
    print('AUDIT',json.dumps(audit))
    manifest=ROOT/'monthly-reports-index.json'
    manifest.write_text(json.dumps([{'brand':BRAND,'start':START.isoformat(),'end':END.isoformat(),'path':dest.relative_to(ROOT).as_posix(),
                                   'saved_source_dates':saved_dates,'verified_items':len(findings),'dated_archival_posts':len(reference_findings),'undated_leads':len(undated_leads),'dated_unverified_leads':len(leads),'retail_snapshots':len(offers),'platforms_with_dated_sources':represented,'coverage_status':'PARTIAL - only 2026-10-30 saved daily collector snapshot'}],indent=2)+'\n')
    print(f'CREATED {dest} | verified={len(findings)} | source_days={len(saved_dates)} | retail={len(offers)} | unverified_leads={len(undated_leads)+len(leads)}')

if __name__=='__main__':main()
