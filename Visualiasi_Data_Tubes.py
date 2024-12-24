import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# 1. Memuat Dataset
df = pd.read_csv("Penyebab Kematian di Indonesia yang Dilaporkan - Clean.csv")

# 2. Judul dan Deskripsi
st.markdown(
    """
    <h1 style='text-align: center;'>
    Analisis Penyebab Kematian di Indonesia
    </h1>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
<div style="text-align: justify;">
<p>Aplikasi ini menyajikan analisis penyebab kematian di Indonesia melalui visualisasi interaktif berbasis data terpercaya. Tujuannya meliputi:</p>

<ul>
    <li><strong>Mengidentifikasi Tren:</strong> Memahami pola kematian dari waktu ke waktu.</li>
    <li><strong>Membandingkan Penyebab:</strong> Menyoroti perbedaan antar penyebab untuk menentukan prioritas.</li>
    <li><strong>Mendeteksi Anomali:</strong> Mengungkap fluktuasi tidak biasa untuk investigasi lebih lanjut.</li>
    <li><strong>Mendukung Keputusan:</strong> Memberikan dasar bukti bagi kebijakan kesehatan yang efektif.</li>
</ul>

<p>Analisis ini penting untuk:</p>
<ul>
    <li>Meningkatkan kesehatan publik</li>
    <li>Mengoptimalkan alokasi sumber daya</li>
    <li>Mengevaluasi kebijakan kesehatan</li>
    <li>Mendukung perencanaan kesehatan jangka panjang</li>
</ul>

<p>Melalui eksplorasi data, aplikasi ini bertujuan untuk memberikan wawasan guna meningkatkan kesejahteraan masyarakat Indonesia.</p>
</div>
""",
    unsafe_allow_html=True,
)

# Menampilkan preview dataset
st.subheader("Preview Dataset")
st.write(df)  # Menampilkan seluruh DataFrame
st.markdown(
    """
    <div style="text-align: justify;">
    Dataset ini menyajikan gambaran komprehensif tentang penyebab kematian di Indonesia selama beberapa tahun. Informasi yang terkandung di dalamnya mencakup berbagai faktor penyebab kematian, mulai dari bencana alam hingga penyakit. Setiap entri dalam dataset ini memberikan detail tentang penyebab spesifik kematian, seperti abrasi air laut atau AIDS, serta mengategorikannya ke dalam tipe yang lebih luas seperti bencana alam atau non-alam.
    <br>
    Data ini dikumpulkan dari tahun ke tahun, memungkinkan analisis tren penyebab kematian dari waktu ke waktu. Jumlah total kematian untuk setiap penyebab juga dicatat, memberikan perspektif tentang dampak relatif dari berbagai faktor.
    <br>
    Keandalan dataset ini didukung oleh sumbernya yang terpercaya, yaitu Profil Kesehatan Indonesia yang diterbitkan oleh Kementerian Kesehatan RI. Untuk setiap entri, disertakan referensi ke halaman spesifik dalam laporan sumber dan URL yang dapat diakses, memudahkan verifikasi dan penelusuran lebih lanjut.
    <br><br>
    </div>
    """,
    unsafe_allow_html=True,
)

# Statistik Deskriptif
st.subheader("Statistik Deskriptif")
st.write(df.describe())

# 3. Filter Rentang Tahun di Sidebar (slider untuk rentang tahun dengan default 2020-2022)
years = df["Year"].unique()
min_year, max_year = min(years), max(years)
selected_years_range = st.sidebar.slider(
    "Pilih Rentang Tahun:",
    min_value=min_year,
    max_value=max_year,
    value=(2020, 2022),  # Default rentang tahun adalah 2020 hingga 2022
    step=1,
)

# Filter data berdasarkan rentang tahun yang dipilih
filtered_data = df[
    (df["Year"] >= selected_years_range[0]) & (df["Year"] <= selected_years_range[1])
]

# Menampilkan rentang tahun yang dipilih
st.write(
    f"Data untuk rentang tahun: {selected_years_range[0]} - {selected_years_range[1]}"
)

# 4. Filter Penyebab Kematian di Sidebar dengan Pilihan "Semua"
causes = ["Semua"] + list(df["Cause"].unique())  # Tambahkan "Semua" sebagai pilihan
selected_cause = st.sidebar.selectbox("Pilih Penyebab Kematian:", causes, index=0)

# Filter data berdasarkan penyebab kematian yang dipilih
if selected_cause != "Semua":
    filtered_data = filtered_data[filtered_data["Cause"] == selected_cause]

# 5. Filter Tipe Kematian di Sidebar dengan Pilihan "Semua"
types = ["Semua"] + list(df["Type"].unique())  # Tambahkan "Semua" sebagai pilihan
selected_type = st.sidebar.selectbox("Pilih Tipe Kematian:", types, index=0)

# Filter data berdasarkan tipe kematian yang dipilih
if selected_type != "Semua":
    filtered_data = filtered_data[filtered_data["Type"] == selected_type]

# 6. **Distribusi Kematian Berdasarkan Penyebab**
st.subheader(
    f"Distribusi Kematian Berdasarkan Penyebab di Tahun {'-'.join(map(str, selected_years_range))}"
)

# Mengelompokkan data berdasarkan penyebab dan menghitung jumlah kematian total
cause_distribution = (
    filtered_data.groupby(["Cause"])["Total Deaths"].sum().reset_index()
)

# Mengurutkan data berdasarkan jumlah kematian total
cause_distribution = cause_distribution.sort_values(by="Total Deaths", ascending=False)

# Membuat Pie Chart dengan Plotly
fig = px.pie(
    cause_distribution,
    names="Cause",
    values="Total Deaths",
    color="Cause",
    color_discrete_sequence=px.colors.qualitative.Set3,
    hole=0.3,
)

# Memperbaiki tampilan Pie Chart
fig.update_traces(
    textposition="inside",
    textinfo="percent+label",
    textfont_size=10,
    insidetextorientation="radial",
    pull=[
        0.1 if x == cause_distribution["Total Deaths"].max() else 0
        for x in cause_distribution["Total Deaths"]
    ],
    marker=dict(line=dict(color="#FFFFFF", width=1)),
    hoverinfo="label+percent+value",
)

# Mengupdate layout Pie Chart
fig.update_layout(
    showlegend=True,
    legend=dict(
        orientation="v",  # Mengubah orientasi legend menjadi vertikal
        yanchor="top",
        y=1,
        xanchor="left",
        x=1.05,  # Memindahkan legend ke kanan chart
        font=dict(size=10),  # Mengurangi ukuran font legend
    ),
    margin=dict(
        l=20, r=120, t=20, b=20
    ),  # Menyesuaikan margin untuk memberi ruang pada legend
    height=600,  # Menambah tinggi chart
    width=800,  # Menambah lebar chart
)

# Menampilkan Pie Chart
st.plotly_chart(fig, use_container_width=True)

# Keterangan tambahan untuk memberikan konteks lebih lanjut
st.markdown(
    """
    <div style="text-align: justify;">
Pada grafik ini, kita melihat <b>distribusi kematian</b> berdasarkan penyebab pada rentang tahun yang dipilih. 
Beberapa penyebab kematian mungkin menunjukkan proporsi yang signifikan, seperti <b>Tuberkulosis (TBC)</b> dan <b>Demam Berdarah (DBD)</b>,
yang memerlukan perhatian lebih lanjut dalam kebijakan kesehatan masyarakat.
<br><br>
</div>
""",
    unsafe_allow_html=True,
)

# 7. **Distribusi Kematian Berdasarkan Tipe**
st.subheader(
    f"Distribusi Kematian Berdasarkan Tipe di Tahun {'-'.join(map(str, selected_years_range))}"
)
type_distribution = filtered_data.groupby(["Type"])["Total Deaths"].sum().reset_index()
type_distribution = type_distribution.sort_values(by="Total Deaths", ascending=False)

fig = px.bar(
    type_distribution,
    x="Type",
    y="Total Deaths",
    color="Total Deaths",
    color_continuous_scale="Blues",
)
st.plotly_chart(fig)

st.markdown(
    """
    <div style="text-align: justify;">
Grafik tersebut menampilkan perbandingan jumlah total kematian dari tahun ke tahun sesuai periode yang dipilih berdasarkan tiga jenis bencana: <br>
1. Bencana Non Alam dan Penyakit <br>
2. Bencana Alam <br>
3. Bencana Alam dan Bencana Sosial. <br>
Warna pada grafik merepresentasikan intensitas jumlah kematian, dengan skala warna di sisi kanan memberikan visualisasi tambahan.
<br><br>
</div>
""",
    unsafe_allow_html=True,
)

# 8. Distribusi Kematian Berdasarkan Tahun
st.subheader(
    f"Distribusi Kematian Berdasarkan Tahun {'-'.join(map(str, selected_years_range))}"
)

# Menghitung total kematian per tahun
yearly_deaths = filtered_data.groupby("Year")["Total Deaths"].sum().reset_index()

# Membuat grafik garis
fig = px.line(
    yearly_deaths,
    x="Year",
    y="Total Deaths",
    markers=True,
    line_shape="linear",
    color="Year",
)

# Menyesuaikan tata letak grafik
fig.update_layout(xaxis_title="Tahun", yaxis_title="Total Kematian", hovermode="x")

# Menampilkan grafik
st.plotly_chart(fig)

# Menambahkan deskripsi
st.write(
    """
    <div style="text-align: justify;">
Grafik di atas menunjukkan distribusi total kematian di Indonesia dari tahun ke tahun selama periode yang dipilih. 
Beberapa poin penting yang dapat diamati:

1. Tren Umum: Grafik ini memvisualisasikan bagaimana jumlah total kematian berubah dari waktu ke waktu. 
   Kita dapat melihat apakah ada tren peningkatan, penurunan, atau fluktuasi dalam jumlah kematian tahunan.
2. Tahun-tahun Puncak: Titik-titik tertinggi pada grafik menunjukkan tahun-tahun dengan jumlah kematian tertinggi. 
   Ini bisa menjadi indikasi adanya peristiwa khusus seperti wabah penyakit, bencana alam, atau faktor lain yang menyebabkan peningkatan kematian.
3. Tahun-tahun Terendah: Sebaliknya, titik-titik terendah menunjukkan tahun-tahun dengan jumlah kematian terendah. 
   Ini bisa mencerminkan perbaikan dalam sistem kesehatan, pencegahan penyakit, atau faktor positif lainnya.
4. Perubahan Mendadak: Lonjakan atau penurunan tajam antara dua tahun berturut-turut bisa menandakan perubahan signifikan 
   dalam faktor-faktor yang mempengaruhi tingkat kematian, seperti kebijakan kesehatan baru atau peristiwa besar.
5. Periode Stabil vs Fluktuatif: Bagian grafik yang relatif datar menunjukkan periode stabilitas dalam jumlah kematian, 
   sementara bagian yang naik-turun menunjukkan periode dengan fluktuasi yang lebih besar.<br>

Interpretasi lebih lanjut dari grafik ini sebaiknya mempertimbangkan konteks historis, kebijakan kesehatan, 
dan faktor-faktor sosial-ekonomi yang mungkin mempengaruhi tren kematian di Indonesia selama periode yang ditampilkan.
</div>
""",
    unsafe_allow_html=True,
)

# 9. Perbandingan Kematian Berdasarkan Penyebab dan Tahun
st.subheader(
    f"10 Penyebab Kematian Teratas Pada Tahun {'-'.join(map(str, selected_years_range))}"
)

# Menghitung total kematian per penyebab dan tahun
cause_yearly = (
    filtered_data.groupby(["Year", "Cause"])["Total Deaths"].sum().reset_index()
)

# Mengurutkan penyebab berdasarkan total kematian
top_causes = (
    cause_yearly.groupby("Cause")["Total Deaths"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .index
)

# Filter data untuk 10 penyebab teratas
cause_yearly_top10 = cause_yearly[cause_yearly["Cause"].isin(top_causes)]

# Membuat grafik batang bertumpuk
fig = px.bar(
    cause_yearly_top10,
    x="Year",
    y="Total Deaths",
    color="Cause",
    barmode="stack",
    height=400,
)

# Menyesuaikan tata letak grafik
fig.update_layout(
    xaxis_title="Tahun",
    yaxis_title="Jumlah Kematian",
    legend_title="Penyebab Kematian",
    hovermode="x unified",
)

# Menampilkan grafik
st.plotly_chart(fig, use_container_width=True)

# Menambahkan deskripsi
st.write(
    """
    <div style="text-align: justify;">
    Grafik batang bertumpuk di atas menunjukkan perbandingan jumlah kematian berdasarkan 10 penyebab teratas untuk setiap tahun. 
    Berikut adalah beberapa insight yang dapat diperoleh dari grafik ini:

    1. Komposisi Penyebab Kematian: Setiap warna pada batang mewakili penyebab kematian yang berbeda. 
       Ini memungkinkan kita untuk melihat kontribusi relatif dari setiap penyebab terhadap total kematian per tahun.
    2. Tren Temporal: Dengan melihat perubahan ketinggian dan komposisi batang dari tahun ke tahun, 
       kita dapat mengamati bagaimana pola penyebab kematian berubah seiring waktu.
    3. Penyebab Dominan: Warna yang mendominasi di sebagian besar batang menunjukkan penyebab kematian yang paling umum 
       atau konsisten selama periode yang ditampilkan.
    4. Perubahan Signifikan: Perubahan drastis dalam proporsi warna tertentu dari satu tahun ke tahun berikutnya 
       dapat mengindikasikan perubahan signifikan dalam faktor penyebab kematian, seperti wabah penyakit atau implementasi kebijakan kesehatan baru.
    
    Interpretasi lebih lanjut dari grafik ini harus mempertimbangkan konteks kesehatan masyarakat, 
    kebijakan pemerintah, dan peristiwa-peristiwa penting yang mungkin mempengaruhi tren kematian di Indonesia selama periode yang ditampilkan.
    </div>
    """,
    unsafe_allow_html=True,
)

# 10. **Tren Kematian Berdasarkan Penyebab dan Tipe**
st.subheader(
    f"Tren Kematian Berdasarkan Penyebab dan Tipe di Tahun {'-'.join(map(str, selected_years_range))}"
)

# Mempersiapkan data
trend_data = df.groupby(["Year", "Cause", "Type"])["Total Deaths"].sum().reset_index()

# Membuat selectbox untuk memilih penyebab kematian
causes = sorted(trend_data["Cause"].unique())
selected_causes = st.multiselect("Pilih Penyebab Kematian:", causes, default=causes[:5])

# Filter data berdasarkan penyebab yang dipilih
filtered_trend_data = trend_data[trend_data["Cause"].isin(selected_causes)]

# Membuat grafik
fig = px.line(
    filtered_trend_data,
    x="Year",
    y="Total Deaths",
    color="Cause",
    line_dash="Type",
    hover_data=["Cause", "Type", "Total Deaths"],
    labels={"Total Deaths": "Jumlah Kematian"},
)

# Memperbaiki tampilan grafik
fig.update_layout(
    xaxis_title="Tahun",
    yaxis_title="Jumlah Kematian",
    legend_title="Penyebab dan Tipe",
    hovermode="x unified",
    height=400,
)

# Menampilkan grafik
st.plotly_chart(fig, use_container_width=True)

# Menambahkan penjelasan
st.markdown(
    """
    <div style="text-align: justify;">
    <p>
    Grafik ini menunjukkan tren kematian berdasarkan penyebab dan tipe dari waktu ke waktu:
    </p>
    <ul>
        <li>Setiap garis mewakili kombinasi unik dari penyebab kematian dan tipenya.</li>
        <li>Gunakan menu dropdown di atas untuk memilih penyebab kematian yang ingin Anda bandingkan.</li>
        <li>Hover di atas garis untuk melihat detail jumlah kematian untuk setiap tahun.</li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

# 11. Visualisasi Scatter untuk Kematian vs. Tahun
st.subheader(
    f"Visualisasi Kematian vs Tahun Berdasarkan Penyebab untuk Periode {'-'.join(map(str, selected_years_range))}"
)

# Menghitung total kematian per penyebab dan tahun
cause_yearly = (
    filtered_data.groupby(["Year", "Cause"])["Total Deaths"].sum().reset_index()
)

# Membuat scatter plot interaktif
fig = px.scatter(
    cause_yearly,
    x="Year",
    y="Total Deaths",
    color="Cause",
    size="Total Deaths",
    hover_name="Cause",
    log_y=True,  # Menggunakan skala logaritmik untuk y-axis
    labels={"Total Deaths": "Jumlah Kematian (skala log)"},
    height=500,
)

# Menyesuaikan tata letak
fig.update_layout(
    xaxis_title="Tahun",
    yaxis_title="Jumlah Kematian (skala log)",
    legend_title="Penyebab Kematian",
    hovermode="closest",
)

# Menampilkan plot
st.plotly_chart(fig, use_container_width=True)

# Deskripsi
st.markdown(
    """
<div style='text-align: justify;'>
<p>Visual ini menunjukkan hubungan antara total kematian (Total Deaths) dan waktu berdasarkan kategori penyebab yang diidentifikasi. Setiap titik data pada grafik merepresentasikan jumlah kematian yang terkait dengan kategori tertentu pada periode tertentu, dengan warna berbeda menunjukkan berbagai kategori penyebab. Sebagian besar kategori memiliki angka kematian yang relatif kecil, kecuali beberapa kategori dengan angka yang jauh lebih tinggi. Mayoritas data terdistribusi dalam rentang tertentu, dengan nilai total kematian yang dominan berada pada angka rendah, menunjukkan bahwa sebagian besar kategori memiliki dampak yang lebih kecil dibandingkan kejadian luar biasa tertentu.</p>
</div>
""",
    unsafe_allow_html=True,
)

# 13. **Heatmap: Korelasi Antara Kematian dan Variabel Lain**
st.subheader(
    f"Korelasi Antara Kematian dan Variabel Lain di Tahun {'-'.join(map(str, selected_years_range))}"
)
correlation_matrix = filtered_data[["Year", "Total Deaths"]].corr()

fig, ax = plt.subplots()
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Matriks Korelasi")
st.pyplot(fig)

# Deskripsi singkat
st.markdown(
    """
<div style='text-align: justify;'>
<p>Heatmap di atas menunjukkan korelasi antara variabel <b>Year</b> dan <b>Total Deaths</b>. Interpretasi nilai korelasi:</p>
<ul>
    <li>Nilai mendekati 1: Korelasi positif kuat (saat satu variabel meningkat, yang lain juga meningkat)</li>
    <li>Nilai mendekati -1: Korelasi negatif kuat (saat satu variabel meningkat, yang lain menurun)</li>
    <li>Nilai mendekati 0: Korelasi lemah atau tidak ada korelasi</li>
</ul>
<p>Diagonal matriks selalu bernilai 1 karena menunjukkan korelasi variabel dengan dirinya sendiri. Korelasi antara <b>Year</b> dan <b>Total Deaths</b> menunjukkan bagaimana jumlah kematian berubah seiring waktu.</p>
</div>
""",
    unsafe_allow_html=True,
)

# 14. **Heatmap Kematian Berdasarkan Waktu, Penyebab, dan Tipe**
st.subheader(
    f"Kematian Berdasarkan Waktu dan Tipe di Tahun {'-'.join(map(str, selected_years_range))}"
)
yearly_cause_type = (
    filtered_data.groupby(["Year", "Cause", "Type"])["Total Deaths"].sum().reset_index()
)

heatmap_data = yearly_cause_type.pivot_table(
    index="Cause", columns="Year", values="Total Deaths", aggfunc="sum"
)
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", fmt="g", ax=ax)
ax.set_title(
    f"Kematian Berdasarkan Waktu, Penyebab, dan Tipe di Tahun {'-'.join(map(str, selected_years_range))}"
)
st.pyplot(fig)

# Deskripsi singkat
st.markdown(
    """
<div style='text-align: justify;'>
<p>Heatmap di atas menyajikan visualisasi komprehensif tentang pola kematian di Indonesia berdasarkan penyebab dan waktu. 
Intensitas warna pada heatmap mencerminkan jumlah kematian, dengan warna yang lebih gelap menunjukkan jumlah kematian yang lebih tinggi.</p>

<p>Dari visualisasi ini, kita dapat mengamati beberapa pola dan tren penting:</p>

<ol>
    <li>Penyebab Kematian Dominan: Baris dengan warna paling intens secara konsisten menunjukkan penyebab kematian yang paling signifikan selama periode yang ditampilkan.</li>
    <li>Perubahan Temporal: Perubahan intensitas warna dari kiri ke kanan untuk setiap penyebab menggambarkan bagaimana dampak dari penyebab tersebut berubah dari tahun ke tahun.</li>
    <li>Anomali dan Kejadian Luar Biasa: Sel-sel dengan warna yang sangat kontras dibandingkan sekitarnya mungkin menandakan kejadian luar biasa atau anomali untuk penyebab dan tahun tertentu.</li>
    <li>Efektivitas Intervensi: Penurunan intensitas warna untuk penyebab tertentu dari waktu ke waktu bisa mencerminkan keberhasilan intervensi kesehatan atau kebijakan pencegahan.</li>
</ol>

<p>Heatmap ini memberikan alat yang kuat untuk mengidentifikasi tren, pola, dan anomali dalam data kematian, 
memungkinkan para pembuat kebijakan dan profesional kesehatan untuk mengalokasikan sumber daya dan merancang intervensi 
yang lebih efektif dalam menangani berbagai penyebab kematian di Indonesia.</p>
</div>
""",
    unsafe_allow_html=True,
)

# 15. Wawasan dan Rekomendasi
st.subheader("Wawasan dan Rekomendasi")

st.markdown(
    """
<div style='text-align: justify;'>
<h4>Analisis Tren</h4>
<ul>
    <li>Variasi Temporal: Data menunjukkan adanya perbedaan tren jumlah kematian yang signifikan tergantung pada penyebab dan tipe kematian. Beberapa penyebab menunjukkan peningkatan kematian yang konsisten selama tahun-tahun terakhir, sementara yang lain mungkin menunjukkan penurunan atau fluktuasi.</li>
    <li>Penyebab Dominan: Identifikasi penyebab kematian yang paling dominan dan konsisten dari tahun ke tahun sangat penting untuk prioritas kebijakan kesehatan.</li>
    <li>Perubahan Pola: Pergeseran dalam pola kematian antar penyebab mungkin mengindikasikan perubahan dalam faktor risiko kesehatan atau efektivitas intervensi yang ada.</li>
</ul>

<h4>Rekomendasi Kebijakan</h4>
<ul>
    <li>Prioritas Intervensi: Fokus pada penyebab utama kematian dengan menerapkan inisiatif kesehatan masyarakat yang ditargetkan, seperti program pencegahan penyakit tidak menular dan pengendalian penyakit menular.</li>
    <li>Peningkatan Infrastruktur: Investasi dalam meningkatkan infrastruktur layanan kesehatan, terutama di daerah dengan akses terbatas ke fasilitas kesehatan berkualitas.</li>
    <li>Edukasi Masyarakat: Memperkuat program edukasi kesehatan masyarakat untuk meningkatkan kesadaran tentang faktor risiko dan langkah-langkah pencegahan untuk penyebab kematian utama.</li>
    <li>Kebijakan Lintas Sektor: Mengembangkan kebijakan yang melibatkan berbagai sektor (kesehatan, pendidikan, lingkungan) untuk mengatasi faktor-faktor sosial dan lingkungan yang mempengaruhi kesehatan.</li>
</ul>

<h4>Penelitian Lebih Lanjut</h4>
<ul>
    <li>Analisis Faktor Sosial Ekonomi: Melakukan studi mendalam tentang bagaimana faktor-faktor seperti pendapatan, pendidikan, dan pekerjaan mempengaruhi pola kematian di berbagai kelompok masyarakat.</li>
    <li>Pemetaan Geografis: Menganalisis variasi geografis dalam penyebab kematian untuk mengidentifikasi daerah-daerah yang memerlukan intervensi khusus.</li>
    <li>Studi Lingkungan: Menyelidiki dampak faktor lingkungan seperti polusi udara, akses air bersih, dan perubahan iklim terhadap tren kematian.</li>
    <li>Evaluasi Intervensi: Melakukan evaluasi sistematis terhadap efektivitas intervensi kesehatan yang ada dan mengidentifikasi area untuk perbaikan.</li>
    <li>Analisis Prediktif: Mengembangkan model prediktif untuk memperkirakan tren kematian di masa depan dan membantu dalam perencanaan kebijakan jangka panjang.</li>
</ul>

<p>Dengan mempertimbangkan wawasan ini dan menerapkan rekomendasi yang diusulkan, diharapkan dapat terjadi peningkatan signifikan dalam upaya mengurangi angka kematian dan meningkatkan kualitas kesehatan masyarakat di Indonesia. Penting untuk memastikan bahwa strategi yang dikembangkan bersifat holistik, berbasis bukti, dan disesuaikan dengan konteks lokal untuk memaksimalkan dampaknya.</p>
</div>
""",
    unsafe_allow_html=True,
)
