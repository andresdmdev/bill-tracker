# Steps to zip
## 1 - In zip folder run: pip install --target ./package {Dependencies}
### Ejem. pip install --target ./package google-api-python-client google-auth python-telegram-bot openai supabase python-dotenv

## 2 - In package folder run: sudo zip -r9 ../function.zip .

## 3 - In zip folder run: sudo zip -g ./function.zip ../{files and folder of your proyect} ..
### Ejem. sudo zip -g ./function.zip ../lambda_function.py ../utils/utils.py ../services/handlers.py ../services/photo_service.py ../repository/bill_tracker_repository.py  ../models/bill.py

## 4 - Upload zip file in Amazon S3 Bucket
### After autenticated
### Ejem. aws s3 cp function.zip s3://[Bucker Name]/


Last update: 08/03/2025

Package                  Version
------------------------ -----------
aiohappyeyeballs         2.4.6
aiohttp                  3.11.13
aiosignal                1.3.2
annotated-types          0.7.0
anyio                    4.8.0
attrs                    25.1.0
cachetools               5.5.2
certifi                  2025.1.31
charset-normalizer       3.4.1
deprecation              2.1.0
distro                   1.9.0
frozenlist               1.5.0
google-api-core          2.24.1
google-api-python-client 2.162.0
google-auth              2.38.0
google-auth-httplib2     0.2.0
googleapis-common-protos 1.68.0
gotrue                   2.11.4
h11                      0.14.0
h2                       4.2.0
hpack                    4.1.0
httpcore                 1.0.7
httplib2                 0.22.0
httpx                    0.28.1
hyperframe               6.1.0
idna                     3.10
iniconfig                2.0.0
jiter                    0.8.2
multidict                6.1.0
openai                   1.65.3
packaging                24.2
pillow                   11.1.0
pip                      24.2
pluggy                   1.5.0
postgrest                0.19.3
propcache                0.3.0
proto-plus               1.26.0
protobuf                 5.29.3
pyasn1                   0.6.1
pyasn1_modules           0.4.1
pydantic                 2.10.6
pydantic_core            2.27.2
pyparsing                3.2.1
pytest                   8.3.4
pytest-asyncio           0.25.3
pytest-mock              3.14.0
python-dateutil          2.9.0.post0
python-dotenv            1.0.1
python-telegram-bot      21.10
realtime                 2.4.1
requests                 2.32.3
rsa                      4.9
six                      1.17.0
sniffio                  1.3.1
storage3                 0.11.3
StrEnum                  0.4.15
supabase                 2.13.0
supafunc                 0.9.3
tqdm                     4.67.1
typing_extensions        4.12.2
uritemplate              4.1.1
urllib3                  2.3.0
websockets               14.2
yarl                     1.18.3


## BUCKET IN AMAZON S3 CONFIGURATION

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowRootAccess",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::[AWS ACCOUNT]:root"
            },
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::[Bucker Name]",
                "arn:aws:s3:::[Bucker Name]/*"
            ]
        },
        {
            "Sid": "AllowSpecificUserOrRole",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::[AWS ACCOUNT]:user/[USER NAME]"
            },
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::[Bucker Name]"
        },
        {
            "Sid": "AllowSpecificUserOrRoleObjects",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::[AWS ACCOUNT]:user/[USER NAME]"
            },
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Resource": "arn:aws:s3:::[Bucker Name]/*"
        },
        {
            "Sid": "DenyEveryoneElse",
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::[Bucker Name]",
                "arn:aws:s3:::[Bucker Name]/*"
            ],
            "Condition": {
                "StringNotLike": {
                    "aws:PrincipalArn": [
                        "arn:aws:iam::[AWS ACCOUNT]:root",
                        "arn:aws:iam::[AWS ACCOUNT]:user/[USER NAME]"
                    ]
                }
            }
        }
    ]
}