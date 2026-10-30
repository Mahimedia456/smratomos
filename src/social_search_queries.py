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
