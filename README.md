# ha_verkeerscentrum

> Home Assistant integration to get live verkeerscentrum BE data


Example config:
```yaml
sensor:
  - platform: verkeerscentrum
    rss:
      refresh_interval: 60
      individual_signs:
         - unique_id: "RSS_AV;A0140001S09;44380"
           name: "RSS To Gent: Sign 1"
         - unique_id: "RSS_AV;A0140001R10;44380"
           name: "RSS To Gent: Sign 2"
         - unique_id: "RSS_AV;A0140001R11;44380"
           name: "RSS To Gent: Sign 3"
         - unique_id: "RSS_AV;A0140001R12;44380"
           name: "RSS To Gent: Sign 4"
         - unique_id: "RSS_AV;A0140001R12;44380"
```
Or using the `site_name` Similar to
```yaml
sensor:
  - platform: verkeerscentrum
    rss:
      refresh_interval: 60
      signs:
         - site_name: "P01"
           name: "RSS To Gent"
```

## RSS Signs
> "rijstrooksignalisatie" signs

`rss:`
| | |
|--|--|
| refresh_interval  | refresh interval in seconds, default 3*60 |
| signs  | list of signs to include |

`signs:`
| | |
|--|--|
| site_name*  | RSS name displayed on the verkeerscentrum.be website, `RSS-` ommitted. E.g: `N14`. _When using this option, all individual signs will be added as sensor. The name will be appended with `{Sign, Pre-sign, Post-sign} {number}`._ |
| name*  | name of the sign. |

`individual_signs:`
| | |
|--|--|
| site_name*  | RSS name displayed on the verkeerscentrum.be website, `RSS-` ommitted. E.g: `N14`. _When using this option, all individual signs will be added as sensor. The name will be appended with `{Sign, Pre-sign, Post-sign} {number}`._ |
| name*  | name of the sign. |

`*` required
