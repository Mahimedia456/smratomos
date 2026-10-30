"""Precision filter for Atomos production-video equipment, not similarly named subjects.
A match is only a candidate for original-source/date verification, never proof by itself.
"""
import re
from urllib.parse import urlparse

BRAND=re.compile(r'\batomos\b|\batom[- ]?os\b|\batomosphere\b',re.I)
PRODUCT=re.compile(r'\b(?:ninja(?:\s+(?:tx(?:\s+go)?|raw|ultra|v\+?))?|shogun(?:\s+(?:ultra|classic|av[- ]?19m?))?|shinobi(?:\s+(?:ii|go|7(?:\s+rx)?))?|sumo(?:\s+pro[- ]?19)?|ultrasync|atomosphere|a[- ]?eye|tx[- ]?rx|studiosonic)\b',re.I)
VIDEO=re.compile(r'\b(?:camera|cameras|videograph(?:er|y)|filmmak(?:er|ing)|monitor[- ]?recorder|video\s+production|monitor|hdmi|sdi|lut|prores|codec|raw\s+video|hdr|cfexpress|ssd|firmware|recorder|recording|timecode|sync|wireless\s+video|livestream|broadcast|atomos\s+connect|atomos\s+(?:ninja|shogun|shinobi|sumo))\b',re.I)
NON_EQUIPMENT=re.compile(r'\b(?:ff14|ffxiv|final\s+fantasy|dj\s+atomos|atomos\s+y\s+ruinas|democritus|leucippus|greek\s+atom|atomic\s+theory|alkheadz|nukranox|atomism)\b|暁月|ネタバレ',re.I)
SPECIFIC=re.compile(r'\b(?:atomos\s+(?:ninja|shogun|shinobi|sumo|connect|monitor|recorder|camera|recording)|(?:ninja|shogun|shinobi|sumo)\s+(?:tx|raw|ultra|go|ii|v\+?|7|pro[- ]?19)|atom[- ]?os\s*\d+(?:\.\d+)+|atomosphere)\b',re.I)

def is_atomos_equipment(text:str,*,title:str='',url:str='')->bool:
    raw=' '.join((str(title or ''),str(text or ''))).strip()
    if not BRAND.search(raw):return False
    if NON_EQUIPMENT.search(raw) and not SPECIFIC.search(raw):return False
    host=(urlparse(str(url or '')).hostname or '').lower()
    if host=='atomos.com' or host.endswith('.atomos.com'):return True
    if SPECIFIC.search(raw):return True
    # A brand-wide monitoring feed cannot depend on an enumerated device list.
    # New/legacy products, software, audio, PTZ, service and accessory mentions
    # are valid candidates even if no classic monitor/recorder term occurs.
    # Homonyms above remain excluded; original content/date is checked later.
    return bool(BRAND.search(raw))
