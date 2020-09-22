import sys, os
import time
import datetime
import json, re
import win32gui

def get_process():
    window=win32gui.GetForegroundWindow()
    name=win32gui.GetWindowText(window)
    full_name=re.split('-|—', name)
    app=full_name[len(full_name)-1].strip()

    if app=='Google Chrome':
        page=full_name[len(full_name)-2].strip()

        return {"app": app, "page": page}
    else:
        return {"app": app}


def add_activity(app, period):

    if os.path.exists('activity.json'):
        activity_json=open("activity.json")
        data=json.load(activity_json)
    else:
        activity_json=open('activity.json', 'x')
        data={}
        activity_json.close()

    today=str(datetime.datetime.now().strftime('%x'))

    app_updated=False
    day_updated=False

    for date in data:
        if date==today:
            day_updated=True
            apps=data[date]
            for _app in apps:
                if _app==app['app']:
                    apps[_app].append(period)
                    data[date]=apps

                    with open('activity.json', 'w') as f:
                        json.dump(data, f, indent=4)
                        f.close()

                    app_updated=True

        if date==today and not app_updated:
            day_updated=True
            apps=data[today]
            apps[app['app']]=[period]
            data[today]=apps

            with open('activity.json', 'w') as f:
                json.dump(data, f, indent=4)
                f.close()
    
    if not day_updated:
        data[today]={
            app['app']:[period]
        }

        with open('activity.json', 'w') as f:
            json.dump(data, f, indent=4)
            f.close()

def summary():
    with open('activity.json') as activity_json:
       data=json.load(activity_json)

    for day in data:
        if day==str(datetime.datetime.now().strftime('%x')):
            apps=data[day]
            for name in apps:
                app=apps[name]
                _time=datetime.datetime.strptime('0:0:0', '%H:%M:%S')
                for period in app:
                    dif=datetime.datetime.strptime(period['end'], '%H:%M:%S')-datetime.datetime.strptime(period['start'], '%H:%M:%S')
                    _time+=dif
                print(name, "   ", _time.strftime('%H:%M:%S'))

while True:
    try:
        try:
            previous=activity
        except:
            previous='none'
            app_time='none'

        activity=get_process()

        if previous==activity:
            app_time["end"]=str(datetime.datetime.now().strftime('%X'))
        elif previous!=activity:
            if app_time!='none' and previous['app']:
                add_activity(previous, app_time)

            app_time={
                "start": (datetime.datetime.now()-datetime.timedelta(seconds=2)).strftime('%X'),
                "end": str(datetime.datetime.now().strftime('%X'))
            }

        time.sleep(3)

    except KeyboardInterrupt:
        summary()
        sys.exit()