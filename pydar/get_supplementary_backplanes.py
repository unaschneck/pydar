# Extract metadata from BIDR files

from planetaryimage import PDS3Image

def getFlybymeta()
    testfile = 'BIBQD49N071_D035_T00AS01_V03.img'
    image = PDS3Image.open(testfile)


    all_var = vars(image)
    
    return all_var