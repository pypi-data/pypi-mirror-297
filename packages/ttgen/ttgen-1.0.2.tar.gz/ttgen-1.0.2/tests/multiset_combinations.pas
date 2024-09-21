{

                            Online Pascal Compiler.
                Code, Compile, Run and Debug Pascal program online.
Write your code in this editor and press "Run" button to execute it.

https://www.onlinegdb.com/online_pascal_compiler#

}

program ex(input,output);

label 10, 20;

var i,i0,ii,n,k,kk,s1,count,lower,upper,lower1,upper1,next:integer;
var b,d,down,up,up1,m,sum,solve,mark:array[0..100] of integer;
var a:array[0..100] of integer;
var up_point,next_landing:boolean;

procedure out;
    var i:integer;
    begin count:=count+1; for i:=1 to n do write(a[i]:2); writeln
end;

function min(x,y:integer):integer;
begin
    if x<=y then min:=x else min:=y
end;

function max(x,y:integer):integer;
begin
    if x>=y then max:=x else max:=y
end;

begin {main}
    {writeln('input k and n');
    readln(k,n);
    kk:=k;
    writeln('input m[1], ..., m[n]');
    for i:=1 to n do read(m[i]);
    readln;}
    k:=3;
    n:=5;
    kk:=k;
    m[1]:=1;
    m[2]:=2;
    m[3]:=3;
    m[4]:=2;
    m[5]:=1;
    for i:=n downto 1 do
        if m[i]<=kk then
            begin
                a[i]:=m[i];
                kk:=kk-a[i]
            end
        else
            begin
                a[i]:=kk;
                goto 10
            end;
   
   
   
    10:
        writeln('a=[', a[1], ' ', a[2], ' ', a[3], ' ', a[4], ' ', a[5], ' ... ]');
        writeln('Start main logic?');

        i0:=i;
        writeln('i0=', i0);
        b[n+1]:=0;
        for i:=n downto 1 do b[i]:=b[i+1]+m[i];
       
        writeln('b=[', b[1], ' ', b[2], ' ', b[3], ' ', b[4], ' ', b[5], ' ... ]');
       
        for i:=0 to n do begin
            up[i]:=i;
            up1[i]:=i;
            solve[i]:=n;
            mark[i]:=0
        end;
        sum[0]:=0;
        a[0]:=0;
        for i:=1 to n do
            sum[i]:=sum[i-1]+a[i-1];
        writeln('[1] sum=[', sum[1], ' ', sum[2], ' ', sum[3], ' ', sum[4], ' ', sum[5], ' ', sum[6], ' ', sum[7], ' ... ]');

        for i:=i0+1 to n do
            sum[i]:=sum[i]+1;
        for i:=1 to i0 do
            d[i]:=1;
        for i:=i0+1 to n do
            d[i]:=-1;
        for i:=1 to n-1 do
            down[i]:=n-1;
        count:=0;
        i:=i0;
        
        writeln('up=[', up[1], ' ', up[2], ' ', up[3], ' ', up[4], ' ', up[5], ' ', up[6], ' ', up[7], ' ... ]');
        writeln('up1=[', up1[1], ' ', up1[2], ' ', up1[3], ' ', up1[4], ' ', up1[5], ' ', up1[6], ' ', up1[7], ' ... ]');
        writeln('solve=[', solve[1], ' ', solve[2], ' ', solve[3], ' ', solve[4], ' ', solve[5], ' ', solve[6], ' ', solve[7], ' ... ]');
        writeln('mark=[', mark[1], ' ', mark[2], ' ', mark[3], ' ', mark[4], ' ', mark[5], ' ', mark[6], ' ', mark[7], ' ... ]');
        writeln('d=[', d[1], ' ', d[2], ' ', d[3], ' ', d[4], ' ', d[5], ' ', d[6], ' ', d[7], ' ... ]');
        writeln('down=[', down[1], ' ', down[2], ' ', down[3], ' ', down[4], ' ', down[5], ' ', down[6], ' ', down[7], ' ... ]');
        writeln('sum=[', sum[1], ' ', sum[2], ' ', sum[3], ' ', sum[4], ' ', sum[5], ' ', sum[6], ' ', sum[7], ' ... ]');
        
        {writeln('b = ');}
        {for i:=1 to n+3 do write(b[i]:2);}
        {for i:=1 to n+3 do write(b[i]:2);}
       
        writeln('Begin repeat sequence');
        {writeln('b=[', b[1], ' ', b[2], ' ', b[3], ' ', b[4], ' ', b[5], ' ... ]');
        writeln('sum=[', sum[1], ' ', sum[2], ' ', sum[3], ' ', sum[4], ' ', sum[5], ' ... ]');
        writeln('m=[', m[1], ' ', m[2], ' ', m[3], ' ', m[4], ' ', m[5], ' ... ]');
        writeln('i=', i);}
        repeat
            out;
            lower:=max(k-b[i+1]-sum[i],0);
            upper:=min(k-sum[i],m[i]);
            {
            writeln('lower=', lower);
            writeln('upper=', upper);
            writeln('##', k, sum[i], m[i]);
            writeln('c1: ', (d[i]>0) and (a[i]=upper));
            writeln('c2: ', (d[i]<0) and (a[i]=lower));
            }
            writeln('full clause: ', not((d[i]>0) and (a[i]=upper) or (d[i]<0) and (a[i]=lower)));
           
            writeln('i=', i);

            if not((d[i]>0) and (a[i]=upper) or (d[i]<0) and (a[i]=lower)) then begin
                writeln('=== Doing 0');
                writeln('    a=', a[1], a[2], a[3], a[4], a[5]);
                writeln('    i=', i);
                writeln('    a[i]=', a[i]);
                writeln('    d=', d[1], d[2], d[3], d[4], d[5]);
                writeln('    solve=', solve[1], solve[2], solve[3], solve[4], solve[5]);
                writeln('    solve[i]=', solve[i]);
                a[i]:=a[i]+d[i];
                a[solve[i]]:=a[solve[i]]-d[i];
            end;
            up[i]:=i;
           
            writeln('a=[', a[1], ' ', a[2], ' ', a[3], ' ', a[4], ' ', a[5], ' ... ]');
            writeln('up=[', up[1], ' ', up[2], ' ', up[3], ' ', up[4], ' ', up[5], ' ... ]');
           

            if (d[i]>0) and (a[i]=upper) or (d[i]<0) and (a[i]=lower) then begin
                writeln('Doing 1');
                up[i]:=up[i-1];
                up[i-1]:=i-1;
                lower1:=max(k-b[i+1]-sum[i]-d[up[i]],0);
                upper1:=min(k-sum[i]-d[up[i]],m[i]);
                writeln('lower1=', lower1, '; upper1=', upper1);
                if d[i]>0 then next:=upper1 else next:=lower1;
                if next<>a[i] then solve[up[i]]:=i else solve[up[i]]:=solve[i];
                mark[up[i]]:=1;
                mark[i]:=1;
                up_point:=(sum[i]+a[i]=k) or (sum[i]+a[i]+b[i+1]=k) or (i=n-1);
                if lower1<>upper1 then sum[i]:=sum[i]+d[up[i]];
                next_landing:=(sum[i]+next=k) or (sum[i]+next+b[i+1]=k) or (i=n-1);
                up1[i]:=up1[i-1];
                up1[i-1]:=i-1;
                if lower1=upper1 then
                    down[up1[i]]:=i
                else if next_landing then
                    down[up[i]]:=i
                else
                    down[up[i]]:=down[i];
                if next_landing then up1[i]:=i;
                d[i]:=-d[i];
                goto 20;
            end;
            writeln('up_point=', up_point);
            if up_point then begin
                writeln('Doing 2');
                ii:=i;
                i:=up[i];
                up[ii]:=ii;
                up_point:=false;
            end
            else begin
                writeln('=== Doing 3');
                if mark[down[i]]=0 then solve[down[i]]:=solve[i];
                mark[i]:=0;
                i:=down[i];
                writeln('    i=', i);
                writeln('    mark=', mark[1], mark[2], mark[3], mark[4], mark[5]);
                writeln('    down=', down[1], down[2], down[3], down[4], down[5]);
            end;
            writeln;
            writeln;
        until i=0;
    out;
    writeln('count= ', count:5);
    20:
end.