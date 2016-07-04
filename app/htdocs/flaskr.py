# all the imports
import sqlite3, time, locale
from os import popen
from math import log10,floor
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask_socketio import SocketIO, send, emit, disconnect
import functools
from flask_login import LoginManager, current_user



# configuration
DATABASE = '/srv/http/app/flaskr.db'
DEBUG = True
SECRET_KEY = 'vader2016pi3'
USERNAME = 'maghum'
PASSWORD = 'snigel2015'

def round_sigfigs(num, sig_figs):
    """Round to specified number of sigfigs."""

    if num != 0:

        exp = int(floor( log10(abs(num)) )) + 1
	
        if(sig_figs > exp): #means result must be a decimal (float) number
            n = sig_figs - exp
            return float( round(num, n ) )

        elif(sig_figs < exp): 
            #significant figures greater than length of number, means
            #result must be of integer type
            return int( round(num, -(exp-sig_figs) ) )

        else: #significant figures equals to length of number, just return int
            return int(num)
    else:
        return 0  # Can't take the log of 0

# create our little application :)
app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config.from_object(__name__)
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)

socketio = SocketIO(app)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


from contextlib import closing
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/about')
def about():

    return render_template('show_about.html')

@app.route('/logg')
def logg():

    return render_template('show_logg.html')

@app.route('/projektredovisning')
def projektredovisning():

    return render_template('show_projektredovisning.html')

@app.route('/battery')
def show_battery():

    locale.setlocale(locale.LC_ALL,"sv_SE.utf8")
    clock_str = time.strftime("%a, %-d %b %H:%M:%S").encode('ascii', 'xmlcharrefreplace').decode('utf8')

    logdata = popen("tail -n 1 /srv/http/app/htdocs/static/batterydata.txt").read().split(";")
    current = -float(logdata[4])
    voltage = float(logdata[5])
    power = voltage*current / 1000 #in watt 
 
    logdata = popen("tail -n 1 /srv/http/app/htdocs/static/sunlightdata.txt").read().split(";")
    lightLux = float(logdata[4])

    current_str = "{0:+.0f}".format(current)
    voltage_str = "{0:.2f}".format(voltage)
    
    if(power < 10):
        power_str = "{0:.2f}".format(power)
    elif(power < 1):
        power_str = "{0:.2f}".format(power)
    else:
        power_str = "{0:.1f}".format(power)

    lightLux_str = "{0:.0f}".format( round_sigfigs(lightLux,3) )

    s0 = 10.0
    s1 = 2.8e-5
    #cal_lightlux(x) = s0 * x + s1 * x **6

    #s0 = 559.626
    #s1 = 0.00164915
    cal_lightlux = s0*lightLux + s1*lightLux**3
    cal_lightlux_str = "{0:.0f}".format( round_sigfigs(cal_lightlux,2) )

    file = open ("/srv/http/app/htdocs/static/trendBattery.txt", "r")
    trend_data_str = file.readline().split(";")
    file.close()
    voltageTrend = float(trend_data_str[1])
    currentTrend = float(trend_data_str[3])
    
    chargeLevel = 67.57 * voltage - 753.1
    if(chargeLevel > 100): chargeLevel=100
    if(chargeLevel <0): chargeLevel=0
    voltageTrend_str = "<span class=trend_battGOOD>{0:.0f}%</span>".format(chargeLevel)

    if( current > 0 ): currentTrend_str = "<span class=trend_charging>laddning</span>"
    else: currentTrend_str = "<span class=trend_discharging>urladdning</span>"

    if( lightLux > 1000 ): 
        lightLuxIcon_str =('<span class="bforecast"><img class="ICON" src="'+url_for('static', filename='ICONsunny.png')+
        '" title="idag, solkraft + laddning">idag</span>')
    elif( lightLux > 200 ): 
        lightLuxIcon_str =('<span class="bforecast"><img class="ICON" src="'+url_for('static', filename='ICONmostlycloudy.png')+        
        '" title="idag, solkraft enbart">idag</span>')
    else: 
        lightLuxIcon_str =('<span class="bforecast"><img class="ICON" src="'+url_for('static', filename='ICONcloudy.png')+
        '" title="idag, batteridrift">idag</span>')

    prognos_str = ""
    with open('/srv/http/solprognosdata.txt', 'r') as file:   
        for line in file:
            (dag_str, val_str) = line.split(":")
            val = int(val_str)




            if(val <= 10):
                prognos_str += ('<span class="bforecast"><img class="ICON" src="'+url_for('static',                
                               filename='ICONsunny.png')+ '" title="' + dag_str + ', solkraft + laddning">'+dag_str+'</span>')
            elif(val < 16):
                prognos_str += ('<span class="bforecast"><img class="ICON" src="'+url_for('static',                
                              filename='ICONmostlycloudy.png')+ '" title="' + dag_str + ', solkraft enbart">'+dag_str+'</span>')
            else:
                prognos_str += ('<span class="bforecast"><img class="ICON" src="'+url_for('static',                
                    filename='ICONcloudy.png')+ '" title="' + dag_str + ', batteridrift">'+dag_str+'</span>' )

            prognos_str += '\n'
    file.close()

    # http://om.yr.no/forklaring/symbol/  för symbolförklaring

    data=dict(clock=clock_str, current=current_str, voltage=voltage_str, power=power_str, lightLux=lightLux_str,
         cal_lightLux=cal_lightlux_str, voltageTrend=voltageTrend_str, currentTrend=currentTrend_str,             
         lightLuxIcon=lightLuxIcon_str, prognosIcon=prognos_str)

    return render_template('show_battery.html', documentdata=data )


@app.route('/')
def show_weather():

    locale.setlocale(locale.LC_ALL,"sv_SE.utf8")
    clock_str = time.strftime("%a, %-d %b %H:%M:%S").encode('ascii', 'xmlcharrefreplace').decode('utf8')

    logdata = popen("tail -n 1 /srv/http/app/htdocs/static/weatherdata.txt").read().split(";")
    temperature = float(logdata[4])
    humidity = float(logdata[5])
    pressure = float(logdata[6])
    dewpoint = float(logdata[7])
    
    temperature_str = "{0:.1f}".format(temperature)
    humidity_str = "{0:.0f}".format(humidity)
    pressure_str = "{0:.0f}".format(pressure/100)
    dewpoint_str = "{0:.1f}".format(dewpoint)

    file = open ("/srv/http/app/htdocs/static/trend.txt", "r")
    trend_data_str = file.readline().split(";")
    file.close()
    tempTrend = float(trend_data_str[1])
    humidTrend = float(trend_data_str[3])
    pressTrend = float(trend_data_str[5])
    dewTrend = float(trend_data_str[7])

    if( tempTrend > 1 ): tempTrend_str = "<span class=trend_rising>stigande</span>"
    elif( tempTrend < -1 ): tempTrend_str = "<span class=trend_dropping>sjunkande</span>"
    else: tempTrend_str = "<span class=trend_steady>stadig</span>"

    if( humidTrend > 2 ): humidTrend_str = "<span class=trend_rising>stigande</span>"
    elif( humidTrend < -2 ): humidTrend_str = "<span class=trend_dropping>sjunkande</span>"
    else: humidTrend_str = "<span class=trend_steady>stadig</span>"

    if( pressTrend > 1.0 ): pressTrend_str = "<span class=trend_rising>stigande</span>"
    elif( pressTrend < -1.0 ): pressTrend_str = "<span class=trend_dropping>sjunkande</span>"
    else: pressTrend_str = "<span class=trend_steady>stadig</span>"

    if( dewTrend > 1 ): dewTrend_str = "<span class=trend_rising>stigande</span>"
    elif( dewTrend < -1 ): dewTrend_str = "<span class=trend_dropping>sjunkande</span>"
    else: dewTrend_str = "<span class=trend_steady>stadig</span>"

    prognos_str = ""
    with open('/srv/http/prognosdata.txt', 'r') as file:   
        for line in file:
            (dag_str, val_str) = line.split(":")
            prognos_str += ('<span class="bforecast"><img class="ICON" src="http://symbol.yr.no/grafikk/sym/b100/'+ 
                                val_str + '.png" title="' + dag_str + '">' + dag_str + '</span>')
            prognos_str += '\n'
    file.close()

    data=dict(clock=clock_str, temperature=temperature_str, humidity=humidity_str, 
              pressure=pressure_str, dewpoint=dewpoint_str, 
              temperatureTrend=tempTrend_str, humidityTrend=humidTrend_str, 
              pressureTrend=pressTrend_str, dewTrend=dewTrend_str, prognosIcon=prognos_str)

    return render_template('show_weather.html', documentdata=data )

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        print(request.data)
        if request.form['username'] != app.config['USERNAME']:
            error = 'ogiltigt användarnamn'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'ogiltigt lösenord'
        else:
            session['logged_in'] = True
            flash('du är inloggad!')
            return redirect(url_for('show_battery'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('du har loggats ut!')
    return redirect(url_for('show_weather'))



def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped


@socketio.on('change settings', namespace='')
#@authenticated_only
def change_settings(message):
    locale.setlocale(locale.LC_ALL,"sv_SE.utf8")
    clock_str = time.strftime("[%H:%M:%S]>").encode('ascii', 'xmlcharrefreplace').decode('utf8')

    settings = {}
    with open('/srv/http/settings.txt', 'r') as file:   
        for setting in file:
            (key, val) = setting.split(":")
            settings[key] = int(val)
    file.close()

    if(message['user'][0:6]=="server"):
        emit('server reply', {'data':clock_str+message['user']+":"+message['note']}, broadcast=True)
    if(message['data']=="manual-latch"):

        if(settings['manual'] == 0): settings['manual'] = 1
        else: settings['manual'] = 0

        if(settings['manual'] == 1):
            if(message['user'][0:6]=="klient"):
                emit('server reply', {'data':clock_str+message['user']+":manuellt läge aktiverat"}, broadcast=True)
            #emit('server reply', {'data': 'manuallt läge på'})
            emit('gpio status', {'data': 'manualon'}, broadcast=True)
        else:
            if(message['user'][0:6]=="klient"):
                emit('server reply', {'data':clock_str+message['user']+":manuellt läge avaktiverat"}, broadcast=True)
            #emit('server reply', {'data': 'manualt läge av'})
            emit('gpio status', {'data': 'manualoff'}, broadcast=True)


    if(message['data']=='solarcell-latch'):

        if(settings['solarcell'] == 1):
            gpio17 = open('/sys/class/gpio/gpio17/value','wb',0)
            gpio17.write(b'1')
            gpio17.close()
            
            # below use for latch-relay
            #gpio27 = open('/sys/class/gpio/gpio27/value','wb',0)
            #gpio27.write(b'1')
            #time.sleep(0.5)
            #gpio27.write(b'0')
            #gpio27.close()
            settings['solarcell'] = 0
            if(message['user'][0:6]=="klient"):
                emit('server reply', {'data':clock_str+message['user']+":solcell urkopplad"}, broadcast=True)
            emit('gpio status', {'data': '17on'}, broadcast=True)
            # emit('gpio status', {'data': '27latch'}, broadcast=True) # use for latch-relay
        else:
            gpio17 = open('/sys/class/gpio/gpio17/value','wb',0)
            gpio17.write(b'0')
            gpio17.close()

            # below use for latch-relay
            #gpio22 = open('/sys/class/gpio/gpio22/value','wb',0)
            #gpio22.write(b'1')
            #time.sleep(0.5)
            #gpio22.write(b'0')
            #gpio22.close()
            settings['solarcell'] = 1
            if(message['user'][0:6]=="klient"):
                emit('server reply', {'data':clock_str+message['user']+":solcell inkopplad"}, broadcast=True)
            emit('gpio status', {'data': '17off'}, broadcast=True)
            #emit('gpio status', {'data': '22latch'}, broadcast=True) # use for latch-relay

    with open('/srv/http/settings.txt','w') as file:
        for key in settings:
            file.write( "{0}:{1}\n".format(key,settings[key]) )
    file.close()

@socketio.on('client event', namespace='')
#@authenticated_only
def test_message(message):
    emit('server reply', {'data': 'klient ansluten med id: '+message['data']}, broadcast=True)


@socketio.on('connect', namespace='')
#@authenticated_only
def test_connect():
    locale.setlocale(locale.LC_ALL,"sv_SE.utf8")
    clock_str = time.strftime("[%H:%M:%S]>").encode('ascii', 'xmlcharrefreplace').decode('utf8')
    client_id = request.sid
    if request.headers.getlist("X-Forwarded-For"):
        client_ip = str(request.headers.getlist("X-Forwarded-For"))
    else:
        client_ip = request.environ["REMOTE_ADDR"]#equest.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    if client_ip != "::1":
        emit('server reply', {'data': clock_str+'klient ansluten med ID: [...' + client_id[-6:]+'], IP: '+ client_ip}, broadcast=True)

    #emit('server reply', {'data': current_client_id})
    settings = {}
    with open('/srv/http/settings.txt', 'r') as file:   
        for setting in file:
            (key, val) = setting.split(":")
            settings[key] = int(val)
    file.close()

    if(settings['manual'] == 1):
        emit('gpio status', {'data': 'manualon'}, broadcast=True)
    else:
        emit('gpio status', {'data': 'manualoff'}, broadcast=True)
   
    if(settings['solarcell'] == 1):
        emit('gpio status', {'data': '17off'}, broadcast=True)
        #emit('gpio status', {'data': '22latch'}, broadcast=True) # use for latch-relay
    else:
        emit('gpio status', {'data': '17on'}, broadcast=True)
        #emit('gpio status', {'data': '27latch'}, broadcast=True) # use for latch-relay


@socketio.on('disconnect', namespace='')
#@authenticated_only
def test_disconnect():
    print('Client disconnected')


#if __name__ == '__main__':
#    app.run(host='lab.hummelgard.com', port=83, debug=True)

