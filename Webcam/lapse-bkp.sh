#!/bin/bash


HOME_DIR=/home/pi/webcam
IMG_DIR=${HOME_DIR}/images

if [ ! -d $IMG_DIR ]; then
	mkdir -p $IMG_DIR
fi

etime=$(date +%s)

RAW_FILE="$IMG_DIR/${etime}_raw.jpg"
TXT_FILE="$IMG_DIR/${etime}_text.jpg"
GIF_FILE="$IMG_DIR/lapse_out.gif"
PUB_FILE="$IMG_DIR/lapse.gif"
VID_FILE="$IMG_DIR/lapse_out.mp4"
PUB_VID_FILE="$IMG_DIR/lapse.mp4"
NEW_FILE="$IMG_DIR/latest.jpg"
TOGGLE_FILE=".toggle"

rm $TXT_FILE >/dev/null 2>&1

echo -n "Capturing ..."
while [ ! -f $TXT_FILE ]
do
  raspistill -h 1536 -w 2048 -o $RAW_FILE -awb greyworld >/dev/null 2>&1
  #fswebcam -r 2592x1944 --no-banner $RAW_FILE >/dev/null 2>&1

  if [[ -f $RAW_FILE ]]; then
    #echo
    #echo "Rotating"
    #mogrify -rotate 270 $RAW_FILE  >/dev/null 2>&1
    echo "Overlaying Text"
    dtime=$(date +"%D %H:%M:%S")

    source ${HOME_DIR}/measurements
    caption="$dtime
Humidity: ${HUMIDITY}%
Temp: ${TEMPERATURE}F
Soil Moisture: ${SOIL_MOISTURE}
Visible Light: ${VISIBLE_LIGHT}
Infrared Light: ${INFRARED}
UV Index: ${UV_INDEX}"

    convert -pointsize 40 -fill white -draw "text 30 50 '$caption' " $RAW_FILE $TXT_FILE  >/dev/null 2>&1

    if [[ ! -f $TXT_FILE ]]; then
      echo -n "."
      sleep 1
    else

     echo "Publishing Latest Image"
     cp $TXT_FILE $NEW_FILE.tmp
     mv $NEW_FILE.tmp $NEW_FILE

     echo "Deleted outdated images"
     find $IMG_DIR -mmin +10080 -type f -name "*.jpg"  -exec rm -f {} \;
     rm $RAW_FILE >/dev/null 2>&1


     if [[ -f $TOGGLE_FILE ]]; then
		c=$(cat $TOGGLE_FILE)
		if [[ "$c" < 5 ]]; then
			c=$(($c+1))
			echo "$c" > $TOGGLE_FILE
			exit 0
		fi
       rm $TOGGLE_FILE
       echo "Generating Animation"
       /usr/local/bin/ffmpeg -y -pattern_type glob -i "$IMG_DIR/*_text.jpg" -c:v h264_omx -b:v 8M -pix_fmt yuv420p -vf scale=1920:1080 -movflags +faststart $VID_FILE 
       mv $VID_FILE $PUB_VID_FILE
      else
        echo "0" > $TOGGLE_FILE
      fi
    fi
  fi
done
