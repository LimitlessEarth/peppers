#!/bin/bash

HOME_DIR=/home/pi/Peppers/webcam
IMG_DIR=${HOME_DIR}/images

if [ ! -d $IMG_DIR ]; then
	mkdir -p $IMG_DIR
fi

etime=$(date +%s)

RAW_FILE="$IMG_DIR/${etime}_raw.jpg"
TXT_FILE="$IMG_DIR/${etime}_text.jpg"
APPEND_LIST_FILE="$IMG_DIR/append.txt"
VID_FILE="$IMG_DIR/lapse_out.mp4"
NEW_VID_FILE="$IMG_DIR/lapse_new_out.mp4"
PUB_VID_FILE="$IMG_DIR/lapse.mp4"
NEW_FILE="$IMG_DIR/latest.jpg"
SEG_NUM_FILE="$IMG_DIR/seg_num.txt"

rm $TXT_FILE >/dev/null 2>&1

echo -n "Capturing ..."
while [ ! -f $TXT_FILE ]
do
    raspistill -h 2464 -w 3280 -o $RAW_FILE -awb greyworld >/dev/null 2>&1
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

            echo "Deleting raw image"
            rm $RAW_FILE >/dev/null 2>&1

            if [[ ! -f $APPEND_LIST_FILE ]]; then
                echo "file $VID_FILE" > $APPEND_LIST_FILE
                echo "file $NEW_VID_FILE" >> $APPEND_LIST_FILE
            fi

            image_count=$(ls $IMG_DIR/*_text.jpg | wc -l)
            if [ "$image_count" -ge "30" ];then
                echo "Generating, Appending Animation"
                /usr/local/bin/ffmpeg -y -pattern_type glob -i "$IMG_DIR/*_text.jpg" -c:v h264_omx -b:v 6M -pix_fmt yuv420p -vf scale=1920:1080 -movflags +faststart $NEW_VID_FILE
                mv $PUB_VID_FILE $VID_FILE
                /usr/local/bin/ffmpeg -f concat -safe 0 -i $APPEND_LIST_FILE -c copy $PUB_VID_FILE

                if [[ ! -f $TOGGLE_FILE ]]; then
                    echo "0" > $SEG_NUM_FILE
                fi

                seg_num=$(cat $SEG_NUM_FILE)
			    seg_num=$(($seg_num+1))
			    echo "$seg_num" > $SEG_NUM_FILE
		        
                mv $NEW_VID_FILE "$seg_num.mp4"
                rm $VID_FILE $IMG_DIR/*_text.jpg
            fi
        fi
    fi
done
