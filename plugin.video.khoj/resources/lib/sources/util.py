import re

def cleanup_url(url):
    regex_substitutions = (
        ('ip=\d+\.\d+\.\d+\.\d+', 'ip=0.0.0.0'),
        ('ipbits=\d+', 'ipbits=0')
    )
    for pattern, replace in regex_substitutions:
        url = re.sub(pattern, replace, url)
    return url

def parseValue(p,a,c,k):
    while(c >= 1):
        c -= 1
        if(k[c]):
            base36str = base36encode(c)
            p = re.sub('\\b'+base36str+'\\b', k[c], p)
    return p

def base36encode(num):
    if not isinstance(num, (int, long)):
        raise TypeError
    if num < 0:
        raise ValueError
    alpha ='0123456789abcdefghijklmnopqrstuvwxyz'
    base36 = ''
    while num:
        num, i = divmod(num, 36)
        base36 = alpha[i] + base36
    return base36 or alpha[0]
