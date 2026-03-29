from __future__ import annotations

"""
Ay Yüzeyi Otonom Rota Planlayıcı (Lunar Surface Autonomous Pathfinder)
======================================================================
Streamlit uygulaması — A* algoritması ile eğim haritası üzerinde en uygun rotayı bulur.
Fare tıklamasıyla başlangıç/hedef noktası seçimi (streamlit-image-coordinates).

Kullanım:
    streamlit run lunar_pathfinder.py
"""

import heapq
import math
import os
import time

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

# ---------------------------------------------------------------------------
# Sayfa Yapılandırması
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title=" Ay Yüzeyi Rota Planlayıcı",
    page_icon="-",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Sabitler
# ---------------------------------------------------------------------------
TIF_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "ldsm_87s_5mpp.tif")  # Güney Kutbu Eğim Haritası
TIF_SUN_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "South_Sun.tiff")  # Güneş / Şarj Haritası
DOWNSAMPLE_FACTOR = 10
SLOPE_THRESHOLD = 20.0        # derece — bu değerin üstü geçilemez
SAFE_ZONE_UPPER = 13.0        # 0°–13° güvenli alan
PIXEL_RESOLUTION_M = 5.0      # her piksel 5 metre (orijinal çözünürlük)
RESOLUTION_M = PIXEL_RESOLUTION_M * DOWNSAMPLE_FACTOR  # downsample sonrası
SQRT2 = math.sqrt(2)

# Tiered cost weights
# (Removed Alan 1 and Alan 2 in favor of continuous function)

# 16 yönlü hareket: (drow, dcol, mesafe çarpanı) (Genişletilmiş Kinematik)
DIRECTIONS = [
    (-1, 0, 1.0),   (1, 0, 1.0),    # yukarı, aşağı
    (0, -1, 1.0),   (0, 1, 1.0),    # sol, sağ
    (-1, -1, SQRT2), (-1, 1, SQRT2), # çaprazlar
    (1, -1, SQRT2),  (1, 1, SQRT2),
    # Ara açılar (Knight jumps) - ~26.5° ve ~63.4° dönüşlere olanak tanır
    (-2, -1, math.sqrt(5)), (-2, 1, math.sqrt(5)),
    (-1, -2, math.sqrt(5)), (-1, 2, math.sqrt(5)),
    (1, -2, math.sqrt(5)),  (1, 2, math.sqrt(5)),
    (2, -1, math.sqrt(5)),  (2, 1, math.sqrt(5))
]


# ---------------------------------------------------------------------------
# Veri Yükleme Fonksiyonları
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner="Haritalar mekansal olarak hizalanıyor (Geospatial Crop)...")
def load_aligned_maps(slope_path: str, sun_path: str, target_res: float) -> tuple[np.ndarray, np.ndarray, dict]:
    """
    Güneş haritasının uzamsal sınırlarını (Bounds) temel alır.
    Büyük eğim haritasını tam olarak bu sınırlara (60.7 km yarıçap) kırpar
    ve her iki haritayı da target_res çözünürlüğüne (örn 50m/px) senkronize eder.
    """
    import rasterio
    from rasterio.vrt import WarpedVRT
    from rasterio.enums import Resampling
    from rasterio.transform import from_bounds

    # Önce Güneş haritasının mekansal sınırlarını öğren
    with rasterio.open(sun_path) as sun_src:
        sun_bounds = sun_src.bounds
        sun_crs = sun_src.crs
        
    # Yeni ortak boyutu hesapla
    width = int((sun_bounds.right - sun_bounds.left) / target_res)
    height = int((sun_bounds.top - sun_bounds.bottom) / target_res)
    
    # Ortak mekansal matrisi (Transform) oluştur
    target_transform = from_bounds(*sun_bounds, width, height)
    
    # Güneş Haritasını Ölçekle
    with rasterio.open(sun_path) as sun_src:
        with WarpedVRT(sun_src, crs=sun_crs, transform=target_transform, 
                       width=width, height=height, resampling=Resampling.bilinear) as vrt:
            sun_data = vrt.read(1)
            
    # Eğim Haritasını Kırp ve Ölçekle (Aynı sınırlara oturt)
    with rasterio.open(slope_path) as slope_src:
        with WarpedVRT(slope_src, crs=sun_crs, transform=target_transform, 
                       width=width, height=height, resampling=Resampling.bilinear) as vrt:
            slope_data = vrt.read(1)

    # Boşlukları ve NaN değerlerini temizle
    slope_data = np.nan_to_num(slope_data, nan=0.0)
    safe_min = np.nanmin(sun_data) if not np.isnan(np.nanmin(sun_data)) else 0.0
    sun_data = np.nan_to_num(sun_data, nan=safe_min)

    # 60.7 km (kare haritanın dış köşeleri) için dairesel maske (Radius = min(width, height) / 2)
    cy, cx = height / 2.0, width / 2.0
    y, x = np.ogrid[:height, :width]
    dist_from_center = np.sqrt((x - cx)**2 + (y - cy)**2)
    radius_pixels = min(width, height) / 2.0
    circular_mask = dist_from_center > radius_pixels
    
    # Köşeleri temizle: Buralar A* için engel (>20°) olsun ve Güneş'te karanlık gözüksün
    slope_data[circular_mask] = 999.0  
    sun_data[circular_mask] = safe_min

    meta = {
        "crs_wkt": sun_crs.to_wkt(),
        "transform": [
            target_transform.a, target_transform.b, target_transform.c, 
            target_transform.d, target_transform.e, target_transform.f
        ],
        "width": width,
        "height": height
    }

    return slope_data.astype(np.float32), sun_data.astype(np.float32), meta

def generate_dummy_slope(rows: int = 150, cols: int = 150,
                         seed: int = 42) -> np.ndarray:
    """Test amaçlı rastgele eğim haritası üretir (0-30 derece arası)."""
    rng = np.random.RandomState(seed)

    x = np.linspace(0, 4 * np.pi, cols)
    y = np.linspace(0, 4 * np.pi, rows)
    xx, yy = np.meshgrid(x, y)

    base = (
        np.sin(xx) * np.cos(yy) * 10
        + np.sin(3 * xx + 1) * np.cos(2 * yy) * 5
        + np.cos(1.5 * xx) * np.sin(0.5 * yy) * 3
    )
    noise = rng.uniform(-2, 2, (rows, cols))
    slope = np.clip(np.abs(base + noise), 0, 30).astype(np.float32)
    return slope

def generate_dummy_sun(rows: int = 150, cols: int = 150,
                       seed: int = 43) -> np.ndarray:
    """Test amaçlı rastgele güneş/sıcaklık haritası üretir."""
    rng = np.random.RandomState(seed)
    
    x = np.linspace(0, 4 * np.pi, cols)
    y = np.linspace(0, 4 * np.pi, rows)
    xx, yy = np.meshgrid(x, y)
    
    # Basit perlin benzeri sahte sıcaklık dağılımı
    base = np.sin(xx * 0.5) * np.cos(yy * 0.5) * 100 + 150
    noise = rng.uniform(-10, 10, (rows, cols))
    sun = np.clip(base + noise, 50, 300).astype(np.float32)
    return sun


# ---------------------------------------------------------------------------
# A* Algoritması — Tiered Cost
# ---------------------------------------------------------------------------
def heuristic(a: tuple[int, int], b: tuple[int, int]) -> float:
    """Euclidean distance — 16-yönlü hareket için en doğru admissible heuristic."""
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _slope_multiplier(slope_val: float) -> float:
    """
    Sürekli maliyet fonksiyonu:
    Eğim arttıkça eksponansiyel olarak artan bir ceza (multiplier).
    Örn: 1.0 + (slope / 10.0)**2
    """
    return 1.0 + (slope_val / 10.0) ** 2

def get_turn_multiplier(in_dir: tuple[int, int], out_dir: tuple[int, int]) -> float:
    """
    Sürekli Rover kinematiği (Aralıklı Dönüş kısıtlamaları):
    Dönüş açısına göre yumuşak artan bir sürekli polinomsal ceza (0-90° arası).
    Sert dönüş (>= 90° tank turn): inf (Yasak)
    """
    if in_dir == (0, 0):
        return 1.0
        
    in_dr, in_dc = in_dir
    out_dr, out_dc = out_dir
    
    if in_dr == out_dr and in_dc == out_dc:
        return 1.0
        
    angle_in = math.atan2(in_dr, in_dc)
    angle_out = math.atan2(out_dr, out_dc)
    diff = abs(angle_in - angle_out)
    
    if diff > math.pi:
        diff = 2 * math.pi - diff
    
    diff_deg = math.degrees(diff)
    
    # 90 derece veya daha fazlası tank-turn sayılır ve kesinlikle yasaktır
    if diff_deg >= 89.9: 
        return math.inf
        
    # Sürekli fonksiyon (Continuous penalty)
    # 0°   -> 1.0x
    # 45°  -> 1.5x (1 + 0.5 * (45/45)^2)
    # Diğer ara açılar (örneğin ~26.5° olan knight jump) formüle göre pürüzsüz hesaplanır.
    return 1.0 + 0.5 * ((diff_deg / 45.0) ** 2)

def get_sun_multiplier(temp_val: float, min_temp: float, max_temp: float) -> float:
    """
    Sıcaklık/Güneş maliyet fonksiyonu:
    Max Temp -> 1.0 (En iyi / Güneş alan)
    Min Temp -> 3.0 (En kötü / Tamamen karanlık)
    Aradaki değerler oaranla yumuşak geçiş yapar.
    """
    if max_temp == min_temp:
        return 1.0
        
    # Sıcaklığa göre 0.0 (en soğuk) ile 1.0 (en sıcak) arasında normalizasyon
    norm = (temp_val - min_temp) / (max_temp - min_temp)
    # norm = 1 (sıcak) -> penalty 1.0
    # norm = 0 (soğuk) -> penalty 3.0
    return 3.0 - 2.0 * norm

def astar_search(
    slope: np.ndarray,
    sun: np.ndarray,
    obstacle_mask: np.ndarray,
    start: tuple[int, int],
    goal: tuple[int, int],
) -> list[tuple[int, int]] | None:
    """
    A* ile en düşük maliyetli yolu bulur.

    Maliyet = mesafe * eğim_cezası * dönüş_cezası * güneş_cezası
    Geçilemez pikseller obstacle_mask ile belirlenir (>20°).
    Yol bulunamazsa None döner.
    """
    rows, cols = slope.shape

    # Sınır kontrolü
    for pt_name, pt in [("Başlangıç", start), ("Hedef", goal)]:
        r, c = pt
        if not (0 <= r < rows and 0 <= c < cols):
            raise ValueError(f"{pt_name} noktası ({r}, {c}) harita dışında. "
                             f"Harita boyutu: {rows}×{cols}.")
        if obstacle_mask[r, c]:
            raise ValueError(
                f"{pt_name} noktası ({r}, {c}) geçilemez alanda "
                f"(eğim > {SLOPE_THRESHOLD}°). Lütfen farklı bir nokta seçin."
            )

    counter = 0
    start_state = (start[0], start[1], 0, 0)
    open_set: list[tuple[float, int, tuple[int, int, int, int]]] = []
    heapq.heappush(open_set, (0.0, counter, start_state))

    came_from: dict[tuple[int, int, int, int], tuple[int, int, int, int]] = {}
    g_score: dict[tuple[int, int, int, int], float] = {start_state: 0.0}

    sun_min = float(np.min(sun))
    sun_max = float(np.max(sun))

    while open_set:
        _, _, current_state = heapq.heappop(open_set)
        cr, cc, in_dr, in_dc = current_state

        if (cr, cc) == goal:
            path = [(cr, cc)]
            curr = current_state
            while curr in came_from:
                curr = came_from[curr]
                path.append((curr[0], curr[1]))
            path.reverse()
            return path

        current_slope = float(slope[cr, cc])
        current_sun = float(sun[cr, cc])

        for dr, dc, dist_mult in DIRECTIONS:
            nr, nc = cr + dr, cc + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if obstacle_mask[nr, nc]:
                continue

            turn_mult = get_turn_multiplier((in_dr, in_dc), (dr, dc))
            if turn_mult == math.inf:
                continue

            neighbor_state = (nr, nc, dr, dc)
            neighbor_slope = float(slope[nr, nc])
            neighbor_sun = float(sun[nr, nc])

            # Maliyet formülü: mesafe * eğim cezası * dönüş cezası * güneş cezası
            avg_slope = (current_slope + neighbor_slope) / 2.0
            slope_mult = _slope_multiplier(avg_slope)
            
            avg_sun = (current_sun + neighbor_sun) / 2.0
            sun_mult = get_sun_multiplier(avg_sun, sun_min, sun_max)
            
            move_cost = dist_mult * slope_mult * turn_mult * sun_mult

            tentative_g = g_score.get(current_state, math.inf) + move_cost

            if tentative_g < g_score.get(neighbor_state, math.inf):
                g_score[neighbor_state] = tentative_g
                f = tentative_g + heuristic((nr, nc), goal)
                came_from[neighbor_state] = current_state
                counter += 1
                heapq.heappush(open_set, (f, counter, neighbor_state))

    return None  # Yol bulunamadı


# ---------------------------------------------------------------------------
# Yol Uzunluğu Hesaplama
# ---------------------------------------------------------------------------
def path_length_meters(path: list[tuple[int, int]],
                       pixel_res: float) -> float:
    """Rota uzunluğunu metre cinsinden hesaplar."""
    total = 0.0
    for i in range(1, len(path)):
        dr = path[i][0] - path[i - 1][0]
        dc = path[i][1] - path[i - 1][1]
        dist_px = math.sqrt(dr * dr + dc * dc)
        total += dist_px * pixel_res
    return total


# ---------------------------------------------------------------------------
# GeoTIFF Dışa Aktarma
# ---------------------------------------------------------------------------
def export_route_to_tif(path_coords: list[tuple[int, int]], meta: dict) -> bytes:
    """Rotayı aynı uzamsal (geospatial) verilerle GeoTIFF olarak belleğe yazar."""
    import rasterio
    from rasterio.io import MemoryFile
    from rasterio.transform import Affine
    
    width = meta["width"]
    height = meta["height"]
    route_array = np.zeros((height, width), dtype=np.uint8)
    
    # Rotayı 255 (tam beyaz) ile çiz
    for r, c in path_coords:
        route_array[r, c] = 255
        
    transform = Affine(*meta["transform"])
    
    with MemoryFile() as memfile:
        with memfile.open(
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=str(route_array.dtype),
            crs=meta["crs_wkt"],
            transform=transform,
            compress='deflate'
        ) as dataset:
            dataset.write(route_array, 1)
        
        return memfile.read()

# ---------------------------------------------------------------------------
# Görüntü (Matplotlib/PIL) Render
# ---------------------------------------------------------------------------
def render_map_image(
    data_array: np.ndarray,
    obstacle_mask: np.ndarray,
    start: tuple[int, int] | None = None,
    goal: tuple[int, int] | None = None,
    path: list[tuple[int, int]] | None = None,
    scale: int = 1,
    view_mode: str = "slope"
) -> Image.Image:
    """
    Tıklanabilir resim altyapısı için Numpy verisini PIL Image objesi olarak çizer.
    view_mode: "slope" veya "sun"
    """
    if view_mode == "slope":
        norm_arr = np.clip(data_array / SLOPE_THRESHOLD, 0, 1.0)
        cmap = plt.get_cmap("viridis")
    else:
        # Sun/Temperature view
        s_min = float(np.min(data_array))
        s_max = float(np.max(data_array))
        if s_max > s_min:
            norm_arr = (data_array - s_min) / (s_max - s_min)
        else:
            norm_arr = np.zeros_like(data_array)
        cmap = plt.get_cmap("inferno")

    rgba_map = cmap(norm_arr)

    # Engelleri belirgin siyah/koyu gri yap
    rgba_map[obstacle_mask] = [0.05, 0.05, 0.05, 1.0]

    img_array = (rgba_map[:, :, :3] * 255).astype(np.uint8)

    # PIL Image olarak yükle ve netliği (pixelated) koruyarak büyüt
    img = Image.fromarray(img_array)
    img = img.resize((img.width * scale, img.height * scale), Image.NEAREST)

    # Çizim
    draw = ImageDraw.Draw(img)

    def to_img_pts(r: int, c: int) -> tuple[int, int]:
        """Array koordinatını Image üzerindeki (x, y) merkeze çevirir."""
        return int(c * scale + scale / 2), int(r * scale + scale / 2)

    # Çizgi (Rota)
    if path and len(path) > 1:
        img_path = [to_img_pts(r, c) for r, c in path]
        draw.line(img_path, fill=(0, 255, 255), width=int(max(2, scale * 0.4)))

    point_radius = int(max(3, scale * 0.8))

    # Start Point
    if start is not None:
        sx, sy = to_img_pts(start[0], start[1])
        draw.ellipse(
            [sx - point_radius, sy - point_radius, sx + point_radius, sy + point_radius],
            fill=(0, 255, 136), outline=(255, 255, 255)
        )

    # Goal Point
    if goal is not None:
        gx, gy = to_img_pts(goal[0], goal[1])
        draw.ellipse(
            [gx - point_radius, gy - point_radius, gx + point_radius, gy + point_radius],
            fill=(255, 68, 68), outline=(255, 255, 255)
        )

    return img


# ---------------------------------------------------------------------------
# Session State Yönetimi
# ---------------------------------------------------------------------------
def _init_session_state():
    """Click state'ini başlat."""
    if "click_stage" not in st.session_state:
        st.session_state.click_stage = "start"  # "start" | "goal" | "done"
    if "start_pt" not in st.session_state:
        st.session_state.start_pt = None
    if "goal_pt" not in st.session_state:
        st.session_state.goal_pt = None
    if "path_result" not in st.session_state:
        st.session_state.path_result = None
    if "calc_stats" not in st.session_state:
        st.session_state.calc_stats = None
    if "last_click" not in st.session_state:
        st.session_state.last_click = None
    if "error_msg" not in st.session_state:
        st.session_state.error_msg = None


# ---------------------------------------------------------------------------
# Ana Streamlit Arayüzü
# ---------------------------------------------------------------------------
def main():
    _init_session_state()

    # ---- Başlık ----
    st.markdown(
        """
        <style>
        .main-title {
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0;
        }
        .sub-title {
            text-align: center;
            color: #888;
            font-size: 1rem;
            margin-top: 0;
        }
        .metric-card {
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            border: 1px solid #333;
            border-radius: 12px;
            padding: 1.2rem;
            text-align: center;
        }
        .metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #00ffff;
        }
        .metric-label {
            font-size: 0.85rem;
            color: #888;
            margin-top: 0.3rem;
        }
        .coord-display {
            background: #16213e;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 0.6rem 0.8rem;
            font-family: monospace;
            color: #e0e0e0;
            font-size: 0.95rem;
        }
        .zone-safe { color: #52b788; font-weight: 600; }
        .zone-hard { color: #f4a261; font-weight: 600; }
        .zone-blocked { color: #d62828; font-weight: 600; }
        .map-container {
            display: flex;
            justify-content: center;
            margin-top: 2rem;
            margin-bottom: 2rem;
            background-color: #0e1117;
            padding: 1rem;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
            border: 1px solid #333;
        }
        </style>
        <h1 class="main-title">🌙 Ay Yüzeyi Rota Planlayıcı</h1>
        <p class="sub-title">A* Pathfinding ile Otonom Lunar Navigasyon</p>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # ---- Kenar Çubuğu ----
    with st.sidebar:
        st.header("⚙️ Ayarlar")

        test_mode = st.toggle("🧪 Test Modu (Dummy Veri)", value=False,
                              help="Gerçek .tif dosyası olmadan 150×150 test "
                                   "verisiyle çalışır.")

        st.divider()

        # ---- Eğim Kuralları Bilgisi ----
        st.subheader("📐 Navigasyon Kuralları")
        st.markdown(
            f'<span class="zone-safe">● Dinamik Eğim Cezası:</span> '
            f'Eğim arttıkça eksponansiyel ceza <code>1 + (derece/10)²</code>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<span class="zone-hard">● Sürekli Kinematik:</span> '
            f'Dönüş açısına göre aralıksız hesaplanan polinomsal ceza. Kesinlikle ≥90° yasak',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<span class="zone-blocked">● Engel (>{SLOPE_THRESHOLD}°):</span> '
            f'Geçilemez',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<span style="color: #ffb703; font-weight: 600;">● Güneş (Batarya) Şartı:</span> '
            f'Sıcaklığa göre 1.0x (güneşli) ile 3.0x (karanlık) ceza. Karanlıklardan kaçınılır.',
            unsafe_allow_html=True,
        )

        st.divider()

        # ---- Koordinat Gösterimi (salt okunur) ----
        st.subheader("📍 Seçilen Noktalar")

        stage = st.session_state.click_stage

        if st.session_state.start_pt is not None:
            sr, sc = st.session_state.start_pt
            st.markdown(
                f'🟢 **Başlangıç:** '
                f'<span class="coord-display">X={sc}, Y={sr}</span>',
                unsafe_allow_html=True,
            )
        else:
            st.info("🟢 Haritaya tıklayarak **Başlangıç** noktasını seçin")

        if st.session_state.goal_pt is not None:
            gr, gc = st.session_state.goal_pt
            st.markdown(
                f'🔴 **Hedef:** '
                f'<span class="coord-display">X={gc}, Y={gr}</span>',
                unsafe_allow_html=True,
            )
        else:
            if stage == "goal":
                st.info("🔴 Haritaya tıklayarak **Hedef** noktasını seçin")
            else:
                st.caption("🔴 Hedef — henüz seçilmedi")

        st.divider()

        # Sıfırla butonu
        if st.button("🔄 Noktaları Sıfırla", use_container_width=True):
            st.session_state.click_stage = "start"
            st.session_state.start_pt = None
            st.session_state.goal_pt = None
            st.session_state.path_result = None
            st.session_state.calc_stats = None
            st.session_state.error_msg = None
            st.session_state.last_click = None
            st.rerun()

    # ---- Veri Yükleme ----
    if test_mode:
        slope = generate_dummy_slope()
        sun = generate_dummy_sun()
        map_meta = None
        current_resolution = PIXEL_RESOLUTION_M
        st.sidebar.success("✅ Test modu — 150×150 dummy eğim ve güneş haritası yüklendi.")
    else:
        if not os.path.exists(TIF_PATH) or not os.path.exists(TIF_SUN_PATH):
            st.warning(
                f"⚠️ Eksik dosyalar:\n`{TIF_PATH}`\nveya\n`{TIF_SUN_PATH}`\n\n"
                "Lütfen dosyaları bu konuma kopyalayın veya **Test Modu**'nu açın.",
                icon="⚠️",
            )
            slope = generate_dummy_slope()
            sun = generate_dummy_sun()
            map_meta = None
            current_resolution = PIXEL_RESOLUTION_M
            st.sidebar.info("ℹ️ Dosya bulunamadı — test verisi kullanılıyor.")
        else:
            with st.spinner(f"TIF haritaları 88-90S sınırlarına ({RESOLUTION_M}m/px) hizalanıyor..."):
                # Haritaları uzamsal olarak (geospatially) eşleştirip yükle
                slope, sun, map_meta = load_aligned_maps(TIF_PATH, TIF_SUN_PATH, target_res=RESOLUTION_M)
                
                if slope.shape != sun.shape:
                    st.error(f"Hata: Boyut uyumsuzluğu! Eğim: {slope.shape}, Güneş: {sun.shape}")
                    st.stop()
                    
                current_resolution = RESOLUTION_M
                st.sidebar.success(
                    f"✅ Haritalar uzamsal (geospatial) olarak eşleştirildi — boyut: {slope.shape[0]}×{slope.shape[1]}"
                )

    # Engel maskesi
    obstacle_mask = slope > SLOPE_THRESHOLD
    rows, cols = slope.shape

    # Devasa resimlerin (örn 4000x4000) tarayıcıyı çökertmemesi için dinamik scale
    dynamic_scale = max(1, 900 // cols)

    # ---- Harita bilgileri ----
    info_cols = st.columns(4)
    with info_cols[0]:
        st.metric("Harita Boyutu", f"{rows} × {cols} px")
    with info_cols[1]:
        st.metric("Piksel Çözünürlük", f"{current_resolution:.0f} m")
    with info_cols[2]:
        obstacle_pct = np.sum(obstacle_mask) / obstacle_mask.size * 100
        st.metric("Engel Oranı", f"%{obstacle_pct:.1f}")
    with info_cols[3]:
        st.metric("Eğim Eşiği", f"{SLOPE_THRESHOLD}°")

    # ---- Kullanıcıya tıklama talimatı ----
    stage = st.session_state.click_stage
    if stage == "start":
        st.info("👆 **1. Adım:** Haritaya tıklayarak **Başlangıç** noktasını seçin.",
                icon="🟢")
    elif stage == "goal":
        st.info("👆 **2. Adım:** Haritaya tıklayarak **Hedef** noktasını seçin. "
                "Seçildikten sonra rota otomatik hesaplanır.", icon="🔴")

    # ---- Harita Çizimi ve UI Gösterimi ----
    
    st.markdown("### Harita Görüntüsü")
    map_view = st.radio(
        "Görüntülenecek Katman:", 
        ["📐 Eğim (Slope)", "☀️ Sıcaklık / Aydınlık (Güneş)"], 
        horizontal=True,
        label_visibility="collapsed"
    )

    if "Eğim" in map_view:
        display_data = slope
        v_mode = "slope"
    else:
        display_data = sun
        v_mode = "sun"

    # Haritayı PIL objesi olarak render et
    map_image = render_map_image(
        display_data, obstacle_mask,
        start=st.session_state.start_pt,
        goal=st.session_state.goal_pt,
        path=st.session_state.path_result,
        scale=dynamic_scale,
        view_mode=v_mode
    )

    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    
    # Haritayı tıklanabilir görüntü olarak bas (Streamlit-image-coordinates)
    click_result = streamlit_image_coordinates(
        map_image,
        key="map_interaction",
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- Tıklama Olay İşleme ----
    if click_result is not None and click_result != st.session_state.last_click:
        st.session_state.last_click = click_result
        
        # Görüntü piksel bazlı olduğu için dynamic_scale'e bölerek asıl array indexine dönüyoruz
        click_col = int(click_result["x"] // dynamic_scale)
        click_row = int(click_result["y"] // dynamic_scale)

        # Sınır kontrolü ve state değişimi
        if 0 <= click_row < rows and 0 <= click_col < cols:
            
            # Seçilen nokta geçilemez ise kullanıcıyı uyar ama state'i bozma
            if obstacle_mask[click_row, click_col]:
                # Yasadışı noktaya tıkladı, işleme
                # Bir nevi uyarısını verdirebiliriz veya tıklamayı yoksayabilir.
                # Biz basit olması için o tıklamayı yoksaymıyoruz, ValueError uyarısını patlatması için bırakıyoruz. 
                pass

            if stage == "start":
                # İlk tıklama → Başlangıç
                # Eğer aynı koordinatı tıklamadıysa ve geçerliyse
                if st.session_state.start_pt != (click_row, click_col):
                    st.session_state.start_pt = (click_row, click_col)
                    st.session_state.goal_pt = None
                    st.session_state.path_result = None
                    st.session_state.calc_stats = None
                    st.session_state.error_msg = None
                    st.session_state.click_stage = "goal"
                    st.rerun()

            elif stage == "goal":
                # İkinci tıklama → Hedef + otomatik hesaplama
                if st.session_state.goal_pt != (click_row, click_col):
                    st.session_state.goal_pt = (click_row, click_col)
                    st.session_state.click_stage = "done"

                    # A* hesaplama
                    try:
                        t0 = time.perf_counter()
                        path = astar_search(
                            slope, sun, obstacle_mask,
                            st.session_state.start_pt,
                            st.session_state.goal_pt,
                        )
                        elapsed = time.perf_counter() - t0

                        if path is None:
                            st.session_state.path_result = None
                            st.session_state.error_msg = (
                                "Rover'ın limiti aşılıyor veya iki nokta "
                                "arasında güvenli bir rota bulunamadı."
                            )
                            st.session_state.calc_stats = None
                        else:
                            length_m = path_length_meters(path, current_resolution)
                            st.session_state.path_result = path
                            st.session_state.error_msg = None
                            st.session_state.calc_stats = {
                                "length_m": length_m,
                                "length_km": length_m / 1000.0,
                                "steps": len(path),
                                "elapsed": elapsed,
                            }
                    except ValueError as exc:
                        st.session_state.path_result = None
                        st.session_state.error_msg = str(exc)
                        st.session_state.calc_stats = None

                    st.rerun()

            elif stage == "done":
                # Üçüncü tıklama → yeni başlangıç (sıfırla ve yeniden başla)
                if st.session_state.start_pt != (click_row, click_col):
                    st.session_state.start_pt = (click_row, click_col)
                    st.session_state.goal_pt = None
                    st.session_state.path_result = None
                    st.session_state.calc_stats = None
                    st.session_state.error_msg = None
                    st.session_state.click_stage = "goal"
                    st.rerun()

    # ---- Hata Mesajı ----
    if st.session_state.error_msg:
        st.error(
            f"❌ **{st.session_state.error_msg}**",
            icon="🚫",
        )

    # ---- Sonuç Kartları ----
    if st.session_state.calc_stats:
        stats = st.session_state.calc_stats
        st.divider()
        res_cols = st.columns(3)
        with res_cols[0]:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-value">{stats["length_m"]:,.0f} m</div>'
                f'<div class="metric-label">Toplam Mesafe</div></div>',
                unsafe_allow_html=True,
            )
        with res_cols[1]:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-value">{stats["length_km"]:,.2f} km</div>'
                f'<div class="metric-label">Kilometre</div></div>',
                unsafe_allow_html=True,
            )
        with res_cols[2]:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-value">{stats["elapsed"]:.2f} s</div>'
                f'<div class="metric-label">Hesaplama Süresi</div></div>',
                unsafe_allow_html=True,
            )

        st.success(
            f"✅ Rota bulundu! **{stats['steps']}** adım, "
            f"**{stats['length_m']:,.0f} m** ({stats['length_km']:,.2f} km) "
            f"uzunluğunda. Hesaplama süresi: {stats['elapsed']:.2f} saniye.",
            icon="🎯",
        )

        if map_meta is not None:
            tif_bytes = export_route_to_tif(st.session_state.path_result, map_meta)
            st.download_button(
                label="📥 Rotayı GeoTIFF Formatında Dışa Aktar",
                data=tif_bytes,
                file_name="rover_calculated_route.tif",
                mime="image/tiff",
                use_container_width=True,
                help="Oluşturulan bu rota, başka CBS (GIS) veya analiz toollarında "
                     "overlay olarak kullanılmak üzere orijinal coğrafi koordinatlarıyla "
                     "birlikte yüksek kaliteli TIFF olarak kaydedilir."
            )

    # ---- Altbilgi ----
    st.divider()
    st.caption(
        f"🔬 A* Algoritması — Maliyet: Mesafe × Eğim × Dönüş × Güneş | "
        f"Dönüş: 1.0 + 0.5×(Açı/45)² | Sert(Yasak) | "
        f"Eğim: 1.0 + (x/10)² | "
        f"Güneş (Şarj): Açığa 1.0x, Karanlığa 3.0x | "
        f"Engel: >{SLOPE_THRESHOLD}° | "
        f"16-yönlü hareket | Çözünürlük: {current_resolution:.0f} m/px"
    )


if __name__ == "__main__":
    main()
