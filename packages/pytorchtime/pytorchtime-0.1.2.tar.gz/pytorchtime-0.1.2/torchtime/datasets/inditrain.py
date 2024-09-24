import glob

files = glob.glob("/home/vincent/.local/share/Cryptomator/mnt/inditrain/vscharf/cache/**/*")

samples = []
for file in files:
    df = pd.read_feather(file)
    samples.append(df)