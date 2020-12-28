t = lambda p: p[2][int(p[0].split('-')[0])-1] == p[1].strip(':')
r = lambda s: int((s[2][int(s[0].split('-')[0])-1] == s[1].strip(':')) ^ (s[2][int(s[0].split('-')[1])-1] == s[1].strip(':')))

print(sum(map(r, [l.split() for l in open('input.txt')])))