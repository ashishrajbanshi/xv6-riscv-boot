# Local Matrix Track

- created_at_utc: `2026-04-26T20:47:47Z`
- runs_per_measurement: `5`
- memories: `['32M', '64M', '128M']`
- include_http: `True`

## local-trigger-32M
- started_utc: 2026-04-26T20:47:47Z
- cwd: `/mnt/c/Work/CourseWork/Spring26/systemSoft/research/xv6/xv6-riscv-boot/serverless-trigger`
- command: `/usr/bin/python3 measure_boot.py --runs 5 --label matrix_local_32m`
- env: `{"XV6_BOOT_TIMEOUT_SEC": "5", "XV6_CPUS": "1", "XV6_MEMORY": "32M"}`

### stdout
```text
saved_json=experiments/results/local/20260426T204812Z_matrix_local_32m.json
saved_csv=experiments/results/local/20260426T204812Z_matrix_local_32m.csv
runs=5 successful_boots=0
trigger_time_ms mean=5057.947 min=2067.644 max=7929.863
run=1 status=200 trigger_ms=7929.863 kernel_ms=None return_code=0 timed_out=True boot_completed=False panic=False
run=2 status=200 trigger_ms=2067.644 kernel_ms=None return_code=0 timed_out=True boot_completed=False panic=False
run=3 status=200 trigger_ms=5188.535 kernel_ms=None return_code=0 timed_out=True boot_completed=False panic=False
run=4 status=200 trigger_ms=5048.895 kernel_ms=None return_code=0 timed_out=True boot_completed=False panic=False
run=5 status=200 trigger_ms=5054.795 kernel_ms=None return_code=0 timed_out=True boot_completed=False panic=False
```
### stderr
```text
```
- exit_code: `0`
- duration_ms: `25460.750`
- saved_outputs: `{"csv": "experiments/results/local/20260426T204812Z_matrix_local_32m.csv", "json": "experiments/results/local/20260426T204812Z_matrix_local_32m.json"}`

## start-http-server-32M
- started_utc: 2026-04-26T20:48:12Z
- env: `{"XV6_CPUS": "1", "XV6_MEMORY": "32M"}`

## http-noop-32M
- started_utc: 2026-04-26T20:48:13Z
- cwd: `/mnt/c/Work/CourseWork/Spring26/systemSoft/research/xv6/xv6-riscv-boot/serverless-trigger`
- command: `/usr/bin/python3 measure_http.py --url http://127.0.0.1:8080/noop --runs 5 --label matrix_noop_32m`
- env: `{"XV6_BOOT_TIMEOUT_SEC": "5", "XV6_CPUS": "1", "XV6_MEMORY": "32M"}`

### stdout
```text
saved_json=experiments/results/http/20260426T204813Z_matrix_noop_32m.json
saved_csv=experiments/results/http/20260426T204813Z_matrix_noop_32m.csv
roundtrip_ms mean=4.292 min=0.446 max=19.089
handler_execution_time_ms mean=0.000 min=0.000 max=0.000
```
### stderr
```text
```
- exit_code: `0`
- duration_ms: `176.882`
- saved_outputs: `{"csv": "experiments/results/http/20260426T204813Z_matrix_noop_32m.csv", "json": "experiments/results/http/20260426T204813Z_matrix_noop_32m.json"}`

## http-trigger-32M
- started_utc: 2026-04-26T20:48:13Z
- cwd: `/mnt/c/Work/CourseWork/Spring26/systemSoft/research/xv6/xv6-riscv-boot/serverless-trigger`
- command: `/usr/bin/python3 measure_http.py --url http://127.0.0.1:8080/trigger --runs 5 --label matrix_trigger_32m`
- env: `{"XV6_BOOT_TIMEOUT_SEC": "5", "XV6_CPUS": "1", "XV6_MEMORY": "32M"}`

### stdout
```text
saved_json=experiments/results/http/20260426T204839Z_matrix_trigger_32m.json
saved_csv=experiments/results/http/20260426T204839Z_matrix_trigger_32m.csv
roundtrip_ms mean=5087.590 min=5048.854 max=5116.076
handler_execution_time_ms mean=5082.405 min=5047.237 max=5114.679
```
### stderr
```text
```
- exit_code: `0`
- duration_ms: `25565.451`
- saved_outputs: `{"csv": "experiments/results/http/20260426T204839Z_matrix_trigger_32m.csv", "json": "experiments/results/http/20260426T204839Z_matrix_trigger_32m.json"}`

### server_output
```text
127.0.0.1 - - [26/Apr/2026 16:48:13] "GET /noop HTTP/1.1" 200 100
127.0.0.1 - - [26/Apr/2026 16:48:13] "GET /noop HTTP/1.1" 200 101
127.0.0.1 - - [26/Apr/2026 16:48:13] "GET /noop HTTP/1.1" 200 83
127.0.0.1 - - [26/Apr/2026 16:48:13] "GET /noop HTTP/1.1" 200 83
127.0.0.1 - - [26/Apr/2026 16:48:13] "GET /noop HTTP/1.1" 200 101
127.0.0.1 - - [26/Apr/2026 16:48:19] "GET /trigger HTTP/1.1" 200 1198
127.0.0.1 - - [26/Apr/2026 16:48:24] "GET /trigger HTTP/1.1" 200 1198
127.0.0.1 - - [26/Apr/2026 16:48:29] "GET /trigger HTTP/1.1" 200 1199
127.0.0.1 - - [26/Apr/2026 16:48:34] "GET /trigger HTTP/1.1" 200 1200
127.0.0.1 - - [26/Apr/2026 16:48:39] "GET /trigger HTTP/1.1" 200 1200
```

## local-trigger-64M
- started_utc: 2026-04-26T20:48:39Z
- cwd: `/mnt/c/Work/CourseWork/Spring26/systemSoft/research/xv6/xv6-riscv-boot/serverless-trigger`
- command: `/usr/bin/python3 measure_boot.py --runs 5 --label matrix_local_64m`
- env: `{"XV6_BOOT_TIMEOUT_SEC": "5", "XV6_CPUS": "1", "XV6_MEMORY": "64M"}`

### stdout
```text
saved_json=experiments/results/local/20260426T204840Z_matrix_local_64m.json
saved_csv=experiments/results/local/20260426T204840Z_matrix_local_64m.csv
runs=5 successful_boots=5
trigger_time_ms mean=275.284 min=264.371 max=289.773
kernel_boot_ms mean=102.293 min=99.762 max=105.602
run=1 status=200 trigger_ms=270.361 kernel_ms=100.3613 return_code=0 timed_out=False boot_completed=True panic=True
run=2 status=200 trigger_ms=264.371 kernel_ms=99.7621 return_code=0 timed_out=False boot_completed=True panic=True
run=3 status=200 trigger_ms=269.869 kernel_ms=100.6474 return_code=0 timed_out=False boot_completed=True panic=True
run=4 status=200 trigger_ms=289.773 kernel_ms=105.0917 return_code=0 timed_out=False boot_completed=True panic=True
run=5 status=200 trigger_ms=282.044 kernel_ms=105.60170000000001 return_code=0 timed_out=False boot_completed=True panic=True
```
### stderr
```text
```
- exit_code: `0`
- duration_ms: `1525.996`
- saved_outputs: `{"csv": "experiments/results/local/20260426T204840Z_matrix_local_64m.csv", "json": "experiments/results/local/20260426T204840Z_matrix_local_64m.json"}`

## start-http-server-64M
- started_utc: 2026-04-26T20:48:40Z
- env: `{"XV6_CPUS": "1", "XV6_MEMORY": "64M"}`

## http-noop-64M
- started_utc: 2026-04-26T20:48:42Z
- cwd: `/mnt/c/Work/CourseWork/Spring26/systemSoft/research/xv6/xv6-riscv-boot/serverless-trigger`
- command: `/usr/bin/python3 measure_http.py --url http://127.0.0.1:8080/noop --runs 5 --label matrix_noop_64m`
- env: `{"XV6_BOOT_TIMEOUT_SEC": "5", "XV6_CPUS": "1", "XV6_MEMORY": "64M"}`

### stdout
```text
saved_json=experiments/results/http/20260426T204842Z_matrix_noop_64m.json
saved_csv=experiments/results/http/20260426T204842Z_matrix_noop_64m.csv
roundtrip_ms mean=3.858 min=0.377 max=17.433
handler_execution_time_ms mean=0.000 min=0.000 max=0.000
```
### stderr
```text
```
- exit_code: `0`
- duration_ms: `119.049`
- saved_outputs: `{"csv": "experiments/results/http/20260426T204842Z_matrix_noop_64m.csv", "json": "experiments/results/http/20260426T204842Z_matrix_noop_64m.json"}`

## http-trigger-64M
- started_utc: 2026-04-26T20:48:42Z
- cwd: `/mnt/c/Work/CourseWork/Spring26/systemSoft/research/xv6/xv6-riscv-boot/serverless-trigger`
- command: `/usr/bin/python3 measure_http.py --url http://127.0.0.1:8080/trigger --runs 5 --label matrix_trigger_64m`
- env: `{"XV6_BOOT_TIMEOUT_SEC": "5", "XV6_CPUS": "1", "XV6_MEMORY": "64M"}`

### stdout
```text
saved_json=experiments/results/http/20260426T204843Z_matrix_trigger_64m.json
saved_csv=experiments/results/http/20260426T204843Z_matrix_trigger_64m.csv
roundtrip_ms mean=310.505 min=273.975 max=371.314
handler_execution_time_ms mean=305.587 min=272.338 max=370.029
kernel_boot_ms mean=117.605 min=104.800 max=135.815
```
### stderr
```text
```
- exit_code: `0`
- duration_ms: `1673.435`
- saved_outputs: `{"csv": "experiments/results/http/20260426T204843Z_matrix_trigger_64m.csv", "json": "experiments/results/http/20260426T204843Z_matrix_trigger_64m.json"}`

### server_output
```text
127.0.0.1 - - [26/Apr/2026 16:48:42] "GET /noop HTTP/1.1" 200 101
127.0.0.1 - - [26/Apr/2026 16:48:42] "GET /noop HTTP/1.1" 200 101
127.0.0.1 - - [26/Apr/2026 16:48:42] "GET /noop HTTP/1.1" 200 83
127.0.0.1 - - [26/Apr/2026 16:48:42] "GET /noop HTTP/1.1" 200 83
127.0.0.1 - - [26/Apr/2026 16:48:42] "GET /noop HTTP/1.1" 200 83
127.0.0.1 - - [26/Apr/2026 16:48:42] "GET /trigger HTTP/1.1" 200 1651
127.0.0.1 - - [26/Apr/2026 16:48:42] "GET /trigger HTTP/1.1" 200 1662
127.0.0.1 - - [26/Apr/2026 16:48:43] "GET /trigger HTTP/1.1" 200 1683
127.0.0.1 - - [26/Apr/2026 16:48:43] "GET /trigger HTTP/1.1" 200 1652
127.0.0.1 - - [26/Apr/2026 16:48:43] "GET /trigger HTTP/1.1" 200 1707
```

## local-trigger-128M
- started_utc: 2026-04-26T20:48:43Z
- cwd: `/mnt/c/Work/CourseWork/Spring26/systemSoft/research/xv6/xv6-riscv-boot/serverless-trigger`
- command: `/usr/bin/python3 measure_boot.py --runs 5 --label matrix_local_128m`
- env: `{"XV6_BOOT_TIMEOUT_SEC": "5", "XV6_CPUS": "1", "XV6_MEMORY": "128M"}`

### stdout
```text
saved_json=experiments/results/local/20260426T204845Z_matrix_local_128m.json
saved_csv=experiments/results/local/20260426T204845Z_matrix_local_128m.csv
runs=5 successful_boots=5
trigger_time_ms mean=282.126 min=276.931 max=285.193
kernel_boot_ms mean=105.516 min=104.489 max=106.888
run=1 status=200 trigger_ms=284.545 kernel_ms=104.9528 return_code=0 timed_out=False boot_completed=True panic=True
run=2 status=200 trigger_ms=281.254 kernel_ms=106.8882 return_code=0 timed_out=False boot_completed=True panic=True
run=3 status=200 trigger_ms=285.193 kernel_ms=104.708 return_code=0 timed_out=False boot_completed=True panic=True
run=4 status=200 trigger_ms=276.931 kernel_ms=104.4885 return_code=0 timed_out=False boot_completed=True panic=True
run=5 status=200 trigger_ms=282.707 kernel_ms=106.5448 return_code=0 timed_out=False boot_completed=True panic=True
```
### stderr
```text
```
- exit_code: `0`
- duration_ms: `1543.430`
- saved_outputs: `{"csv": "experiments/results/local/20260426T204845Z_matrix_local_128m.csv", "json": "experiments/results/local/20260426T204845Z_matrix_local_128m.json"}`

## start-http-server-128M
- started_utc: 2026-04-26T20:48:45Z
- env: `{"XV6_CPUS": "1", "XV6_MEMORY": "128M"}`

## http-noop-128M
- started_utc: 2026-04-26T20:48:46Z
- cwd: `/mnt/c/Work/CourseWork/Spring26/systemSoft/research/xv6/xv6-riscv-boot/serverless-trigger`
- command: `/usr/bin/python3 measure_http.py --url http://127.0.0.1:8080/noop --runs 5 --label matrix_noop_128m`
- env: `{"XV6_BOOT_TIMEOUT_SEC": "5", "XV6_CPUS": "1", "XV6_MEMORY": "128M"}`

### stdout
```text
saved_json=experiments/results/http/20260426T204846Z_matrix_noop_128m.json
saved_csv=experiments/results/http/20260426T204846Z_matrix_noop_128m.csv
roundtrip_ms mean=4.059 min=0.499 max=17.831
handler_execution_time_ms mean=0.000 min=0.000 max=0.000
```
### stderr
```text
```
- exit_code: `0`
- duration_ms: `121.525`
- saved_outputs: `{"csv": "experiments/results/http/20260426T204846Z_matrix_noop_128m.csv", "json": "experiments/results/http/20260426T204846Z_matrix_noop_128m.json"}`

## http-trigger-128M
- started_utc: 2026-04-26T20:48:46Z
- cwd: `/mnt/c/Work/CourseWork/Spring26/systemSoft/research/xv6/xv6-riscv-boot/serverless-trigger`
- command: `/usr/bin/python3 measure_http.py --url http://127.0.0.1:8080/trigger --runs 5 --label matrix_trigger_128m`
- env: `{"XV6_BOOT_TIMEOUT_SEC": "5", "XV6_CPUS": "1", "XV6_MEMORY": "128M"}`

### stdout
```text
saved_json=experiments/results/http/20260426T204848Z_matrix_trigger_128m.json
saved_csv=experiments/results/http/20260426T204848Z_matrix_trigger_128m.csv
roundtrip_ms mean=298.194 min=282.509 max=347.687
handler_execution_time_ms mean=293.285 min=281.163 max=329.003
kernel_boot_ms mean=112.695 min=105.072 max=139.160
```
### stderr
```text
```
- exit_code: `0`
- duration_ms: `1611.255`
- saved_outputs: `{"csv": "experiments/results/http/20260426T204848Z_matrix_trigger_128m.csv", "json": "experiments/results/http/20260426T204848Z_matrix_trigger_128m.json"}`

### server_output
```text
127.0.0.1 - - [26/Apr/2026 16:48:46] "GET /noop HTTP/1.1" 200 100
127.0.0.1 - - [26/Apr/2026 16:48:46] "GET /noop HTTP/1.1" 200 101
127.0.0.1 - - [26/Apr/2026 16:48:46] "GET /noop HTTP/1.1" 200 101
127.0.0.1 - - [26/Apr/2026 16:48:46] "GET /noop HTTP/1.1" 200 101
127.0.0.1 - - [26/Apr/2026 16:48:46] "GET /noop HTTP/1.1" 200 83
127.0.0.1 - - [26/Apr/2026 16:48:47] "GET /trigger HTTP/1.1" 200 1679
127.0.0.1 - - [26/Apr/2026 16:48:47] "GET /trigger HTTP/1.1" 200 1671
127.0.0.1 - - [26/Apr/2026 16:48:47] "GET /trigger HTTP/1.1" 200 1666
127.0.0.1 - - [26/Apr/2026 16:48:47] "GET /trigger HTTP/1.1" 200 1665
127.0.0.1 - - [26/Apr/2026 16:48:48] "GET /trigger HTTP/1.1" 200 1685
```
