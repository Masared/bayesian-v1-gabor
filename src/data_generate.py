import numpy as np

def calculate_s_x(x, xm, fn, sigma):
    """
    ガボール変換 S(x) を計算する関数
    
    Parameters:
    -----------
    x : float or np.ndarray
        場所座標
    xm : float
        ガウス関数のピーク位置
    fn : float
        空間周波数
    sigma : float
        ガウス関数の裾の広がり（標準偏差に関連するパラメータ）
        
    Returns:
    --------
    s_x : float or np.ndarray
        計算結果 S(x)
    """
    # ガウス関数部分（エンベロープ）の計算
    # 数式通り、分母は 4 * sigma^2 としています
    envelope = np.exp(-(x - xm)**2 / (4 * sigma**2))
    
    # 余弦波部分の計算
    oscillation = np.cos(2 * np.pi * fn * (x - xm))
    # S(X)は負を取らないため、1を加算して正の値に調整
    return envelope * oscillation + 1


def add_gaussian_noise(signal, sigma=0.1, rng=None):
    """
    信号にガウスノイズを加える関数

    定義式:
        y(x) = S(x) + n(x),  n(x) ~ N(0, sigma^2)

    Parameters:
    -----------
    signal : np.ndarray
        ノイズを加える対象の信号
    sigma : float
        ガウスノイズの標準偏差
    rng : np.random.Generator | None
        乱数生成器。None なら `np.random.default_rng()` を使用

    Returns:
    --------
    noisy : np.ndarray
        ノイズを加えた信号
    """
    rng = rng if rng is not None else np.random.default_rng()
    signal = np.asarray(signal, dtype=float)
    return signal + rng.normal(0.0, sigma, size=signal.shape)


def add_poisson_noise(signal, scale=1.0, rng=None):
    """
    信号にポアソンノイズを加える関数

    定義式:
        y(x) = Poisson(scale * S(x))
        （scale は光子数換算の強度。大きいほど相対ノイズが小さくなる）

    Parameters:
    -----------
    signal : np.ndarray
        ノイズを加える対象の信号（非負を想定）
    scale : float
        ポアソン強度のスケール係数
    rng : np.random.Generator | None
        乱数生成器。None なら `np.random.default_rng()` を使用

    Returns:
    --------
    noisy : np.ndarray
        ノイズを加えた信号
    """
    rng = rng if rng is not None else np.random.default_rng()
    signal = np.asarray(signal, dtype=float)
    lam = np.clip(signal * scale, 0, None)
    return rng.poisson(lam)


if __name__ == "__main__":
    xm_val = 0.0
    fn_val = 5.0
    sigma_val = 1.0

    x_range = np.linspace(-5, 5, 1000)
    s_x_values = calculate_s_x(x_range, xm_val, fn_val, sigma_val)
    s_x_gauss = add_gaussian_noise(s_x_values, sigma=0.05)
    s_x_poiss = add_poisson_noise(s_x_values, scale=100.0)

    print("計算が完了しました。")