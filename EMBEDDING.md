## Embedding the NGPF Check Writing Interactive

This app is a Streamlit frontend with no backend or persistence. It can be embedded in an iframe.

### Recommended iframe snippet
```html
<iframe
  src="https://your-host.example.com/check-writing/"
  title="NGPF Check Writing Interactive"
  style="width: 100%; height: 720px; border: 0;"
  allow="clipboard-read; clipboard-write"
  loading="lazy"
></iframe>
```

### Streamlit baseUrlPath
When hosting under a sub-path, set Streamlit's base URL path so internal assets resolve correctly:

```bash
streamlit run app.py \
  --server.baseUrlPath check-writing \
  --server.headless true \
  --browser.gatherUsageStats false
```

Alternatively, set in `.streamlit/config.toml`:
```toml
[server]
baseUrlPath = "check-writing"
headless = true

[browser]
gatherUsageStats = false
```

### Sizing and responsiveness
- The UI is responsive from 320px wide; for classroom projectors, a height of 720–900px is recommended.
- The iframe can be placed in a container with `max-width` constraints to match site layout.

### Privacy
- No analytics, cookies, or external calls; all state remains in the browser and resets on refresh.


