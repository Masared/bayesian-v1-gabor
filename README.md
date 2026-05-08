# bayesian-v1-gabor

ガボール関数で生成した視覚信号にノイズを付加し、シミュレーションデータとして保存するツールキットです。

**参考文献:** [ガボール視覚信号モデル (J-STAGE)](https://www.jstage.jst.go.jp/article/jpnjvissci/32/3/32_32.51/_pdf/-char/ja)

---

## モデル

ガボール関数 $S(x)$ を以下の式で定義します。

$$S(x) = \exp\!\left(-\frac{(x-x_m)^2}{4\sigma^2}\right) \cos\!\left(2\pi f_n (x - x_m)\right) + 1$$

| パラメータ | 意味 |
|---|---|
| $x_m$ | ガウスエンベロープのピーク位置 |
| $f_n$ | 空間周波数 |
| $\sigma$ | エンベロープの広がり |

### ノイズモデル

| モデル | 式 | 用途 |
|---|---|---|
| ガウス | $y(x) = S(x) + \mathcal{N}(0, \sigma_n^2)$ | 一般的な観測ノイズ |
| ポアソン | $y(x) = \mathrm{Poisson}(\mathrm{scale} \cdot S(x))$ | 光子計数など離散ノイズ |

---

## ディレクトリ構成

```
bayesian-v1-gabor/
├── notebooks/
│   └── gabor_simulation.ipynb   # データ生成・可視化・保存
├── simulated_data/              # 生成データの保存先
│   ├── gauss_xm0.0_fn0.52_sigma1.0/
│   │   ├── params.json          # 生成時のパラメータ
│   │   └── data.txt             # x y 形式のデータ
│   └── poisson_xm0.0_fn0.52_sigma1.0_scale5.0/
│       ├── params.json
│       └── data.txt
├── src/
│   └── data_generate.py         # ガボール関数・ノイズ生成の実装
└── documents/                   # 関連資料
```

---

## セットアップ

Python 3.10 以上を推奨します。

```bash
pip install numpy matplotlib
```

---

## 使い方

### 1. 作業ディレクトリに移動して、simulated_data/ を作成する

```bash
cd bayesian-v1-gabor
mkdir simulated_data
```

### 2. パラメータを設定する（セル3）

```python
xm_val        = 0.0   # ピーク位置
fn_val        = 0.52  # 空間周波数
sigma_val     = 1.0   # エンベロープの広がり
noise_level   = 0.1   # ガウスノイズの標準偏差
poisson_scale = 5.0   # ポアソンノイズのスケール（大きいほどノイズ小）
```

### 3. ノイズの種類と保存を設定する（セル11）

```python
noise = 'gauss'   # 'gauss' または 'poisson'
save  = True      # True にすると simulated_data/ 以下に保存
```

### 4. 全セルを実行する

`save=True` にすると以下が自動生成されます。

```
simulated_data/gauss_xm0.0_fn0.52_sigma1.0/
├── params.json   # 全パラメータ（再現に必要な情報をすべて記録）
└── data.txt      # "x  y" 形式、1000点
```

---

## `src/data_generate.py` API

```python
from data_generate import calculate_s_x, add_gaussian_noise, add_poisson_noise

x       = np.linspace(-5, 5, 1000)
s_x     = calculate_s_x(x, xm=0.0, fn=0.52, sigma=1.0)
gauss   = add_gaussian_noise(s_x, sigma=0.1)
poisson = add_poisson_noise(s_x, scale=5.0)
```

---

## `params.json` の例

**ガウスノイズの場合**
```json
{
    "noise_model": "gauss",
    "xm": 0.0,
    "fn": 0.52,
    "sigma": 1.0,
    "noise_level": 0.1,
    "x_min": -5.0,
    "x_max": 5.0,
    "n_points": 1000
}
```

**ポアソンノイズの場合**
```json
{
    "noise_model": "poisson",
    "xm": 0.0,
    "fn": 0.52,
    "sigma": 1.0,
    "poisson_scale": 5.0,
    "x_min": -5.0,
    "x_max": 5.0,
    "n_points": 1000
}
```
