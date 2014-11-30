#regexes
import re
re_hashtag = re.compile(r'(?<=#)[0-9a-zA-Z+_:]*', re.IGNORECASE)
re_mentions = re.compile(r'(?<=@)[A-Za-z0-9_]+', re.IGNORECASE)
re_retweets = re.compile(r'(?<=RT\s@)[A-Za-z0-9_]+', re.IGNORECASE)
re_urls = re.compile(r'([h-t]+:\/\/[A-Za-z0-9./]+)',re.IGNORECASE)
re_comp = re.compile(r'(?<=\s)([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+|\'s)+)')
re_acronym = re.compile(r'(?<=\s)([A-Z]{2,}|[A-Z](?:\.[A-Z])+)')
