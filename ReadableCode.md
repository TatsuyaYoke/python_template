# Readable Code

## 5. コメントすべきことを知る

### 5.1 コメントするべきでは「ない」こと

- コードからすぐにわかることをコメントしない

- コードを見ればわかるけど、コード理解するよりも、コメントを読んだ方が早くできるコメントをする

```py
# 2番目の'*'以降を全て削除
name = '*'.join(line.split('*')[:2])
```

- ひどい名前はコメントをつけずに名前を変える

```py
# NG
# Replyに対してRequestで記述した制限を課す
# 例えば、返ってくる項目数や合計バイト数など。
def clean_reply(request, reply)

# OK
def enforce_limits_from_request(request, reply)
```

### 5.2 自分の考えを記録する

- なぜコードが他のやり方ではなくこうなっているかを書く

```py
# ハッシュテーブルよりもバイナリツリーの方が40%速かった
# 左右の比較よりもハッシュの計算コストの方が高いようだ

# このクラスは汚くなってきている
# サブクラスをつくって整理した方が良いかもしれない
```

- コードの欠陥にコメントをつける

vscodeの拡張機能todo treeを活用する。
TODO : あとで手をつける
FIXME : 既知の不具合がある
HACK : あまりきれいじゃない解決策
XXX : 危険。大きな問題がある

```json
"todo-tree.general.tags": ["FIXME", "HACK", "TODO", "XXX"],
"todo-tree.highlights.defaultHighlight": {
"gutterIcon": true
},
"todo-tree.highlights.customHighlight": {
"TODO": {
    "icon": "check-circle-fill",
    "foreground": "orange",
    "iconColour": "orange"
},
"FIXME": {
    "icon": "flame",
    "foreground": "yellow",
    "iconColour": "yellow"
},
"HACK": {
    "icon": "shield",
    "foreground": "#00bfff",
    "iconColour": "#00bfff"
},
"XXX": {
    "icon": "zap",
    "foreground": "red",
    "iconColour": "red"
}
},
```

- 定数にコメントをつける

```py
# 合理的な限界値。人間はこんなに読めない。
MAX_RSS_SUBSCRIPTIONS = 1000

# 0.72ならユーザはファイルサイズと品質の面で妥協できる
image_quality = 0.72
```

### 5.3 読み手の立場になって考える

- 質問されそうなことを想像する
他人のコードを読んでいて疑問に思うところにコメントをつける

- ハマりそうな罠を告知する

```py
# メールを送信する外部サービスを呼び出している(1分でタイムアウト)
def send_email(to, subject, body)
```

- 「全体像」のコメント
大量の正式文書のように書く必要はない。
短い適切な文章で構わない。何もないよりマシ。

- 要約コメント
関数内部で「全体像」についてコメントする。
関数内部にある大きな塊ごとにコメントをつけても良い。