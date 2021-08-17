#$1 --> path to usage detection script
#$2 --> Logging directory
#$3 --> python version
#$4 --> 5G or Ethernet # Requirement
#$5 --> PPID

if [ $# -lt 1 ] ; then 
	echo "Too few Arguments (1--> path to usage detection script, 2--> Logging directory)"
	return 1
fi

sleepTime=1

echo "PID of this script: $$"
echo "PPID of this script: $PPID"


#check 5G or Ethernet
if [ -z "$4" ]
then
	TECH_VER=0 # 0 ---> 5G by default
else
	TECH_VER=$4 # 0 ---> 5G and 1 ---> Ethernet
fi

if [ $TECH_VER == 1 ] ; then
	
	#Do Ethernet Magic
	if [ -z "$VVED_DOMAIN_ID" ]
	then
		  DOMAIN_ID=0
	else
		  DOMAIN_ID=$VVED_DOMAIN_ID
	fi

else
	# Check the value of ETHG Domain ID
	if [ -z "$ETHG_DOMAIN_ID" ]
	then
		  DOMAIN_ID=0
	else
		  DOMAIN_ID=$ETHG_DOMAIN_ID
	fi
fi

if [ -z "$3" ]
then
      PY_VER=2
else
      PY_VER=$3
fi

usageDetectionScript=$1

if [[ $TECH_VER == 0 ]]; then
	ethg_usage_command="$usageDetectionScript $PY_VER  | grep $USER| grep $DOMAIN_ID"
	echo "$ethg_usage_command"	
else
	ethg_usage_command="$usageDetectionScript  | grep $USER| grep $DOMAIN_ID"
	echo "$ethg_usage_command"
fi



InstancesNo=0
#Wait for both GUI and DUT to be launched
while [ $InstancesNo -lt 2 ]
do
	#InstancesNo=`/home/rsalah/scratch/solution_usage/vefusage.sh| grep $USER| grep $DOMAIN_ID| wc -l`
	InstancesNo=`eval $ethg_usage_command | wc -l`
	sleep $sleepTime
done

echo `eval $ethg_usage_command`

re='^[0-9]+$'
python_id=$PPID
parentpid_list=`eval ps -o ppid=$python_id -C controller.bin`
echo $parentpid_list
echo "${parentpid_list[*]}"

pids=()
#Extract PIDs by greping all digits with execluding 0->9
for procInfo in `eval $ethg_usage_command`
do
	if  [[ $procInfo =~ $re ]]
	then
		if  [[ $(expr length $procInfo) -gt 1 ]]
		then
			pids+=( $procInfo )
		fi
	fi
done

echo "${pids[*]}"


#argument 
tstLoggingDirectory=$2
if [[ $tstLoggingDirectory = "" ]]; then
	tstLoggingDirectory=$(pwd)
fi
cd $tstLoggingDirectory || return
#$(printenv TST_CASE_LOGGING_DIRECTORY)

#$STAMP_REG_PATH/Ethernet/SW/Shell/regression-launch/is-alive.sh ${pids[*]}& 
/home/hwalied/Project/pysqlite3_helper/is-alive.sh ${pids[*]}& 
