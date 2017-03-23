# キーボードからのマウス操作補助「NXmouse」。

capslockキーでマウスカーソルの移動(押し続けると加速)、押す度に方向転換。  
無変換(nfer)キーで左クリック、かな(kana)キーで中クリック、変換(xfer)キーを押した時に右クリック。  
設定変更は「NXmouse.tsv」を編集。  


## 挙動について。
キーロックの類は一切してないのでマウス操作のつもりが文字入力される場合があることに注意。  
マウスカーソルの座標が変わるだけなので移動量や加速度を測定しているアプリではクリックしか聞かなくなるので注意。


## リポジトリ名とファイル名の違いについて。

元々「NXmouse」という名前で開発→気が付くとcapslockのマウス移動が本体になる→リポジトリ名も「capsmouse」に変更予定。  


## 動作環境。

「Tahrpup6.0.5,Python2.7.6」+「L:Tsv20170119R141608」で開発。  
別途「xdotool」が必要だったりGTKのNotifyに常駐するのでLinux限定(そもそもcapslockキーの取得がWindowsでは無理)。  


## ライセンス・著作権など。
Copyright (c) 2017 ooblog  
License: MIT  
[https://github.com/ooblog/NXmouse/blob/master/LICENSE](LICENSE "https://github.com/ooblog/NXmouse/blob/master/LICENSE")  
