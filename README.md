# My custom geo data for Xray

This repository provides:
- `geosite.dat` with custom categories: `ru-all`, `torrent`, `ads`
- `geoip.dat` with `ru` category (from runetfreedom)

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