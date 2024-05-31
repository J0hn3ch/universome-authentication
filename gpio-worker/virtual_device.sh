while
   # timeout 5 seconds
   ! timeout 5 sh -c '
     # read one line
     if IFS= read -r line; then
        # output the line
        printf "%s\n" "$line"
        # discard the input for the rest of 5 seconds
        cat >/dev/null
     fi
     # will get here only, if there is nothing to read
   '
   # that means that `timeout` will always return 124 if stdin is still open
   # and it will return 0 exit status only if there is nothing to read
   # so we loop on nonzero exit status of timeout.
do :; done