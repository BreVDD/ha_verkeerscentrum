# ha_verkeerscentrum

> Home Assistant integration to get live verkeerscentrum BE data

Version 0.0.1 adds support for RSS signs.
Example config:
```yaml

sensor:
  - platform: verkeerscentrum
    rss:
      refresh_interval: 60
      signs:
         - unique_id: "RSS_AV;A0140001S09;44380"
           name: "RSS 1 > Gent: Sign 1"
         - unique_id: "RSS_AV;A0140001R10;44380"
           name: "RSS 1 > Gent: Sign 2"
         - unique_id: "RSS_AV;A0140001R11;44380"
           name: "RSS 1 > Gent: Sign 3"
         - unique_id: "RSS_AV;A0140001R12;44380"
           name: "RSS 1 > Gent: Sign 4"

```

