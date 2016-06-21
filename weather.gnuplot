set term pngcairo size 950,300 font "dejavu,8" 
#background '#FFFFFCF6'
set format y "%4.0f"
set grid front
set datafile separator ";"
    

set timefmt "%Y-%m-%d_%H:%M:%S"
set xdata time   

set xtics format "%d" time rotate by 0

set xtics 3600*24
set autoscale xfix
set ytics 10
set ylabel 'Temperatur (grad C)'
set output "/srv/http/app/htdocs/static/temperaturePlot.png"
plot [*:*][-30:30]\
    0 axes x1y1 with filledcurves x1 fs solid 0.05 noborder title '' \
    lc rgb "#002050", \
    0 axes x1y1 with filledcurves x2 fs solid 0.05 noborder title '' \
    lc rgb "#d01000",  '< tail -10000 /srv/http/app/htdocs/static/weatherdata.txt' \
    every 20 using 3:8 axes x1y1 with lines title '' lw 1 lc rgb '#606060', \
    '< tail -10000 /srv/http/app/htdocs/static/weatherdata.txt' every 20 \
    using 3:5 axes x1y1 with lines title '' lw 1 lc rgb '#009e60'


set ytics 10
    
set ylabel 'Luftfuktighet (rel%)'
set output "/srv/http/app/htdocs/static/humidityPlot.png"
plot [*:*][20:100]\
    50 with filledcurves x2 fs solid 0.05 noborder title '' lc rgb "#002050", \
    80 with filledcurves x2 fs solid 0.1 noborder title '' lc rgb "#002050", \
    '< tail -10000 /srv/http/app/htdocs/static/weatherdata.txt' every 20 \
    using 3:6 with lines title '' lw 1 lc rgb '#009e60'

set xtics
set xtics format "%d/%m %H:%M" time rotate by -45
set ytics 10
set ylabel 'Lufttryck (hPa)'
set output "/srv/http/app/htdocs/static/pressurePlot.png"
plot [*:*][960:1040]\
1020 with filledcurves x2 fs solid 0.05 noborder title '' lc rgb "#002050",\
    980 with filledcurves x1 fs solid 0.05 noborder title '' lc rgb "#d01000",\
    '< tail -10000 /srv/http/app/htdocs/static/weatherdata.txt' every 20 \
    using 3:($7/100) with lines title '' lw 1 lc rgb '#009e60'



set term pngcairo size 310,200 font "dejavu,8" 
#background '#FFFFFCF6'
set xtics format "%H:%M" time rotate by -45
set xtics 1800
set autoscale xfix
set format y "%3.0f"


set output "/dev/null"
plot [*:*][*:*]\
'< tail -180 /srv/http/app/htdocs/static/weatherdata.txt' using 3:5
if(GPVAL_DATA_Y_MAX-GPVAL_DATA_Y_MIN < 10){ 
    ymax=(GPVAL_DATA_Y_MAX+GPVAL_DATA_Y_MIN)/2+5
    ymin=(GPVAL_DATA_Y_MAX+GPVAL_DATA_Y_MIN)/2-5
}
else {
    ymax=GPVAL_DATA_Y_MAX
    ymin=GPVAL_DATA_Y_MIN
}
    
set ytics auto
set ylabel 'Temperatur (grad C)'
set output "/srv/http/app/htdocs/static/temperaturePlot1h.png"
plot [*:*][ymin:ymax]\
  0 title '' lc -1, '< tail -180 /srv/http/app/htdocs/static/weatherdata.txt' \
  using 3:8 with lines title '' lw 1 lc rgb '#606060', \
  '< tail -180 /srv/http/app/htdocs/static/weatherdata.txt' using 3:5 with \
  lines title '' lw 1 lc rgb '#009e60'


set output "/dev/null"
plot [*:*][*:*]\
  '< tail -180 /srv/http/app/htdocs/static/weatherdata.txt' using 3:6

if(GPVAL_DATA_Y_MAX-GPVAL_DATA_Y_MIN < 10){ 
    ymax=(GPVAL_DATA_Y_MAX+GPVAL_DATA_Y_MIN)/2+5
    ymin=(GPVAL_DATA_Y_MAX+GPVAL_DATA_Y_MIN)/2-5
}
else {
    ymax=GPVAL_DATA_Y_MAX
    ymin=GPVAL_DATA_Y_MIN
}

set ytics auto
set ylabel 'Luftfuktighet (rel%)'
set output "/srv/http/app/htdocs/static/humidityPlot1h.png"
plot [*:*][ymin:ymax]\
  '< tail -180 /srv/http/app/htdocs/static/weatherdata.txt' using 3:6 with \
  lines title '' lw 1 lc rgb '#009e60'


set output "/dev/null"
plot [*:*][*:*]\
  '< tail -180 /srv/http/app/htdocs/static/weatherdata.txt' using 3:($7/100)

if(GPVAL_DATA_Y_MAX-GPVAL_DATA_Y_MIN < 10){ 
    ymax=(GPVAL_DATA_Y_MAX+GPVAL_DATA_Y_MIN)/2+5
    ymin=(GPVAL_DATA_Y_MAX+GPVAL_DATA_Y_MIN)/2-5
}
else {
    ymax=GPVAL_DATA_Y_MAX
    ymin=GPVAL_DATA_Y_MIN
}

set format y "%4.0f"
set ytics auto
set ylabel 'Lufttryck (hPa)'
set output "/srv/http/app/htdocs/static/pressurePlot1h.png"
plot [*:*][ymin:ymax]\
  '< tail -180 /srv/http/app/htdocs/static/weatherdata.txt' using 3:($7/100) \
  with lines title '' lw 1 lc rgb '#009e60'


set fit quiet
set print '/srv/http/app/htdocs/static/trend.txt'
trendT(x) = (T/60.0)*x + T0
fit [*:*] trendT(x) \
'< tail -180 /srv/http/app/htdocs/static/weatherdata.txt' using 0:($5) via T,T0

trendH(x) = (H/60.0)*x + H0
fit [*:*] trendH(x) \
'< tail -180 /srv/http/app/htdocs/static/weatherdata.txt' using 0:($6) via H,H0

trendP(x) = (p/60.0)*x + p0
fit [*:*] trendP(x) \
'< tail -180 /srv/http/app/htdocs/static/weatherdata.txt' using 0:($7/100) via p,p0

trendD(x) = (d/60.0)*x + d0
fit [*:*] trendD(x) \
'< tail -180 /srv/http/app/htdocs/static/weatherdata.txt' using 0:8 via d,d0


print sprintf("TemperatureTrend;%.2f;HumidityTrend;%.2f;PressureTrend;%.2f;DewPointTrend;%.2f",T,H,p,d)



quit
