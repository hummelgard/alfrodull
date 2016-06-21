
set term pngcairo size 950,300 font "dejavu,8"
#background '#FFFFFCF6';
set grid front;
set datafile separator ";";
set timefmt "%Y-%m-%d_%H:%M:%S";
set xdata time;
    

set xtics format "%d" time rotate by 0;
set xtics 3600*24;
set autoscale xfix;

set output "/srv/http/app/htdocs/static/currentPlot.png";

#set format y "%6.0f"
#set ylabel 'Batteriström (mA)';
#plot [*:*][-200:400]\
#0 axes x1y1 with filledcurves x1 fs solid 0.05 noborder title '' lc rgb "#d03020",\
#0 axes x1y1 with filledcurves x2 fs solid 0.05 noborder title '' lc rgb "#009020",\
#  '< tail -10000 /srv/http/app/htdocs/static/batterydata.txt' every 10 using 3:(-$5)\
#  axes x1y1 with lines title '' lw 1 lc rgb '#009e60'


set multiplot layout 2,1
set size 1,0.3
set origin 0.0,0.70
unset xtics
set bmargin 0
set grid mytics
set xtics format "%d" time rotate by 0;
set xtics 3600*24;
set autoscale xfix;
set ytics 500;
set format y "%6.0f";
set ylabel 'Batteriström (mA)';

#set log y

plot [*:*][100:2000]\
0 axes x1y1 with filledcurves x1 fs solid 0.05 noborder title '' lc rgb "#d03020",\
0 axes x1y1 with filledcurves x2 fs solid 0.1 noborder title '' lc rgb "#009020",\
  '< tail -10000 /srv/http/app/htdocs/static/batterydata.txt' every 10 using 3:(-$5>50?-$5:0)\
  axes x1y1 with lines title '' lw 1 lc rgb '#009e60'

set origin 0.0,0.0
set size 1,0.70
set tmargin 0
unset bmargin 
set xtics 3600*24;
unset log y
set grid nomytics
set ytics 20
set ylabel " "
set format y "%6.0f";
plot [*:*][-100:100]\
0 axes x1y1 with filledcurves x1 fs solid 0.05 noborder title '' lc rgb "#d03020",\
0 axes x1y1 with filledcurves x2 fs solid 0.05 noborder title '' lc rgb "#009020",\
  '< tail -10000 /srv/http/app/htdocs/static/batterydata.txt' every 10 using 3:(-$5)\
  axes x1y1 with lines title '' lw 1 lc rgb '#009e60'
unset multiplot






set output "/srv/http/app/htdocs/static/powerPlot.png";
set multiplot layout 2,1

set size 1,0.6
set origin 0.0,0.35
set xtics 3600*24;
set bmargin 0
set ytics 4;
set grid mytics
set format y "%6.0f";
set ylabel 'Producerad Effekt (W)';

#set log y

plot [*:*][1:30]\
0 axes x1y1 with filledcurves x1 fs solid 0.05 noborder title '' lc rgb "#d03020",\
0 axes x1y1 with filledcurves x2 fs solid 0.05 noborder title '' lc rgb "#009020",\
  '< tail -10000 /srv/http/app/htdocs/static/batterydata.txt' every 10 using 3:(-$5*$6/1000>0.5?-$5*$6/1000:0)\
  axes x1y1 with fillsteps fs solid 1.0 noborder title '' lw 1 lc rgb '#009e60'

set origin 0.0,0.0
set size 1,0.35
set tmargin 0
unset bmargin 
set xtics 3600*24;
unset log y
set grid nomytics
set ytics 0.5
set ylabel " "
set format y "%6.1f";
plot [*:*][-1.5:1.0]\
0 axes x1y1 with filledcurves x1 fs solid 0.05 noborder title '' lc rgb "#d03020",\
0 axes x1y1 with filledcurves x2 fs solid 0.05 noborder title '' lc rgb "#009020",\
  '< tail -10000 /srv/http/app/htdocs/static/batterydata.txt' every 10 using 3:(-$5*$6/1000>0?-$5*$6/1000:0)\
  axes x1y1 with fillsteps fs solid 1.0 noborder title '' lw 1 lc rgb '#009e60',\
  '< tail -10000 /srv/http/app/htdocs/static/batterydata.txt' every 10 using 3:(-$5*$6/1000<0?-$5*$6/1000:0)\
  axes x1y1 with fillsteps fs solid 1.0 noborder title '' lw 1 lc rgb '#d03020'

unset multiplot

set ytics 0.2 nomirror;
set format y "%6.1f";
set rmargin 3
set ylabel 'Batterispänning (V)';

set y2tics ("100%%" 12.626, "90%%" 12.478, "80%%" 12.330, "70%%" 12.182, \
  "60%%" 12.034, "50%%" 11.886,"40%%" 11.738,"30%%" 11.590,\
  "20%%" 11.442,"10%%" 11.294,"0%%" 11.146) offset -5 nomirror

set y2range [11.1:13.0]
set output "/srv/http/app/htdocs/static/voltagePlot.png";
plot [*:*][11.1:13.0]\
11.442 with filledcurves x1 fs solid 0.05 noborder title '' lc rgb "#d01000",\
11.442 with filledcurves y=12.182 fs solid 0.05 noborder title '' lc rgb "#ffa020",\
12.182 with filledcurves y=12.7 fs solid 0.1 noborder title '' lc rgb "#009020",\
'< tail -10000 /srv/http/app/htdocs/static/batterydata.txt' every 10 using 3:6 \
  with lines title '' lw 1 lc rgb '#009e60'

unset y2tics

set term pngcairo size 310,200 font "dejavu,8" 
#background '#FFFFFCF6';
set xtics format "%H:%M" time rotate by -45;
set xtics 3600;
set autoscale xfix;
set format y "%3.0f";
set ytics auto;
unset log y;
set grid nomytics;
set output "/dev/null";
plot [*:*][*:*]\
'< tail -240 /srv/http/app/htdocs/static/batterydata.txt' using 3:(-$5)

if(GPVAL_DATA_Y_MAX-GPVAL_DATA_Y_MIN < 100){ 
    ymax=(GPVAL_DATA_Y_MAX+GPVAL_DATA_Y_MIN)/2+50
    ymin=(GPVAL_DATA_Y_MAX+GPVAL_DATA_Y_MIN)/2-50

}
else {
    ymax=GPVAL_DATA_Y_MAX
    ymin=GPVAL_DATA_Y_MIN
}
    
set ytics auto;
set ylabel 'Batteriström (mA)';
set output "/srv/http/app/htdocs/static/currentPlot1h.png";
plot [*:*][ymin:ymax]\
0 title '' lc rgb "#808080",\
'< tail -240 /srv/http/app/htdocs/static/batterydata.txt' using 3:(-$5)\
  with lines title '' lw 1 lc rgb '#009e60'


set output "/dev/null";
plot [*:*][*:*]\
'< tail -240 /srv/http/app/htdocs/static/batterydata.txt' using 3:6

if(GPVAL_DATA_Y_MAX-GPVAL_DATA_Y_MIN < 1){ 
    ymax=(GPVAL_DATA_Y_MAX+GPVAL_DATA_Y_MIN)/2+0.5
    ymin=(GPVAL_DATA_Y_MAX+GPVAL_DATA_Y_MIN)/2-0.5
}
else {
    ymax=GPVAL_DATA_Y_MAX
    ymin=GPVAL_DATA_Y_MIN
}

set ytics auto;
set format y "%4.1f";
set ylabel 'Batterispänning (Volt)';
set output "/srv/http/app/htdocs/static/voltagePlot1h.png";
plot [*:*][ymin:ymax]\
'< tail -240 /srv/http/app/htdocs/static/batterydata.txt' using 3:6\
  with lines title '' lw 1 lc rgb '#009e60'



set fit quiet
set print '/srv/http/app/htdocs/static/trendBattery.txt';
trendI(x) = (I/60.0)*x + I0;
fit [*:*] trendI(x)\
'< tail -180 /srv/http/app/htdocs/static/batterydata.txt' using 0:(-$5) via I,I0;


trendU(x) = (U/60.0)*x + U0;
fit [*:*] trendU(x)\
'< tail -180 /srv/http/app/htdocs/static/batterydata.txt' using 0:($6) via U,U0;

print sprintf("voltTrend;%.2f;currentTrend;%.2f",I,U);


quit
