# Performance Tracker

## requirements

```
python 3
sqlite3
subprocess
```

## How to Run

- configure the run regression in the [ input_configuration.json ] (input_configuration.json)  

  for ex:

  ```json
  {
    "application": "ethernet",
    "instances": [
      {
        "DUT": "SA",
        "key": "speed",
        "value": [
          "CGMII"
        ],
        "is_streaming": false
      }
    ],
    "python_version": 3,
    "tracker_path": "./track-memory-dut-gui.sh",
    "logging_dir": "./log2"
  }
  ```

* then run the main script

[main.py]: main.py	"main script"



