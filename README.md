# OpenVPN3 manage scripts

Simple scripts for:
1. Import configs
2. Configure service
3. Start connection with:
   - Automatic OTP processing
   - Monitoring VPN resource accessibility
   - Restart in case of log eror or VPN stuck

## Requirements

1. OpenVPN3 as main VPN tool
2. For the password storage [pass](https://www.passwordstore.org/) used. So you need setup your PGP keys before
3. [oathtool](https://www.nongnu.org/oath-toolkit/oathtool.1.html) used to obtain OTP password and do not ask it form external device
4. Commands `curl` and `ping` needed for monitoring purpose

## How to start

1. Import your config.ovpn by [CONFIGS/import]() script
2. Provide it name into [_config]() file
3. Start script [start.auto.service](). And enjoy!