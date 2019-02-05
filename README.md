# Phonto
- ほんとにPhoto?
- 写真orイラスト判定


## 試したこと
- 写真orイラストの判定をしたい
- 画像の局所特徴量とSVMでできるらしい[[K.Terayama+, 2015]](https://ieeexplore.ieee.org/document/7153192)
- 簡単そうなL(輝度成分)を使ったLBP特徴でやってみる
  - だめだった
  - LBP(HSV + L)でやってみてもだめだった
- DCNNでやると精度が上がるとのこと[[G.Gando+, 2016]](https://www.sciencedirect.com/science/article/pii/S0957417416304560)
  - Fine tuningしたAlexNetを用いていた
- 非力なサーバで動かしたい、MobileNetでFine tuningしてみる
  - いけたようだ
  - よくわからんが、まぁ動いているからヨシ！


## Datasets
- train
  - photo: 秘伝の写真500枚くらい + [COCO Dataset](http://cocodataset.org/)(2017)からランダムに選択した1500枚くらい = 計2000枚
  - non-photo: 秘伝のイラストとスクリーンショット2000枚
- validation
  - photo: 秘伝の写真50枚くらい + COCO Datasetからtrain用の画像を除いてランダムに抽出した350枚くらい = 計400枚
  - non-photo: train用に収まり切らなかった秘伝のイラストとスクリーンショット400枚


## TODO
- C++から使えるようにする
  - https://github.com/Dobiasd/frugally-deep
- 秘伝の画像を使わないようにする
  - 少なくとも実写画像は容易に用意できる
- もう少し細かく分類する
  - 実写
  - イラスト
  - ポンチ絵系
  - グラフ・チャート
  - CG
  - 写実的なイラスト？
  - 絵画？

```
$ cd docker/
$ make build
$ make run
```
