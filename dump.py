from stathat import StatHat
import time

stats = StatHat()
for line in open('tracking.txt'):
    d, v = line.strip().split()
    t = time.mktime(time.strptime(d + " 12:00", '%Y-%m-%d %H:%M'))
    stats.ez_post_value("site-stathat.com@ars.iki.fi",
        "days since last case", d, timestamp=t)