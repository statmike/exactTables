data table;
	call streaminit(0);
	do level = 1 to 5;
		measureA=rand('Uniform'); measureB=rand('Uniform'); output;
	end;
run;

proc sort data=table out=temp; by level; run;
proc transpose data=temp out=temp;
	by level;
run;
data temp;
	set temp;
	label=compress(_NAME_||"_"||put(level,8.2));
run;
proc transpose data=temp out=wide(drop=_NAME_);
	id label;
	var col1;
run;


