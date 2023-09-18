# test_CardIndex

## test_suites

- Normal
- Exception
- Edge

## Suite

### Normal Suite

- group:
  - unit: 個別のハンド指定: 1326通り.
    - `2c2d`: 0
    - `2c2h`: 1
    - `2c2s`: 2
    - `2c3c`: 3

  - pocket: ポケットペアで指定. 13通り.
    - `22`: [0, 1, 2, 51, 52, 101]
    - `33`: [198, 199, 200, 245, 246, 291]
    - `44`: [380, 381, 382, 423, 424, 465]
    - `55`: [546, 547, 548, 585, 586, 623]
    - `66`: [696, 697, 698, 731, 732, 765]
    - `77`: [830, 831, 832, 861, 862, 891]
    - `88`: [948, 949, 950, 975, 976, 1001]
    - `99`: [1050, 1051, 1052, 1073, 1074, 1095]
    - `TT`: [1136, 1137, 1138, 1155, 1156, 1173]
    - `JJ`: [1206, 1207, 1208, 1221, 1222, 1235]
    - `QQ`: [1260, 1261, 1262, 1271, 1272, 1281]
    - `KK`: [1298, 1299, 1300, 1305, 1306, 1311]
    - `AA`: [1320, 1321, 1322, 1323, 1324, 1325]

  - pocket & specific suit: `club`と`dia`の場合
    - `2c2d`: [0]

  - suited: スーテッドで指定. 13*12通り.
    - `AKs`: [1301, 1308, 1314, 1319]
    - `KQs`: ...
    - `QJs`: ...

  - off-suited: オフスートで指定. 13*12通り.
    - `AKo`: ...