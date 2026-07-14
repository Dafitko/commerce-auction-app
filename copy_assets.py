import shutil

src = "/Users/davidpirchala/.gemini/antigravity-ide/brain/9f0a1a0f-fdb8-4487-be6c-64a232f5f705/premium_gavel_favicon_1784061808683.png"
dst = "/Users/davidpirchala/Desktop/CS50W/Projects/commerce/auctions/static/auctions/favicon.png"

try:
    shutil.copy(src, dst)
    print("Success")
except Exception as e:
    print(f"Error: {e}")
