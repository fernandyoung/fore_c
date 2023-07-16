class dstatn:
  def __init__(self, actual, predict):
    self.predict = predict
    self.actual = actual

  def at(self, h):
    prediksi=[]
    for i in range(len(h)-1):
      hasil = h[i+1]-h[i]
      if hasil >= 0:
        prediksi.append(hasil)
      else:
        prediksi.append(hasil)
    return prediksi

  def dstathasil(self):
    nilai_predict = self.at(self.predict)
    nilai_asli = self.at(self.actual)
  
    he = []
    for i in range(len(nilai_asli)):
      nilai = nilai_asli[i]*nilai_predict[i]
      if nilai > 0:
        he.append(1)
      else:
        he.append(0)
    sigma = sum([1 for j in he if j == 1])
    dstat = sigma/len(nilai_asli)
    return dstat