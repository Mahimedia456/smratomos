"""Automatic public discovery queries. No supplied example links become findings.
All search hits still require original-source evidence before verified KPI inclusion.
"""
BRAND="Atomos"
GROUPS={
 'Facebook':[
    'site:facebook.com/posts/ "Atomos" {date}',
    'site:facebook.com "Atomos" camera creator tagged mentions {month} {year}',
    'site:facebook.com/reel/ "Atomos" video production {month} {year}'],
 'Instagram':[
    'site:instagram.com/p/ "Atomos" {month} {year}',
    'site:instagram.com/reel/ "Atomos" {month} {year}',
    'site:instagram.com/stories/ "Atomos" {month} {year}',
    'site:instagram.com "Atomos" hashtag mention tagged creator {date}'],
 'LinkedIn':[
    'site:linkedin.com/posts/ "Atomos" {date}',
    'site:linkedin.com/feed/update/ "Atomos" {month} {year}'],
 'X / Twitter':[
    'site:x.com/status/ "Atomos" {date}',
    'site:twitter.com "Atomos" review mention {month} {year}'],
 'Reddit':[
    'site:reddit.com/r/ "Atomos" {date}',
    'site:reddit.com/r/ "Atomos" camera product problems {month} {year}'],
 'YouTube':['site:youtube.com/watch "Atomos" {date}'],
 'Camera forums':[
    'site:dpreview.com/forums "Atomos" {date}',
    '"Atomos" hands-on camera production forum {month} {year}'],
 'Industry articles':[
    'site:newsshooter.com "Atomos" {month} {year}',
    'site:cined.com "Atomos" {month} {year}',
    '"Atomos" video production review article {date}'],
 'Retailers':[
    'site:bhphotovideo.com "Atomos" {month} {year}',
    'site:cvp.com "Atomos" {month} {year}']
}

# Extra device-level public discovery. Candidates remain unverified until original-source validation.
for _group,_queries in {"Facebook":["site:facebook.com \"Shinobi II\" \"Atomos\" {month} {year}","site:facebook.com \"Shogun Ultra\" \"Atomos\" {month} {year}","site:facebook.com/groups/ \"Atomos\" \"firmware\" {month} {year}"],"Instagram":["site:instagram.com/p/ \"Ninja V\" \"Atomos\" {month} {year}","site:instagram.com/reel/ \"Shinobi\" \"Atomos\" {month} {year}","site:instagram.com \"atomos.global\" \"{month}\" \"{year}\""],"LinkedIn":["site:linkedin.com/posts/ \"Shinobi\" \"Atomos\" {month} {year}","site:linkedin.com/posts/ \"Shogun\" \"Atomos\" {month} {year}"],"X / Twitter":["site:x.com/ \"Shinobi\" \"Atomos\" {month} {year}","site:x.com/ \"Ninja V\" \"Atomos\" {month} {year}","site:twitter.com/ \"Shogun\" \"Atomos\" {month} {year}"],"Camera forums":["site:forum.blackmagicdesign.com \"Atomos\" \"{month}\" \"{year}\"","site:dpreview.com/forums \"Shinobi\" \"{month}\" \"{year}\"","site:reddit.com/r/videography \"Atomos\" \"support\" {month} {year}"]}.items():
    GROUPS[_group].extend(_queries)

# Expanded public Meta discovery for archived-month and date-scoped runs.
# These are search candidates, never evidence of post publication or audience metrics.
GROUPS['Facebook'].extend([
  "site:facebook.com/ \"Shinobi 7 II\" \"Atomos\" {month} {year}",
  "site:facebook.com/ \"Shinobi II\" \"Atomos\" {month} {year}",
  "site:facebook.com/ \"Ninja RAW\" \"Atomos\" {month} {year}",
  "site:facebook.com/ \"Shogun Ultra\" \"Atomos\" {month} {year}",
  "site:facebook.com/ \"Sumo PRO 19\" \"Atomos\" {month} {year}",
  "site:facebook.com/ \"AtomOS\" \"Atomos\" {month} {year}",
  "site:facebook.com/ \"Atomos Ninja V\" \"Atomos\" {month} {year}",
  "site:facebook.com/ \"UltraSync Blue\" \"Atomos\" {month} {year}",
  "site:facebook.com/AtomosGlobal/posts/ {month} {year}",
  "site:facebook.com/atomos/posts/ {month} {year}",
  "site:facebook.com/AtomosTech/posts/ {month} {year}",
  "site:facebook.com/reel/ \"Atomos\" camera review {year}",
  "site:facebook.com/groups/ \"Atomos\" camera compatibility {month} {year}",
  "site:facebook.com/photo/ \"Atomos\" {month} {year}",
  "site:facebook.com/watch/ \"Atomos\" professional video {year}",
  "\"Atomos\" Facebook videographer testimonial {month} {year}",
  "\"Atomos\" Facebook comment memory camera issues {month} {year}"
])
GROUPS['Instagram'].extend([
  "site:instagram.com/p/ \"Atomos\" creator {month} {year}",
  "site:instagram.com/reel/ \"Atomos\" filmmaker {month} {year}",
  "site:instagram.com/ \"Atomos\" \"camera\" {month} {year}",
  "\"Atomos\" Instagram tagged posts {date}"
])
GROUPS['Camera forums'].extend([
  "site:forum.blackmagicdesign.com \"Atomos\" {month} {year}",
  "site:dpreview.com/forums \"Atomos\" {month} {year}",
  "site:reddit.com/r/cinematography \"Atomos\" {month} {year}"
])

# Brand-first discovery is the foundation. These search themes apply to EVERY
# present, discontinued, new, legacy, accessory and unlisted product, as well
# as company-wide service, firmware, creator and partnership mentions.
# Named model queries elsewhere are optional supplements, never filters.
_BROAD_BRAND_QUERIES={
  "Facebook": [
    "site:facebook.com \"{brand}\" {date}",
    "site:facebook.com \"{brand}\" support OR firmware OR update OR customer {month} {year}",
    "site:facebook.com \"{brand}\" launch OR event OR review OR unboxing {month} {year}",
    "site:facebook.com \"{brand}\" reel OR livestream OR story {month} {year}",
    "site:facebook.com/groups/ \"{brand}\" user experience {month} {year}",
    "site:facebook.com \"{brand}\" seller OR dealer OR reseller {month} {year}"
  ],
  "Instagram": [
    "site:instagram.com \"{brand}\" {date}",
    "site:instagram.com \"{brand}\" tagged creator {month} {year}",
    "site:instagram.com/reel/ \"{brand}\" {month} {year}",
    "site:instagram.com/p/ \"{brand}\" {month} {year}",
    "site:instagram.com \"{brand}\" review OR tutorial OR launch {month} {year}"
  ],
  "LinkedIn": [
    "site:linkedin.com/posts/ \"{brand}\" {month} {year}",
    "site:linkedin.com \"{brand}\" product OR partnership OR event {month} {year}",
    "site:linkedin.com \"{brand}\" dealer OR trade show OR news {date}"
  ],
  "X / Twitter": [
    "site:x.com \"{brand}\" {date}",
    "site:x.com/status/ \"{brand}\" support OR review {month} {year}",
    "site:twitter.com \"{brand}\" announcement OR customer {month} {year}"
  ],
  "Reddit": [
    "site:reddit.com \"{brand}\" {date}",
    "site:reddit.com/r/ \"{brand}\" review OR compatibility {month} {year}",
    "site:reddit.com \"{brand}\" firmware OR problem OR recommendation {month} {year}"
  ],
  "YouTube": [
    "site:youtube.com/watch \"{brand}\" {date}",
    "site:youtube.com \"{brand}\" review OR tutorial {month} {year}",
    "site:youtube.com \"{brand}\" live OR shorts OR first impressions {month} {year}"
  ],
  "Camera forums": [
    "\"{brand}\" camera forum compatibility {month} {year}",
    "site:dpreview.com/forums \"{brand}\" {date}",
    "site:forum.blackmagicdesign.com \"{brand}\" {date}",
    "site:forums.red.com \"{brand}\" {date}",
    "site:community.sony.com \"{brand}\" {month} {year}"
  ],
  "Industry articles": [
    "\"{brand}\" industry news {date}",
    "\"{brand}\" review or release or firmware {month} {year}",
    "site:newsshooter.com \"{brand}\" {month} {year}",
    "site:cined.com \"{brand}\" {month} {year}",
    "site:petapixel.com \"{brand}\" {month} {year}"
  ],
  "Retailers": [
    "\"{brand}\" buy reseller inventory {month} {year}",
    "site:bhphotovideo.com \"{brand}\" {month} {year}",
    "site:cvp.com \"{brand}\" {month} {year}",
    "site:adorama.com \"{brand}\" {month} {year}",
    "site:wexphotovideo.com \"{brand}\" {month} {year}",
    "site:proav.co.uk \"{brand}\" {month} {year}",
    "site:galaxus.com \"{brand}\" {month} {year}"
  ]
}
for _platform,_broad in _BROAD_BRAND_QUERIES.items():
    GROUPS[_platform]=[q.replace('{brand}',BRAND) for q in _broad]+GROUPS.get(_platform,[])
