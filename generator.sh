#!/bin/bash

printHelp () {
  echo "usage: $0 [-h] [-w NumberFrom0-100] [-b]

  -h  help: print this help and exit.
  -w  tristate weight percentage as an interger: If unset, will default to 33. This is the percentage chance that a flag that can roll tristate will roll tristate. So, if you set this to 67, then it will be a 67% chance that a tristate flag will roll as unknown, and a 16.5% chance that it will roll either yes or no each.
  -b  bistate only: Will disable the tristate option entirely. This *should* override the -w flag."

  exit 0
}

while getopts "w:hb" opt ; do
  case ${opt} in
    h)
      # Print the help.
      printHelp
      ;;
    w)
      # Tristate Weighting
      TQW=$OPTARG
      declare -i TQW
      nve='^[0-9]+$'
      if ! [[ $TQW =~ $nve ]] ; then
        echo "Error: Invalid entry for -w flag. Please use a whole, postive number." >&2 ; exit 1
      fi
      if [[ $TQW -gt 100 ]] ; then
        echo "Error: Please enter a number between 0 and 100." >&2 ; exit 1
      fi
      ;;
    b)
      # Disable Tristate
      TDI=1
      ;;
    *)
      #Anything else. print help and exit.
      printHelp
      ;;
  esac
done


HEADER=$(head -n40 default.json)
LIST=$(tail -n329 default.json | head -n-2 | cut -d":" -f1)
x=41
BODY=""


bistate () {
  local TFNV=$(shuf -i 1-2 -n 1)
  if [ "$TFNV" = "1" ] ; then
    echo "true"
  else
    echo "false"
  fi
}

if [ "$TDI" = "1" ] ; then
  tristate () {
    bistate
  }
else
  if [ -z ${TQW+x} ] ; then
    TQW=33
  fi
  PNP=$(echo "scale=0; 100-$TQW" | bc)
  POSP=$(echo "scale=0; $PNP/2" | bc)
  declare -i PNP
  declare -i POSP
  tristate () {
    local TFNV=$(shuf -i 1-100 -n 1)
    declare -i TFNV
    if [[ $TFNV -gt $PNP ]] ; then
      echo "null"
    elif [[ $TFNV -lt $POSP ]] ; then
      echo "false"
    else
      echo "true"
    fi
  }
fi

nrange () {
  echo "$(shuf -i $1-$2 -n 1)"
}

for i in $LIST ; do
  VAL=""
  case $x in
    43 | 46 | 64 | 96 | 15[0-1] | 157 | 158 | 163 | 176 | 195 | 20[3-6] | 20[8-9] | 210 | 301 | 30[4-7] | 310 | 317 | 353 | 364)
      VAL="$(bistate)"
      ;;
    44)
      if [ "$val43" = "true" ] ; then
        VAL="$(nrange 0 8)"
      else
        VAL="0"
      fi
      ;;
    45)
      VAL="$(nrange 0 5)"
      ;;
    54)
      if [ "$val53" = "true" ] ; then
        VAL="$(tristate)"
      else
        VAL="$false"
      fi
      ;;
    56 | 6[0-1] )
      if [ "$val55" = "true" ] ; then
        VAL="$(tristate)"
      else
        VAL="false"
      fi
      ;;
    65 | 231 | 335 | 36[2-3] )
      VAL="$(nrange 0 4)"
      ;;
    62)
      VAL="$(nrange 0 8)"
      ;;
    73)
      if [ "$val43" = "true" ] ; then
        VAL="$(tristate)"
      else
        VAL="false"
      fi
      ;;
    76 | 79 | 83)
      if [ "$val75" = "true" ] ; then
        VAL="$(tristate)"
      else
        VAL="false"
      fi
      ;;
    85 | 134 | 13[6-7] | 361)
      VAL="$(nrange 0 3)"
      ;;
    87 | 360)
      VAL="$(nrange 0 2)"
      ;;
    97 | 167 | 182 | 19[6-9] | 20[0-2] | 29[4-5] | 29[8-9] | 300 | 30[2-3] | 309 | 316 | 322 | 33[3-4] | 350 | 337)
      VAL="false"
      ;;
    11[2-9] | 16[8-9] | 17[0-5] | 17[7-9] | 18[0-1] | 18[5-9] | 19[0-4] | 315 | 164 )
      VAL="true"
      ;;
    102 | 105 | 110 )
      if [ "$val100" = "true" ] ; then
        VAL="$(tristate)"
      else
        VAL="false"
      fi
      ;;
    103 | 104 | 111 )
      if [ "$val101" = "true" ] ; then
        VAL="$(tristate)"
      else
        VAL="false"
      fi
      ;;
    106 | 164 | 168 | 169 )
      if [ "$val98" = "true" ] ; then
        VAL="$(tristate)"
      else
        VAL="false"
      fi
      ;;
    13[0-3] | 135 | 13[8-9] )
      VAL="$(nrange 0 1)"
      ;;
    183 )
      VAL="$(nrange 0 50)"
      ;;
    184 | 207)
      VAL="$(nrange 0 7)"
      ;;
    211)
      if [ "$val210" = "true" ] ; then
        VAL="$(nrange 0 12)"
      else
        VAL=0
      fi
      ;;
    212 | 214 )
      if [ "$val210" = "true" ] ; then
        VAL="$(tristate)"
      else
        VAL="false"
      fi
      ;;
    213)
      if [ "$val209" = "true" ] ; then
        VAL="$(tristate)"
      else
        VAL="false"
      fi
      ;;
    215 | 217 | 219 | 221 | 223)
      VAL="$(nrange 25 100)"
      ;;
    216 | 218 | 220 | 222 | 224)
      VAL="$(nrange 100 500)"
      ;;
    225)
      VALp="$(nrange 10 50)"
      VAL=$(echo "scale=1; $VALp/10" | bc)
      VALp=""
      ;;
    226)
      VAL="$(nrange 0 500)"
      ;;
    22[7-8])
      VAL="$(nrange 0 45)"
      ;;
    229)
      VAL="$(nrange 0 11)"
      ;;
    230)
      VAL="$(nrange 0 9)"
      ;;
    28[8-9] | 29[0-3] | 29[6-7])
      if [ "$val287" = "true" ] ; then
        VAL="$(tristate)"
      else
        VAL="false"
      fi
      ;;
    308)
      if [ "$val307" = "true" ] ; then
        VAL="$(bistate)"
      else
        VAL="false"
      fi
      ;;
    312)
      if [ "$val311" = "true" ] ; then
        VAL="$(tristate)"
      else
        VAL="false"
      fi
      ;;
    314)
      if [ "$val313" = "true" ] ; then
        VAL="$(tristate)"
      else
        VAL="false"
      fi
      ;;
    321)
      if [ "$val319" = "true" ] || [ "$val320" = "true" ] ; then
        VAL="$(tristate)"
      else
        VAL="false"
      fi
      ;;
    326 | 328 )
      VALp="$(nrange 0 9)"
      VAL=$(echo "$VALp*-1" | bc)
      VALp=""
      ;;
    327 | 329 )
      VAL="$(nrange 0 9)"
      ;;
    330)
      if [ "$val57" = "true" ] ; then
        VAL="$(tristate)"
      else
        VAL="false"
      fi
      ;;
    339 | 340)
      if [ "$val338" = "true" ] ; then
        VAL="$(tristate)"
      else
        VAL="false"
      fi
      ;;
    34[2-3])
      if [ "$val340" = "true" ] ; then
        VAL="$(tristate)"
      else
        VAL="false"
      fi
      ;;
    35[1-2])
      if [ "$val341" = "true" ] ; then
        VAL="$(nrange 0 4)"
      else
        VAL=0
      fi
      ;;
    35[4-6])
      VAL="$(nrange 6 9)"
      ;;
    35[7-8])
      VAL="$(nrange 2 6)"
      ;;
    359)
      VAL=3
      ;;
    367)
      if [ "$val81" = "true" ] ; then
        VAL="$(tristate)"
      else
        VAL="false"
      fi
      ;;
    *)
      VAL="$(tristate)"
      ;;
  esac

  valname="val$x"
  export $valname="$VAL"
  if [ "$x" = "41" ] ; then
    BODY="
  $i: $VAL"
  else
    BODY="$BODY,
  $i: $VAL"
  fi
  x=$(expr $x + 1)
done
TSTAMP=$(date +%Y%m%d%H%M%S)
echo "$HEADER $BODY
  }
}
" >> $TSTAMP-random.json
