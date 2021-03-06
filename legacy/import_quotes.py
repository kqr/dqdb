from quotes.models import Quote
from urllib.request import urlopen
from datetime import datetime

def download_quotes(url):
    quote = {}
    with urlopen(url) as f:
        for line in f:
            line = line.strip().decode('utf-8')
            if not line:
                continue
            elif line == '~':
                yield quote
                quote = {}
            elif 'timestamp' not in quote:
                quote['timestamp'] = datetime.fromtimestamp(int(line))
            elif 'legacy_hash' not in quote:
                quote['legacy_hash'] = line
            else:
                if 'text' not in quote:
                    quote['text'] = []
                quote['text'].append(line)


def save_quotes(quotes, user):
    quotes = list(quotes)

    for quote in quotes:
        Quote(text='\n'.join(quote['text']), legacy_hash=quote['legacy_hash'], submitter=user).save()
        q = Quote.objects.get(legacy_hash=quote['legacy_hash'])
        q.timestamp = quote['timestamp']
        q.save()



