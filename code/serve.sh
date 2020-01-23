#!/bin/bash
printf ‘HTTP/1.1 200 OK\n\n%s’ “$(cat index.html)” | netcat -l -k -v 80
# EOF
