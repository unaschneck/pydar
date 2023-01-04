from planetaryimage import PDS3Image

testfile = 'BIBQD49N071_D035_T00AS01_V03.img'
image = PDS3Image.open(testfile)

print(vars(image))