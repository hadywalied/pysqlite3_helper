#Log file output :
#[Time]
#[Machine CPU Load Percentage], [Machine Memory Total], [Machine Memory Used], [Machine Memory Free]
#[Process Name], [Process ID], [Process CPU Percentage], [Process Memory Virtual], [Process Memory Resident], [Process Memory Shared], [Process Thread Count], [Process Directory Free disk space]
usage="[USAGE]: is-alive.sh (PID's or Processnames)"
sleepTime=30
#######################################################################
#######################################################################
#######################################################################
# Functions section

# [USAGE] : IsProcessRunning PID
# if process died ----> return 1
# Otherwise		  ----> return 0
shopt -s xpg_echo
function IsProcessRunning {
	if ps -p $1 > /dev/null   # process is running
		then
   		return 0
   	else                      # process is not running
   		return 1
	fi
}

function SendMail
{
	if [ $1 == 0 ]; then
		return
	else
		Field1=`printf "%-20s%s" "Run-Number:" "run-$TrialNo"`
		Field2=`printf "%-20s%s" "Testtype:" "$testtype"`
		Field3=`printf "%-20s%s" "BufferSize:" "$BufferSize"`
		Field4=`printf "%-20s%s" "MII-Type:" "$exampleName"`
		Field5=`printf "%-20s%s" "Mode:" "$CompilationMode"`
		Field6=`printf "%-20s%s" "Machine:" "$machineName"`
		Field7=`printf "%s" "=============================================================="`
		Field8=`printf "%s" "Description:"`
		Field9="$4"
		EmailBody="$Field1\n$Field2\n$Field3\n$Field4\n$Field5\n$Field6\n$Field7\n$Field8\n$Field9\n"
		echo "EmailBody:$EmailBody .. subject:$3 .. atta:$2 .. $MAIL .. $2"
		# if [ -f $2 ]; then

		# 	printf "$EmailBody" | mail -s "$3" -a "$2" "$MAIL"
		# else
			printf "$EmailBody" | mail -s "$3" "$MAIL"
		# fi
	fi
}

# [USAGE] : Notifyme Pname PID Powner Mail 
function Notifyme
{
MessageBody="The following process is gone from `hostname` at `date`

-Process Name  :  $1
-Process ID  :  $2
-Process Owner  :  $3"
echo "Will send Mail .. "
echo "$MessageBody" | mail -s "$1 is down" "$Mail"
SendMail $NotifyOnCrashEnable "--" "$1 is down" "$MessageBody"
}

# [USAGE] : ParseProcessName Pname
# Convert process name to a list of PID's and add them to the list 
function ParseProcessName
{
	InstancesNo=`pgrep -u $USER -x $1 | wc -l`
	printf "$1 : $InstancesNo Processes have been found for $1 [ "
	for fcount in `pgrep -u $USER -x $1`
	do
		pidList+=("$fcount")
		printf "$fcount "
	done
	echo "]"
}


#######################################################################
#######################################################################
#######################################################################
# This is the Main program
pidList=()
hostName=$(hostname)
#sleep 30 

if [ $# -lt 1 ] ; then 
	echo "Too few Arguments"
	echo $usage
	return 1
fi


for var in ${@}
do
	if ! [[ $var =~ ^-?[0-9]+$ ]] ; then     	# not a number
    	ParseProcessName $var
    else                                 		# number
 		IsProcessRunning $var
 		if [ $? -eq 0 ] ; then 
   			pidList+=("$var")
   		else
   			echo "$var is not a running process"
   		fi
	fi
done

if [ -z "$pidList" ]; then
    echo "No Processes is found , Terminating the script ... "
    exit 1
fi

# Removing Duplicates
temp=($(printf "%s\n" "${pidList[@]}" | sort -u))
pidList=("${temp[@]}") 

echo "Number of Valid Processes =  ${#pidList[@]}"
echo "Processes Monitored : ${pidList[@]}\n"
start=0
end=`expr ${#pidList[@]} - 1`
# Get processes Info from their ID's
for ((i=$start;i<=$end;i++))
do
	InfoName[${pidList[$i]}]=`ps -p ${pidList[$i]} -o comm=`
	InfoUsername[${pidList[$i]}]=`ps -p ${pidList[$i]} -o ruser=`
done


PrintPid() 
{
	local pid=$1
	local lvl=$2 #proclvl
	for (( c=1; c<=$lvl; c++ )) #c-> numberoftabs
	do
		printf "\t"
	done
	local procName=$(ps -p $pid -o comm=)
	#local TOTAL_CPU_MHZ=$(cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq | awk '{s+=$1/1000} END {print s}')
	#local CPU_COUNT=$(cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq | wc -l)
	local cpuPercent=$(ps -p $pid -o %cpu | tail -1 | xargs)
	
	#local CPU_ABS_UNFORMATTED=$(echo "$cpuPercent * $TOTAL_CPU_MHZ * 0.01 / $CPU_COUNT" | bc -l ) 
	#local CPU_ABS=$(printf "%0.2f",$CPU_ABS_UNFORMATTED ) #in MHz
	
	local memVrt=$(( $(ps -o vsz -p $pid | tail -1)/1024 )) #in MB
	local memRes=$(( $(ps -o rss -p $pid | tail -1)/1024 ))
	#local memShrd=$(( $(pmap -d $pid | tail -1 | awk '{print $NF}' ) /1024 )) #in MB
	local memShrd=200
	
	local threadCount=$(ps huH p $pid | wc -l)			
	local procPath=$(pwdx $pid | grep -o '\/.*')
	local fdProcInGb=$(df -a $procPath | tail -1 | awk '{printf "%0.2f" , $3/1024/1024}' ) #in GB
	
	printf "%s, %s, %s%%, %s, %s, %s, %s, %s\n" "$procName" "$pid" "$cpuPercent" "$memVrt" "$memRes" "$memShrd" "$threadCount" "$fdProcInGb"

}

GetChildren()
{

	local cmdp='pgrep -P '$1
	local children=$($cmdp)
	local i
	local lvl=$2
	lvl=$((lvl+1)) # Generation Level of current process 
	
	# if process has children recursively print them
	if [ ! -z "$children" ] ;then  
		for i in $children
		do
		  PrintPid $i $lvl 
		  GetChildren $i $lvl
		done
	fi
}
for ((i=$start;i<=$end;i++)) 
do
	echo "Process Name: $(ps -p ${pidList[$i]} -o comm=), Process ID: ${pidList[$i]}" > memory_${pidList[$i]}.log
done

while true
do
	for ((i=$start;i<$end+1;i++)) 
	do
		IsProcessRunning ${pidList[$i]}
		isProcessRunningreturnvalue=$?

		if [ $isProcessRunningreturnvalue -eq 0 ] ; then 
			procID=${pidList[$i]}
			
		# 	###old command
			echo " $('date') $(($(pmap ${pidList[$i]}| grep -i Total | awk '/[0-9]/{print $2}'  | sed 's/[^0-9]*//g') /1024)) MB" >> memory_${procID}.log
			
			now=$(date) #time
			printf "#%s \n" "$now" >> ${hostName}_cpu_mem_${procID}.log
			
			
			cpuLoad=$(grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {printf "%0.2f",usage }') #in Percentage
			machineMemoryTotal=$(free | grep Mem | awk '{printf "%0.2f", $2/1024}')
			machineMemoryUsed=$(free | grep Mem | awk '{printf "%0.2f", $3/1024 }')
			machineMemoryFree=$(free | grep Mem | awk '{printf "%0.2f", $4/1024 }')
			printf "%s%%, %s, %s, %s\n" "$cpuLoad" "$machineMemoryTotal" "$machineMemoryUsed" "$machineMemoryFree" >> ${hostName}_cpu_mem_${procID}.log
			PrintPid $procID 0  >> ${hostName}_cpu_mem_${procID}.log
			GetChildren $procID 0 >> ${hostName}_cpu_mem_${procID}.log
		fi
		if [ $isProcessRunningreturnvalue -eq 1 ] ; then
			echo "Will notify of PID: ${pidList[$i]}"
		#	Send mail raises an error on some machines (to be fixed)
    		Notifyme ${InfoName[${pidList[$i]}]} ${pidList[$i]} ${InfoUsername[${pidList[$i]}]}
    		unset pidList[$i]
			pidList=( "${pidList[@]}" )
    		((end--))
    		if [ $end -eq -1 ] ; then
				exit 0
			fi
    		((i--))
    	fi
	done
	sleep $sleepTime
done
