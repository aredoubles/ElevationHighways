# Charting elevations of every major US Highway
# Using Google Maps APIs

import googlemaps
import json
#from pymongo import MongoClient
#import pandas as pd
#import pprint
#import urllib
#import simplejson
#import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from ggplot import *
import re

#sns.set(style = '')

mykey = 'AIzaSyD4ipXow67rS9YM9eljgCiVJkL0yyIg7nQ'
gmaps = googlemaps.Client(key=mykey)

# Testing that APIs are current:
#geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
# print(geocode_result)

elevlist=[]
dfelev=[]

def WhereTo(highway):
    '''I-40 polyline setup'''
    # Get directions from Wilmington NC to Barstow CA
    # Wilmington: 34.272427,-77.868283
    I40_start = '34.272427,-77.868283'
    # Barstow: 34.886330, -117.011548
    I40_end = '34.886330,-117.011548'
    # Requires a waypoint in western NC to stay on I-40 entirely
    I40_way1 = '35.619243,-83.009142'
    waypts = [I40_start, I40_end, I40_way1]
    return waypts


def Routing(waypts):
    I40_path = gmaps.directions(waypts[0], waypts[1],
                                waypoints=[waypts[2]])
    # Output is in JSON format

    # Save this JSON output to file
    # with open('I40_path.json', 'w') as fp: json.dump(I40_path, fp)

    # Haven't figured out a way to parse out the polyline for this route, so just paste in manually for now
    #poly40 = R"""sydpEtsgzMtlFjfSwmOfadAsvBftzAohLt_XmwQp{MwsLxvEa}B|oLpgAtgGfqGdsRveNrfTtxd@n`hA`zJfl\dtAlav@eeDlvzApcKt_Sh|Npbh@tyE~w\sfRj{Vmqk@xovAwfU~`]_dSlcMuqw@buQmia@v|I{c_@r`ZozEjeOg|A~{PqgYl_[_z]txTbtA~qb@gDrvVkhNdzPa}FyqBshEpnHu_GkuAuzCxiH{nGhaKqfAzcEylLdgC_eK|zAmvCrkIwfOr{R`nJbtg@yu@rbi@brBtcY`qDbiJtdNjeeAz]|vWu_Fz~Vbx@rhh@iiDt`Wsb]txx@qmI`aSua@daTeAd|a@b~HpvVaoMzn`@{wDvq`AboCvvv@|vD|eZke@xjPiyCfnJdeHnbSlzHlrKweApgNlqJnnXljGva}@`tMhhVfoDxqk@|}@jvb@lfMvr`Avbb@`{zB~pIf{_@h}LhjSdcYzjk@tkYfwm@ptL~s[qiFxgI~eBvaOdoCzfCujA`ca@taEdtu@vsQ`}q@l|Wn{rAlxNjxz@`vC|~gAxmBpopAclTzaV}~e@fcDcdLruf@_iJpnf@{fD|nd@sfMr~]mlBjuV_mGrxH{oL|sSieHx~b@opCffk@g}@jlP`oE~de@hdFjet@lhLro[gqItti@mfGnic@nj@r_YfnCrqbBjdDd|}@laAhvcAxqFhseAyBzo_By~M`ucA_Yzdi@q`Fjrl@koD`rwAlk@jqpApmLf|_AxqEnnh@fuG`v^v}Tx`Ux{ExicAlA~l}AtlFr|_AnJlsj@}~Bd`n@oqAxns@hnDj|\kH~joAgqM|dxBraSpvlA~pI|{h@}|IvzXbmAfsx@ztF~gS|mCbve@z}NnkrAphLpq`@auCbvTyhFnftCDlolAcrGjfh@kwJ~}\x`HrpYouGbr`@~uB|~WvvSjeqAgxAbhZghGdkKds@vsQanGnwNdh@x|c@{{M~rVgsRptSupOpdGytJ|q_@emYbapAse@v__@xsKrrd@fqS`tT|`Nb|a@tvO|la@hr[f}kAt`Qvr{@n}EfzDaR|rWelQxvoAszQjmnAavKxet@a~BbfU|\v`[|Nv~VijItwTi`Anan@pdFvzj@kgBfiaA}zKlfd@l|@rec@xfLp_g@zuEfu_@`lEr{\ojJhs{A|dHn{GrgWbkIdni@~eBrsLb~Kl}Dbu[xi@xra@ssTphLewH~vKlWfxPx_CjkVl_JlluAvdNv}|@us@dii@zDboqAksJrle@{_Ihg`A}rGtnf@"""

    for rec in I40_path:
        poly40 = rec['overview_polyline']['points']
    #poly40.decode('unicode_escape')

    poly40 = poly40.encode('utf8')

    return poly40

# Plug this polyline into the Elevations API


def Elevations(poly40):
    # 500 seems to be the max. number of samples allowed? Not really sure about the error message, honestly
    I40_elev = gmaps.elevation_along_path(poly40, samples=500)

    # with open('I40_elev.json', 'w') as fp: json.dump(I40_elev, fp)

    elevlist = {}
    for spt in I40_elev:
        #elevlist.append(spt['elevation'])
        elevlist[spt['location']['lng']] = spt['elevation']

    #dfelev = pd.DataFrame(elevlist, columns=['longitude', 'elevation'])
    dfelev = pd.DataFrame.from_dict(elevlist, orient='index')
    dfelev.columns = ['elevation']
    dfelev.index.names = ['longitude']
    dfelev.reset_index(inplace=True)
    #dfelev['longitude'] = abs(dfelev['longitude'])

    return dfelev

def Plotting(dfelev):
    #plotter = plt.scatter(x = dfelev['longitude'], y = dfelev['elevation'])
    #plt.savefig('I40plot.png')
    p = ggplot(dfelev, aes('longitude', 'elevation')) + geom_line() + xlab('Longitude') + ylab('Elevation') + ggtitle('Interstate 40') + theme_bw()
    ggplot.save(p, filename = 'I40plot.png')

def main():
    highway = 'I40'
    waypts = WhereTo(highway)
    poly40 = Routing(waypts)
    dfelev = Elevations(poly40)
    Plotting(dfelev)

main()
