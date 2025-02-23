# Steps to zip
## 1 - In zip folder run: pip install --target ./package {Dependencies}
### Ejem. pip install ./package google-api-python-client google-auth python-telegram-bot

## 2 - In package folder run: sudo zip -r9 ../function.zip .

## 3 - In zip folder run: sudo zip -g ./function.zip ../{files and folder of your proyect} ..
### Ejem. sudo zip -g ./function.zip ../lambda_function.py ../services ../utils

Last update: 23/02/2025

Package                  Version
------------------------ ---------
anyio                    4.8.0
cachetools               5.5.2
certifi                  2025.1.31
charset-normalizer       3.4.1
google-api-core          2.24.1
google-api-python-client 2.161.0
google-auth              2.38.0
google-auth-httplib2     0.2.0
googleapis-common-protos 1.68.0
h11                      0.14.0
httpcore                 1.0.7
httplib2                 0.22.0
httpx                    0.28.1
idna                     3.10
iniconfig                2.0.0
packaging                24.2
pip                      24.2
pluggy                   1.5.0
proto-plus               1.26.0
protobuf                 5.29.3
pyasn1                   0.6.1
pyasn1_modules           0.4.1
pyparsing                3.2.1
pytest                   8.3.4
pytest-asyncio           0.25.3
pytest-mock              3.14.0
python-dotenv            1.0.1
python-telegram-bot      21.10
requests                 2.32.3
rsa                      4.9
sniffio                  1.3.1
typing_extensions        4.12.2
uritemplate              4.1.1
urllib3                  2.3.0