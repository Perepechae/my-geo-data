# My custom geo data for Xray

This repository provides:

- [geoip.dat](https://raw.githubusercontent.com/Perepechae/my-geo-data/release/geoip.dat) – IP-адреса РФ (категория `geoip:ru`)
- [geosite.dat](https://raw.githubusercontent.com/Perepechae/my-geo-data/release/geosite.dat) – домены РФ, реклама, торренты (категории `ru-all`, `ads`, `torrent`)

## Usage

Place both files in your Xray directory and add routing rules:

```json
{
  "routing": {
    "rules": [
      {"type": "field", "domain": ["geosite:ads"], "outboundTag": "block"},
      {"type": "field", "domain": ["geosite:torrent"], "outboundTag": "direct"},
      {"type": "field", "domain": ["geosite:ru-all"], "outboundTag": "direct"},
      {"type": "field", "ip": ["geoip:ru"], "outboundTag": "direct"}
    ]
  }
}
