# chronicler

chronicle = A historical account of facts or events disposed in the order of time; a history; especially, a bare or simple record of occurrences in their order of time. 

I want to adopt structured logs inspired by Ambient installation, which uses Rust language.

```
16:09:56 INFO ambient::cli::package::new: Ambient version: 0.3.1 
16:09:56 INFO ambient::cli::package::new: Package "my_project" created; doing first build 
16:09:56 INFO build_package: ambient_build: Building package "my_project" (nlod4jbaixcidrnr5fikliogocnz237x) name="my_project" 
16:09:56 INFO build_package: ambient_build: Assets built, building source code... name="my_project" above, those are really clean logs. They have a timestamp, a log level, some kind of reference to a code set, and text. i like the format and want to use it for my python code. is there a name for this format or convention?
```

Why? Each log message is consistent and includes timestamps, log levels, and other relevant data. Logs are easy to read and parse by both humans and machines.

current output:
```zsh
➜  chronicler git:(main) ✗ /bin/python3.11 /home/garth/develop/chronicler/chronicler.py
20240128_062518 INFO [chronicler.py:21 - log_system_info()]: ✧------------------------ meta info ------------------------✧
20240128_062518 INFO [chronicler.py:22 - log_system_info()]: whoami:     jomamma
20240128_062518 INFO [chronicler.py:23 - log_system_info()]: py ver:     3.11.5
20240128_062518 INFO [chronicler.py:24 - log_system_info()]: file:       /home/jomomma/develop/chronicler/chronicler.py
20240128_062518 INFO [chronicler.py:25 - log_system_info()]: os:         Linux
20240128_062518 INFO [chronicler.py:30 - log_system_info()]: git branch: main
20240128_062518 INFO [chronicler.py:35 - log_system_info()]: git hash:   cb2c189f86e3808c01bc0e91051f70a439a3e26c
20240128_062518 INFO [chronicler.py:39 - log_system_info()]: ✧-----------------------------------------------------------✧
20240128_062518 INFO [chronicler.py:42 - hello_world()]: Hello, world!
20240128_062518 INFO [chronicler.py:45 - my_function()]: This is an info message
20240128_062518 INFO [chronicler.py:50 - log_total_runtime()]: Total runtime: 0.00 seconds
```