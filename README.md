# キーボードからのマウス操作補助「NXmouse」。

capslockキーでマウスカーソルの移動(押し続けると加速)、押す度に方向転換。  
無変換(nfer)キーで左クリック、変換(xfer)キーを押した時に右クリック。  
kanaキーとASWZの組み合わせでもマウスカーソルの移動可能(等速)。  
設定変更は「NXmouse.tsv」を編集。  
キーロックの類は一切してないのでマウス操作のつもりが文字入力される場合があることに注意。  


## 動作環境。

「Tahrpup6.0.5,Python2.7.6」で開発。  
別途「xdotool」が必要だったりGTKのNotifyに常駐するのでLinux限定(CapsLockキーの取得がWindowsでは無理)。  


## ライセンス・著作権など。
11
Copyright (c) 2017 ooblog  
License: MIT  
[https://github.com/ooblog/NXmouse/blob/master/LICENSE](LICENSE "https://github.com/ooblog/NXmouse/blob/master/LICENSE")  
