# Sung-Jin Choi Research Group

Academic website for Sung-Jin Choi and his research team at Kookmin University, featuring research, publications, patents and awards, team members, and media coverage.

- Website address: [sjchoiee-research.github.io](https://sjchoiee-research.github.io/)
- Repository: [sjchoiee-research/sjchoiee-research.github.io](https://github.com/sjchoiee-research/sjchoiee-research.github.io)
- Google Scholar: [Sung-Jin Choi](https://scholar.google.com/citations?user=7epJAS4AAAAJ&hl=en)

The website was published and verified on 23 September 2026. HTTPS is enforced.

## Maintenance

Edit `content.json` to update publications, research, patents, awards, media, and team information. Then regenerate the static pages with Python 3:

```sh
python build.py
```

Update the generated HTML files and any changed assets in the repository. Changes made only to generated HTML may be overwritten by the next build. No Python runtime is required for visitors.

Google Scholar metrics are a dated snapshot of the public profile. They are updated manually on request; automatic or scheduled collection is not enabled. The displayed metrics and Scholar links open the original profile.

## Publishing

The GitHub Pages source is the `main` branch, `/(root)` folder. Keep `index.html`, `.nojekyll`, and the `assets` directory at the repository root. No custom domain is configured.

For a local preview, open `index.html` in a browser or run:

```sh
python -m http.server 8765
```

Figure and photograph sources are listed on the website's [credits page](credits.html).
