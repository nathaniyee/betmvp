from backend.app.ingestion.prizepicks import fetch_prizepicks_props

df = fetch_prizepicks_props()

print(df.head(100))
print("\nTotal props:", len(df))
