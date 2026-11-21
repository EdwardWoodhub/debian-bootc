if [ "$(id -un)" = "live" ] && [ "$(tty)" = "/dev/tty1" ]; then
    export WLR_RENDERER=pixman
    export LIBGL_ALWAYS_SOFTWARE=1
    export WLR_NO_HARDWARE_CURSORS=1
    exec cage -- bootc-installer
fi
