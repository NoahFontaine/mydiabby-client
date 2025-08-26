# Structure of the keys in the 'data' key of the output of `MyDiabbyClient.get_pump_data()`:

### 1. `closed_loop_mode`:

List of dict, where each dict contains the keys start, mode, end. Tells you when the pump changes mode (sleep, normal, or physicalActivity). The start of the next entry is either the end of the previous entry, or 1 second after.

Example:
```json
[
  {
    "start": "2022-03-24T16:59:54+01:00",
    "mode": "physicalActivity",
    "end": "2022-03-24T16:59:59+01:00"
  },
  {
    "start": "2022-03-24T16:59:59+01:00",
    "mode": "normal",
    "end": "2022-03-24T21:30:34+01:00"
  }
]
```

### 2. `cgm`.

List of dict, where each dict is a CGM reading with date and value. It always gives it in g/L.

Example:
```json
[
  {
    "value": "1.7100",
    "date": "2024-08-26T00:00:42+02:00"
  },
  {
    "value": "1.7000",
    "date": "2024-08-26T00:05:47+02:00"
  },
]
```
### 3. `snack`.

Nothing.

### 4. `study`.

Nothing.

### 5. `lighten`.

Nothing.

### 6. `listwaitdata`.

Nothing.

### 7. `insulinflow`.

Nothing.

### 8. `closed_loop`.

List of dict, where each dict contains the keys start, mode, end, device. Tells you when the closed loop is on or off (mode can only be on or off). There has to be at least 1 entry per day, even if the mode does not change.

Example:
```json
[
  {
    "start": "2022-03-25T02:02:07+01:00",
    "mode": "off",
    "end": "2022-03-25T11:20:14+01:00",
    "device": 229661
  },
  {
    "start": "2022-03-25T11:20:14+01:00",
    "mode": "on",
    "end": "2022-03-25T23:59:59+01:00",
    "device": 229661
  },
  {
    "start": "2022-03-26T00:00:00+01:00",
    "mode": "on",
    "end": "2022-03-26T23:59:59+01:00",
    "device": 229661
  },
]
```

### 9. `pumpevents`.

List of dict, where each dict is a event with date, event_type (alert, tube priming, alarm), and data. data gives more information about the event type. It is a dict with 1 key called KEY or PrimingAmount. It either gives the priming amount as a float in U if the event_type is tube priming, or something like low_power, low_insulin, reservoir_change, Control-IQ High, occlusion etc.

Example:
```json
[
  {
    "date": "2022-11-01T07:29:23+01:00",
    "event_type": "alarm",
    "data": {
      "KEY": "reservoir_change"
    }
  },
  {
    "date": "2022-11-01T07:29:23+01:00",
    "event_type": "tube priming",
    "data": {
      "PrimingAmount": 12.73125
    }
  },
  {
    "date": "2022-11-01T09:49:33+01:00",
    "event_type": "alarm",
    "data": {
      "KEY": "occlusion"
    }
  },
]
```

### 10. `glycemia`.

Quite messy data. Gives data whenever there is a bolus or automated correction. List of dict, but the dicts vary depending on the type of entry it is. Gives a lot of data about every injection. Meals are duplicated with carbs in one entry and insulin in another. Basal is always None, so seems to imply that this is about bolus only.

Example:
```json
[
  {
    "id": 639652356,
    "date": "2024-08-27",
    "time": "16:06",
    "pro": false,
    "insulin": {
      "bolus": "1.1052",
      "bolus_corr": null,
      "basal": null,
      "device": 229661,
      "datas": [
        {
          "id": 258365336,
          "type": "automated",
          "data": true
        }
      ]
    }
  },
  {
    "id": 639652357,
    "date": "2024-08-27",
    "time": "16:18",
    "pro": false,
    "insulin": {
      "bolus": "5.8300",
      "bolus_corr": null,
      "basal": null,
      "device": 229661,
      "datas": [
        {
          "id": 258365337,
          "type": "expected",
          "data": 5.83
        }
      ]
    }
  },
  {
    "id": 639652358,
    "date": "2024-08-27",
    "time": "16:18",
    "pro": false,
    "meal": {
      "list": null,
      "description": null,
      "carb": 35,
      "device": 229661
    }
  },
]
```

### 11. `insulinflow_device`.

Not sure, but contains data about basal rates. Every key is a date, and each value seems to another dict of keys date, flow, hour, list. date is the date again.

flow seems to be the total basal of the whole 24 hours. hour seems to be a list with each element the total basal that happened each hour. List is another dict with key as some id, and value is a list of dictionaries of each entry when the basal changes, and why.

Example of the `list` value of the `2025-08-24` entry:
```json
[
  {
    "start": "2025-08-24T20:01:16+02:00",
    "end": "2025-08-24T20:01:18+02:00",
    "rate": "0.4500",
    "temp": 0,
    "datas": []
  },
  {
    "start": "2025-08-24T20:01:18+02:00",
    "end": "2025-08-24T20:11:17+02:00",
    "rate": "0.0000",
    "temp": 0,
    "datas": [
                {
                  "type": "status",
                  "data": {
                            "suspended": {
                                          "reason": "automatic",
                                          "type": "Auto suspend by PLGS"
                                         }
                          }
                }
              ]
  },
    {
        "start": "2025-08-24T20:11:17+02:00",
        "end": "2025-08-24T22:51:17+02:00",
        "rate": "0.4500",
        "temp": 0,
        "datas": [
                  [
                    {
                      "type": "status",
                      "data": {"resumed": {
                                            "reason": "automatic"
                                          }
                              }
                    }
                  ]
                 ]
    }
]
```

### 12. `avgdata`.

Seems to be data about maunal fingerpricks but not sure. Doesn't seem to be actual average data.

### 13. `avgdata7`.

Seems to be data about maunal fingerpricks but not sure. Doesn't seem to be actual average 1 week data.

### 14.  `avgdata30`.

Seems to be data about maunal fingerpricks but not sure. Doesn't seem to be actual average 1 month data.
