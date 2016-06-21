
set term pngcairo size 950,300 font "dejavu,8" 
#background '#FFFFFCF6';



set grid front;
set datafile separator ";";
set timefmt "%Y-%m-%d_%H:%M:%S";
set xdata time;
    
s0 = 11
s1 = 2e-16
cal_lightlux(x) = s0 * x + s1 * x **6

#set xtics format "%d" time rotate by 0;
set xtics format "%d/%m %H:%M" time rotate by -45;
set xtics 3600*24;
set autoscale xfix;


set format y "%6.0f";
set grid mytics;
set ytics 10;
set log y;
set ylabel 'Ljusintensitet (lux)';
set output "/srv/http/app/htdocs/static/sunlightPlot.png";
plot [*:*][30:3000]\
1000 with filledcurves x2 fs solid 0.1 noborder title '' lc rgb "#009020",\
200 with filledcurves y=1000 fs solid 0.05 noborder title '' lc rgb "#009020",\
50 with filledcurves y=200 fs solid 0.05 noborder title '' lc rgb "#ffa020",\
'< tail -10000 /srv/http/app/htdocs/static/sunlightdata.txt' every 1 using 3:($5>0?$5:0.1)\
  with fillsteps fs solid 1.0 noborder title '' lw 2 lc rgb '#009e60'




set term pngcairo size 310,200 font "dejavu,8" 
#background '#FFFFFCF6';
set xtics format "%H:%M" time rotate by -45;
set xtics 3600;
set autoscale xfix;
set format y "%3.0f";
unset log y;
set grid nomytics;
set output "/dev/null";

plot [*:*][*:*]\
'< tail -720 /srv/http/app/htdocs/static/sunlightdata.txt' using 3:($5)

 {    
    if(GPVAL_DATA_Y_MIN < 1){
        ymin = 1
    }
    else{
        ymin=GPVAL_DATA_Y_MIN
    }
    if(GPVAL_DATA_Y_MAX < 1){
        ymax = 100
    }    
    else{
        ymax=GPVAL_DATA_Y_MAX
    }
    
}

set log y
set format y "%5.0f";
set ytics auto;
set ylabel 'Ljusintensitet (lux)';
set output "/srv/http/app/htdocs/static/sunlightPlot1h.png";
plot [*:*][ymin:ymax]\
'< tail -240 /srv/http/app/htdocs/static/sunlightdata.txt' using 3:($5)\
  with lines title '' lw 1 lc rgb '#009e60'


#set fit quiet
#set print '/srv/http/app/htdocs/static/trendSunlight.txt';

#trendL(x) = (L/60.0)*x + L0;
#fit [*:*] trendL(x)\
#'< tail -180 /srv/http/app/htdocs/static/sunlightdata.txt' using 0:5 via L,L0;



#print sprintf("lightLuxTrend;%.2f",L);


quit
