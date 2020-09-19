#!/usr/bin/env bash
# script to run test cases
#

# test-1
../cleanup 2> /dev/null
../jobsubmit |grep "For bug"  > /dev/null && touch test1.done
# test-2
../jobsubmit --help|grep "For bug"  > /dev/null && touch test2.done
# test-3
../jobsubmit -h|grep "For bug"  > /dev/null && touch test3.done
# test-4
../jobsubmit -v|grep "MERCHANTABILITY or FITNESS"  > /dev/null && touch test4.done
# test-5
../jobsubmit --version|grep "MERCHANTABILITY or FITNESS"  > /dev/null && touch test5.done
# test-6
mkdir -p done notdone stdout stderr
../jobsubmit --cleanup
if [ ! -d stdout ]; then
  touch test6.done
fi
# test-7
touch test.log
mkdir -p done notdone stdout stderr
../jobsubmit --fullcleanup
if [ ! -d test.log ]; then
  touch test7.done
fi
# test-8
../jobsubmit ./cmd.lst|grep "For bug"  > /dev/null && touch test8.done
# test-9
../jobsubmit ./cmd.lst 3
if [ $(cat stdout/cmd.lst_line_3.out|xargs) == $(whoami) ];
then
  touch test9.done
fi
# test-10
../jobsubmit ./cmd.lst 399|grep "Fatal Error: num > max_line in file" > /dev/null && touch test10.done
# test-11
../jobsubmit ./cmd.lst 4,3
if [ $(cat stdout/cmd.lst_line_3.out|xargs) == $(whoami) ];
then
  touch test11.done
fi
# test-12
if [ $(cat stdout/cmd.lst_line_4.out|xargs) == $(uname) ];
then
  touch test12.done
fi
# test-13
../jobsubmit ./cmd.lst 1-4
if [ $(cat stdout/cmd.lst_line_3.out|xargs) == $(whoami) ];
then
  touch test13.done
fi
# test-14
if [ $(cat stdout/cmd.lst_line_4.out|xargs) == $(uname) ];
then
  touch test14.done
fi
# test-15
../jobsubmit ./cmd.lst 1-45 |grep "Fatal Error: end_line > max_line in file" > /dev/null && touch test15.done
# test-16
../jobsubmit ./cmd.lst 4-1 |grep "Fatal Error: start_line > end_line" > /dev/null && touch test16.done


rm -rf *log stdout stderr notdone done
