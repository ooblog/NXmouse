# capslockでのマウスカーソル移動「capsmouse」。

capslockキーでマウスカーソルの移動(押し続けると加速)、押す度に方向転換。  
無変換(nfer)キーで左クリック、かな(kana)キーで中クリック、変換(xfer)キーを押した時に右クリック。  
設定変更は「capsmouse.tsv」を編集。  


## 挙動について。
キーロックの類は一切してないのでマウス操作のつもりが文字入力される場合があることに注意。  
マウスカーソルの座標移動はマウスジェスチャー関連で認知されない場合があるので注意。  


## 動作環境。

「Tahrpup6.0.5,Python2.7.6」+「L:Tsv20170119R141608」で開発。  
別途「xdotool」が必要だったりGTKのNotifyに常駐するのでLinux限定(そもそもcapslockキーの取得がWindowsでは無理)。  


## ライセンス・著作権など。
Copyright (c) 2017 ooblog  
License: MIT  
[https://github.com/ooblog/capsmouse/blob/master/LICENSE](LICENSE "https://github.com/ooblog/capsmouse/blob/master/LICENSE")  
