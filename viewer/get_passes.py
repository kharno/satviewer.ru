from datetime import timedelta, datetime
from skyfield.api import load, wgs84, utc
from tzwhere import tzwhere
from pytz import timezone
from zoneinfo import ZoneInfo


def get_passes(view_param,
               az_min=0, az_max=360, alt_min=10, alt_max=90,
               dist_min=0, dist_max=1000000):

    # correcting data type html form values
    for item in view_param.items():
        try:
            view_param[item[0]] = float(item[1])
        except ValueError:
            pass

    # loading satellite from a TLE file¶
    stations_url = 'viewer/3le.txt'
    satellites = load.tle_file(stations_url)
    satellite = {sat.model.satnum: sat for sat in satellites}[view_param['norad cat id']]

    # defining view position in wgs84
    view_position = wgs84.latlon(view_param['latitude'],
                                 view_param['longitude'],
                                 view_param['elevation_m'])

    # defining datetime data
    if view_param['latitude'] == 55.7556 and view_param['longitude'] == 37.643:
        tzName = 'Europe/Moscow'
        tz = timezone(tzName)
        start = tz.localize(datetime.strptime(view_param['start datetime'], '%Y-%m-%dT%H:%M'))
        end = tz.localize(datetime.strptime(view_param['end datetime'], '%Y-%m-%dT%H:%M'))
    else:
        tz = tzwhere.tzwhere()
        tzName = tz.tzNameAt(view_param['latitude'], view_param['longitude'])
        tz = timezone(tzName)
        start = tz.localize(view_param['start datetime'])
        end = tz.localize(view_param['end datetime'])

    # finding when a satellite rises and sets¶
    ts = load.timescale()
    t0 = ts.from_datetime(start)
    t1 = ts.from_datetime(end)
    t, events = satellite.find_events(view_position, t0, t1, altitude_degrees=0)
    satpass_events = []
    for ti, event in zip(t, events):
        if event == 0:
            satpass_event = []
        satpass_events.append((ti, satpass_event))
        if event == 2:
            satpass_events.append(satpass_event)

    # collecting info when a satellite in field of view
    satpasses_coords = []
    for sp in satpass_events:
        t = sp[0][0].utc_datetime()
        t = t.replace(tzinfo=utc)
        satpass_coords = []
        while t < sp[2][0].utc_datetime():
            difference = satellite - view_position
            geocentric = satellite.at(ts.from_datetime(t))
            topocentric = difference.at(ts.from_datetime(t))
            height = wgs84.height_of(geocentric)
            alt, az, distance = topocentric.altaz()
            if (az_min <= az._degrees <= az_max and
                    alt_min <= alt._degrees <= alt_max and
                    dist_min <= distance.km <= dist_max):
                satpass_coords.append(
                    (t.astimezone(ZoneInfo(tzName)), distance.km, az._degrees, alt._degrees, height.km))
            t = t + timedelta(seconds=5)
        if satpass_coords:
            satpasses_coords.append(satpass_coords)

    satpasses = []
    for item in satpasses_coords:
        satpass = {
            'sat_name': satellite.name,
            'sat_epoch': satellite.epoch.utc_datetime().strftime("%Y-%m-%d %H:%M:%S UTC"),
            'norad': view_param['norad cat id'],
            'enter': {
                'time': item[0][0].strftime("%Y-%m-%d %H:%M:%S %z"),
                'distance': round(item[0][1], 1),
                'azimuth': round(item[0][2], 1),
                'altitude': round(item[0][3], 1),
                'height': round(item[0][4], 1)
            },
            'mid': {
                'time': item[int(len(item) / 2)][0].strftime("%Y-%m-%d %H:%M:%S %z"),
                'distance': round(item[int(len(item) / 2)][1], 1),
                'azimuth': round(item[int(len(item) / 2)][2], 1),
                'altitude': round(item[int(len(item) / 2)][3], 1),
                'height': round(item[int(len(item) / 2)][4], 1)
            },
            'exit': {
                'time': item[-1][0].strftime("%Y-%m-%d %H:%M:%S %z"),
                'distance': round(item[-1][1], 1),
                'azimuth': round(item[-1][2], 1),
                'altitude': round(item[-1][3], 1),
                'height': round(item[-1][4], 1)
            }
        }
        satpasses.append(satpass)

    return satpasses
