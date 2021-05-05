import pandas as pd
import numpy as np

pd.set_option('display.max_columns',None)
pd.set_option('display.expand_frame_repr',False)

df = pd.read_csv("Hafta-03/tips.csv")

# Sutun isimlerini Güncelleme
isimler = ["odenen","bahsis","sex","sigara","gun","saat","sayi"]
df.columns = isimler

# Cinsiyet değerlerini değiştirme
df["sex"].unique()
df["sex"].loc[df["sex"] == "Female"] = "Kadin"
df["sex"].loc[df["sex"] == "Male"] = "Erkek"

# Servis saatleri değiştirme
df["saat"].unique()
type(df["saat"])
ilk_isim = list(df["saat"].unique())
yeni_isim = ["Akşam Yemeği","Öğle Yemeği"]
df["saat"].replace(ilk_isim,yeni_isim,inplace=True)

# sigara ve gün değerlerinin değerlerini değiştirme

deger_sozluk = {"sigara":{"No":"Hayır","Yes":"Evet"},
                "gun": {"Sun":"Pazar",
                        "Sat":"Cumartesi",
                        "Thur":"Persembe",
                        "Fri":"Cuma"}}

df.replace(deger_sozluk,inplace=True)

# Oluşturulan veri setini cvs olarak kaydet
df.to_csv("Hafta-03/tips_yeni.csv")

# Toplulaştırma ve Gruplama

df = pd.read_csv("Hafta-03/diamonds.csv")

# Kategorik değişkenlerin isinlerini listeleme
df.dtypes # object değerler listenelecek
kategorik = []
for col in df.columns:
    if df[col].dtype == 'O':
        kategorik.append(col)

# aynı senaryoyu comphrension ile gösterimi
kategorik = [col for col in df.columns if df[col].dtype == 'O']

# Sasıyal değişkenlerin isinlerini listeleme
sayısal = [col for col in df.columns if df[col].dtype != 'O']

# cut kategorisine göre sayısal değişkenlerin ortalaması
df.groupby("cut").agg("mean")

# cut kategorisine göre x,y,z sayısal değişkenleri hariç diğer değişkenlerin ortalaması
df.groupby("cut").agg({'carat':"mean",
                       'depth':"mean",
                       'table':"mean",
                       'price':"mean"})

# üst senaryonun pratik hali
agg_sozluk = {deger:"mean" for deger in sayısal if deger not in ["x","y","z"]}
df.groupby("cut").agg(agg_sozluk)

# color ve cut kategorilerine göre sayısal değişkenlerin medyan değerleri
df.groupby(["color","cut"]).agg("median")

# color, cut ve clarity kategorierine göre x,y,z değişkenlerinin
# medyan, ortalama ve std değerleri
agg_sozluk2 = {deger:["median","mean","std"] for deger in sayısal if deger in ["x","y","z"]}
df2= df.groupby(["cut","color","clarity"]).agg(agg_sozluk2)

#  'x' , 'mean' --> 'x_mean'
# ayrık hali
for col in df2.columns:
    print(col)

# birleştirilmiş sonuc
for col in df2.columns:
    print("_".join(col))

birlestirilmis = ["_".join(col) for col in df2.columns]

# sutun isimleri üst senaryodaki hali ile değiştirme
df2.columns = birlestirilmis

# oluşturulan df satır isimlerini sutuna dönüştürme
df2.reset_index(inplace=True)

# cut, color ve clarity değişkenlerini tek bir sutunda birleştirme
for index, row in df2.iterrows():
    df2.loc[index,"kategori"] = row["cut"]+"_"+row["color"]+"_"+row["clarity"]

# Üstteki senaryonun apply ile gösterimi
df2["kategori_yeni"] = df2.apply(lambda row: row["cut"]+"_"+row["color"]+"_"+row["clarity"], axis=1)

# cut, color, clarity ve kategori değişkenlerini sil
df2.drop(["cut","color","clarity","kategori"],axis=1,inplace=True)

# kategori_yeni değişkenini en başa al
yeni_liste = [col for col in df2.columns if col != "kategori_yeni"]
yeni_liste.insert(0,"kategori_yeni")
df2 = df2[yeni_liste]

# aplly
tips = pd.read_csv("Hafta-03/tips_yeni.csv",index_col=0)

# hesap değerlerini z-standartlaştırma
# z-standartlaştırma = (x - x.mean()) / x.std()
def z_standartlastirma(deger,seri:pd.Series):
    return (deger - seri.mean()) / seri.std()

sonuc = []
for deger in tips["odenen"].values:
    sonuc.append(z_standartlastirma(deger,tips["odenen"]))

tips["odenen_hesap"] = sonuc

tips["odenen_apply"] = tips["odenen"].apply(lambda x: (x - tips["odenen"].mean()) / tips["odenen"].std())

# servis saati değerlerini hepsini büyük harf yapınız
sonuc = []
for x in tips["saat"].values:
    sonuc.append(x.upper())

tips["saat"] = sonuc

tips["saat"] = tips["saat"].apply(lambda x: (x.upper()))

# günlere göre ödenen hesap miktarları toplamı
# gün değişkenine göre grupby yaparsak liste tupplle çifti elde ederiz

tips["gun"].unique()
tips.groupby("gun").apply(sum)["odenen"]

import seaborn as sns
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
data = pd.read_excel("MarketSales (1).xlsx")
df = data.copy()

# veri seti boyutları
def bilgi(dataframe:pd.DataFrame):
    print("DataFrame Boyutu:".center(30,"*"))
    print(df.shape)
    print("DataFrame Hakkında:".center(30,"*"))
    print(df.info)
    print("DataFrame' de boş değer var mı:".center(30,"*"))
    print(df.isnull().any())
    print("DataFrame'de toplam boş değer:".center(30,"*"))
    print(df.isnull().sum())
    print("DataFrame tüm satırlarda toplam boş değer:".center(30,"*"))
    print(df.isnull().sum().sum())
    print("DataFrame Boş olan sutunlar:".center(30,"*"))
    print(df.columns[df.isnull().any()])
    print("DataFrame Dolu Olanlar:".center(30,"*"))
    print(df.columns[df.isnull().any() == False])
    print("DataFrame Kaç Veri Tipi Var:".center(30,"*"))
    print(df.dtypes.nunique())
    print("DataFrame ilk 5 satır:".center(30,"*"))
    print(df.head())
    print("DataFrame so 5 satır:".center(30,"*"))
    print(df.tail())
    print("DataFrame:".center(30,"*"))
    print(df[["AMOUNT","PRICE"]].head())
    print("DataFrame:".center(30,"*"))
    print(df[df["LINENETTOTAL"] > 15])
    print("DataFrame:".center(30,"*"))
    print(df[df["BRANCH"]=="Balıkesir Subesi"].head())
    print("DataFrame:".center(30,"*"))
    print(df[(df["LINENETTOTAL"] < 2) & (df["BRANCH"] == "Balıkesir Subesi")])
    print("DataFrame:".center(30,"*"))
    print(df.rename(columns={"ITEMNAME":"URUNADI",
                             "ITEMCODE":"URUN_ID",
                             "BRANCH":"SUBE_ADI"},inplace=True)
    print("DataFrame:".center(30,"*"))
    print(df.loc[100:103,"ID":"LINENETTOTAL"])
    print("DataFrame:".center(30,"*"))
    print(df.drop("CATEGORY_NAME3",axis=1,inplace=True))
    print("En büyük değer".center(30,"*"))
    print(df.URUN_ID.max())
    df["URUN_ID"] = df["URUN_ID"].fillna(99999)

df.URUN_ID.isnull().any()
df.URUN_ID.max()
bilgi(df)

# URUN_ADI kısmında boş değerlere Bilinmeyen ürün yazma
df["URUNADI"].isnull().any()
df.loc[(df["URUNADI"].isnull()),"URUNADI"] = "Bilinmeyen Urun"
df.loc[49,"URUNADI"]

# CLIENTCODE sutununda boş değerlere #un99 yazınız
df[df["CLIENTCODE"].isnull()].head()
df.loc[(df["CLIENTCODE"].isnull()),"CLIENTCODE"] = "#un99"
df.loc[[51,94],"CLIENTCODE"]

# CLIENTNAME sutununda boş değerlere bilinmeyen atayınız
df.loc[df["CLIENTNAME"].isnull(),"CLIENTNAME"] = "Bilinmeyen"

# category1 dolu olup category2 boş olan satırlara category1 değerlerini atayınız
df.loc[[55,1302],["CATEGORY_NAME1","CATEGORY_NAME2"]] # örnek
a = df[df["CATEGORY_NAME1"].notnull() & df["CATEGORY_NAME2"].isnull()]["CATEGORY_NAME1"]
df.loc[df["CATEGORY_NAME1"].notnull() & df["CATEGORY_NAME2"].isnull(),"CATEGORY_NAME2"] = a

# Cinsiyet değerleri nan olanları bilinmeyen ile değiştiriiniz
df.loc[df["GENDER"].isnull(),"GENDER"] = "Bilinmeyen"
df.loc[51,"GENDER"]

# BRANDCODE ve BRAND sutunlarında boş değerlere bilinmeyen adı atayın
df.loc[df["BRANDCODE"].isnull(),"BRANDCODE"] = "Bilinmeyen"
df.loc[df["BRAND"].isnull(),"BRAND"] = "Bilinmeyen"

# Category1 ve 2 de boş değerlere bilinmeyen kategori ismini atayınız
df.loc[df["CATEGORY_NAME1"].isnull(),"CATEGORY_NAME1"] = "Bilinmeyen_Kategori"
df["CATEGORY_NAME1"].isnull().any()

df.loc[df["CATEGORY_NAME2"].isnull(),"CATEGORY_NAME2"] = "Bilinmeyen_Kategori"
df["CATEGORY_NAME2"].isnull().any()

# hala boş değer varsa siliniz
df.isnull().sum()
df = df.dropna()


