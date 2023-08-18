# Script to manage bot process
BOT_DIR="/root/vdjk"
BOT_CMD="(cd $BOT_DIR && source $BOT_DIR/.venv/bin/activate && python3.10 -m app)"

BOT_PID_FILE="$BOT_DIR/bot.pid"
BOT_LOG_FILE="$BOT_DIR/bot.log"

case "$1" in
start)
    echo "Starting bot process..."
    nohup bash -c "$BOT_CMD" >>$BOT_LOG_FILE 2>&1 &
    echo $! >$BOT_PID_FILE
    ;;
stop)
    if [ -f $BOT_PID_FILE ]; then
        rm $BOT_PID_FILE
    fi
    pkill -9 -f "pyngrok"
    pkill -9 -f "python3.10 -m app"
    ;;
restart)
    $0 stop
    sleep 2
    $0 start
    ;;
status)
    if [ -f $BOT_PID_FILE ]; then
        echo "Bot.sh main process is running (PID $(cat $BOT_PID_FILE))."
    else
        echo "Bot.sh main process is not running."
    fi
    echo "Related bot processes:"
    pgrep -f "python3.10 -m app"
    ## echo pyngrok runs at process:
    echo "pyngrok:" $(pgrep -f "pyngrok")
    ## ngrok public url of current tunnels:
    echo "Public Ngrok URL:" $(curl -s localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')

    ;;
log)
    less $BOT_DIR/bot.log
    ;;
*)
    echo "Usage: $0 {start|stop|restart|status|log}"
    exit 1
    ;;
esac

exit 0
